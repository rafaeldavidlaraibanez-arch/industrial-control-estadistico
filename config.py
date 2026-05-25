import os
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent
DATABASE_URL = "sqlite:///cec_agro.db"

# Streamlit config
STREAMLIT_CONFIG = {
    "page_title": "CEC Agroindustrial",
    "page_icon": "leaf",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configuracion de la aplicacion
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
APP_NAME = "Sistema de Control Estadistico de Calidad"
APP_VERSION = "2.0.0"

# Limites del sistema
MIN_SUBGRUPOS = 25
MAX_OBSERVACIONES_POR_SUBGRUPO = 50

# Tipos de productos
TIPOS_PRODUCTO = ["fruta", "hortaliza", "planta_medicinal"]

# Tipos de graficos para atributos
TIPOS_GRAFICO_ATRIBUTO = ["P", "NP", "C", "U"]
