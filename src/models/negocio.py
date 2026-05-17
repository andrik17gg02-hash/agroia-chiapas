from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.database import Base
import enum

class TipoTransaccion(str, enum.Enum):
    ingreso = "ingreso"
    egreso = "egreso"

class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(Enum(TipoTransaccion), nullable=False)
    concepto = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    cultivo = Column(String)
    notas = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String, nullable=False)
    costo_unitario = Column(Float)
    notas = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
