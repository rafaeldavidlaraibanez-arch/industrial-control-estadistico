from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.muestra import Muestra, MedicionVariable, MedicionAtributo
from typing import List, Optional

class MuestraRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def crear(self, id_producto: int, id_analista: int, num_subgrupo: int,
              lote: str = None, origen: str = None, observaciones: str = None) -> Muestra:
        muestra = Muestra(
            id_producto=id_producto,
            id_analista=id_analista,
            num_subgrupo=num_subgrupo,
            lote=lote,
            origen=origen,
            observaciones=observaciones
        )
        self.session.add(muestra)
        self.session.commit()
        self.session.refresh(muestra)
        return muestra
    
    def obtener_por_id(self, id_muestra: int) -> Optional[Muestra]:
        return self.session.query(Muestra).filter(Muestra.id_muestra == id_muestra).first()
    
    def obtener_por_producto(self, id_producto: int) -> List[Muestra]:
        return self.session.query(Muestra).filter(
            Muestra.id_producto == id_producto
        ).order_by(desc(Muestra.fecha_hora)).all()
    
    def obtener_por_analista(self, id_analista: int) -> List[Muestra]:
        return self.session.query(Muestra).filter(
            Muestra.id_analista == id_analista
        ).order_by(desc(Muestra.fecha_hora)).all()
    
    def obtener_todas(self) -> List[Muestra]:
        return self.session.query(Muestra).order_by(desc(Muestra.fecha_hora)).all()
    
    def obtener_ultimas(self, limit: int = 100) -> List[Muestra]:
        return self.session.query(Muestra).order_by(
            desc(Muestra.fecha_hora)
        ).limit(limit).all()
    
    def obtener_por_producto_y_subgrupo(self, id_producto: int, num_subgrupo: int) -> Optional[Muestra]:
        return self.session.query(Muestra).filter(
            Muestra.id_producto == id_producto,
            Muestra.num_subgrupo == num_subgrupo
        ).first()
    
    def obtener_por_lote(self, lote: str) -> List[Muestra]:
        return self.session.query(Muestra).filter(
            Muestra.lote == lote
        ).order_by(desc(Muestra.fecha_hora)).all()
    
    def contar_por_producto(self, id_producto: int) -> int:
        return self.session.query(Muestra).filter(
            Muestra.id_producto == id_producto
        ).count()
    
    def eliminar(self, id_muestra: int) -> bool:
        muestra = self.obtener_por_id(id_muestra)
        if muestra:
            self.session.delete(muestra)
            self.session.commit()
            return True
        return False


class MedicionVariableRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def crear(self, id_muestra: int, id_variable: int, num_observacion: int,
              valor: float, es_atipico: bool = False) -> MedicionVariable:
        medicion = MedicionVariable(
            id_muestra=id_muestra,
            id_variable=id_variable,
            num_observacion=num_observacion,
            valor=valor,
            es_atipico=es_atipico
        )
        self.session.add(medicion)
        self.session.commit()
        self.session.refresh(medicion)
        return medicion
    
    def obtener_por_muestra(self, id_muestra: int) -> List[MedicionVariable]:
        return self.session.query(MedicionVariable).filter(
            MedicionVariable.id_muestra == id_muestra
        ).all()
    
    def obtener_por_variable(self, id_variable: int) -> List[MedicionVariable]:
        return self.session.query(MedicionVariable).filter(
            MedicionVariable.id_variable == id_variable
        ).all()
    
    def obtener_todos(self) -> List[MedicionVariable]:
        return self.session.query(MedicionVariable).all()
    
    def contar_por_variable(self, id_variable: int) -> int:
        return self.session.query(MedicionVariable).filter(
            MedicionVariable.id_variable == id_variable
        ).count()


class MedicionAtributoRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def crear(self, id_muestra: int, id_atributo: int, n_inspeccionados: int,
              n_defectuosos: int, fuera_control: bool = False) -> MedicionAtributo:
        medicion = MedicionAtributo(
            id_muestra=id_muestra,
            id_atributo=id_atributo,
            n_inspeccionados=n_inspeccionados,
            n_defectuosos=n_defectuosos,
            fuera_control=fuera_control
        )
        self.session.add(medicion)
        self.session.commit()
        self.session.refresh(medicion)
        return medicion
    
    def obtener_por_muestra(self, id_muestra: int) -> List[MedicionAtributo]:
        return self.session.query(MedicionAtributo).filter(
            MedicionAtributo.id_muestra == id_muestra
        ).all()
    
    def obtener_por_atributo(self, id_atributo: int) -> List[MedicionAtributo]:
        return self.session.query(MedicionAtributo).filter(
            MedicionAtributo.id_atributo == id_atributo
        ).all()
    
    def obtener_todos(self) -> List[MedicionAtributo]:
        return self.session.query(MedicionAtributo).all()
    
    def contar_por_atributo(self, id_atributo: int) -> int:
        return self.session.query(MedicionAtributo).filter(
            MedicionAtributo.id_atributo == id_atributo
        ).count()
