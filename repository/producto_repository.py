from sqlalchemy.orm import Session
from models.producto import Producto
from typing import List, Optional

class ProductoRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def crear(self, nombre: str, tipo: str, variedad: str = None, 
              unidad_medida: str = None, descripcion: str = None) -> Producto:
        producto = Producto(
            nombre=nombre,
            tipo=tipo,
            variedad=variedad,
            unidad_medida=unidad_medida,
            descripcion=descripcion
        )
        self.session.add(producto)
        self.session.commit()
        self.session.refresh(producto)
        return producto
    
    def obtener_por_id(self, id_producto: int) -> Optional[Producto]:
        return self.session.query(Producto).filter(Producto.id_producto == id_producto).first()
    
    def obtener_por_nombre(self, nombre: str) -> Optional[Producto]:
        return self.session.query(Producto).filter(Producto.nombre == nombre).first()
    
    def obtener_todos(self) -> List[Producto]:
        return self.session.query(Producto).all()
    
    def obtener_por_tipo(self, tipo: str) -> List[Producto]:
        return self.session.query(Producto).filter(Producto.tipo == tipo).all()
    
    def actualizar(self, id_producto: int, **kwargs) -> Optional[Producto]:
        producto = self.obtener_por_id(id_producto)
        if producto:
            for key, value in kwargs.items():
                if hasattr(producto, key):
                    setattr(producto, key, value)
            self.session.commit()
            self.session.refresh(producto)
        return producto
    
    def eliminar(self, id_producto: int) -> bool:
        producto = self.obtener_por_id(id_producto)
        if producto:
            self.session.delete(producto)
            self.session.commit()
            return True
        return False
    
    def contar(self) -> int:
        return self.session.query(Producto).count()
