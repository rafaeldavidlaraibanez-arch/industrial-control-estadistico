import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import List, Dict, Optional

class GraficosControl:
    """Clase para generar gráficos de control usando Plotly"""
    
    @staticmethod
    def grafico_xbar_r(datos: Dict) -> go.Figure:
        """Genera gráfico X-barra y R combinado"""
        if "error" in datos:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {datos['error']}", showarrow=False)
            return fig
        
        n_subgrupos = datos["n_subgrupos"]
        subgrupos = list(range(1, n_subgrupos + 1))
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Gráfico de Promedios (X̄)", "Gráfico de Rangos (R)"),
            shared_xaxes=True,
            vertical_spacing=0.12
        )
        
        # Gráfico X-barra
        fig.add_trace(
            go.Scatter(x=subgrupos, y=datos["xbars"], mode='lines+markers',
                      name='X̄', line=dict(color='blue'), marker=dict(size=8)),
            row=1, col=1
        )
        fig.add_hline(y=datos["xbar_bar"], line_dash="dash", line_color="green",
                     annotation_text="LC", row=1, col=1)
        fig.add_hline(y=datos["lcs_xbar"], line_dash="dash", line_color="red",
                     annotation_text="LCS", row=1, col=1)
        fig.add_hline(y=datos["lci_xbar"], line_dash="dash", line_color="red",
                     annotation_text="LCI", row=1, col=1)
        
        # Marcar puntos fuera de control
        for punto in datos["puntos_fuera_xbar"]:
            fig.add_trace(
                go.Scatter(x=[punto+1], y=[datos["xbars"][punto]], 
                          mode='markers', marker=dict(size=15, color='red', symbol='circle-open'),
                          showlegend=False, name='Fuera de control'),
                row=1, col=1
            )
        
        # Gráfico R
        fig.add_trace(
            go.Scatter(x=subgrupos, y=datos["rangos"], mode='lines+markers',
                      name='R', line=dict(color='purple'), marker=dict(size=8)),
            row=2, col=1
        )
        fig.add_hline(y=datos["rango_promedio"], line_dash="dash", line_color="green",
                     annotation_text="LC", row=2, col=1)
        fig.add_hline(y=datos["lcs_r"], line_dash="dash", line_color="red",
                     annotation_text="LCS", row=2, col=1)
        fig.add_hline(y=datos["lci_r"], line_dash="dash", line_color="red",
                     annotation_text="LCI", row=2, col=1)
        
        for punto in datos["puntos_fuera_r"]:
            fig.add_trace(
                go.Scatter(x=[punto+1], y=[datos["rangos"][punto]], 
                          mode='markers', marker=dict(size=15, color='red', symbol='circle-open'),
                          showlegend=False),
                row=2, col=1
            )
        
        fig.update_xaxes(title_text="Subgrupo", row=2, col=1)
        fig.update_yaxes(title_text="X̄", row=1, col=1)
        fig.update_yaxes(title_text="Rango", row=2, col=1)
        fig.update_layout(height=700, title_text="Gráfico de Control X̄-R")
        
        return fig
    
    @staticmethod
    def grafico_xbar_s(datos: Dict) -> go.Figure:
        """Genera gráfico X-barra y S combinado"""
        if "error" in datos:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {datos['error']}", showarrow=False)
            return fig
        
        n_subgrupos = datos["n_subgrupos"]
        subgrupos = list(range(1, n_subgrupos + 1))
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Gráfico de Promedios (X̄)", "Gráfico de Desviación Estándar (S)"),
            shared_xaxes=True,
            vertical_spacing=0.12
        )
        
        # Gráfico X-barra
        fig.add_trace(
            go.Scatter(x=subgrupos, y=datos["xbars"], mode='lines+markers',
                      name='X̄', line=dict(color='blue'), marker=dict(size=8)),
            row=1, col=1
        )
        fig.add_hline(y=datos["xbar_bar"], line_dash="dash", line_color="green",
                     annotation_text="LC", row=1, col=1)
        fig.add_hline(y=datos["lcs_xbar"], line_dash="dash", line_color="red",
                     annotation_text="LCS", row=1, col=1)
        fig.add_hline(y=datos["lci_xbar"], line_dash="dash", line_color="red",
                     annotation_text="LCI", row=1, col=1)
        
        for punto in datos["puntos_fuera_xbar"]:
            fig.add_trace(
                go.Scatter(x=[punto+1], y=[datos["xbars"][punto]], 
                          mode='markers', marker=dict(size=15, color='red', symbol='circle-open'),
                          showlegend=False),
                row=1, col=1
            )
        
        # Gráfico S
        fig.add_trace(
            go.Scatter(x=subgrupos, y=datos["desv_stds"], mode='lines+markers',
                      name='S', line=dict(color='purple'), marker=dict(size=8)),
            row=2, col=1
        )
        fig.add_hline(y=datos["s_promedio"], line_dash="dash", line_color="green",
                     annotation_text="LC", row=2, col=1)
        fig.add_hline(y=datos["lcs_s"], line_dash="dash", line_color="red",
                     annotation_text="LCS", row=2, col=1)
        fig.add_hline(y=datos["lci_s"], line_dash="dash", line_color="red",
                     annotation_text="LCI", row=2, col=1)
        
        for punto in datos["puntos_fuera_s"]:
            fig.add_trace(
                go.Scatter(x=[punto+1], y=[datos["desv_stds"][punto]], 
                          mode='markers', marker=dict(size=15, color='red', symbol='circle-open'),
                          showlegend=False),
                row=2, col=1
            )
        
        fig.update_xaxes(title_text="Subgrupo", row=2, col=1)
        fig.update_yaxes(title_text="X̄", row=1, col=1)
        fig.update_yaxes(title_text="Desv. Est.", row=2, col=1)
        fig.update_layout(height=700, title_text="Gráfico de Control X̄-S")
        
        return fig
    
    @staticmethod
    def grafico_p(datos: Dict) -> go.Figure:
        """Genera gráfico P"""
        if "error" in datos:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {datos['error']}", showarrow=False)
            return fig
        
        n_subgrupos = datos["n_subgrupos"]
        subgrupos = list(range(1, n_subgrupos + 1))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=subgrupos, y=datos["proporciones"], mode='lines+markers',
                                name='p', line=dict(color='blue'), marker=dict(size=8)))
        
        fig.add_hline(y=datos["p_promedio"], line_dash="dash", line_color="green",
                     annotation_text="LC")
        
        for i, (lcs, lci) in enumerate(zip(datos["lcs"], datos["lci"])):
            if i == 0:
                fig.add_hline(y=lcs, line_dash="dash", line_color="red",
                             annotation_text="LCS" if i == 0 else "")
                fig.add_hline(y=lci, line_dash="dash", line_color="red",
                             annotation_text="LCI" if i == 0 else "")
        
        for punto in datos["puntos_fuera"]:
            fig.add_trace(go.Scatter(x=[punto+1], y=[datos["proporciones"][punto]], 
                                    mode='markers', 
                                    marker=dict(size=15, color='red', symbol='circle-open'),
                                    showlegend=False))
        
        fig.update_layout(
            title="Gráfico de Control P",
            xaxis_title="Subgrupo",
            yaxis_title="Proporción de Defectuosos",
            height=500
        )
        
        return fig
    
    @staticmethod
    def grafico_np(datos: Dict) -> go.Figure:
        """Genera gráfico NP"""
        if "error" in datos:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {datos['error']}", showarrow=False)
            return fig
        
        n_subgrupos = datos["n_subgrupos"]
        subgrupos = list(range(1, n_subgrupos + 1))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=subgrupos, y=datos["defectuosos"], mode='lines+markers',
                                name='NP', line=dict(color='blue'), marker=dict(size=8)))
        
        fig.add_hline(y=datos["np_promedio"], line_dash="dash", line_color="green",
                     annotation_text="LC")
        fig.add_hline(y=datos["lcs"], line_dash="dash", line_color="red",
                     annotation_text="LCS")
        fig.add_hline(y=datos["lci"], line_dash="dash", line_color="red",
                     annotation_text="LCI")
        
        for punto in datos["puntos_fuera"]:
            fig.add_trace(go.Scatter(x=[punto+1], y=[datos["defectuosos"][punto]], 
                                    mode='markers', 
                                    marker=dict(size=15, color='red', symbol='circle-open'),
                                    showlegend=False))
        
        fig.update_layout(
            title="Gráfico de Control NP",
            xaxis_title="Subgrupo",
            yaxis_title="Número de Defectuosos",
            height=500
        )
        
        return fig
    
    @staticmethod
    def grafico_c(datos: Dict) -> go.Figure:
        """Genera gráfico C"""
        if "error" in datos:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {datos['error']}", showarrow=False)
            return fig
        
        n_subgrupos = datos["n_subgrupos"]
        subgrupos = list(range(1, n_subgrupos + 1))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=subgrupos, y=datos["defectos"], mode='lines+markers',
                                name='C', line=dict(color='blue'), marker=dict(size=8)))
        
        fig.add_hline(y=datos["c_promedio"], line_dash="dash", line_color="green",
                     annotation_text="LC")
        fig.add_hline(y=datos["lcs"], line_dash="dash", line_color="red",
                     annotation_text="LCS")
        fig.add_hline(y=datos["lci"], line_dash="dash", line_color="red",
                     annotation_text="LCI")
        
        for punto in datos["puntos_fuera"]:
            fig.add_trace(go.Scatter(x=[punto+1], y=[datos["defectos"][punto]], 
                                    mode='markers', 
                                    marker=dict(size=15, color='red', symbol='circle-open'),
                                    showlegend=False))
        
        fig.update_layout(
            title="Gráfico de Control C",
            xaxis_title="Subgrupo",
            yaxis_title="Número de Defectos",
            height=500
        )
        
        return fig
    
    @staticmethod
    def grafico_u(datos: Dict) -> go.Figure:
        """Genera gráfico U"""
        if "error" in datos:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {datos['error']}", showarrow=False)
            return fig
        
        n_subgrupos = datos["n_subgrupos"]
        subgrupos = list(range(1, n_subgrupos + 1))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=subgrupos, y=datos["u_valores"], mode='lines+markers',
                                name='U', line=dict(color='blue'), marker=dict(size=8)))
        
        fig.add_hline(y=datos["u_promedio"], line_dash="dash", line_color="green",
                     annotation_text="LC")
        
        for i, (lcs, lci) in enumerate(zip(datos["lcs"], datos["lci"])):
            if i == 0:
                fig.add_hline(y=lcs, line_dash="dash", line_color="red",
                             annotation_text="LCS")
                fig.add_hline(y=lci, line_dash="dash", line_color="red",
                             annotation_text="LCI")
        
        for punto in datos["puntos_fuera"]:
            fig.add_trace(go.Scatter(x=[punto+1], y=[datos["u_valores"][punto]], 
                                    mode='markers', 
                                    marker=dict(size=15, color='red', symbol='circle-open'),
                                    showlegend=False))
        
        fig.update_layout(
            title="Gráfico de Control U",
            xaxis_title="Subgrupo",
            yaxis_title="Defectos por Unidad",
            height=500
        )
        
        return fig


