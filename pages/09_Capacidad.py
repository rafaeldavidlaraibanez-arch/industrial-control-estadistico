import streamlit as st
import pandas as pd
from calculators.estadisticas import calcular_indices_capacidad, estadisticas_descriptivas
from utils.graficos import GraficosAnalisis
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_error, mostrar_info,
    seleccionar_producto, seleccionar_variable
)

# Configuración de la página
st.set_page_config(
    page_title="Capacidad del Proceso - CEC",
    page_icon="💪",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Índices de Capacidad del Proceso",
    "Cálculo de Cp, Cpk, Pp y Ppk",
    "💪"
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
        
        if len(mediciones_obj) < 30:
            mostrar_info(f"Se recomiendan al menos 30 mediciones. Actualmente hay {len(mediciones_obj)}")
        
        if len(mediciones_obj) < 2:
            mostrar_error("Se necesitan al menos 2 mediciones")
        else:
            valores_medidos = [float(m.valor) for m in mediciones_obj]
            
            # Usar los límites de la variable (si no existen, permitir entrada temporal)
            lcs = variable.lcs
            lci = variable.lci

            if lcs is None or lci is None:
                st.warning("La variable no tiene LCS/LCI definidos. Introduce límites temporales para calcular índices:")
                c1, c2 = st.columns(2)
                with c1:
                    lcs_input = st.text_input("LCS (Límite de Especificación Superior)", value=str(lcs) if lcs is not None else "")
                with c2:
                    lci_input = st.text_input("LCI (Límite de Especificación Inferior)", value=str(lci) if lci is not None else "")

                # Parsear entradas
                try:
                    lcs_val = float(lcs_input) if lcs_input and lcs_input.strip() != "" else None
                except Exception:
                    lcs_val = None
                try:
                    lci_val = float(lci_input) if lci_input and lci_input.strip() != "" else None
                except Exception:
                    lci_val = None

                if lcs_val is None or lci_val is None:
                    mostrar_error("Debes introducir valores numéricos para LCS y LCI para continuar.")
                    indices = {"error": "LCS/LCI no proporcionados"}
                else:
                    lcs = lcs_val
                    lci = lci_val
                    indices = calcular_indices_capacidad(valores_medidos, lcs, lci, variable.valor_nominal)
            else:
                # Calcular índices
                indices = calcular_indices_capacidad(valores_medidos, lcs, lci, variable.valor_nominal)
            
            if "error" not in indices:
                # Tabs
                tab1, tab2, tab3 = st.tabs(["📊 Índices", "📈 Gráficos", "📋 Interpretación"])
                
                with tab1:
                    st.subheader("Índices de Capacidad")
                    
                    col_indices1, col_indices2 = st.columns(2)
                    
                    with col_indices1:
                        st.markdown("### Corto Plazo (Cp, Cpk)")
                        cp_cpk_df = pd.DataFrame({
                            "Índice": ["Cp", "Cpk"],
                            "Valor": [indices["cp"], indices["cpk"]],
                            "Interpretación": [
                                "Potencial del proceso",
                                "Capacidad real del proceso"
                            ]
                        })
                        st.dataframe(cp_cpk_df, hide_index=True, use_container_width=True)
                    
                    with col_indices2:
                        st.markdown("### Largo Plazo (Pp, Ppk)")
                        pp_ppk_df = pd.DataFrame({
                            "Índice": ["Pp", "Ppk"],
                            "Valor": [indices["pp"], indices["ppk"]],
                            "Interpretación": [
                                "Desempeño del proceso",
                                "Desempeño real del proceso"
                            ]
                        })
                        st.dataframe(pp_ppk_df, hide_index=True, use_container_width=True)
                    
                    st.markdown("---")
                    
                    col_stats1, col_stats2 = st.columns(2)
                    
                    with col_stats1:
                        st.markdown("### Parámetros del Proceso")
                        params_df = pd.DataFrame({
                            "Parámetro": ["Media", "Desviación Estándar", "LCS", "LCI"],
                            "Valor": [
                                f"{indices['media']:.4f}",
                                f"{indices['sigma']:.4f}",
                                (f"{lcs:.4f}" if lcs is not None else "No definido"),
                                (f"{lci:.4f}" if lci is not None else "No definido")
                            ]
                        })
                        st.dataframe(params_df, hide_index=True, use_container_width=True)
                    
                    with col_stats2:
                        st.markdown("### Clasificación")
                        
                        if indices['semaforo'] == 'verde':
                            col_color = st.columns(1)[0]
                            col_color.success(f"✅ **Proceso CAPAZ** (Cpk = {indices['cpk']:.4f})")
                        elif indices['semaforo'] == 'amarillo':
                            col_color = st.columns(1)[0]
                            col_color.warning(f"⚠️ **Proceso CONDICIONALMENTE CAPAZ** (Cpk = {indices['cpk']:.4f})")
                        else:
                            col_color = st.columns(1)[0]
                            col_color.error(f"❌ **Proceso NO CAPAZ** (Cpk = {indices['cpk']:.4f})")
                        
                        st.markdown(f"""
                        **Estado Actual:** {indices['estado']}
                        
                        **Recomendación:** {
                            'Continuar monitoreo normal' if indices['cpk'] >= 1.33 
                            else 'Mejorar el proceso' if indices['cpk'] >= 1.0 
                            else 'Acción correctiva urgente'
                        }
                        """)
                
                with tab2:
                    st.subheader("Visualización")
                    
                    # Gráfico de índices
                    fig_indices = GraficosAnalisis.grafico_capacidad_proceso(indices)
                    st.plotly_chart(fig_indices, use_container_width=True)
                
                with tab3:
                    st.subheader("Interpretación de Índices")
                    
                    st.markdown("""
                    ### Escalas de Desempeño
                    
                    | Índice | Cpk < 1.0 | 1.0 ≤ Cpk < 1.33 | Cpk ≥ 1.33 |
                    |--------|-----------|-----------------|-----------|
                    | **Estado** | No Capaz | Condicionalmente Capaz | Capaz |
                    | **Interpretación** | Proceso inaceptable, requiere acción inmediata | Aceptable pero requiere mejora | Aceptable, continuar monitoreo |
                    | **% Defectos** | > 0.27% | 0.027% - 0.27% | < 0.027% |
                    | **Sigma Level** | < 3.0σ | 3.0σ - 4.0σ | > 4.0σ |
                    
                    ### Diferencia Cp vs Cpk
                    
                    - **Cp**: Índice potencial (si el proceso estuviera centrado)
                    - **Cpk**: Índice actual (considera descentrado)
                    - Si Cp > Cpk: El proceso no está centrado en el nominal
                    
                    ### Pp vs Pp
                    
                    - **Pp/Ppk**: Desempeño a largo plazo (variabilidad total)
                    - **Cp/Cpk**: Capacidad a corto plazo (variabilidad controlada)
                    """)
                    
                    st.markdown("---")
                    
                    st.markdown("### Análisis del Proceso")
                    
                    if indices['media'] < lci or indices['media'] > lcs:
                        st.error("⚠️ El proceso está operando fuera de especificaciones")
                    else:
                        distancia_lcs = lcs - indices['media']
                        distancia_lci = indices['media'] - lci
                        
                        if distancia_lcs < distancia_lci:
                            st.warning(f"⚠️ El proceso está descentrado hacia el LCS. Margen: {distancia_lcs:.4f}")
                        elif distancia_lci < distancia_lcs:
                            st.warning(f"⚠️ El proceso está descentrado hacia el LCI. Margen: {distancia_lci:.4f}")
                        else:
                            st.success("✅ El proceso está bien centrado")

            else:
                mostrar_error(indices["error"])

finally:
    cerrar_sesion(repos['session'])
