import streamlit as st
import pandas as pd
from config import TIPOS_PRODUCTO
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_exito, mostrar_error, mostrar_info
)

# Configuración de la página
st.set_page_config(
    page_title="Productos - CEC",
    page_icon="🌽",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Gestión de Productos",
    "Crear y administrar productos agroindustriales",
    "🌽"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Tabs
    tab1, tab2 = st.tabs(["➕ Crear Producto", "📋 Lista de Productos"])
    
    with tab1:
        st.subheader("Crear Nuevo Producto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre del producto *", placeholder="Ej: Tomate Roma")
            tipo = st.selectbox("Tipo *", TIPOS_PRODUCTO, format_func=lambda x: x.capitalize())
            variedad = st.text_input("Variedad", placeholder="Ej: Roma, Cherry, etc.")
        
        with col2:
            unidad_medida = st.text_input("Unidad de medida *", placeholder="Ej: kg, gramos, unidades")
            descripcion = st.text_area("Descripción", placeholder="Características o notas del producto")
        
        if st.button("✅ Guardar Producto", use_container_width=True):
            if not nombre or not unidad_medida:
                mostrar_error("El nombre y la unidad de medida son obligatorios")
            else:
                # Verificar que no exista otro con el mismo nombre
                existente = repos['producto'].obtener_por_nombre(nombre)
                if existente:
                    mostrar_error(f"Ya existe un producto llamado '{nombre}'")
                else:
                    try:
                        nuevo_producto = repos['producto'].crear(
                            nombre=nombre,
                            tipo=tipo,
                            variedad=variedad,
                            unidad_medida=unidad_medida,
                            descripcion=descripcion
                        )
                        mostrar_exito(f"Producto '{nombre}' creado exitosamente")
                        st.rerun()
                    except Exception as e:
                        mostrar_error(f"Error al crear el producto: {str(e)}")
    
    with tab2:
        st.subheader("Lista de Productos Registrados")
        
        productos = repos['producto'].obtener_todos()
        
        if productos:
            col_info, col_delete = st.columns([3, 1])
            
            with col_info:
                productos_data = []
                for p in productos:
                    num_vars = repos['variable'].contar_por_producto(p.id_producto)
                    num_atrs = repos['atributo'].contar_por_producto(p.id_producto)
                    num_muestras = repos['muestra'].contar_por_producto(p.id_producto)
                    
                    productos_data.append({
                        "ID": p.id_producto,
                        "Nombre": p.nombre,
                        "Tipo": p.tipo.capitalize(),
                        "Variedad": p.variedad or "-",
                        "Unidad": p.unidad_medida,
                        "Variables": num_vars,
                        "Atributos": num_atrs,
                        "Muestras": num_muestras,
                        "Descripción": p.descripcion or "-"
                    })
                
                df = pd.DataFrame(productos_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Opción para eliminar producto
            st.subheader("Eliminar Producto")
            producto_eliminar = st.selectbox(
                "Selecciona un producto para eliminar:",
                [p.nombre for p in productos]
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🗑️ Eliminar", use_container_width=True, type="secondary"):
                    producto = repos['producto'].obtener_por_nombre(producto_eliminar)
                    if repos['producto'].eliminar(producto.id_producto):
                        mostrar_exito(f"Producto '{producto_eliminar}' eliminado")
                        st.rerun()
                    else:
                        mostrar_error("No se pudo eliminar el producto")
        
        else:
            st.info("No hay productos registrados. Crea uno en la pestaña anterior.")

finally:
    cerrar_sesion(repos['session'])
