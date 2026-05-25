from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Analista(Base):
    __tablename__ = "analistas"
    
    id_analista = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=True)
    contacto = Column(String(100), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    muestras = relationship("Muestra", back_populates="analista")
    
    def __repr__(self):
        return f"<Analista {self.nombre} {self.apellido}>"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
