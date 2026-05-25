import streamlit as st
from database.engine import SessionLocal
from repository.producto_repository import ProductoRepository
from repository.analista_repository import AnalistaRepository
from repository.variable_repository import VariableRepository, AtributoRepository
from repository.muestra_repository import MuestraRepository, MedicionVariableRepository, MedicionAtributoRepository

def obtener_sesion():
    """Obtiene una sesión de base de datos"""
    return SessionLocal()

def obtener_repositorios():
    """Obtiene todos los repositorios inicializados"""
    session = obtener_sesion()
    return {
        'producto': ProductoRepository(session),
        'analista': AnalistaRepository(session),
        'variable': VariableRepository(session),
        'atributo': AtributoRepository(session),
        'muestra': MuestraRepository(session),
        'medicion_variable': MedicionVariableRepository(session),
        'medicion_atributo': MedicionAtributoRepository(session),
        'session': session
    }

def cerrar_sesion(session):
    """Cierra una sesión de base de datos"""
    session.close()

def _set_feedback(mensaje: str, tipo: str = "success"):
    """Almacena el mensaje en el estado de sesión para mostrarlo después del rerun."""
    st.session_state['_feedback_mensaje'] = mensaje
    st.session_state['_feedback_tipo'] = tipo


def _mostrar_feedback():
    """Muestra el mensaje almacenado en el estado de sesión, si existe."""
    mensaje = st.session_state.get('_feedback_mensaje')
    tipo = st.session_state.get('_feedback_tipo')
    if mensaje:
        if tipo == 'success':
            st.success(f"✅ {mensaje}")
        elif tipo == 'error':
            st.error(f"❌ {mensaje}")
        elif tipo == 'warning':
            st.warning(f"⚠️ {mensaje}")
        else:
            st.info(f"ℹ️ {mensaje}")
        st.session_state['_feedback_mensaje'] = ''
        st.session_state['_feedback_tipo'] = ''


def mostrar_exito(mensaje: str, persist: bool = True):
    """Muestra un mensaje de éxito."""
    if persist:
        _set_feedback(mensaje, 'success')
        _mostrar_feedback()
    else:
        st.success(f"✅ {mensaje}")


def mostrar_error(mensaje: str, persist: bool = True):
    """Muestra un mensaje de error."""
    if persist:
        _set_feedback(mensaje, 'error')
        _mostrar_feedback()
    else:
        st.error(f"❌ {mensaje}")


def mostrar_info(mensaje: str, persist: bool = False):
    """Muestra un mensaje de información."""
    if persist:
        _set_feedback(mensaje, 'info')
        _mostrar_feedback()
    else:
        st.info(f"ℹ️ {mensaje}")


def mostrar_advertencia(mensaje: str, persist: bool = False):
    """Muestra un mensaje de advertencia."""
    if persist:
        _set_feedback(mensaje, 'warning')
        _mostrar_feedback()
    else:
        st.warning(f"⚠️ {mensaje}")

