"""
Scraping automation router for executing ETL processes.
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException
import subprocess
import os
from pathlib import Path

router = APIRouter(prefix="/api/scraping", tags=["scraping"])

# Path to the ETL script
ETL_SCRIPT_PATH = Path(__file__).parent.parent.parent / "1_motor_etl" / "main_auto.py"


@router.post("/run")
async def run_scraping(background_tasks: BackgroundTasks):
    """
    Execute the main_auto.py scraping script in the background.
    
    This endpoint triggers the ETL process that scrapes SEACE data
    and loads it into the database.
    
    Returns:
        dict: Status message indicating the process has started
        
    Raises:
        HTTPException: If the script file is not found
    """
    if not ETL_SCRIPT_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Script not found at: {ETL_SCRIPT_PATH}"
        )
    
    def run_etl_script():
        """Background task to execute the ETL script."""
        try:
            # Execute the Python script
            result = subprocess.run(
                ["python", str(ETL_SCRIPT_PATH)],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"ETL Script Output: {result.stdout}")
            if result.stderr:
                print(f"ETL Script Errors: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"ETL Script failed with error: {e}")
            print(f"Output: {e.output}")
    
    # Add the task to background tasks
    background_tasks.add_task(run_etl_script)
    
    return {
        "status": "started",
        "message": "Proceso de scraping iniciado en segundo plano",
        "script_path": str(ETL_SCRIPT_PATH)
    }


@router.get("/status")
async def get_scraping_status():
    """
    Get the current status of the scraping process.
    
    Note: This is a placeholder. In production, you would implement
    proper status tracking using a task queue like Celery or Redis.
    
    Returns:
        dict: Current status of the scraping process
    """
    # TODO: Implement proper status tracking
    return {
        "status": "idle",
        "message": "No hay procesos en ejecución actualmente"
    }


@router.get("/script-info")
async def get_script_info():
    """
    Get information about the ETL script.
    
    Returns:
        dict: Script path and existence status
    """
    return {
        "script_path": str(ETL_SCRIPT_PATH),
        "exists": ETL_SCRIPT_PATH.exists(),
        "absolute_path": str(ETL_SCRIPT_PATH.absolute())
    }
