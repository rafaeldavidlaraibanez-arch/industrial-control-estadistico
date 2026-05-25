import streamlit as st
import pandas as pd
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_exito, mostrar_error, mostrar_info,
    seleccionar_producto
)

# Configuración de la página
st.set_page_config(
    page_title="Variables - CEC",
    page_icon="📊",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Configuración de Variables",
    "Crear y administrar variables continuas de medición",
    "📊"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Tabs
    tab1, tab2 = st.tabs(["➕ Crear Variable", "📋 Lista de Variables"])
    
    with tab1:
        st.subheader("Crear Nueva Variable Continua")
        
        # Seleccionar producto
        producto = seleccionar_producto(repos, key_suffix="crear")
        
        if producto:
            col1, col2 = st.columns(2)
            
            with col1:
                nombre_variable = st.text_input("Nombre de la variable *", placeholder="Ej: Peso, Diámetro, Humedad")
                tipo_dato = st.selectbox("Tipo de dato", ["continua", "discreta"], format_func=lambda x: "Continua" if x == "continua" else "Discreta")
                tam_subgrupo = st.number_input("Tamaño de subgrupo", min_value=2, max_value=50, value=5)
                unidad_medida = st.text_input("Unidad de medida", placeholder="Ej: kg, cm, %")
            
            with col2:
                valor_nominal = st.number_input("Valor nominal (opcional)", value=0.0, step=0.1)
                lcs = st.number_input("Límite de Control Superior (LCS) *", value=100.0, step=0.1)
                lci = st.number_input("Límite de Control Inferior (LCI) *", value=0.0, step=0.1)
                descripcion = st.text_area("Descripción", placeholder="Características de la variable")
            
            if st.button("✅ Guardar Variable", use_container_width=True):
                if not nombre_variable or lcs is None or lci is None:
                    mostrar_error("El nombre y los límites de control son obligatorios")
                elif lcs <= lci:
                    mostrar_error("El LCS debe ser mayor que el LCI")
                else:
                    try:
                        nueva_variable = repos['variable'].crear(
                            id_producto=producto.id_producto,
                            nombre_variable=nombre_variable,
                            tipo_dato=tipo_dato,
                            lcs=lcs,
                            lci=lci,
                            valor_nominal=valor_nominal if valor_nominal != 0.0 else None,
                            tam_subgrupo=tam_subgrupo,
                            unidad_medida=unidad_medida or None,
                            descripcion=descripcion or None
                        )
                        mostrar_exito(f"Variable '{nombre_variable}' creada exitosamente")
                        st.rerun()
                    except Exception as e:
                        mostrar_error(f"Error al crear la variable: {str(e)}")
    
    with tab2:
        st.subheader("Lista de Variables")
        
        producto = seleccionar_producto(repos, key_suffix="listar")
        
        if producto:
            variables = repos['variable'].obtener_por_producto(producto.id_producto)
            
            if variables:
                variables_data = []
                for v in variables:
                    num_mediciones = repos['medicion_variable'].contar_por_variable(v.id_variable)
                    
                    variables_data.append({
                        "ID": v.id_variable,
                        "Nombre": v.nombre_variable,
                        "Tipo": "Continua" if v.tipo_dato == "continua" else "Discreta",
                        "Unidad": v.unidad_medida or "-",
                        "LCS": v.lcs,
                        "LCI": v.lci,
                        "Nominal": v.valor_nominal or "-",
                        "Subgrupo": v.tam_subgrupo,
                        "Mediciones": num_mediciones
                    })
                
                df = pd.DataFrame(variables_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                
                # Opción para editar
                st.subheader("Editar Variable")
                variable_seleccionada = st.selectbox(
                    "Selecciona una variable:",
                    [v.nombre_variable for v in variables],
                    key="variable_editar"
                )
                
                variable = next(v for v in variables if v.nombre_variable == variable_seleccionada)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    lcs_nuevo = st.number_input("Nuevo LCS", value=float(variable.lcs), step=0.1, key="lcs_editar")
                    lci_nuevo = st.number_input("Nuevo LCI", value=float(variable.lci), step=0.1, key="lci_editar")
                
                with col2:
                    valor_nominal_nuevo = st.number_input("Nuevo Valor Nominal", value=float(variable.valor_nominal) if variable.valor_nominal else 0.0, step=0.1, key="nominal_editar")
                    tam_subgrupo_nuevo = st.number_input("Nuevo Tamaño de Subgrupo", value=variable.tam_subgrupo, min_value=2, max_value=50, key="subgrupo_editar")
                
                if st.button("💾 Actualizar Variable", use_container_width=True):
                    try:
                        repos['variable'].actualizar(
                            variable.id_variable,
                            lcs=lcs_nuevo,
                            lci=lci_nuevo,
                            valor_nominal=valor_nominal_nuevo if valor_nominal_nuevo != 0.0 else None,
                            tam_subgrupo=tam_subgrupo_nuevo
                        )
                        mostrar_exito("Variable actualizada exitosamente")
                        st.rerun()
                    except Exception as e:
                        mostrar_error(f"Error al actualizar: {str(e)}")
                
                st.markdown("---")
                
                # Eliminar
                if st.button("🗑️ Eliminar Variable", use_container_width=True, type="secondary"):
                    if repos['variable'].eliminar(variable.id_variable):
                        mostrar_exito("Variable eliminada")
                        st.rerun()
                    else:
                        mostrar_error("No se pudo eliminar la variable")
            
            else:
                mostrar_info(f"No hay variables para '{producto.nombre}'. Crea una en la pestaña anterior.")

finally:
    cerrar_sesion(repos['session'])
