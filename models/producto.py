from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base
import enum

class TipoProducto(str, enum.Enum):
    FRUTA = "fruta"
    HORTALIZA = "hortaliza"
    PLANTA_MEDICINAL = "planta_medicinal"

class Producto(Base):
    __tablename__ = "productos"
    
    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    tipo = Column(Enum(TipoProducto), nullable=False)
    variedad = Column(String(100), nullable=True)
    unidad_medida = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    variables = relationship("VariableConfig", back_populates="producto", cascade="all, delete-orphan")
    atributos = relationship("AtributoConfig", back_populates="producto", cascade="all, delete-orphan")
    muestras = relationship("Muestra", back_populates="producto", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Producto {self.nombre}>"