def cargar_css_personalizado():
    """Carga CSS personalizado para las páginas"""
    st.markdown("""
    <style>
    .card-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #3498db;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .section-title {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def crear_sidebar_navegacion():
    """Crea barra lateral con navegación"""
    st.sidebar.title("🗂️ Navegación Rápida")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("**Configuración Inicial**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🌽 Productos"):
            st.switch_page("pages/01_Productos.py")
    with col2:
        if st.button("👤 Analistas"):
            st.switch_page("pages/02_Analistas.py")
    
    st.sidebar.markdown("**Configuración de Variables**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("📊 Variables"):
            st.switch_page("pages/03_Variables.py")
    with col2:
        if st.button("📌 Atributos"):
            st.switch_page("pages/04_Atributos.py")
    
    st.sidebar.markdown("**Captura y Análisis**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("📝 Captura"):
            st.switch_page("pages/05_Captura.py")
    with col2:
        if st.button("📊 Dashboard"):
            st.switch_page("pages/00_Dashboard.py")
    
    st.sidebar.markdown("**Análisis Estadístico**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("📈 Variables"):
            st.switch_page("pages/06_Analisis_Variables.py")
    with col2:
        if st.button("🎯 Atributos"):
            st.switch_page("pages/07_Analisis_Atributos.py")
    
    st.sidebar.markdown("**Herramientas**")
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        if st.button("✅ Normalidad"):
            st.switch_page("pages/08_Normalidad.py")
    with col2:
        if st.button("💪 Capacidad"):
            st.switch_page("pages/09_Capacidad.py")
    with col3:
        if st.button("🎨 Pareto"):
            st.switch_page("pages/10_Pareto.py")
    
    st.sidebar.markdown("**Reportes**")
    if st.button("💾 Exportar"):
        st.switch_page("pages/11_Exportar.py")
    
    st.sidebar.markdown("---")
    st.sidebar.info("Sistema de Control Estadístico de Calidad v2.0")

def crear_encabezado_pagina(titulo: str, descripcion: str = None, icono: str = "📊"):
    """Crea encabezado consistente para páginas"""
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.markdown(f"# {icono}")
    with col2:
        st.title(titulo)
    
    if descripcion:
        st.markdown(f"_{descripcion}_")
    
    st.markdown("---")
    _mostrar_feedback()

def seleccionar_producto(repos, key_suffix=""):
    """Widget para seleccionar un producto"""
    productos = repos['producto'].obtener_todos()
    
    if not productos:
        st.error("⚠️ No hay productos registrados. Crea uno primero.")
        return None
    
    nombres = [p.nombre for p in productos]
    seleccionado = st.selectbox("Selecciona un producto:", nombres, key=f"producto_{key_suffix}" if key_suffix else None)
    
    producto = next(p for p in productos if p.nombre == seleccionado)
    return producto

def seleccionar_analista(repos, key_suffix=""):
    """Widget para seleccionar un analista"""
    analistas = repos['analista'].obtener_todos()
    
    if not analistas:
        st.error("⚠️ No hay analistas registrados. Crea uno primero.")
        return None
    
    nombres = [f"{a.nombre_completo}" for a in analistas]
    seleccionado = st.selectbox("Selecciona un analista:", nombres, key=f"analista_{key_suffix}" if key_suffix else None)
    
    analista = next(a for a in analistas if f"{a.nombre_completo}" == seleccionado)
    return analista

def seleccionar_variable(repos, id_producto: int, key_suffix=""):
    """Widget para seleccionar una variable"""
    variables = repos['variable'].obtener_por_producto(id_producto)
    
    if not variables:
        st.error("⚠️ No hay variables registradas para este producto.")
        return None
    
    nombres = [v.nombre_variable for v in variables]
    seleccionado = st.selectbox("Selecciona una variable:", nombres, key=f"variable_{key_suffix}" if key_suffix else None)
    
    variable = next(v for v in variables if v.nombre_variable == seleccionado)
    return variable

def seleccionar_atributo(repos, id_producto: int, key_suffix=""):
    """Widget para seleccionar un atributo"""
    atributos = repos['atributo'].obtener_por_producto(id_producto)
    
    if not atributos:
        st.error("⚠️ No hay atributos registrados para este producto.")
        return None
    
    nombres = [a.nombre_atributo for a in atributos]
    seleccionado = st.selectbox("Selecciona un atributo:", nombres, key=f"atributo_{key_suffix}" if key_suffix else None)
    
    atributo = next(a for a in atributos if a.nombre_atributo == seleccionado)
    return atributo

def crear_tabla_datos(datos, columnas_ocultas=None):
    """Crea tabla formateada de datos"""
    if columnas_ocultas is None:
        columnas_ocultas = []
    
    columnas_visibles = [col for col in datos.columns if col not in columnas_ocultas]
    # Intentar normalizar tipos para evitar errores de serialización a Arrow
    df_display = datos[columnas_visibles].copy()
    try:
        for col in df_display.columns:
            # intentar convertir a numérico; si todos los valores son numéricos, usamos el resultado
            coerced = pd.to_numeric(df_display[col], errors='coerce')
            if not coerced.isna().any():
                df_display[col] = coerced
            else:
                # si la conversión falla parcialmente, forzar todo a string para mantener un dtype homogéneo
                df_display[col] = df_display[col].astype(str)

        st.dataframe(df_display, use_container_width=True)
    except Exception:
        # En caso inesperado, mostramos la tabla sin conversión y evitamos que la app falle
        try:
            st.dataframe(datos[columnas_visibles], use_container_width=True)
        except Exception as e:
            st.write("No se pudo renderizar la tabla:", str(e))
