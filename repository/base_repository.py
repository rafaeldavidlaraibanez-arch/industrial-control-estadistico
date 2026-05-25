from sqlalchemy.orm import Session
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Clase base para operaciones CRUD"""
    
    def __init__(self, session: Session, model_class):
        self.session = session
        self.model_class = model_class
    
    def crear(self, obj_in) -> T:
        """Crea un nuevo registro"""
        db_obj = self.model_class(**obj_in.dict())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def obtener_por_id(self, obj_id: int) -> Optional[T]:
        """Obtiene un registro por ID"""
        return self.session.query(self.model_class).filter(
            self.model_class.id == obj_id
        ).first()
    
    def obtener_todos(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtiene todos los registros"""
        return self.session.query(self.model_class).offset(skip).limit(limit).all()
    
    def actualizar(self, obj_id: int, obj_in) -> Optional[T]:
        """Actualiza un registro"""
        db_obj = self.obtener_por_id(obj_id)
        if db_obj:
            for key, value in obj_in.dict().items():
                setattr(db_obj, key, value)
            self.session.commit()
            self.session.refresh(db_obj)
        return db_obj
    
    def eliminar(self, obj_id: int) -> bool:
        """Elimina un registro"""
        db_obj = self.obtener_por_id(obj_id)
        if db_obj:
            self.session.delete(db_obj)
            self.session.commit()
            return True
        return False
    
    def contar(self) -> int:
        """Cuenta el total de registros"""
        return self.session.query(self.model_class).count()
