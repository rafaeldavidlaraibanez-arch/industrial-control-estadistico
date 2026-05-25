from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Muestra(Base):
    __tablename__ = "muestras"
    
    id_muestra = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_analista = Column(Integer, ForeignKey("analistas.id_analista"), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    num_subgrupo = Column(Integer, nullable=False)
    lote = Column(String(100), nullable=True)
    origen = Column(String(200), nullable=True)
    observaciones = Column(Text, nullable=True)
    
    # Relaciones
    producto = relationship("Producto", back_populates="muestras")
    analista = relationship("Analista", back_populates="muestras")
    mediciones_variables = relationship("MedicionVariable", back_populates="muestra", cascade="all, delete-orphan")
    mediciones_atributos = relationship("MedicionAtributo", back_populates="muestra", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Muestra {self.id_muestra}>"

class MedicionVariable(Base):
    __tablename__ = "mediciones_variables"
    
    id_medicion = Column(Integer, primary_key=True, index=True)
    id_muestra = Column(Integer, ForeignKey("muestras.id_muestra"), nullable=False)
    id_variable = Column(Integer, ForeignKey("variable_configs.id_variable"), nullable=False)
    num_observacion = Column(Integer, nullable=False, doc="Numero dentro del subgrupo")
    valor = Column(Float, nullable=False)
    es_atipico = Column(Boolean, default=False)
    
    # Relaciones
    muestra = relationship("Muestra", back_populates="mediciones_variables")
    variable = relationship("VariableConfig", back_populates="mediciones")
    
    def __repr__(self):
        return f"<MedicionVariable {self.valor}>"

class MedicionAtributo(Base):
    __tablename__ = "mediciones_atributos"
    
    id_med_atrib = Column(Integer, primary_key=True, index=True)
    id_muestra = Column(Integer, ForeignKey("muestras.id_muestra"), nullable=False)
    id_atributo = Column(Integer, ForeignKey("atributo_configs.id_atributo"), nullable=False)
    n_inspeccionados = Column(Integer, nullable=False)
    n_defectuosos = Column(Integer, nullable=False)
    fuera_control = Column(Boolean, default=False)
    
    # Relaciones
    muestra = relationship("Muestra", back_populates="mediciones_atributos")
    atributo = relationship("AtributoConfig", back_populates="mediciones")
    
    def __repr__(self):
        return f"<MedicionAtributo defectos:{self.n_defectuosos}/{self.n_inspeccionados}>"
