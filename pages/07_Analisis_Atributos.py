import streamlit as st
import pandas as pd
from calculators.estadisticas import (
    calcular_grafico_p, calcular_grafico_np, 
    calcular_grafico_c, calcular_grafico_u
)
from utils.graficos import GraficosControl
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_error, mostrar_info,
    seleccionar_producto, seleccionar_atributo
)

# Configuración de la página
st.set_page_config(
    page_title="Análisis por Atributos - CEC",
    page_icon="🎯",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Control por Atributos",
    "Análisis de gráficos P, NP, C y U",
    "🎯"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Seleccionar producto y atributo
    col_select1, col_select2 = st.columns(2)
    
    with col_select1:
        producto = seleccionar_producto(repos)
    
    with col_select2:
        if producto:
            atributo = seleccionar_atributo(repos, producto.id_producto)
    
    if producto and atributo:
        # Obtener mediciones de atriboto
        mediciones = repos['medicion_atributo'].obtener_por_atributo(atributo.id_atributo)
        
        if len(mediciones) < 5:
            mostrar_info(f"Se recomiendan al menos 25 muestras. Actualmente hay {len(mediciones)}")
        else:
            # Extraer datos según el tipo de gráfico
            tipo_grafico = atributo.tipo_grafico
            
            defectuosos = [m.n_defectuosos for m in mediciones]
            inspeccionados = [m.n_inspeccionados for m in mediciones]
            
            # Tabs para diferentes análisis
            if tipo_grafico == "P":
                st.subheader("Gráfico de Control P (Proporción de Defectuosos)")
                
                datos = calcular_grafico_p(defectuosos, inspeccionados)
                
                if "error" not in datos:
                    fig = GraficosControl.grafico_p(datos)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("### Resumen P")
                        resumen = pd.DataFrame({
                            "Parámetro": ["p Promedio", "Puntos Fuera"],
                            "Valor": [datos["p_promedio"], len(datos["puntos_fuera"])]
                        })
                        st.dataframe(resumen, hide_index=True, use_container_width=True)
                    
                    with col_right:
                        st.markdown("### Interpretación")
                        if len(datos["puntos_fuera"]) == 0:
                            st.success("✅ Proceso bajo control")
                        else:
                            st.warning(f"⚠️ {len(datos['puntos_fuera'])} puntos fuera de control")
                else:
                    mostrar_error(datos["error"])
            
            elif tipo_grafico == "NP":
                st.subheader("Gráfico de Control NP (Número de Defectuosos)")
                
                datos = calcular_grafico_np(defectuosos, atributo.tam_subgrupo)
                
                if "error" not in datos:
                    fig = GraficosControl.grafico_np(datos)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("### Resumen NP")
                        resumen = pd.DataFrame({
                            "Parámetro": ["NP Promedio", "LCS", "LCI", "Puntos Fuera"],
                            "Valor": [
                                datos["np_promedio"],
                                datos["lcs"],
                                datos["lci"],
                                len(datos["puntos_fuera"])
                            ]
                        })
                        st.dataframe(resumen, hide_index=True, use_container_width=True)
                    
                    with col_right:
                        st.markdown("### Interpretación")
                        if len(datos["puntos_fuera"]) == 0:
                            st.success("✅ Proceso bajo control")
                        else:
                            st.warning(f"⚠️ {len(datos['puntos_fuera'])} puntos fuera de control")
                else:
                    mostrar_error(datos["error"])
            
            elif tipo_grafico == "C":
                st.subheader("Gráfico de Control C (Número de Defectos)")
                
                datos = calcular_grafico_c(defectuosos)
                
                if "error" not in datos:
                    fig = GraficosControl.grafico_c(datos)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("### Resumen C")
                        resumen = pd.DataFrame({
                            "Parámetro": ["C Promedio", "LCS", "LCI", "Puntos Fuera"],
                            "Valor": [
                                datos["c_promedio"],
                                datos["lcs"],
                                datos["lci"],
                                len(datos["puntos_fuera"])
                            ]
                        })
                        st.dataframe(resumen, hide_index=True, use_container_width=True)
                    
                    with col_right:
                        st.markdown("### Interpretación")
                        if len(datos["puntos_fuera"]) == 0:
                            st.success("✅ Proceso bajo control")
                        else:
                            st.warning(f"⚠️ {len(datos['puntos_fuera'])} puntos fuera de control")
                else:
                    mostrar_error(datos["error"])
            
            elif tipo_grafico == "U":
                st.subheader("Gráfico de Control U (Defectos por Unidad)")
                
                datos = calcular_grafico_u(defectuosos, inspeccionados)
                
                if "error" not in datos:
                    fig = GraficosControl.grafico_u(datos)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("### Resumen U")
                        resumen = pd.DataFrame({
                            "Parámetro": ["U Promedio", "Puntos Fuera"],
                            "Valor": [datos["u_promedio"], len(datos["puntos_fuera"])]
                        })
                        st.dataframe(resumen, hide_index=True, use_container_width=True)
                    
                    with col_right:
                        st.markdown("### Interpretación")
                        if len(datos["puntos_fuera"]) == 0:
                            st.success("✅ Proceso bajo control")
                        else:
                            st.warning(f"⚠️ {len(datos['puntos_fuera'])} puntos fuera de control")
                else:
                    mostrar_error(datos["error"])

finally:
    cerrar_sesion(repos['session'])
