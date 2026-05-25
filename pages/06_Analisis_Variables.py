import streamlit as st
import pandas as pd
from calculators.estadisticas import calcular_xbar_r, calcular_xbar_s, estadisticas_descriptivas
from utils.graficos import GraficosControl
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_exito, mostrar_error, mostrar_info,
    seleccionar_producto, seleccionar_variable
)
from models.muestra import Muestra, MedicionVariable

# Configuración de la página
st.set_page_config(
    page_title="Análisis por Variables - CEC",
    page_icon="📈",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Control por Variables",
    "Análisis de gráficos X̄-R y X̄-S",
    "📈"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Seleccionar producto y variable
    col_select1, col_select2 = st.columns(2)
    
    with col_select1:
        producto = seleccionar_producto(repos)
    
    with col_select2:
        if producto:
            variable = seleccionar_variable(repos, producto.id_producto)
    
    if producto and variable:
        # Obtener mediciones
        mediciones = repos['medicion_variable'].obtener_por_variable(variable.id_variable)
        
        if len(mediciones) < variable.tam_subgrupo * 2:
            mostrar_error(f"Se necesitan al menos {variable.tam_subgrupo * 2} mediciones. Actualmente hay {len(mediciones)}")
        else:
            valores_medidos = [float(m.valor) for m in mediciones]
            
            # Tabs para diferentes análisis
            tab1, tab2, tab3 = st.tabs(["📊 Gráfico X̄-R", "📈 Gráfico X̄-S", "📉 Estadísticas"])
            
            with tab1:
                st.subheader("Gráfico de Control X̄-R")
                
                datos_xr = calcular_xbar_r(valores_medidos, variable.tam_subgrupo)
                
                if "error" not in datos_xr:
                    # Mostrar gráfico
                    fig = GraficosControl.grafico_xbar_r(datos_xr)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Mostrar datos
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("### Datos de Promedios")
                        resumen_xbar = pd.DataFrame({
                            "Parámetro": ["X̄ Promedio", "LCS (X̄)", "LCI (X̄)", "Puntos Fuera"],
                            "Valor": [
                                datos_xr["xbar_bar"],
                                datos_xr["lcs_xbar"],
                                datos_xr["lci_xbar"],
                                len(datos_xr["puntos_fuera_xbar"])
                            ]
                        })
                        st.dataframe(resumen_xbar, hide_index=True, use_container_width=True)
                    
                    with col_right:
                        st.markdown("### Datos de Rangos")
                        resumen_r = pd.DataFrame({
                            "Parámetro": ["R Promedio", "LCS (R)", "LCI (R)", "Puntos Fuera"],
                            "Valor": [
                                datos_xr["rango_promedio"],
                                datos_xr["lcs_r"],
                                datos_xr["lci_r"],
                                len(datos_xr["puntos_fuera_r"])
                            ]
                        })
                        st.dataframe(resumen_r, hide_index=True, use_container_width=True)
                    
                    # Interpretación
                    st.markdown("---")
                    st.markdown("### Interpretación")
                    
                    col_interp1, col_interp2 = st.columns(2)
                    
                    with col_interp1:
                        if len(datos_xr["puntos_fuera_xbar"]) == 0:
                            st.success("✅ Promedios bajo control - El proceso es estable en centrado")
                        else:
                            st.warning(f"⚠️ {len(datos_xr['puntos_fuera_xbar'])} puntos fuera de control en X̄")
                    
                    with col_interp2:
                        if len(datos_xr["puntos_fuera_r"]) == 0:
                            st.success("✅ Rangos bajo control - La variabilidad es consistente")
                        else:
                            st.warning(f"⚠️ {len(datos_xr['puntos_fuera_r'])} puntos fuera de control en R")
                else:
                    mostrar_error(datos_xr["error"])
            
            with tab2:
                st.subheader("Gráfico de Control X̄-S")
                
                datos_xs = calcular_xbar_s(valores_medidos, variable.tam_subgrupo)
                
                if "error" not in datos_xs:
                    # Mostrar gráfico
                    fig = GraficosControl.grafico_xbar_s(datos_xs)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Mostrar datos
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("### Datos de Promedios")
                        resumen_xbar = pd.DataFrame({
                            "Parámetro": ["X̄ Promedio", "LCS (X̄)", "LCI (X̄)", "Puntos Fuera"],
                            "Valor": [
                                datos_xs["xbar_bar"],
                                datos_xs["lcs_xbar"],
                                datos_xs["lci_xbar"],
                                len(datos_xs["puntos_fuera_xbar"])
                            ]
                        })
                        st.dataframe(resumen_xbar, hide_index=True, use_container_width=True)
                    
                    with col_right:
                        st.markdown("### Datos de Desviación Estándar")
                        resumen_s = pd.DataFrame({
                            "Parámetro": ["S Promedio", "LCS (S)", "LCI (S)", "Puntos Fuera"],
                            "Valor": [
                                datos_xs["s_promedio"],
                                datos_xs["lcs_s"],
                                datos_xs["lci_s"],
                                len(datos_xs["puntos_fuera_s"])
                            ]
                        })
                        st.dataframe(resumen_s, hide_index=True, use_container_width=True)
                    
                    # Interpretación
                    st.markdown("---")
                    st.markdown("### Interpretación")
                    
                    col_interp1, col_interp2 = st.columns(2)
                    
                    with col_interp1:
                        if len(datos_xs["puntos_fuera_xbar"]) == 0:
                            st.success("✅ Promedios bajo control")
                        else:
                            st.warning(f"⚠️ {len(datos_xs['puntos_fuera_xbar'])} puntos fuera en X̄")
                    
                    with col_interp2:
                        if len(datos_xs["puntos_fuera_s"]) == 0:
                            st.success("✅ Desviación estándar bajo control")
                        else:
                            st.warning(f"⚠️ {len(datos_xs['puntos_fuera_s'])} puntos fuera en S")
                else:
                    mostrar_error(datos_xs["error"])
            
            with tab3:
                st.subheader("Estadísticas Descriptivas")
                
                stats = estadisticas_descriptivas(valores_medidos)
                
                stats_df = pd.DataFrame({
                    "Medida": ["N", "Media", "Mediana", "Desv. Est.", "Varianza", "Mínimo", "Máximo", "Rango", "Q1", "Q3"],
                    "Valor": [
                        stats["n"],
                        f"{stats['media']:.4f}",
                        f"{stats['mediana']:.4f}",
                        f"{stats['desv_std']:.4f}",
                        f"{stats['varianza']:.4f}",
                        f"{stats['minimo']:.4f}",
                        f"{stats['maximo']:.4f}",
                        f"{stats['rango']:.4f}",
                        f"{stats['q1']:.4f}",
                        f"{stats['q3']:.4f}"
                    ]
                })
                
                st.dataframe(stats_df, hide_index=True, use_container_width=True)

finally:
    cerrar_sesion(repos['session'])
