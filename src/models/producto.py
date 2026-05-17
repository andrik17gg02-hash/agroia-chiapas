from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.db.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)
    unidad = Column(String, nullable=False)
    municipio = Column(String, nullable=False)
    cultivo = Column(String, nullable=False)
    disponible = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
