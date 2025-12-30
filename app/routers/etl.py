"""
ETL Router - Endpoints for managing the ETL motor (main_auto.py)
"""
import subprocess
import sys
import os
import logging
from fastapi import APIRouter, HTTPException
from typing import Dict, List
from datetime import datetime
import asyncio
from pydantic import BaseModel

router = APIRouter(prefix="/api/etl", tags=["ETL"])

# Global state for ETL execution
etl_state = {
    "is_running": False,
    "current_step": None,
    "start_time": None,
    "logs": [],
    "process": None
}

class ETLStatusResponse(BaseModel):
    is_running: bool
    current_step: str | None
    start_time: str | None
    logs: List[str]

class ETLExecutionResponse(BaseModel):
    success: bool
    message: str

class ETLHistoryItem(BaseModel):
    timestamp: str
    status: str
    details: str

@router.post("/execute", response_model=ETLExecutionResponse)
async def execute_etl():
    """
    Execute the ETL motor (main_auto.py) in the background.
    """
    global etl_state
    
    if etl_state["is_running"]:
        raise HTTPException(status_code=400, detail="ETL process is already running")
    
    # Reset state
    etl_state["is_running"] = True
    etl_state["current_step"] = "Iniciando proceso ETL..."
    etl_state["start_time"] = datetime.now().isoformat()
    etl_state["logs"] = []
    
    # Get paths
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    etl_script = os.path.join(script_dir, "1_motor_etl", "main_auto.py")
    
    if not os.path.exists(etl_script):
        etl_state["is_running"] = False
        raise HTTPException(status_code=404, detail=f"ETL script not found: {etl_script}")
    
    # Start ETL process in background
    asyncio.create_task(run_etl_process(etl_script))
    
    return ETLExecutionResponse(
        success=True,
        message="ETL process started successfully"
    )

async def run_etl_process(script_path: str):
    """
    Run the ETL process asynchronously.
    """
    global etl_state
    
    try:
        etl_state["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando motor ETL...")
        etl_state["current_step"] = "Ejecutando main_auto.py"
        
        # Execute the ETL script
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.path.dirname(script_path)
        )
        
        etl_state["process"] = process
        
        # Read output in real-time
        async def read_stream(stream, prefix):
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded = line.decode('utf-8', errors='replace').strip()
                if decoded:
                    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {prefix}: {decoded}"
                    etl_state["logs"].append(log_entry)
                    # Keep only last 500 logs
                    if len(etl_state["logs"]) > 500:
                        etl_state["logs"] = etl_state["logs"][-500:]
        
        # Read both stdout and stderr
        await asyncio.gather(
            read_stream(process.stdout, "INFO"),
            read_stream(process.stderr, "ERROR")
        )
        
        # Wait for process to complete
        await process.wait()
        
        if process.returncode == 0:
            etl_state["current_step"] = "Proceso completado exitosamente"
            etl_state["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ ETL finalizado con éxito")
        else:
            etl_state["current_step"] = f"Proceso finalizado con errores (código: {process.returncode})"
            etl_state["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ ETL finalizado con errores")
            
    except Exception as e:
        etl_state["current_step"] = f"Error: {str(e)}"
        etl_state["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error crítico: {str(e)}")
    finally:
        etl_state["is_running"] = False
        etl_state["process"] = None

@router.get("/status", response_model=ETLStatusResponse)
async def get_etl_status():
    """
    Get the current status of the ETL process.
    """
    return ETLStatusResponse(
        is_running=etl_state["is_running"],
        current_step=etl_state["current_step"],
        start_time=etl_state["start_time"],
        logs=etl_state["logs"][-100:]  # Return last 100 logs
    )

@router.get("/history", response_model=List[ETLHistoryItem])
async def get_etl_history():
    """
    Get the history of ETL executions from the log file.
    """
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_file = os.path.join(script_dir, "1_motor_etl", "historial_ejecuciones.log")
    
    history = []
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
                # Parse last 20 entries
                for line in lines[-20:]:
                    if line.strip():
                        history.append(ETLHistoryItem(
                            timestamp=datetime.now().isoformat(),
                            status="completed",
                            details=line.strip()
                        ))
        except Exception as e:
            logging.error(f"Error reading history: {e}")
    
    return history

@router.post("/stop")
async def stop_etl():
    """
    Stop the currently running ETL process.
    """
    global etl_state
    
    if not etl_state["is_running"]:
        raise HTTPException(status_code=400, detail="No ETL process is currently running")
    
    if etl_state["process"]:
        try:
            etl_state["process"].terminate()
            etl_state["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] 🛑 Proceso detenido por el usuario")
            etl_state["current_step"] = "Proceso detenido"
            etl_state["is_running"] = False
            return {"success": True, "message": "ETL process stopped"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error stopping process: {str(e)}")
    
    raise HTTPException(status_code=400, detail="Process reference not found")
