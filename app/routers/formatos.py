from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
import os

router = APIRouter(prefix="/formatos", tags=["formatos"])

# Directorio donde están los formatos
FORMATOS_DIR = Path(__file__).parent.parent.parent / "formatosc"

@router.get("/list")
async def list_formatos():
    """Listar todos los formatos disponibles"""
    try:
        if not FORMATOS_DIR.exists():
            return {"formatos": []}
        
        formatos = []
        allowed_extensions = {".docx", ".pdf", ".xlsx", ".pptx", ".txt", ".zip"}
        
        # Iterar sobre todos los archivos
        for file_path in FORMATOS_DIR.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in allowed_extensions:
                file_stat = file_path.stat()
                formatos.append({
                    "id": len(formatos) + 1,
                    "nombre": file_path.stem,
                    "nombreArchivo": file_path.name,
                    "nombreOriginal": file_path.name,  # Nombre original para descarga
                    "tamano": file_stat.st_size,
                    "extension": file_path.suffix,
                    "icon": get_icon_for_extension(file_path.suffix)
                })
        
        return {"formatos": formatos}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_formato(file: UploadFile = File(...)):
    """Subir un nuevo formato"""
    try:
        # Validar extensión del archivo
        allowed_extensions = [".docx", ".pdf", ".xlsx", ".pptx", ".txt", ".zip"]
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(allowed_extensions)}"
            )
        
        # Crear el directorio si no existe
        FORMATOS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generar ruta del archivo
        file_path = FORMATOS_DIR / file.filename
        
        # Verificar si el archivo ya existe
        if file_path.exists():
            raise HTTPException(status_code=400, detail="Ya existe un archivo con ese nombre")
        
        # Guardar el archivo
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "message": "Archivo subido exitosamente",
            "filename": file.filename,
            "size": len(content),
            "extension": file_extension
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")


@router.get("/download/{filename}")
async def download_formato(filename: str):
    """Descargar un formato específico"""
    file_path = FORMATOS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Ruta inválida")
    
    # Verificar que el archivo esté dentro del directorio de formatos (seguridad)
    try:
        file_path.resolve().relative_to(FORMATOS_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    # Leer el archivo
    def iterfile():
        with open(file_path, mode="rb") as file_like:
            yield from file_like
    
    # Crear la respuesta con headers CORS explícitos
    from fastapi.responses import StreamingResponse
    import os
    
    response = StreamingResponse(
        iterfile(),
        media_type='application/octet-stream',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Expose-Headers': 'Content-Disposition',
        }
    )
    
    return response


@router.delete("/delete/{filename}")
async def delete_formato(filename: str, pin: str):
    """Eliminar un formato específico (Requiere PIN de admin)"""
    # PIN de seguridad (Idealmente debería estar en .env)
    ADMIN_PIN = os.getenv("ADMIN_DELETE_PIN", "123456")
    
    if pin != ADMIN_PIN:
        raise HTTPException(status_code=403, detail="PIN de seguridad incorrecto")

    file_path = FORMATOS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Ruta inválida")
    
    # Verificar que el archivo esté dentro del directorio de formatos (seguridad)
    try:
        file_path.resolve().relative_to(FORMATOS_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        # Eliminar el archivo físicamente
        file_path.unlink()
        return {"message": "Archivo eliminado exitosamente", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el archivo: {str(e)}")


def get_icon_for_extension(extension: str) -> str:
    """Obtener el icono FontAwesome según la extensión"""
    icons = {
        ".docx": "fa-file-word",
        ".pdf": "fa-file-pdf",
        ".xlsx": "fa-file-excel",
        ".pptx": "fa-file-powerpoint",
        ".txt": "fa-file-alt",
        ".zip": "fa-file-archive"
    }
    return icons.get(extension.lower(), "fa-file")
