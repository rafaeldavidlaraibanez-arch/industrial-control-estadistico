import streamlit as st
import pandas as pd
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado
)

# Configuración de la página
st.set_page_config(
    page_title="Dashboard - CEC",
    page_icon="📊",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Dashboard General",
    "Resumen estadístico completo del sistema",
    "📊"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Métricas principales
    col1, col2, col3, col4, col5 = st.columns(5)
    
    from models.muestra import Muestra
    from models.variables import VariableConfig, AtributoConfig
    
    num_productos = repos['producto'].contar()
    num_muestras = repos['muestra'].session.query(Muestra).count()
    num_analistas = repos['analista'].contar()
    num_variables = repos['variable'].session.query(VariableConfig).count()
    num_atributos = repos['variable'].session.query(AtributoConfig).count()
    
    with col1:
        st.metric(label="🌽 Productos", value=num_productos)
    
    with col2:
        st.metric(label="📝 Muestras", value=num_muestras)
    
    with col3:
        st.metric(label="👤 Analistas", value=num_analistas)
    
    with col4:
        st.metric(label="📊 Variables", value=num_variables)
    
    with col5:
        st.metric(label="📌 Atributos", value=num_atributos)
    
    st.markdown("---")
    
    # Secciones del dashboard
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Resumen", "🌽 Productos", "📊 Actividad", "⚙️ Sistema"])
    
    with tab1:
        st.subheader("Información General")
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### Estadísticas del Sistema")
            stats_df = pd.DataFrame({
                "Elemento": ["Productos", "Muestras", "Analistas", "Variables", "Atributos"],
                "Cantidad": [num_productos, num_muestras, num_analistas, num_variables, num_atributos]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with col_right:
            st.markdown("### Estado del Sistema")
            st.info("✅ **Sistema Operativo**")
            st.markdown("""
            - Base de datos: **Conectada**
            - Módulos: **Todos activos**
            - Última actualización: **Hoy**
            """)
    
    with tab2:
        st.subheader("Productos Registrados")
        productos = repos['producto'].obtener_todos()
        
        if productos:
            productos_data = []
            for p in productos:
                num_vars = repos['variable'].contar_por_producto(p.id_producto)
                num_atrs = repos['atributo'].contar_por_producto(p.id_producto)
                num_muestras_prod = repos['muestra'].contar_por_producto(p.id_producto)
                
                productos_data.append({
                    "Producto": p.nombre,
                    "Tipo": p.tipo,
                    "Variedad": p.variedad or "-",
                    "Unidad": p.unidad_medida or "-",
                    "Variables": num_vars,
                    "Atributos": num_atrs,
                    "Muestras": num_muestras_prod
                })
            
            df_productos = pd.DataFrame(productos_data)
            st.dataframe(df_productos, use_container_width=True, hide_index=True)
        else:
            st.warning("No hay productos registrados")
    
    with tab3:
        st.subheader("Actividad Reciente")
        
        col_left, col_right = st.columns([1.5, 1])
        
        with col_left:
            st.markdown("#### Últimas Muestras")
            muestras = repos['muestra'].obtener_ultimas(limit=10)
            
            if muestras:
                muestras_data = []
                for m in muestras:
                    muestras_data.append({
                        "Producto": m.producto.nombre,
                        "Analista": m.analista.nombre_completo,
                        "Subgrupo": m.num_subgrupo,
                        "Fecha": m.fecha_hora.strftime("%d/%m/%Y %H:%M"),
                        "Lote": m.lote or "-"
                    })
                
                df_muestras = pd.DataFrame(muestras_data)
                st.dataframe(df_muestras, use_container_width=True, hide_index=True)
            else:
                st.info("No hay muestras registradas")
        
        with col_right:
            st.markdown("#### Analistas")
            analistas = repos['analista'].obtener_todos()
            
            if analistas:
                from models.muestra import Muestra
                analistas_data = []
                for a in analistas:
                    num_muestras_analista = repos['muestra'].session.query(Muestra).filter(
                        Muestra.id_analista == a.id_analista
                    ).count()
                    
                    analistas_data.append({
                        "Analista": a.nombre_completo,
                        "Cargo": a.cargo or "-",
                        "Muestras": num_muestras_analista
                    })
                
                df_analistas = pd.DataFrame(analistas_data)
                st.dataframe(df_analistas, use_container_width=True, hide_index=True)
            else:
                st.info("No hay analistas registrados")
    
    with tab4:
        st.subheader("Información del Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Versión")
            st.markdown("**v2.0.0** - Sistema de Control Estadístico de Calidad Agroindustrial")
            
            st.markdown("### Base de Datos")
            st.markdown("- **Motor**: SQLite")
            st.markdown("- **Archivo**: `cec_agro.db`")
            st.markdown("- **ORM**: SQLAlchemy")
        
        with col2:
            st.markdown("### Características")
            st.markdown("""
            - ✅ Gráficos de control (X̄-R, X̄-S, P, NP, C, U)
            - ✅ Pruebas de normalidad
            - ✅ Índices de capacidad
            - ✅ Diagrama de Pareto
            - ✅ Exportación de reportes
            """)

finally:
    cerrar_sesion(repos['session'])
