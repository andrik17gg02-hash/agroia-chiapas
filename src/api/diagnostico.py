from fastapi import APIRouter, UploadFile, File, Form
from src.services.diagnostico import diagnosticar_planta

router = APIRouter()

@router.post("/diagnostico")
async def crear_diagnostico(
    imagen: UploadFile = File(...),
    cultivo: str = Form(...),
    municipio: str = Form(...)
):
    imagen_bytes = await imagen.read()
    tipo_imagen = imagen.content_type
    
    resultado = diagnosticar_planta(imagen_bytes, tipo_imagen, cultivo, municipio)
    
    return {
        "cultivo": cultivo,
        "municipio": municipio,
        "diagnostico": resultado
    }
