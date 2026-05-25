import streamlit as st
import pandas as pd
from config import TIPOS_GRAFICO_ATRIBUTO
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_exito, mostrar_error, mostrar_info,
    seleccionar_producto
)

# Configuración de la página
st.set_page_config(
    page_title="Atributos - CEC",
    page_icon="📌",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Configuración de Atributos",
    "Definir características discretas (defectos y atributos)",
    "📌"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Tabs
    tab1, tab2 = st.tabs(["➕ Crear Atributo", "📋 Lista de Atributos"])
    
    with tab1:
        st.subheader("Crear Nuevo Atributo")
        
        # Seleccionar producto
        producto = seleccionar_producto(repos, key_suffix="crear_attr")
        
        if producto:
            col1, col2 = st.columns(2)
            
            with col1:
                nombre_atributo = st.text_input("Nombre del atributo *", placeholder="Ej: Defectos de forma, Manchas, etc.", key="nombre_attr_crear")
                tipo_grafico = st.selectbox("Tipo de gráfico *", TIPOS_GRAFICO_ATRIBUTO, format_func=lambda x: {
                    "P": "P (Proporción de defectuosos)",
                    "NP": "NP (Número de defectuosos)",
                    "C": "C (Número de defectos)",
                    "U": "U (Defectos por unidad)"
                }.get(x, x), key="tipo_grafico_crear")
            
            with col2:
                tam_subgrupo = st.number_input("Tamaño del subgrupo", min_value=5, max_value=1000, value=50, key="tam_subgrupo_crear")
                descripcion = st.text_area("Descripción", placeholder="Definición del defecto o característica", key="desc_attr_crear")
            
            if st.button("✅ Guardar Atributo", use_container_width=True):
                if not nombre_atributo:
                    mostrar_error("El nombre del atributo es obligatorio")
                else:
                    try:
                        nuevo_atributo = repos['atributo'].crear(
                            id_producto=producto.id_producto,
                            nombre_atributo=nombre_atributo,
                            tipo_grafico=tipo_grafico,
                            tam_subgrupo=tam_subgrupo,
                            descripcion=descripcion or None
                        )
                        mostrar_exito(f"Atributo '{nombre_atributo}' creado exitosamente")
                        st.rerun()
                    except Exception as e:
                        mostrar_error(f"Error al crear el atributo: {str(e)}")
    
    with tab2:
        st.subheader("Lista de Atributos")
        
        producto = seleccionar_producto(repos, key_suffix="listar_attr")
        
        if producto:
            atributos = repos['atributo'].obtener_por_producto(producto.id_producto)
            
            if atributos:
                atributos_data = []
                for a in atributos:
                    num_mediciones = repos['medicion_atributo'].contar_por_atributo(a.id_atributo)
                    
                    tipo_desc = {
                        "P": "Proporción",
                        "NP": "Número",
                        "C": "Defectos",
                        "U": "Por unidad"
                    }.get(a.tipo_grafico, a.tipo_grafico)
                    
                    atributos_data.append({
                        "ID": a.id_atributo,
                        "Nombre": a.nombre_atributo,
                        "Tipo Gráfico": a.tipo_grafico,
                        "Descripción": tipo_desc,
                        "Tamaño Subgrupo": a.tam_subgrupo,
                        "Mediciones": num_mediciones,
                        "Descripción Completa": a.descripcion or "-"
                    })
                
                # Mostrar tabla sin la columna de descripción completa
                df = pd.DataFrame(atributos_data)
                df_display = df.drop(columns=["Descripción Completa"])
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                
                # Opción para editar
                st.subheader("Editar Atributo")
                atributo_seleccionado = st.selectbox(
                    "Selecciona un atributo:",
                    [a.nombre_atributo for a in atributos],
                    key="atributo_editar"
                )
                
                atributo = next(a for a in atributos if a.nombre_atributo == atributo_seleccionado)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    tipo_grafico_nuevo = st.selectbox(
                        "Nuevo Tipo de Gráfico",
                        TIPOS_GRAFICO_ATRIBUTO,
                        index=TIPOS_GRAFICO_ATRIBUTO.index(atributo.tipo_grafico),
                        format_func=lambda x: {
                            "P": "P (Proporción)",
                            "NP": "NP (Número)",
                            "C": "C (Defectos)",
                            "U": "U (Por unidad)"
                        }.get(x, x),
                        key="tipo_grafico_editar"
                    )
                
                with col2:
                    tam_subgrupo_nuevo = st.number_input(
                        "Nuevo Tamaño de Subgrupo",
                        value=atributo.tam_subgrupo,
                        min_value=5,
                        max_value=1000,
                        key="tam_subgrupo_editar"
                    )
                
                if st.button("💾 Actualizar Atributo", use_container_width=True):
                    try:
                        repos['atributo'].actualizar(
                            atributo.id_atributo,
                            tipo_grafico=tipo_grafico_nuevo,
                            tam_subgrupo=tam_subgrupo_nuevo
                        )
                        mostrar_exito("Atributo actualizado exitosamente")
                        st.rerun()
                    except Exception as e:
                        mostrar_error(f"Error al actualizar: {str(e)}")
                
                st.markdown("---")
                
                # Eliminar
                if st.button("🗑️ Eliminar Atributo", use_container_width=True, type="secondary"):
                    if repos['atributo'].eliminar(atributo.id_atributo):
                        mostrar_exito("Atributo eliminado")
                        st.rerun()
                    else:
                        mostrar_error("No se pudo eliminar el atributo")
            
            else:
                mostrar_info(f"No hay atributos para '{producto.nombre}'. Crea uno en la pestaña anterior.")

finally:
    cerrar_sesion(repos['session'])
