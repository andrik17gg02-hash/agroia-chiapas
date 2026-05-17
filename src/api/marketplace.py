from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.usuario import Usuario
from src.models.producto import Producto
from pydantic import BaseModel
from jose import JWTError, jwt
from typing import Optional

SECRET_KEY = "agroia-chiapas-secret-key-2026"
ALGORITHM = "HS256"

router = APIRouter()

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    unidad: str
    municipio: str
    cultivo: str
    disponible: float

@router.get("/marketplace")
def listar_productos(municipio: Optional[str] = None, cultivo: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Producto)
    if municipio:
        query = query.filter(Producto.municipio == municipio)
    if cultivo:
        query = query.filter(Producto.cultivo == cultivo)
    productos = query.order_by(Producto.created_at.desc()).all()
    return {
        "total": len(productos),
        "productos": productos
    }

@router.post("/marketplace")
def crear_producto(data: ProductoCreate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    producto = Producto(
        usuario_id=current_user.id,
        nombre=data.nombre,
        descripcion=data.descripcion,
        precio=data.precio,
        unidad=data.unidad,
        municipio=data.municipio,
        cultivo=data.cultivo,
        disponible=data.disponible
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

@router.delete("/marketplace/{producto_id}")
def eliminar_producto(producto_id: int, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id, Producto.usuario_id == current_user.id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"mensaje": "Producto eliminado"}
