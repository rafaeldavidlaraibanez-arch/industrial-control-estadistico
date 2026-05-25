from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from models.base import Base
import enum

class TipoGrafico(str, enum.Enum):
    P = "P"
    NP = "NP"
    C = "C"
    U = "U"

class VariableConfig(Base):
    __tablename__ = "variable_configs"
    
    id_variable = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    nombre_variable = Column(String(100), nullable=False)
    tipo_dato = Column(String(50), default="continua")
    lcs = Column(Float, nullable=True, doc="Limite Control Superior")
    lci = Column(Float, nullable=True, doc="Limite Control Inferior")
    valor_nominal = Column(Float, nullable=True)
    tam_subgrupo = Column(Integer, default=5)
    unidad_medida = Column(String(50), nullable=True)
    descripcion = Column(Text, nullable=True)
    
    # Relaciones
    producto = relationship("Producto", back_populates="variables")
    mediciones = relationship("MedicionVariable", back_populates="variable", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<VariableConfig {self.nombre_variable}>"

class AtributoConfig(Base):
    __tablename__ = "atributo_configs"
    
    id_atributo = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    nombre_atributo = Column(String(100), nullable=False)
    tipo_grafico = Column(Enum(TipoGrafico), nullable=False)
    tam_subgrupo = Column(Integer, default=50)
    descripcion = Column(Text, nullable=True)
    
    # Relaciones
    producto = relationship("Producto", back_populates="atributos")
    mediciones = relationship("MedicionAtributo", back_populates="atributo", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AtributoConfig {self.nombre_atributo}>"
