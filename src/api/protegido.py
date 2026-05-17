from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.usuario import Usuario
from src.models.negocio import Transaccion, Inventario
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

@router.get("/auth/me")
def get_me(current_user: Usuario = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "telefono": current_user.telefono,
        "municipio": current_user.municipio,
        "email": current_user.email,
        "cultivo_principal": current_user.cultivo_principal,
    }

@router.get("/transacciones")
def listar_transacciones(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    transacciones = db.query(Transaccion).filter(Transaccion.usuario_id == current_user.id).all()
    total_ingresos = sum(t.monto for t in transacciones if t.tipo == "ingreso")
    total_egresos = sum(t.monto for t in transacciones if t.tipo == "egreso")
    return {
        "transacciones": transacciones,
        "resumen": {
            "total_ingresos": total_ingresos,
            "total_egresos": total_egresos,
            "balance": total_ingresos - total_egresos
        }
    }

class TransaccionCreate(BaseModel):
    tipo: str
    concepto: str
    monto: float
    cultivo: Optional[str] = None
    notas: Optional[str] = None

@router.post("/transacciones")
def crear_transaccion(data: TransaccionCreate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    transaccion = Transaccion(
        usuario_id=current_user.id,
        tipo=data.tipo,
        concepto=data.concepto,
        monto=data.monto,
        cultivo=data.cultivo,
        notas=data.notas
    )
    db.add(transaccion)
    db.commit()
    db.refresh(transaccion)
    return transaccion

@router.get("/inventario")
def listar_inventario(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Inventario).filter(Inventario.usuario_id == current_user.id).all()

class InventarioCreate(BaseModel):
    nombre: str
    cantidad: float
    unidad: str
    costo_unitario: Optional[float] = None
    notas: Optional[str] = None

@router.post("/inventario")
def crear_inventario(data: InventarioCreate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    item = Inventario(
        usuario_id=current_user.id,
        nombre=data.nombre,
        cantidad=data.cantidad,
        unidad=data.unidad,
        costo_unitario=data.costo_unitario,
        notas=data.notas
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

class InventarioUpdate(BaseModel):
    cantidad: Optional[float] = None
    costo_unitario: Optional[float] = None

@router.put("/inventario/{item_id}")
def actualizar_inventario(item_id: int, data: InventarioUpdate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Inventario).filter(Inventario.id == item_id, Inventario.usuario_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    if data.cantidad is not None:
        item.cantidad = data.cantidad
    if data.costo_unitario is not None:
        item.costo_unitario = data.costo_unitario
    db.commit()
    db.refresh(item)
    return item

@router.delete("/inventario/{item_id}")
def eliminar_inventario(item_id: int, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Inventario).filter(Inventario.id == item_id, Inventario.usuario_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(item)
    db.commit()
    return {"mensaje": "Item eliminado"}
