from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.usuario import Usuario

router = APIRouter()

@router.post("/usuarios")
def crear_usuario(nombre: str, telefono: str, municipio: str, db: Session = Depends(get_db)):
    usuario = Usuario(nombre=nombre, telefono=telefono, municipio=municipio)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()