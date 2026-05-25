import streamlit as st
import pandas as pd
import re
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_exito, mostrar_error, mostrar_info,
    seleccionar_producto, seleccionar_analista, seleccionar_variable,
    seleccionar_atributo
)
from models.producto import TipoProducto

# Configuración de la página
st.set_page_config(
    page_title="Captura de Datos - CEC",
    page_icon="📝",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Captura de Datos",
    "Registrar nuevas muestras y mediciones",
    "📝"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Tabs
    tab1, tab2 = st.tabs(["📊 Captura por Variables", "📌 Captura por Atributos"])
    
    with tab1:
        st.subheader("Captura de Mediciones (Variables Continuas)")
        
        def obtener_o_crear_producto(nombre, tipo, unidad_medida=None):
            nombre = (nombre or "").strip()
            if not nombre:
                return None
            producto = repos['producto'].obtener_por_nombre(nombre)
            if not producto:
                producto = repos['producto'].crear(
                    nombre=nombre,
                    tipo=tipo,
                    unidad_medida=unidad_medida or "",
                    variedad=None,
                    descripcion=None
                )
            return producto

        def obtener_o_crear_variable(id_producto, nombre_variable, unidad_medida=None, tam_subgrupo=5):
            nombre_variable = (nombre_variable or "").strip()
            if not nombre_variable:
                return None
            variables = repos['variable'].obtener_por_producto(id_producto)
            variable = next((v for v in variables if v.nombre_variable == nombre_variable), None)
            if not variable:
                variable = repos['variable'].crear(
                    id_producto=id_producto,
                    nombre_variable=nombre_variable,
                    tipo_dato="continua",
                    tam_subgrupo=tam_subgrupo,
                    unidad_medida=unidad_medida or "",
                    descripcion=None
                )
            return variable

        def parse_product_variable(header: str):
            """Parsea un encabezado de columna y retorna (producto, variable).
            Si el encabezado contiene un separador común, usa la primera parte como producto
            y el resto como nombre de la variable. Si no, devuelve (header, header).
            """
            if not header or not isinstance(header, str):
                return ("", "")
            parts = re.split(r"[-|:/\\;,]+", header)
            parts = [p.strip() for p in parts if p.strip()]
            if len(parts) >= 2:
                prod = parts[0]
                var = " - ".join(parts[1:])
            else:
                prod = header.strip()
                var = header.strip()
            return prod, var

        # Seleccionar producto y variable
        col_select1, col_select2 = st.columns(2)
        
        with col_select1:
            producto = seleccionar_producto(repos, key_suffix="var")
        
        with col_select2:
            if producto:
                variable = seleccionar_variable(repos, producto.id_producto, key_suffix="var")
        
        if producto and variable:
                # Datos de la muestra
                col1, col2, col3 = st.columns(3)

                with col1:
                    num_subgrupo = st.number_input("Número de subgrupo (inicio)", min_value=1, value=1)

                with col2:
                    analista = seleccionar_analista(repos, key_suffix="var")

                with col3:
                    lote = st.text_input("Lote (opcional)", placeholder="Ej: LOTE-2024-001")

                origen = st.text_input("Origen (opcional)", placeholder="Ej: Parcela A, Invernadero B")

                # Modo de captura: individual (subgrupo único) o masivo (varios subgrupos pegados)
                modo = st.radio("Modo de captura", ["Individual (un subgrupo)", "Masivo (varios subgrupos)"], index=0)

                if modo == "Masivo (varios subgrupos)":
                    st.markdown("### Captura masiva por subgrupos")
                    modo_archivo = st.radio(
                        "Tipo de importación de archivo",
                        ["Columna única", "Varias columnas / productos"],
                        horizontal=True
                    )
                    uploaded_file = st.file_uploader("Subir archivo CSV/XLSX (opcional)", type=['csv', 'xlsx'])
                    file_import = uploaded_file is not None
                    valores_texto = None
                    df_from_file = None
                    df_converted = None
                    selected_cols = []
                    import_multi_columns = modo_archivo == "Varias columnas / productos"
                    modo_columnas = "Mismo producto"
                    producto_excel_nombre = ""
                    producto_excel_tipo = TipoProducto.FRUTA.value
                    producto_excel_unidad = ""
                    excel_total_values = None
                    calculated_n_subgrupos = None

                    if not file_import:
                        n_subgrupos = st.number_input("Número de subgrupos a capturar", min_value=1, value=1)
                    else:
                        n_subgrupos = 1

                    info_text = ""
                    if file_import and not import_multi_columns:
                        info_text = f"Introduce datos por Excel y el sistema calculará automáticamente los subgrupos según el tamaño de subgrupo ({variable.tam_subgrupo})."
                    elif file_import and import_multi_columns:
                        info_text = "Introduce datos por Excel y el sistema generará muestras según cada fila del archivo."
                    else:
                        info_text = f"Introduce {n_subgrupos * variable.tam_subgrupo} valores (separados por comas, espacios o saltos de línea), o sube un archivo CSV/XLSX con la columna de valores.\nEj: pegar {n_subgrupos * variable.tam_subgrupo} valores para {n_subgrupos} subgrupos de {variable.tam_subgrupo}."
                    st.info(info_text)

                    if uploaded_file is not None:
                        try:
                            if uploaded_file.name.lower().endswith('.csv'):
                                df_from_file = pd.read_csv(uploaded_file)
                            else:
                                df_from_file = pd.read_excel(uploaded_file)

                            # Intentar convertir a numérico cualquier columna que sea convertible
                            df_converted = df_from_file.copy()
                            for c in df_converted.columns:
                                if not pd.api.types.is_numeric_dtype(df_converted[c]):
                                    coerced = pd.to_numeric(
                                        df_converted[c].astype(str)
                                        .str.replace(',', '.', regex=False)
                                        .str.replace(' ', '', regex=False),
                                        errors='coerce'
                                    )
                                    if not coerced.isna().all():
                                        df_converted[c] = coerced

                            numeric_cols = [c for c in df_converted.columns if pd.api.types.is_numeric_dtype(df_converted[c])]

                            if not numeric_cols:
                                st.error('No se encontraron columnas numéricas en el archivo. Asegúrate de que exista una columna con valores numéricos o un formato compatible.')
                            else:
                                selected_cols = st.multiselect(
                                    'Selecciona la(s) columna(s) de valores',
                                    numeric_cols,
                                    default=[numeric_cols[0]]
                                )

                                if selected_cols:
                                    if import_multi_columns:
                                        modo_columnas = st.radio(
                                            'Interpretar columnas como:',
                                            ['Mismo producto', 'Producto por columna'],
                                            horizontal=True
                                        )

                                        if modo_columnas == 'Mismo producto':
                                            producto_excel_nombre = st.text_input(
                                                'Nombre del producto destino (si no existe se creará)',
                                                value=producto.nombre if producto else '',
                                                placeholder='Ej: Banano'
                                            )
                                            tipo_options = [t.value for t in TipoProducto]
                                            default_tipo_index = tipo_options.index(producto.tipo) if producto and producto.tipo in tipo_options else 0
                                            producto_excel_tipo = st.selectbox(
                                                'Tipo de producto',
                                                tipo_options,
                                                index=default_tipo_index
                                            )
                                            producto_excel_unidad = st.text_input(
                                                'Unidad de medida del producto',
                                                value=producto.unidad_medida if producto and producto.unidad_medida else '',
                                                placeholder='Ej: kg'
                                            )
                                        else:
                                            producto_excel_tipo = st.selectbox(
                                                'Tipo de producto por columna',
                                                [t.value for t in TipoProducto],
                                                index=0
                                            )
                                            producto_excel_unidad = st.text_input(
                                                'Unidad de medida por defecto para productos creados',
                                                placeholder='Ej: kg'
                                            )

                                        st.markdown('**Vista previa de datos para importación:**')
                                        st.dataframe(df_converted[selected_cols].head(50), use_container_width=True)
                                    else:
                                        valores_series = df_converted[selected_cols].apply(pd.to_numeric, errors='coerce').stack().reset_index(drop=True).dropna()
                                        if valores_series.empty:
                                            st.error('No se detectaron valores numéricos válidos en las columnas seleccionadas.')
                                        else:
                                            valores_texto = '\n'.join([str(v) for v in valores_series.tolist()])
                                            excel_total_values = len(valores_series)
                                            if variable.tam_subgrupo > 0:
                                                base_groups = excel_total_values // variable.tam_subgrupo
                                                remainder = excel_total_values % variable.tam_subgrupo
                                                if remainder == 0:
                                                    calculated_n_subgrupos = base_groups
                                                    st.success(
                                                        f'Se detectaron {excel_total_values} valores y se usarán {calculated_n_subgrupos} subgrupos de {variable.tam_subgrupo} observaciones cada uno.'
                                                    )
                                                else:
                                                    calculated_n_subgrupos = base_groups + 1
                                                    st.success(
                                                        f'Se detectaron {excel_total_values} valores y se usarán {calculated_n_subgrupos} subgrupos: '
                                                        f'{base_groups} de {variable.tam_subgrupo} y 1 de {remainder} observaciones.'
                                                    )
                                            st.markdown('**Vista previa de valores detectados:**')
                                            st.dataframe(valores_series.head(50).to_frame('Valor'), use_container_width=True)
                                else:
                                    st.info('Selecciona al menos una columna de valores para continuar.')
                        except Exception as e:
                            st.error(f'Error al leer el archivo: {str(e)}')

                    if valores_texto is None and not import_multi_columns:
                        valores_texto = st.text_area("Valores (masivo)", height=160, placeholder="12.3, 11.9, 13.0, ...")

                    observaciones_txt = st.text_area(
                        "Observaciones de las muestras",
                        placeholder="Notas adicionales aplicables a todas las muestras masivas"
                    )

                    if st.button("✅ Guardar Muestras Masivas y Mediciones", use_container_width=True):
                        if not analista:
                            mostrar_error("Debes seleccionar un analista")
                        else:
                            if import_multi_columns:
                                if df_converted is None or df_converted.empty or not selected_cols:
                                    mostrar_error('Debes subir un archivo válido y seleccionar al menos una columna.')
                                else:
                                    if modo_columnas == 'Mismo producto':
                                        if not producto_excel_nombre:
                                            mostrar_error('Debes indicar el nombre del producto destino.')
                                        else:
                                            if producto and producto.nombre.strip().lower() == producto_excel_nombre.strip().lower():
                                                producto_obj = producto
                                            else:
                                                producto_obj = obtener_o_crear_producto(
                                                    producto_excel_nombre,
                                                    producto_excel_tipo,
                                                    producto_excel_unidad
                                                )

                                            if not producto_obj:
                                                mostrar_error('No se pudo crear el producto objetivo.')
                                            else:
                                                try:
                                                    variable_objs = {}
                                                    for col in selected_cols:
                                                        _, var_name = parse_product_variable(col)
                                                        variable_objs[col] = obtener_o_crear_variable(
                                                            producto_obj.id_producto,
                                                            var_name,
                                                            unidad_medida=producto_excel_unidad
                                                        )

                                                    for idx, fila in df_converted[selected_cols].iterrows():
                                                        muestra = repos['muestra'].crear(
                                                            id_producto=producto_obj.id_producto,
                                                            id_analista=analista.id_analista,
                                                            num_subgrupo=num_subgrupo + idx,
                                                            lote=lote or None,
                                                            origen=origen or None,
                                                            observaciones=(observaciones_txt or None)
                                                        )
                                                        for col, variable in variable_objs.items():
                                                            valor = fila[col]
                                                            if pd.isna(valor):
                                                                continue
                                                            repos['medicion_variable'].crear(
                                                                id_muestra=muestra.id_muestra,
                                                                id_variable=variable.id_variable,
                                                                num_observacion=1,
                                                                valor=float(valor)
                                                            )

                                                    mostrar_exito(
                                                        f"{len(df_converted.index)} muestras importadas en el producto '{producto_obj.nombre}' "
                                                        f"y variables {', '.join(selected_cols)}"
                                                    )
                                                    st.rerun()
                                                except Exception as e:
                                                    mostrar_error(f"Error al guardar importación masiva: {str(e)}")
                                    else:
                                        try:
                                            for col in selected_cols:
                                                prod_name, var_name = parse_product_variable(col)
                                                producto_obj = obtener_o_crear_producto(
                                                    prod_name,
                                                    producto_excel_tipo,
                                                    producto_excel_unidad
                                                )
                                                if not producto_obj:
                                                    continue

                                                variable_obj = obtener_o_crear_variable(
                                                    producto_obj.id_producto,
                                                    var_name,
                                                    unidad_medida=producto_excel_unidad
                                                )

                                                for idx, valor in df_converted[col].dropna().items():
                                                    muestra = repos['muestra'].crear(
                                                        id_producto=producto_obj.id_producto,
                                                        id_analista=analista.id_analista,
                                                        num_subgrupo=num_subgrupo + idx,
                                                        lote=lote or None,
                                                        origen=origen or None,
                                                        observaciones=(observaciones_txt or None)
                                                    )
                                                    repos['medicion_variable'].crear(
                                                        id_muestra=muestra.id_muestra,
                                                        id_variable=variable_obj.id_variable,
                                                        num_observacion=1,
                                                        valor=float(valor)
                                                    )

                                            mostrar_exito(f"Importación masiva terminada con {len(selected_cols)} productos/columnas.")
                                            st.rerun()
                                        except Exception as e:
                                            mostrar_error(f"Error al guardar importación masiva: {str(e)}")
                            else:
                                # Parsear valores
                                raw = re.split(r"[\n,;\s]+", (valores_texto or ""))
                                raw = [r for r in raw if r != ""]
                                try:
                                    valores = [float(v.replace(',', '.')) for v in raw]
                                except Exception:
                                    mostrar_error("Error al parsear los valores. Asegúrate de usar números separados por comas o saltos de línea.")
                                    valores = None

                                if valores is not None:
                                    if file_import and not import_multi_columns:
                                        if calculated_n_subgrupos is None:
                                            mostrar_error(
                                                "No se pudo determinar el número de subgrupos desde el archivo. Revisa el contenido del Excel."
                                            )
                                            valores = None
                                        else:
                                            n_subgrupos = calculated_n_subgrupos
                                    else:
                                        esperado = n_subgrupos * variable.tam_subgrupo
                                        if len(valores) != esperado:
                                            mostrar_error(f"Se esperaban {esperado} valores pero se recibieron {len(valores)}.")
                                            valores = None

                                if valores is not None:
                                    try:
                                        # Crear una muestra y sus mediciones por cada subgrupo
                                        for sg in range(n_subgrupos):
                                            muestra = repos['muestra'].crear(
                                                id_producto=producto.id_producto,
                                                id_analista=analista.id_analista,
                                                num_subgrupo=num_subgrupo + sg,
                                                lote=lote or None,
                                                origen=origen or None,
                                                observaciones=(observaciones_txt or None)
                                            )

                                            inicio = sg * variable.tam_subgrupo
                                            fin = min(inicio + variable.tam_subgrupo, len(valores))
                                            grupo_vals = valores[inicio:fin]

                                            for idx, valor in enumerate(grupo_vals):
                                                repos['medicion_variable'].crear(
                                                    id_muestra=muestra.id_muestra,
                                                    id_variable=variable.id_variable,
                                                    num_observacion=idx + 1,
                                                    valor=valor
                                                )

                                        mostrar_exito(f"{n_subgrupos} muestras y sus mediciones guardadas exitosamente")
                                        st.rerun()
                                    except Exception as e:
                                        mostrar_error(f"Error al guardar masivo: {str(e)}")

                else:
                    # Captura individual (subgrupo único) — comportamiento existente
                    st.markdown("### Observaciones del Subgrupo")
                    st.info(f"Introduce {variable.tam_subgrupo} observaciones para este subgrupo")

                    observaciones = []
                    cols_obs = st.columns(variable.tam_subgrupo)

                    for i in range(variable.tam_subgrupo):
                        with cols_obs[i % len(cols_obs)]:
                            valor = st.number_input(
                                f"Obs {i+1}",
                                value=0.0,
                                step=0.01,
                                key=f"obs_{i}"
                            )
                            observaciones.append(valor)

                    observaciones_txt = st.text_area(
                        "Observaciones de la muestra",
                        placeholder="Notas adicionales sobre la toma de la muestra"
                    )

                    if st.button("✅ Guardar Muestra y Mediciones", use_container_width=True):
                        if not analista:
                            mostrar_error("Debes seleccionar un analista")
                        elif any(o == 0.0 for o in observaciones):
                            mostrar_error("Todas las observaciones deben tener valores válidos")
                        else:
                            try:
                                # Crear muestra
                                muestra = repos['muestra'].crear(
                                    id_producto=producto.id_producto,
                                    id_analista=analista.id_analista,
                                    num_subgrupo=num_subgrupo,
                                    lote=lote or None,
                                    origen=origen or None,
                                    observaciones=observaciones_txt or None
                                )

                                # Crear mediciones
                                for idx, valor in enumerate(observaciones):
                                    repos['medicion_variable'].crear(
                                        id_muestra=muestra.id_muestra,
                                        id_variable=variable.id_variable,
                                        num_observacion=idx + 1,
                                        valor=valor
                                    )

                                mostrar_exito("Muestra y mediciones guardadas exitosamente")
                                st.rerun()
                            except Exception as e:
                                mostrar_error(f"Error al guardar: {str(e)}")
    
    with tab2:
        st.subheader("Captura de Atributos (Defectos y Características)")
        
        # Seleccionar producto y atributo
        col_select1, col_select2 = st.columns(2)
        
        with col_select1:
            producto = seleccionar_producto(repos, key_suffix="atrib")
        
        with col_select2:
            if producto:
                atributo = seleccionar_atributo(repos, producto.id_producto, key_suffix="atrib")
        
        if producto and atributo:
            # Datos de la muestra
            col1, col2, col3 = st.columns(3)
            
            with col1:
                num_subgrupo = st.number_input("Número de subgrupo", min_value=1, value=1, key="subgrupo_atrib")
            
            with col2:
                analista = seleccionar_analista(repos, key_suffix="atrib")
            
            with col3:
                lote = st.text_input("Lote (opcional)", placeholder="Ej: LOTE-2024-001", key="lote_atrib")
            
            origen = st.text_input("Origen (opcional)", placeholder="Ej: Parcela A", key="origen_atrib")
            
            # Datos de inspección
            st.markdown("### Datos de Inspección")
            
            col1, col2 = st.columns(2)
            
            with col1:
                n_inspeccionados = st.number_input(
                    "Cantidad inspeccionada",
                    min_value=1,
                    value=atributo.tam_subgrupo
                )
            
            with col2:
                if atributo.tipo_grafico in ["P", "NP"]:
                    n_defectuosos = st.number_input(
                        "Cantidad de defectuosos",
                        min_value=0,
                        max_value=n_inspeccionados,
                        value=0
                    )
                else:  # C o U
                    n_defectuosos = st.number_input(
                        "Cantidad de defectos",
                        min_value=0,
                        value=0
                    )
            
            observaciones_txt = st.text_area(
                "Observaciones",
                placeholder="Notas sobre los defectos encontrados",
                key="obs_atrib"
            )
            
            if st.button("✅ Guardar Datos de Atributos", use_container_width=True):
                if not analista:
                    mostrar_error("Debes seleccionar un analista")
                else:
                    try:
                        # Crear muestra
                        muestra = repos['muestra'].crear(
                            id_producto=producto.id_producto,
                            id_analista=analista.id_analista,
                            num_subgrupo=num_subgrupo,
                            lote=lote or None,
                            origen=origen or None,
                            observaciones=observaciones_txt or None
                        )
                        
                        # Crear medición de atributo
                        repos['medicion_atributo'].crear(
                            id_muestra=muestra.id_muestra,
                            id_atributo=atributo.id_atributo,
                            n_inspeccionados=n_inspeccionados,
                            n_defectuosos=n_defectuosos
                        )
                        
                        mostrar_exito("Datos de atributos guardados exitosamente")
                        st.rerun()
                    except Exception as e:
                        mostrar_error(f"Error al guardar: {str(e)}")

finally:
    cerrar_sesion(repos['session'])
