from sqlalchemy.orm import Session
from models.analista import Analista
from models.muestra import Muestra
from typing import List, Optional

class AnalistaRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def crear(self, nombre: str, apellido: str, cargo: str = None, 
              contacto: str = None) -> Analista:
        analista = Analista(
            nombre=nombre,
            apellido=apellido,
            cargo=cargo,
            contacto=contacto
        )
        self.session.add(analista)
        self.session.commit()
        self.session.refresh(analista)
        return analista
    
    def obtener_por_id(self, id_analista: int) -> Optional[Analista]:
        return self.session.query(Analista).filter(Analista.id_analista == id_analista).first()
    
    def obtener_todos(self) -> List[Analista]:
        return self.session.query(Analista).all()
    
    def actualizar(self, id_analista: int, **kwargs) -> Optional[Analista]:
        analista = self.obtener_por_id(id_analista)
        if analista:
            for key, value in kwargs.items():
                if hasattr(analista, key):
                    setattr(analista, key, value)
            self.session.commit()
            self.session.refresh(analista)
        return analista
    
    def eliminar(self, id_analista: int) -> bool:
        analista = self.obtener_por_id(id_analista)
        if analista:
            tiene_muestras = self.session.query(Muestra).filter(
                Muestra.id_analista == id_analista
            ).count() > 0
            if tiene_muestras:
                return False
            self.session.delete(analista)
            self.session.commit()
            return True
        return False
    
    def contar(self) -> int:
        return self.session.query(Analista).count()
    
    def buscar_por_nombre(self, nombre: str) -> List[Analista]:
        return self.session.query(Analista).filter(
            Analista.nombre.like(f"%{nombre}%")
        ).all()
