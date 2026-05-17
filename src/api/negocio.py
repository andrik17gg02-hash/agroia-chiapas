from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.negocio import Transaccion, Inventario, TipoTransaccion
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class TransaccionRequest(BaseModel):
    usuario_id: int
    tipo: TipoTransaccion
    concepto: str
    monto: float
    cultivo: Optional[str] = None
    notas: Optional[str] = None

class InventarioRequest(BaseModel):
    usuario_id: int
    nombre: str
    cantidad: float
    unidad: str
    costo_unitario: Optional[float] = None
    notas: Optional[str] = None

@router.post("/negocio/transaccion")
def crear_transaccion(data: TransaccionRequest, db: Session = Depends(get_db)):
    transaccion = Transaccion(
        usuario_id=data.usuario_id,
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

@router.get("/negocio/transacciones/{usuario_id}")
def listar_transacciones(usuario_id: int, db: Session = Depends(get_db)):
    transacciones = db.query(Transaccion).filter(Transaccion.usuario_id == usuario_id).all()
    total_ingresos = sum(t.monto for t in transacciones if t.tipo == TipoTransaccion.ingreso)
    total_egresos = sum(t.monto for t in transacciones if t.tipo == TipoTransaccion.egreso)
    return {
        "transacciones": transacciones,
        "resumen": {
            "total_ingresos": total_ingresos,
            "total_egresos": total_egresos,
            "balance": total_ingresos - total_egresos
        }
    }

@router.post("/negocio/inventario")
def agregar_inventario(data: InventarioRequest, db: Session = Depends(get_db)):
    item = Inventario(
        usuario_id=data.usuario_id,
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

@router.get("/negocio/inventario/{usuario_id}")
def listar_inventario(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Inventario).filter(Inventario.usuario_id == usuario_id).all()
