import streamlit as st
import pandas as pd
from datetime import datetime
from utils.datos import ExportadorDatos, GeneradorReportes
from utils.streamlit_utils import (
    obtener_repositorios, cerrar_sesion, crear_encabezado_pagina,
    cargar_css_personalizado, mostrar_exito, mostrar_error, mostrar_info,
    seleccionar_producto, seleccionar_variable
)
from models.muestra import Muestra
from models.variables import VariableConfig

# Configuración de la página
st.set_page_config(
    page_title="Exportar Reportes - CEC",
    page_icon="💾",
    layout="wide"
)

cargar_css_personalizado()

# Encabezado
crear_encabezado_pagina(
    "Generación de Reportes",
    "Exportar datos y resultados en formato Excel",
    "💾"
)

# Obtener repositorios
repos = obtener_repositorios()

try:
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Reportes por Variable", "📋 Reportes Generales", "📈 Datos Brutos"])
    
    with tab1:
        st.subheader("Exportar Reporte de Variable")
        
        # Seleccionar producto y variable
        col_select1, col_select2 = st.columns(2)
        
        with col_select1:
            producto = seleccionar_producto(repos)
        
        with col_select2:
            if producto:
                variable = seleccionar_variable(repos, producto.id_producto)
        
        if producto and variable:
            # Obtener mediciones
            mediciones = repos['medicion_variable'].obtener_por_variable(variable.id_variable)
            
            if len(mediciones) == 0:
                mostrar_info("No hay mediciones para esta variable")
            else:
                valores = [float(m.valor) for m in mediciones]
                
                # Crear datos para exportar
                datos_exportar = {}
                
                # Hoja 1: Datos brutos
                datos_brutos = []
                for m in mediciones:
                    muestra = m.muestra
                    datos_brutos.append({
                        "ID Muestra": m.id_muestra,
                        "Subgrupo": muestra.num_subgrupo,
                        "Lote": muestra.lote or "-",
                        "Origen": muestra.origen or "-",
                        "Analista": muestra.analista.nombre_completo,
                        "Fecha": muestra.fecha_hora.strftime("%d/%m/%Y %H:%M"),
                        "Observación": m.num_observacion,
                        "Valor": m.valor
                    })
                
                datos_exportar["Datos Brutos"] = pd.DataFrame(datos_brutos)
                
                # Hoja 2: Estadísticas
                from calculators.estadisticas import estadisticas_descriptivas
                stats = estadisticas_descriptivas(valores)
                
                stats_df = pd.DataFrame({
                    "Parámetro": list(stats.keys()),
                    "Valor": list(stats.values())
                })
                datos_exportar["Estadísticas"] = stats_df
                
                # Hoja 3: Información de la variable
                info_var = pd.DataFrame({
                    "Propiedad": [
                        "Nombre",
                        "Producto",
                        "Tipo",
                        "Unidad",
                        "LCS",
                        "LCI",
                        "Valor Nominal",
                        "Tamaño Subgrupo",
                        "Total Mediciones"
                    ],
                    "Valor": [
                        variable.nombre_variable,
                        producto.nombre,
                        variable.tipo_dato,
                        variable.unidad_medida or "-",
                        variable.lcs,
                        variable.lci,
                        variable.valor_nominal or "-",
                        variable.tam_subgrupo,
                        len(mediciones)
                    ]
                })
                datos_exportar["Información"] = info_var
                
                # Generar archivo
                nombre_archivo = f"Reporte_{producto.nombre}_{variable.nombre_variable}_{datetime.now().strftime('%d%m%Y')}"
                
                excel_bytes = ExportadorDatos.exportar_a_excel(datos_exportar, nombre_archivo)
                
                st.download_button(
                    label="📥 Descargar Excel",
                    data=excel_bytes,
                    file_name=f"{nombre_archivo}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                mostrar_exito(f"Reporte listo para descargar: {nombre_archivo}.xlsx")
    
    with tab2:
        st.subheader("Reportes Generales del Proyecto")
        
        # Obtener estadísticas generales
        num_productos = repos['producto'].contar()
        num_analistas = repos['analista'].contar()
        num_variables = repos['variable'].session.query(VariableConfig).count()
        num_muestras = repos['muestra'].session.query(Muestra).count()
        
        # Generar resumen
        if num_muestras > 0:
            primera_muestra = repos['muestra'].obtener_ultimas(limit=999999)[-1] if len(repos['muestra'].obtener_ultimas(limit=999999)) > 0 else None
            ultima_muestra = repos['muestra'].obtener_ultimas(limit=1)[0] if num_muestras > 0 else None
            
            fecha_inicio = primera_muestra.fecha_hora if primera_muestra else datetime.now()
            fecha_fin = ultima_muestra.fecha_hora if ultima_muestra else datetime.now()
        else:
            fecha_inicio = datetime.now()
            fecha_fin = datetime.now()
        
        resumen = GeneradorReportes.resumen_proyecto(
            num_productos,
            num_muestras,
            num_analistas,
            fecha_inicio,
            fecha_fin
        )
        
        col_resumen1, col_resumen2 = st.columns(2)
        
        with col_resumen1:
            st.markdown("### Resumen del Proyecto")
            resumen_df = pd.DataFrame({
                "Métrica": list(resumen.keys()),
                "Valor": list(resumen.values())
            })
            st.dataframe(resumen_df, hide_index=True, use_container_width=True)
        
        with col_resumen2:
            st.markdown("### Detalles")
            st.info(f"""
            **Período de Análisis**
            - Desde: {fecha_inicio.strftime('%d/%m/%Y')}
            - Hasta: {fecha_fin.strftime('%d/%m/%Y')}
            
            **Composición**
            - Productos: {num_productos}
            - Variables: {num_variables}
            - Muestras totales: {num_muestras}
            """)
        
        # Generar reporte general en Excel
        if num_productos > 0:
            datos_reporte = {}
            
            # Resumen general
            datos_reporte["Resumen"] = resumen_df
            
            # Productos
            productos = repos['producto'].obtener_todos()
            productos_data = []
            for p in productos:
                num_vars = repos['variable'].contar_por_producto(p.id_producto)
                num_atrs = repos['atributo'].contar_por_producto(p.id_producto)
                num_muestras_prod = repos['muestra'].contar_por_producto(p.id_producto)
                
                productos_data.append({
                    "Producto": p.nombre,
                    "Tipo": p.tipo,
                    "Variables": num_vars,
                    "Atributos": num_atrs,
                    "Muestras": num_muestras_prod
                })
            
            datos_reporte["Productos"] = pd.DataFrame(productos_data)
            
            # Analistas
            analistas = repos['analista'].obtener_todos()
            analistas_data = []
            for a in analistas:
                num_muestras_a = repos['muestra'].session.query(Muestra).filter(
                    Muestra.id_analista == a.id_analista
                ).count()
                
                analistas_data.append({
                    "Analista": a.nombre_completo,
                    "Cargo": a.cargo or "-",
                    "Muestras": num_muestras_a
                })
            
            datos_reporte["Analistas"] = pd.DataFrame(analistas_data)
            
            nombre_archivo = f"Reporte_General_{datetime.now().strftime('%d%m%Y_%H%M%S')}"
            
            excel_bytes = ExportadorDatos.exportar_a_excel(datos_reporte, nombre_archivo)
            
            st.download_button(
                label="📥 Descargar Reporte General",
                data=excel_bytes,
                file_name=f"{nombre_archivo}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    with tab3:
        st.subheader("Exportar Datos Brutos")
        
        opcion_datos = st.selectbox(
            "Selecciona qué datos exportar:",
            ["Todas las Muestras", "Productos", "Analistas", "Variables"]
        )
        
        if opcion_datos == "Todas las Muestras":
            muestras = repos['muestra'].obtener_ultimas(limit=10000)
            
            if len(muestras) == 0:
                mostrar_info("No hay muestras para exportar")
            else:
                datos_muestras = []
                for m in muestras:
                    datos_muestras.append({
                        "ID": m.id_muestra,
                        "Producto": m.producto.nombre,
                        "Analista": m.analista.nombre_completo,
                        "Subgrupo": m.num_subgrupo,
                        "Lote": m.lote or "-",
                        "Origen": m.origen or "-",
                        "Fecha": m.fecha_hora.strftime("%d/%m/%Y %H:%M")
                    })
                
                df_muestras = pd.DataFrame(datos_muestras)
                
                csv_bytes = ExportadorDatos.exportar_a_csv(df_muestras, "Muestras")
                
                st.download_button(
                    label="📥 Descargar CSV",
                    data=csv_bytes,
                    file_name=f"Muestras_{datetime.now().strftime('%d%m%Y')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.dataframe(df_muestras, use_container_width=True, hide_index=True)
        
        elif opcion_datos == "Productos":
            productos = repos['producto'].obtener_todos()
            
            productos_data = []
            for p in productos:
                productos_data.append({
                    "ID": p.id_producto,
                    "Nombre": p.nombre,
                    "Tipo": p.tipo,
                    "Variedad": p.variedad or "-",
                    "Unidad": p.unidad_medida,
                    "Descripción": p.descripcion or "-"
                })
            
            df_productos = pd.DataFrame(productos_data)
            
            csv_bytes = ExportadorDatos.exportar_a_csv(df_productos, "Productos")
            
            st.download_button(
                label="📥 Descargar CSV",
                data=csv_bytes,
                file_name=f"Productos_{datetime.now().strftime('%d%m%Y')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.dataframe(df_productos, use_container_width=True, hide_index=True)

finally:
    cerrar_sesion(repos['session'])
