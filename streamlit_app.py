import streamlit as st
from database.engine import init_db
import os
import pandas as pd

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="CEC Agroindustrial v2",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏭"
)

# =========================================================
# ESTILOS ADAPTATIVOS STREAMLIT
# =========================================================
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
}

/* HERO */
.hero-box {
    padding: 28px;
    border-radius: 16px;
    background-color: var(--secondary-background-color);
    border: 1px solid rgba(128,128,128,0.15);
    margin-bottom: 25px;
}

/* KPI */
.kpi-card {
    background-color: var(--secondary-background-color);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.15);
    text-align: center;
    transition: 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border: 1px solid #2563eb;
}

/* MODULOS */
.module-card {
    background-color: var(--secondary-background-color);
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 12px;
    border: 1px solid rgba(128,128,128,0.15);
    transition: 0.2s ease;
}

.module-card:hover {
    border: 1px solid #2563eb;
    transform: translateY(-2px);
}

/* SECCIONES */
.section-card {
    background-color: var(--secondary-background-color);
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.15);
    height: 100%;
}

/* FOOTER */
.footer-box {
    text-align: center;
    padding-top: 25px;
    opacity: 0.9;
}

/* TEXOS KPI */
.kpi-number {
    font-size: 32px;
    font-weight: 700;
    color: var(--text-color);
}

.kpi-label {
    font-size: 15px;
    color: var(--text-color);
    opacity: 0.8;
}

/* ICON BOX */
.icon-box {
    text-align: center;
    padding: 10px;
}

.icon-img {
    width: 120px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# BASE DE DATOS
# =========================================================
if not os.path.exists("cec_agro.db"):
    init_db()
    st.success("Base de datos inicializada correctamente")

# =========================================================
# HEADER PRINCIPAL
# =========================================================
st.markdown("""
<div class="hero-box">

<h1 style="margin-bottom:0;">
🏭 Control Estadístico de Calidad Agroindustrial
</h1>

<p style="font-size:18px; opacity:0.85;">
Sistema inteligente para monitoreo, análisis y optimización
de procesos agroindustriales mediante herramientas estadísticas.
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# KPIs
# =========================================================
st.subheader("Indicadores Generales")

k1, k2, k3, k4 = st.columns(4)

cards = [
    ("12", "Módulos"),
    ("2.0.0", "Versión"),
    ("Activo", "Estado"),
    ("SPC", "Metodología")
]

for col, card in zip([k1, k2, k3, k4], cards):

    numero, texto = card

    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{numero}</div>
            <div class="kpi-label">{texto}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# =========================================================
# DESCRIPCIÓN + ILUSTRACIÓN
# =========================================================
left, right = st.columns([2,1])

with left:

    st.subheader("Plataforma de Ingeniería Industrial")

    st.markdown("""
El sistema CEC Agroindustrial permite ejecutar procesos de:

- Control Estadístico de Procesos (SPC)
- Gestión de calidad
- Optimización industrial
- Mejora continua
- Monitoreo de producción
- Análisis estadístico avanzado

Aplicado a:

- Frutas
- Hortalizas
- Plantas medicinales
- Procesos agroindustriales
""")

    st.info("""
Herramientas integradas:
Gráficos X̄-R, X̄-S, P, NP, C y U,
Pareto, capacidad del proceso,
normalidad y análisis estadístico.
""")

with right:

    st.markdown("""
    <div class="section-card icon-box">

    <img class="icon-img"
    src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png">

    <h3>
    Ingeniería Industrial
    </h3>

    <p style="opacity:0.8;">
    Calidad · Productividad · SPC · Six Sigma
    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FLUJO OPERATIVO
# =========================================================
st.divider()

st.subheader("Flujo Operativo")

f1, f2, f3, f4, f5, f6 = st.columns(6)

steps = [
    ("📦", "Productos"),
    ("⚙️", "Variables"),
    ("📝", "Captura"),
    ("📊", "Análisis"),
    ("🎯", "Evaluación"),
    ("📁", "Reportes")
]

for col, step in zip([f1, f2, f3, f4, f5, f6], steps):

    icono, texto = step

    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size:34px;">{icono}</div>
            <div class="kpi-label">{texto}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# HERRAMIENTAS
# =========================================================
st.divider()

st.subheader("Herramientas Estadísticas")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="section-card">

    ### ⚙️ Control Estadístico

    - X̄-R
    - X̄-S
    - P
    - NP
    - C
    - U

    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="section-card">

    ### 📈 Calidad

    - Pareto
    - Cp y Cpk
    - Pp y Ppk
    - Normalidad

    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="section-card">

    ### 🏭 Ingeniería Industrial

    - SPC
    - Six Sigma
    - Productividad
    - Mejora continua

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MINI DASHBOARD
# =========================================================
st.divider()

st.subheader("Estado General del Sistema")

datos = pd.DataFrame({
    "Módulo": [
        "Productos",
        "Variables",
        "Captura",
        "Capacidad",
        "Pareto"
    ],
    "Estado": [95, 88, 92, 85, 90]
})

st.bar_chart(datos.set_index("Módulo"))

# =========================================================
# MÓDULOS
# =========================================================
st.divider()

st.subheader("Módulos Disponibles")

modulos = {
    "📊 Dashboard": "Indicadores generales y métricas",
    "📦 Productos": "Gestión de productos agroindustriales",
    "👨‍🔬 Analistas": "Administración del personal",
    "⚙️ Variables": "Configuración de variables continuas",
    "🧩 Atributos": "Control de defectos",
    "📝 Captura": "Registro de muestras",
    "📈 Variables SPC": "Gráficos X̄-R y X̄-S",
    "📉 Atributos SPC": "Gráficos P, NP, C y U",
    "🧪 Normalidad": "Pruebas estadísticas",
    "🎯 Capacidad": "Índices Cp y Cpk",
    "📋 Pareto": "Priorización de defectos",
    "💾 Exportación": "Reportes Excel"
}

cols = st.columns(2)

for idx, (titulo, descripcion) in enumerate(modulos.items()):

    with cols[idx % 2]:

        st.markdown(f"""
        <div class="module-card">

        <strong>{titulo}</strong><br>
        {descripcion}

        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TECNOLOGÍAS
# =========================================================
st.divider()

st.subheader("Arquitectura Tecnológica")

t1, t2, t3 = st.columns(3)

with t1:
    st.code("""
Python
Streamlit
SQLAlchemy
SQLite
""")

with t2:
    st.code("""
Pandas
NumPy
SciPy
Plotly
""")

with t3:
    st.code("""
SPC
Six Sigma
Shewhart
Pareto
""")

# =========================================================
# FINAL
# =========================================================
st.success(
    "Sistema listo para operar. Utilice el menú lateral para acceder a los módulos."
)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer-box">

<h3>
🏭 Ingeniería Industrial Aplicada al Control Estadístico
</h3>

<p>
Sistema orientado al análisis, monitoreo y optimización
de procesos agroindustriales.
</p>

<br>

<strong>Desarrollado por</strong><br>
Ing. Yoimar Rudas<br>
Ing. Rafael Lara<br>
Ing. José Gutierrez
            

<br><br>

Universidad del Magdalena · 2026

</div>
""", unsafe_allow_html=True)