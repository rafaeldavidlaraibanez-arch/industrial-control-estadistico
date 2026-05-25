import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
from typing import List, Dict, Any
from datetime import datetime

class ExportadorDatos:
    """Clase para exportar datos a diferentes formatos"""
    
    @staticmethod
    def exportar_a_excel(datos: Dict[str, pd.DataFrame], nombre_archivo: str = "reporte") -> bytes:
        """
        Exporta múltiples DataFrames a un archivo Excel con múltiples hojas
        """
        buffer = BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            for nombre_hoja, df in datos.items():
                df.to_excel(writer, sheet_name=nombre_hoja[:31], index=False)
                
                # Aplicar formato
                worksheet = writer.sheets[nombre_hoja[:31]]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        buffer.seek(0)
        return buffer.getvalue()
    
    @staticmethod
    def exportar_a_csv(df: pd.DataFrame, nombre_archivo: str = "datos") -> bytes:
        """Exporta DataFrame a CSV"""
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        return csv_bytes
    
    @staticmethod
    def crear_reporte_estadistico(estadisticas: Dict, nombre_producto: str) -> Dict[str, pd.DataFrame]:
        """Crea un reporte con estadísticas descriptivas"""
        reporte = {}
        
        # Estadísticas descriptivas
        stats_df = pd.DataFrame({
            "Parámetro": list(estadisticas.keys()),
            "Valor": list(estadisticas.values())
        })
        reporte["Estadísticas"] = stats_df
        
        return reporte
    
    @staticmethod
    def crear_reporte_control(datos_control: Dict, tipo: str = "XR") -> Dict[str, pd.DataFrame]:
        """Crea reporte de gráficos de control"""
        reporte = {}
        
        if tipo == "XR":
            df_xbars = pd.DataFrame({
                "Subgrupo": list(range(1, len(datos_control["xbars"]) + 1)),
                "X̄": datos_control["xbars"],
                "R": datos_control["rangos"],
                "Fuera de Control (X̄)": [i+1 if i in datos_control["puntos_fuera_xbar"] else "" 
                                         for i in range(len(datos_control["xbars"]))]
            })
            reporte["Datos Control"] = df_xbars
            
            resumen = pd.DataFrame({
                "Parámetro": ["X̄ Promedio", "R Promedio", "LCS (X̄)", "LCI (X̄)", "LCS (R)", "LCI (R)"],
                "Valor": [
                    datos_control["xbar_bar"],
                    datos_control["rango_promedio"],
                    datos_control["lcs_xbar"],
                    datos_control["lci_xbar"],
                    datos_control["lcs_r"],
                    datos_control["lci_r"]
                ]
            })
            reporte["Resumen"] = resumen
        
        elif tipo == "XS":
            df_xbars = pd.DataFrame({
                "Subgrupo": list(range(1, len(datos_control["xbars"]) + 1)),
                "X̄": datos_control["xbars"],
                "S": datos_control["desv_stds"],
                "Fuera de Control (X̄)": [i+1 if i in datos_control["puntos_fuera_xbar"] else "" 
                                         for i in range(len(datos_control["xbars"]))]
            })
            reporte["Datos Control"] = df_xbars
            
            resumen = pd.DataFrame({
                "Parámetro": ["X̄ Promedio", "S Promedio", "LCS (X̄)", "LCI (X̄)", "LCS (S)", "LCI (S)"],
                "Valor": [
                    datos_control["xbar_bar"],
                    datos_control["s_promedio"],
                    datos_control["lcs_xbar"],
                    datos_control["lci_xbar"],
                    datos_control["lcs_s"],
                    datos_control["lci_s"]
                ]
            })
            reporte["Resumen"] = resumen
        
        return reporte


class ConvertidorDatos:
    """Utilidades para convertir y procesar datos"""
    
    @staticmethod
    def lista_a_dataframe(datos: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convierte lista de diccionarios a DataFrame"""
        return pd.DataFrame(datos)
    
    @staticmethod
    def agrupar_por_producto(muestras_con_datos: List[Dict]) -> Dict[str, List[Dict]]:
        """Agrupa muestras por producto"""
        agrupadas = {}
        for muestra in muestras_con_datos:
            producto = muestra.get('producto_nombre', 'Sin producto')
            if producto not in agrupadas:
                agrupadas[producto] = []
            agrupadas[producto].append(muestra)
        return agrupadas
    
    @staticmethod
    def preparar_datos_para_grafico_control(mediciones: List[float], 
                                            tam_subgrupo: int) -> List[float]:
        """Prepara datos para análisis de gráficos de control"""
        # Validar que hay suficientes datos
        if len(mediciones) < tam_subgrupo * 2:
            raise ValueError(f"Se necesitan al menos {tam_subgrupo * 2} mediciones")
        return mediciones
    
    @staticmethod
    def obtener_estadisticas_basicas(serie: pd.Series) -> Dict[str, float]:
        """Obtiene estadísticas básicas de una serie"""
        return {
            "media": serie.mean(),
            "mediana": serie.median(),
            "desv_est": serie.std(),
            "min": serie.min(),
            "max": serie.max(),
            "q1": serie.quantile(0.25),
            "q3": serie.quantile(0.75),
            "rango": serie.max() - serie.min()
        }

class GeneradorReportes:
    """Generador de reportes profesionales"""
    
    @staticmethod
    def resumen_proyecto(
        num_productos: int,
        num_muestras: int,
        num_analistas: int,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Dict[str, str]:
        """Genera resumen del proyecto"""
        dias = (fecha_fin - fecha_inicio).days
        
        return {
            "Productos registrados": str(num_productos),
            "Muestras analizadas": str(num_muestras),
            "Analistas": str(num_analistas),
            "Período": f"{fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}",
            "Días de análisis": str(dias),
            "Promedio muestras/día": f"{num_muestras / dias:.1f}" if dias > 0 else "0"
        }
