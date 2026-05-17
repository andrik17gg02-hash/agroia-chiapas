from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.services.auth import registrar_usuario, login_usuario
from pydantic import BaseModel

router = APIRouter()

class RegistroRequest(BaseModel):
    nombre: str
    telefono: str
    municipio: str
    password: str
    email: str = None

class LoginRequest(BaseModel):
    telefono: str
    password: str

@router.post("/auth/registro")
def registro(data: RegistroRequest, db: Session = Depends(get_db)):
    try:
        usuario = registrar_usuario(
            db=db,
            nombre=data.nombre,
            telefono=data.telefono,
            municipio=data.municipio,
            password=data.password,
            email=data.email
        )
        return {
            "mensaje": "Usuario registrado correctamente",
            "id": usuario.id,
            "nombre": usuario.nombre,
            "telefono": usuario.telefono,
            "municipio": usuario.municipio
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="El telefono o email ya esta registrado")

@router.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    resultado = login_usuario(db=db, telefono=data.telefono, password=data.password)
    if not resultado:
        raise HTTPException(status_code=401, detail="Telefono o password incorrectos")
    return {
        "token": resultado["token"],
        "nombre": resultado["usuario"].nombre,
        "municipio": resultado["usuario"].municipio
    }
