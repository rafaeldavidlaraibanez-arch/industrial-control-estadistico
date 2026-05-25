from sqlalchemy.orm import Session
from models.variables import VariableConfig, AtributoConfig
from typing import List, Optional

class VariableRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def crear(self, id_producto: int, nombre_variable: str, tipo_dato: str = "continua",
              lcs: float = None, lci: float = None, valor_nominal: float = None,
              tam_subgrupo: int = 5, unidad_medida: str = None, 
              descripcion: str = None) -> VariableConfig:
        variable = VariableConfig(
            id_producto=id_producto,
            nombre_variable=nombre_variable,
            tipo_dato=tipo_dato,
            lcs=lcs,
            lci=lci,
            valor_nominal=valor_nominal,
            tam_subgrupo=tam_subgrupo,
            unidad_medida=unidad_medida,
            descripcion=descripcion
        )
        self.session.add(variable)
        self.session.commit()
        self.session.refresh(variable)
        return variable
    
    def obtener_por_id(self, id_variable: int) -> Optional[VariableConfig]:
        return self.session.query(VariableConfig).filter(
            VariableConfig.id_variable == id_variable
        ).first()
    
    def obtener_por_producto(self, id_producto: int) -> List[VariableConfig]:
        return self.session.query(VariableConfig).filter(
            VariableConfig.id_producto == id_producto
        ).all()
    
    def obtener_todos(self) -> List[VariableConfig]:
        return self.session.query(VariableConfig).all()
    
    def actualizar(self, id_variable: int, **kwargs) -> Optional[VariableConfig]:
        variable = self.obtener_por_id(id_variable)
        if variable:
            for key, value in kwargs.items():
                if hasattr(variable, key):
                    setattr(variable, key, value)
            self.session.commit()
            self.session.refresh(variable)
        return variable
    
    def eliminar(self, id_variable: int) -> bool:
        variable = self.obtener_por_id(id_variable)
        if variable:
            self.session.delete(variable)
            self.session.commit()
            return True
        return False
    
    def contar_por_producto(self, id_producto: int) -> int:
        return self.session.query(VariableConfig).filter(
            VariableConfig.id_producto == id_producto
        ).count()


class AtributoRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def crear(self, id_producto: int, nombre_atributo: str, tipo_grafico: str,
              tam_subgrupo: int = 50, descripcion: str = None) -> AtributoConfig:
        atributo = AtributoConfig(
            id_producto=id_producto,
            nombre_atributo=nombre_atributo,
            tipo_grafico=tipo_grafico,
            tam_subgrupo=tam_subgrupo,
            descripcion=descripcion
        )
        self.session.add(atributo)
        self.session.commit()
        self.session.refresh(atributo)
        return atributo
    
    def obtener_por_id(self, id_atributo: int) -> Optional[AtributoConfig]:
        return self.session.query(AtributoConfig).filter(
            AtributoConfig.id_atributo == id_atributo
        ).first()
    
    def obtener_por_producto(self, id_producto: int) -> List[AtributoConfig]:
        return self.session.query(AtributoConfig).filter(
            AtributoConfig.id_producto == id_producto
        ).all()
    
    def obtener_todos(self) -> List[AtributoConfig]:
        return self.session.query(AtributoConfig).all()
    
    def actualizar(self, id_atributo: int, **kwargs) -> Optional[AtributoConfig]:
        atributo = self.obtener_por_id(id_atributo)
        if atributo:
            for key, value in kwargs.items():
                if hasattr(atributo, key):
                    setattr(atributo, key, value)
            self.session.commit()
            self.session.refresh(atributo)
        return atributo
    
    def eliminar(self, id_atributo: int) -> bool:
        atributo = self.obtener_por_id(id_atributo)
        if atributo:
            self.session.delete(atributo)
            self.session.commit()
            return True
        return False
    
    def contar_por_producto(self, id_producto: int) -> int:
        return self.session.query(AtributoConfig).filter(
            AtributoConfig.id_producto == id_producto
        ).count()