class GraficosAnalisis:
    """Clase para gráficos de análisis"""
    
    @staticmethod
    def diagrama_pareto(datos: Dict) -> go.Figure:
        """Genera diagrama de Pareto"""
        if "error" in datos:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {datos['error']}", showarrow=False)
            return fig
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Barras
        fig.add_trace(
            go.Bar(x=datos["tipos"], y=datos["cantidades"], name="Defectos",
                  marker=dict(color='lightblue')),
            secondary_y=False
        )
        
        # Línea de porcentaje acumulado
        fig.add_trace(
            go.Scatter(x=datos["tipos"], y=datos["porcentajes_acumulados"],
                      name="% Acumulado", mode='lines+markers',
                      line=dict(color='red', width=3),
                      marker=dict(size=8)),
            secondary_y=True
        )
        
        fig.update_yaxes(title_text="Cantidad de Defectos", secondary_y=False)
        fig.update_yaxes(title_text="Porcentaje Acumulado (%)", secondary_y=True)
        fig.update_xaxes(title_text="Tipo de Defecto")
        
        fig.update_layout(
            title="Diagrama de Pareto",
            height=500,
            hovermode="x unified"
        )
        
        return fig
    
    @staticmethod
    def histograma_con_normal(datos: List[float], media: float, sigma: float) -> go.Figure:
        """Genera histograma con curva normal"""
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(x=datos, name="Datos", nbinsx=30,
                                  marker=dict(color='lightblue')))
        
        # Curva normal teórica
        x_normal = np.linspace(min(datos), max(datos), 100)
        from scipy import stats
        y_normal = stats.norm.pdf(x_normal, media, sigma) * len(datos) * (max(datos) - min(datos)) / 30
        
        fig.add_trace(go.Scatter(x=x_normal, y=y_normal, name="Distribución Normal",
                                mode='lines', line=dict(color='red', width=2)))
        
        fig.update_layout(
            title="Histograma con Curva Normal",
            xaxis_title="Valor",
            yaxis_title="Frecuencia",
            height=500
        )
        
        return fig
    
    @staticmethod
    def grafico_capacidad_proceso(indices: Dict) -> go.Figure:
        """Genera visualización de índices de capacidad"""
        if "error" in indices:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {indices['error']}", showarrow=False)
            return fig
        
        fig = go.Figure()
        
        indicadores = ["Cp", "Cpk", "Pp", "Ppk"]
        valores = [indices.get("cp", 0), indices.get("cpk", 0), 
                  indices.get("pp", 0), indices.get("ppk", 0)]
        colores = ["green" if v >= 1.33 else "orange" if v >= 1.0 else "red" for v in valores]
        
        fig.add_trace(go.Bar(x=indicadores, y=valores, marker=dict(color=colores),
                            text=valores, textposition="auto"))
        
        fig.add_hline(y=1.0, line_dash="dash", line_color="orange",
                     annotation_text="Mínimo aceptable (1.0)")
        fig.add_hline(y=1.33, line_dash="dash", line_color="green",
                     annotation_text="Óptimo (1.33)")
        
        fig.update_layout(
            title="Índices de Capacidad del Proceso",
            yaxis_title="Valor del Índice",
            showlegend=False,
            height=400
        )
        
        return fig
    
    @staticmethod
    def grafico_q_q(datos: List[float]) -> go.Figure:
        """Genera gráfico Q-Q"""
        from scipy import stats
        
        datos_ordenados = np.sort(datos)
        teoricos = stats.norm.ppf(np.linspace(0.01, 0.99, len(datos)))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=teoricos, y=datos_ordenados, mode='markers',
                                name="Datos", marker=dict(size=8, color='blue')))
        
        # Línea de referencia
        min_val = min(teoricos)
        max_val = max(teoricos)
        fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val],
                                mode='lines', name="Referencia", 
                                line=dict(color='red', dash='dash')))
        
        fig.update_layout(
            title="Gráfico Q-Q",
            xaxis_title="Cuantiles Teóricos",
            yaxis_title="Cuantiles Observados",
            height=500
        )
        
        return fig
