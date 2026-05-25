import streamlit as st
import pandas as pd
import numpy as np
from calculators.estadisticas import (
    normalidad_shapiro_wilk, normalidad_ks, normalidad_anderson_darling,
    estadisticas_descriptivas
)
from utils.graficos import GraficosAnalisis
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_error, mostrar_info,
    seleccionar_producto, seleccionar_variable
)

# Configuración de la página
st.set_page_config(
    page_title="Pruebas de Normalidad - CEC",
    page_icon="✅",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Análisis de Normalidad",
    "Pruebas de distribución normal (Shapiro-Wilk, Kolmogorov-Smirnov, Anderson-Darling)",
    "✅"
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
        mediciones_obj = repos['medicion_variable'].obtener_por_variable(variable.id_variable)
        
        if len(mediciones_obj) < 3:
            mostrar_error("Se necesitan al menos 3 mediciones para realizar las pruebas de normalidad")
        else:
            valores_medidos = [float(m.valor) for m in mediciones_obj]
            
            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Shapiro-Wilk", "📈 Kolmogorov-Smirnov", "🔍 Anderson-Darling", "📉 Visualización"])
            
            with tab1:
                st.subheader("Prueba de Normalidad Shapiro-Wilk")
                
                resultado_sw = normalidad_shapiro_wilk(valores_medidos)
                
                if "error" not in resultado_sw:
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("### Resultados")
                        resultados_df = pd.DataFrame({
                            "Parámetro": ["Estadístico W", "p-valor", "Nivel de Significancia"],
                            "Valor": [
                                f"{resultado_sw['estadistico_w']:.6f}",
                                f"{resultado_sw['p_valor']:.6f}",
                                "α = 0.05"
                            ]
                        })
                        st.dataframe(resultados_df, hide_index=True, use_container_width=True)
                    
                    with col_right:
                        st.markdown("### Conclusión")
                        if resultado_sw['es_normal']:
                            st.success(f"✅ {resultado_sw['interpretacion']}")
                            st.markdown("Los datos provienen de una distribución normal con 95% de confianza.")
                        else:
                            st.warning(f"⚠️ {resultado_sw['interpretacion']}")
                            st.markdown("Los datos NO provienen de una distribución normal.")
                else:
                    mostrar_error(resultado_sw["error"])
            
            with tab2:
                st.subheader("Prueba de Normalidad Kolmogorov-Smirnov")
                
                resultado_ks = normalidad_ks(valores_medidos)
                
                if "error" not in resultado_ks:
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("### Resultados")
                        resultados_df = pd.DataFrame({
                            "Parámetro": ["Estadístico D", "p-valor", "Nivel de Significancia"],
                            "Valor": [
                                f"{resultado_ks['estadistico']:.6f}",
                                f"{resultado_ks['p_valor']:.6f}",
                                "α = 0.05"
                            ]
                        })
                        st.dataframe(resultados_df, hide_index=True, use_container_width=True)
                    
                    with col_right:
                        st.markdown("### Conclusión")
                        if resultado_ks['es_normal']:
                            st.success(f"✅ {resultado_ks['interpretacion']}")
                        else:
                            st.warning(f"⚠️ {resultado_ks['interpretacion']}")
                else:
                    mostrar_error(resultado_ks["error"])
            
            with tab3:
                st.subheader("Prueba de Normalidad Anderson-Darling")
                
                resultado_ad = normalidad_anderson_darling(valores_medidos)
                
                if "error" not in resultado_ad:
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("### Resultados")
                        resultados_df = pd.DataFrame({
                            "Parámetro": ["Estadístico A²", "Valor Crítico (5%)", "Decisión"],
                            "Valor": [
                                f"{resultado_ad['estadistico']:.6f}",
                                f"{resultado_ad['valores_criticos'][2]:.6f}",
                                "Normal" if resultado_ad['es_normal'] else "No Normal"
                            ]
                        })
                        st.dataframe(resultados_df, hide_index=True, use_container_width=True)
                        
                        st.markdown("### Valores Críticos")
                        valores_criticos_df = pd.DataFrame({
                            "Nivel de Significancia": resultado_ad['niveles_significancia'],
                            "Valor Crítico": resultado_ad['valores_criticos']
                        })
                        st.dataframe(valores_criticos_df, hide_index=True, use_container_width=True)
                    
                    with col_right:
                        st.markdown("### Conclusión")
                        if resultado_ad['es_normal']:
                            st.success(f"✅ {resultado_ad['interpretacion']}")
                        else:
                            st.warning(f"⚠️ {resultado_ad['interpretacion']}")
                else:
                    mostrar_error(resultado_ad["error"])
            
            with tab4:
                st.subheader("Visualización de Distribución")
                
                # Estadísticas
                stats = estadisticas_descriptivas(valores_medidos)
                
                col_viz1, col_viz2 = st.columns(2)
                
                with col_viz1:
                    # Histograma con curva normal
                    fig_hist = GraficosAnalisis.histograma_con_normal(
                        valores_medidos,
                        stats['media'],
                        stats['desv_std']
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col_viz2:
                    # Gráfico Q-Q
                    fig_qq = GraficosAnalisis.grafico_q_q(valores_medidos)
                    st.plotly_chart(fig_qq, use_container_width=True)
                
                st.markdown("---")
                st.markdown("### Resumen de Pruebas")
                
                pruebas_resumen = pd.DataFrame({
                    "Prueba": ["Shapiro-Wilk", "Kolmogorov-Smirnov", "Anderson-Darling"],
                    "Normal": [
                        "✅" if normalidad_shapiro_wilk(valores_medidos).get('es_normal', False) else "❌",
                        "✅" if normalidad_ks(valores_medidos).get('es_normal', False) else "❌",
                        "✅" if normalidad_anderson_darling(valores_medidos).get('es_normal', False) else "❌"
                    ]
                })
                st.dataframe(pruebas_resumen, hide_index=True, use_container_width=True)

finally:
    cerrar_sesion(repos['session'])
