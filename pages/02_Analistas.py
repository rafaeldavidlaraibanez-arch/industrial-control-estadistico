import streamlit as st
import pandas as pd
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_exito, mostrar_error
)

# Configuración de la página
st.set_page_config(
    page_title="Analistas - CEC",
    page_icon="👤",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Gestión de Analistas",
    "Registrar y administrar analistas de calidad",
    "👤"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Tabs
    tab1, tab2 = st.tabs(["➕ Registrar Analista", "📋 Lista de Analistas"])
    
    with tab1:
        st.subheader("Registrar Nuevo Analista")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre *", placeholder="Ej: Juan")
            apellido = st.text_input("Apellido *", placeholder="Ej: Pérez")
        
        with col2:
            cargo = st.text_input("Cargo", placeholder="Ej: Técnico en Calidad")
            contacto = st.text_input("Contacto", placeholder="Ej: juan.perez@empresa.com")
        
        if st.button("✅ Guardar Analista", use_container_width=True):
            if not nombre or not apellido:
                mostrar_error("El nombre y apellido son obligatorios")
            else:
                try:
                    nuevo_analista = repos['analista'].crear(
                        nombre=nombre,
                        apellido=apellido,
                        cargo=cargo or None,
                        contacto=contacto or None
                    )
                    mostrar_exito(f"Analista '{nombre} {apellido}' registrado exitosamente")
                    st.rerun()
                except Exception as e:
                    mostrar_error(f"Error al registrar el analista: {str(e)}")
    
    with tab2:
        st.subheader("Lista de Analistas Registrados")
        
        analistas = repos['analista'].obtener_todos()
        
        if analistas:
            analistas_data = []
            from models.muestra import Muestra
            
            for a in analistas:
                num_muestras = repos['muestra'].session.query(Muestra).filter(
                    Muestra.id_analista == a.id_analista
                ).count()
                
                analistas_data.append({
                    "ID": a.id_analista,
                    "Nombre": a.nombre_completo,
                    "Cargo": a.cargo or "-",
                    "Contacto": a.contacto or "-",
                    "Muestras": num_muestras,
                    "Registro": a.fecha_creacion.strftime("%d/%m/%Y")
                })
            
            df = pd.DataFrame(analistas_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Opción para eliminar
            st.subheader("Eliminar Analista")
            analista_eliminar = st.selectbox(
                "Selecciona un analista para eliminar:",
                [a.nombre_completo for a in analistas]
            )
            
            if st.button("🗑️ Eliminar", use_container_width=True, type="secondary"):
                analista = next(a for a in analistas if a.nombre_completo == analista_eliminar)
                num_muestras = repos['muestra'].session.query(Muestra).filter(
                    Muestra.id_analista == analista.id_analista
                ).count()
                if num_muestras > 0:
                    mostrar_error("No se puede eliminar: el analista tiene muestras asociadas.")
                elif repos['analista'].eliminar(analista.id_analista):
                    mostrar_exito(f"Analista '{analista_eliminar}' eliminado")
                    st.rerun()
                else:
                    mostrar_error("No se pudo eliminar el analista")
        
        else:
            st.info("No hay analistas registrados. Crea uno en la pestaña anterior.")

finally:
    cerrar_sesion(repos['session'])
