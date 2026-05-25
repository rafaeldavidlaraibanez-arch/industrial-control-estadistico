# Sistema de Control Estadistico de Calidad - Version 2

Sistema desarrollado en Python con Streamlit y SQLAlchemy para monitorear la calidad de frutas, hortalizas y plantas medicinales mediante herramientas estadisticas.

## Caracteristicas

- Graficos de control por variables (X-barra R, X-barra S)
- Graficos de control por atributos (P, NP, C, U)
- Prueba de normalidad Shapiro-Wilk
- Indices de capacidad del proceso (Cp, Cpk, Pp, Ppk)
- Diagrama de Pareto
- Deteccion de datos atipicos
- Exportacion a Excel

## Estructura del Proyecto

```
cec-agroindustrial-v2/
├── config.py                 # Configuracion general
├── streamlit_app.py         # Aplicacion principal Streamlit
├── requirements.txt         # Dependencias
│
├── database/                # Conexion a la base de datos
│   ├── engine.py           # SQLAlchemy engine y sessionmaker
│   └── init_db.py          # Inicializacion de tablas
│
├── models/                  # Modelos SQLAlchemy
│   ├── base.py             # Base declarativa
│   ├── producto.py         # Modelo Producto
│   ├── analista.py         # Modelo Analista
│   ├── variables.py        # Modelos VariableConfig y AtributoConfig
│   └── muestra.py          # Modelos Muestra y Mediciones
│
├── schemas/                 # Validacion con Pydantic
├── repository/              # Capa de acceso a datos
├── services/                # Logica de negocio
├── calculators/             # Calculo de estadisticas
│   ├── constantes_spc.py   # Constantes estadisticas tabuladas
│   └── estadisticas.py     # Funciones de calculo
│
├── pages/                   # Paginas multipage de Streamlit
└── utils/                   # Funciones auxiliares
```

## Instalacion

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicacion:
```bash
streamlit run streamlit_app.py
```

3. Acceder en el navegador:
```
http://localhost:8501
```

## Uso

La aplicacion cuenta con las siguientes secciones:

1. **Configuracion**: Inicializar base de datos
2. **Productos**: Registrar productos a monitorear
3. **Analistas**: Registrar personal responsable del muestreo
4. **Muestras**: Ingreso de datos de campo
5. **Variables**: Analisis de graficos de control para variables continuas
6. **Atributos**: Analisis de graficos de control para atributos
7. **Capacidad**: Calculo de indices de capacidad
8. **Reportes**: Exportacion a Excel

## Requisitos

- Python 3.11+
- SQLite3
- Las dependencias listadas en requirements.txt

## Notas de Desarrollo

- Todos los calculos estadisticos se hacen en memoria, no se guardan en la BD
- La validacion se realiza con Pydantic en la capa de services
- SQLAlchemy ORM garantiza que las queries sean type-safe
- El codigo está comentado en español siguiendo el contexto académico
