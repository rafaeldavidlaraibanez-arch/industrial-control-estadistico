import streamlit as st
import pandas as pd
from calculators.estadisticas import calcular_diagrama_pareto
from utils.graficos import GraficosAnalisis
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_error, mostrar_info,
    seleccionar_producto, seleccionar_atributo
)

# Configuración de la página
st.set_page_config(
    page_title="Diagrama de Pareto - CEC",
    page_icon="🎨",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Análisis de Pareto",
    "Identificar los defectos vitales (Regla 80/20)",
    "🎨"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Seleccionar producto
    producto = seleccionar_producto(repos)
    
    if producto:
        st.markdown("---")
        
        # Opción: Usar datos de un atributo específico o entrada manual
        opcion_pareto = st.radio(
            "Selecciona la fuente de datos:",
            ["Datos de Atributo Registrado", "Entrada Manual de Defectos"]
        )
        
        if opcion_pareto == "Datos de Atributo Registrado":
            atributo = seleccionar_atributo(repos, producto.id_producto)
            
            if atributo:
                # Obtener mediciones
                mediciones = repos['medicion_atributo'].obtener_por_atributo(atributo.id_atributo)
                
                if len(mediciones) == 0:
                    mostrar_info("No hay datos registrados para este atributo")
                else:
                    # Contar total de defectos
                    total_defectos = sum(m.n_defectuosos for m in mediciones)
                    
                    if total_defectos == 0:
                        mostrar_error("No hay defectos registrados")
                    else:
                        # Para Pareto, necesitamos desglose por tipo de defecto
                        # Como no tenemos eso en el modelo, usamos una aproximación
                        st.warning("⚠️ Para un análisis más detallado, necesitas especificar los tipos de defectos")
                        
                        # Mostrar resumen general
                        st.markdown("### Resumen General de Defectos")
                        resumen_df = pd.DataFrame({
                            "Métrica": ["Total de Muestras", "Total de Defectos", "Promedio Defectos/Muestra"],
                            "Valor": [len(mediciones), total_defectos, total_defectos / len(mediciones)]
                        })
                        st.dataframe(resumen_df, hide_index=True, use_container_width=True)
        
        else:  # Entrada manual
            st.markdown("### Ingresa los Tipos de Defectos y sus Cantidades")
            
            # Área para entrada de defectos
            defectos_input = st.text_area(
                "Ingresa los defectos (uno por línea, formato: Nombre,Cantidad)",
                placeholder="""Grietas,15
Manchas,8
Deformaciones,5
Tamaño incorrecto,3
Coloración,2""",
                height=200
            )
            
            if defectos_input:
                try:
                    # Procesar entrada
                    defectos_dict = {}
                    for linea in defectos_input.strip().split('\n'):
                        if ',' in linea:
                            nombre, cantidad = linea.split(',')
                            defectos_dict[nombre.strip()] = int(cantidad.strip())
                    
                    if defectos_dict:
                        # Calcular Pareto
                        datos_pareto = calcular_diagrama_pareto(defectos_dict)
                        
                        if "error" not in datos_pareto:
                            # Mostrar gráfico
                            fig = GraficosAnalisis.diagrama_pareto(datos_pareto)
                            st.plotly_chart(fig, use_container_width=True)
                            
                            st.markdown("---")
                            
                            # Mostrar datos
                            col_datos, col_factores = st.columns(2)
                            
                            with col_datos:
                                st.markdown("### Detalle de Defectos")
                                datos_detalle = pd.DataFrame({
                                    "Tipo de Defecto": datos_pareto["tipos"],
                                    "Cantidad": datos_pareto["cantidades"],
                                    "% Individual": datos_pareto["porcentajes"],
                                    "% Acumulado": datos_pareto["porcentajes_acumulados"]
                                })
                                st.dataframe(datos_detalle, hide_index=True, use_container_width=True)
                            
                            with col_factores:
                                st.markdown("### Factores Vitales")
                                
                                factores_vitales = [datos_pareto["tipos"][i] for i in datos_pareto["factores_vitales"]]
                                cantidades_vitales = [datos_pareto["cantidades"][i] for i in datos_pareto["factores_vitales"]]
                                
                                st.info(f"""
                                **Número de Factores Vitales:** {datos_pareto['num_factores_vitales']} de {len(datos_pareto['tipos'])}
                                
                                **Regla 80/20:** El {len(datos_pareto['factores_vitales'])} {len(datos_pareto['factores_vitales']) == 1 and 'factor' or 'factores'} vital{len(datos_pareto['factores_vitales']) > 1 and 'es' or ''} represent{len(datos_pareto['factores_vitales']) > 1 and 'an' or 'a'} 
                                aproximadamente el 80% de los defectos.
                                """)
                                
                                factores_df = pd.DataFrame({
                                    "Factor Vital": factores_vitales,
                                    "Cantidad": cantidades_vitales
                                })
                                st.dataframe(factores_df, hide_index=True, use_container_width=True)
                            
                            st.markdown("---")
                            
                            st.markdown("### Recomendaciones")
                            st.markdown(f"""
                            1. **Enfoque**: Concentrar esfuerzos en los {datos_pareto['num_factores_vitales']} factor{datos_pareto['num_factores_vitales'] > 1 and 'es' or ''} vital{datos_pareto['num_factores_vitales'] > 1 and 'es' or ''} identificado{datos_pareto['num_factores_vitales'] > 1 and 's' or ''}:
                               {", ".join(factores_vitales)}
                            
                            2. **Impacto Potencial**: Reduciendo solo estos defectos podrías eliminar ~80% de los problemas.
                            
                            3. **Próximos Pasos**:
                               - Investigar las causas raíz
                               - Implementar plan de mejora
                               - Monitorear continuamente
                            """)
                        else:
                            mostrar_error(datos_pareto["error"])
                    else:
                        mostrar_error("No se encontraron defectos válidos")
                except Exception as e:
                    mostrar_error(f"Error procesando los datos: {str(e)}")

finally:
    cerrar_sesion(repos['session'])
