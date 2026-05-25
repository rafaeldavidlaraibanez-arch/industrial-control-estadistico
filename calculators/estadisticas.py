import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
from calculators.constantes_spc import obtener_constante

def normalidad_shapiro_wilk(datos: List[float]) -> Dict:
    """
    Realiza la prueba de normalidad de Shapiro-Wilk
    
    Args:
        datos: lista de valores numericos
    
    Returns:
        diccionario con estadistico W, p-valor e interpretacion
    """
    if len(datos) < 3:
        return {
            "error": "Se necesitan al menos 3 observaciones para la prueba de normalidad"
        }
    
    statistic, p_value = stats.shapiro(datos)
    
    return {
        "estadistico_w": round(statistic, 6),
        "p_valor": round(p_value, 6),
        "es_normal": p_value > 0.05,
        "interpretacion": "Los datos siguen una distribucion normal" if p_value > 0.05 
                         else "Los datos NO siguen una distribucion normal"
    }

def estadisticas_descriptivas(datos: List[float]) -> Dict:
    """
    Calcula estadisticas descriptivas basicas
    """
    arr = np.array(datos)
    return {
        "n": len(datos),
        "media": round(float(np.mean(arr)), 4),
        "mediana": round(float(np.median(arr)), 4),
        "desv_std": round(float(np.std(arr, ddof=1)), 4),
        "varianza": round(float(np.var(arr, ddof=1)), 4),
        "minimo": round(float(np.min(arr)), 4),
        "maximo": round(float(np.max(arr)), 4),
        "rango": round(float(np.max(arr) - np.min(arr)), 4),
        "q1": round(float(np.percentile(arr, 25)), 4),
        "q3": round(float(np.percentile(arr, 75)), 4),
    }

def calcular_xbar_r(mediciones: List[float], tam_subgrupo: int) -> Dict:
    """
    Calcula graficos de control X-barra y R
    
    Args:
        mediciones: lista de valores medidos
        tam_subgrupo: tamanio de cada subgrupo
    
    Returns:
        diccionario con datos de ambos graficos
    """
    n_subgrupos = len(mediciones) // tam_subgrupo
    
    if n_subgrupos < 2:
        return {"error": f"Se necesitan al menos {tam_subgrupo * 2} observaciones"}
    
    subgrupos = [mediciones[i*tam_subgrupo:(i+1)*tam_subgrupo] for i in range(n_subgrupos)]
    
    xbars = [np.mean(sg) for sg in subgrupos]
    rangos = [np.max(sg) - np.min(sg) for sg in subgrupos]
    
    xbar_bar = np.mean(xbars)
    rango_prom = np.mean(rangos)
    
    const = obtener_constante(tam_subgrupo, 'A2')
    d3 = obtener_constante(tam_subgrupo, 'D3')
    d4 = obtener_constante(tam_subgrupo, 'D4')
    
    lcs_xbar = xbar_bar + const * rango_prom
    lci_xbar = xbar_bar - const * rango_prom
    lcs_r = d4 * rango_prom
    lci_r = d3 * rango_prom
    
    puntos_fuera_xbar = [i for i, x in enumerate(xbars) if x > lcs_xbar or x < lci_xbar]
    puntos_fuera_r = [i for i, r in enumerate(rangos) if r > lcs_r or r < lci_r]
    
    return {
        "xbars": [round(x, 4) for x in xbars],
        "rangos": [round(r, 4) for r in rangos],
        "xbar_bar": round(xbar_bar, 4),
        "rango_promedio": round(rango_prom, 4),
        "lcs_xbar": round(lcs_xbar, 4),
        "lci_xbar": round(lci_xbar, 4),
        "lcs_r": round(lcs_r, 4),
        "lci_r": round(lci_r, 4),
        "puntos_fuera_xbar": puntos_fuera_xbar,
        "puntos_fuera_r": puntos_fuera_r,
        "n_subgrupos": n_subgrupos,
        "tam_subgrupo": tam_subgrupo
    }

def calcular_indices_capacidad(mediciones: List[float], lcs: float, lci: float, 
                               valor_nominal: float = None) -> Dict:
    """
    Calcula indices de capacidad del proceso Cp, Cpk, Pp, Ppk
    """
    arr = np.array(mediciones)
    media = np.mean(arr)
    sigma_largo = np.std(arr, ddof=1)
    
    if sigma_largo == 0:
        return {"error": "No hay variacion en los datos"}

    # Validar límites de especificación
    if lcs is None or lci is None:
        return {"error": "LCS o LCI no definidos para la variable. Establece los límites o provee valores temporales."}

    try:
        lcs_val = float(lcs)
        lci_val = float(lci)
    except Exception:
        return {"error": "LCS o LCI inválidos. Deben ser números."}

    cp = (lcs_val - lci_val) / (6 * sigma_largo)
    cpk = min((lcs_val - media) / (3 * sigma_largo), (media - lci_val) / (3 * sigma_largo))
    pp = (lcs_val - lci_val) / (6 * sigma_largo)
    ppk = min((lcs_val - media) / (3 * sigma_largo), (media - lci_val) / (3 * sigma_largo))
    
    estado_cpk = "No capaz" if cpk < 1.0 else ("Condicionalmente capaz" if cpk < 1.33 else "Capaz")
    
    return {
        "cp": round(cp, 4),
        "cpk": round(cpk, 4),
        "pp": round(pp, 4),
        "ppk": round(ppk, 4),
        "media": round(media, 4),
        "sigma": round(sigma_largo, 4),
        "estado": estado_cpk,
        "semaforo": "rojo" if cpk < 1.0 else ("amarillo" if cpk < 1.33 else "verde")
    }

def detectar_atipicos(mediciones: List[float], metodo: str = "iqr") -> Dict:
    """
    Detecta valores atipicos usando IQR o Z-score
    """
    arr = np.array(mediciones)
    
    if metodo == "iqr":
        q1 = np.percentile(arr, 25)
        q3 = np.percentile(arr, 75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        
        atipicos = [(i, v) for i, v in enumerate(arr) 
                   if v < limite_inferior or v > limite_superior]
    
    elif metodo == "zscore":
        z_scores = np.abs(stats.zscore(arr))
        atipicos = [(i, v) for i, v in enumerate(arr) if z_scores[i] > 3]
    
    else:
        return {"error": "Metodo no valido"}
    
    return {
        "cantidad_atipicos": len(atipicos),
        "indices": [a[0] for a in atipicos],
        "valores": [round(a[1], 4) for a in atipicos],
        "metodo": metodo
    }


def calcular_xbar_s(mediciones: List[float], tam_subgrupo: int) -> Dict:
    """
    Calcula graficos de control X-barra y S
    
    Args:
        mediciones: lista de valores medidos
        tam_subgrupo: tamanio de cada subgrupo
    
    Returns:
        diccionario con datos de ambos graficos
    """
    n_subgrupos = len(mediciones) // tam_subgrupo
    
    if n_subgrupos < 2:
        return {"error": f"Se necesitan al menos {tam_subgrupo * 2} observaciones"}
    
    subgrupos = [mediciones[i*tam_subgrupo:(i+1)*tam_subgrupo] for i in range(n_subgrupos)]
    
    xbars = [np.mean(sg) for sg in subgrupos]
    desv_stds = [np.std(sg, ddof=1) if len(sg) > 1 else 0 for sg in subgrupos]
    
    xbar_bar = np.mean(xbars)
    s_promedio = np.mean(desv_stds)
    
    c4 = obtener_constante(tam_subgrupo, 'c4')
    a3 = obtener_constante(tam_subgrupo, 'A3')
    b3 = obtener_constante(tam_subgrupo, 'B3')
    b4 = obtener_constante(tam_subgrupo, 'B4')
    
    lcs_xbar = xbar_bar + a3 * s_promedio
    lci_xbar = xbar_bar - a3 * s_promedio
    lcs_s = b4 * s_promedio
    lci_s = b3 * s_promedio
    
    puntos_fuera_xbar = [i for i, x in enumerate(xbars) if x > lcs_xbar or x < lci_xbar]
    puntos_fuera_s = [i for i, s in enumerate(desv_stds) if s > lcs_s or s < lci_s]
    
    return {
        "xbars": [round(x, 4) for x in xbars],
        "desv_stds": [round(s, 4) for s in desv_stds],
        "xbar_bar": round(xbar_bar, 4),
        "s_promedio": round(s_promedio, 4),
        "lcs_xbar": round(lcs_xbar, 4),
        "lci_xbar": round(lci_xbar, 4),
        "lcs_s": round(lcs_s, 4),
        "lci_s": round(lci_s, 4),
        "puntos_fuera_xbar": puntos_fuera_xbar,
        "puntos_fuera_s": puntos_fuera_s,
        "n_subgrupos": n_subgrupos,
        "tam_subgrupo": tam_subgrupo
    }


def calcular_grafico_p(defectuosos: List[int], inspeccionados: List[int]) -> Dict:
    """
    Calcula grafico de control P (proporcion de defectuosos)
    
    Args:
        defectuosos: lista con numero de defectuosos en cada subgrupo
        inspeccionados: lista con numero inspeccionados en cada subgrupo
    
    Returns:
        diccionario con datos del grafico
    """
    if len(defectuosos) != len(inspeccionados):
        return {"error": "Las listas deben tener la misma longitud"}
    
    n_subgrupos = len(defectuosos)
    
    proporciones = [d / i if i > 0 else 0 for d, i in zip(defectuosos, inspeccionados)]
    p_promedio = sum(defectuosos) / sum(inspeccionados) if sum(inspeccionados) > 0 else 0
    
    if p_promedio == 0 or p_promedio == 1:
        return {"error": "La proporcion promedio debe estar entre 0 y 1 (excluyendo extremos)"}
    
    limites_superiores = []
    limites_inferiores = []
    
    for n in inspeccionados:
        if n > 0:
            error_std = np.sqrt(p_promedio * (1 - p_promedio) / n)
            lcs = p_promedio + 3 * error_std
            lci = max(0, p_promedio - 3 * error_std)
        else:
            lcs = lci = 0
        limites_superiores.append(lcs)
        limites_inferiores.append(lci)
    
    puntos_fuera = [i for i, p in enumerate(proporciones) if p > limites_superiores[i] or p < limites_inferiores[i]]
    
    return {
        "proporciones": [round(p, 4) for p in proporciones],
        "p_promedio": round(p_promedio, 4),
        "lcs": [round(l, 4) for l in limites_superiores],
        "lci": [round(l, 4) for l in limites_inferiores],
        "puntos_fuera": puntos_fuera,
        "n_subgrupos": n_subgrupos
    }


def calcular_grafico_np(defectuosos: List[int], tam_subgrupo: int) -> Dict:
    """
    Calcula grafico de control NP (numero de defectuosos)
    
    Args:
        defectuosos: lista con numero de defectuosos en cada subgrupo
        tam_subgrupo: tamanio del subgrupo (constante)
    
    Returns:
        diccionario con datos del grafico
    """
    n_subgrupos = len(defectuosos)
    np_promedio = np.mean(defectuosos)
    p = np_promedio / tam_subgrupo
    
    if p <= 0 or p >= 1:
        return {"error": "La proporcion debe estar entre 0 y 1"}
    
    error_std = np.sqrt(tam_subgrupo * p * (1 - p))
    lcs_np = np_promedio + 3 * error_std
    lci_np = max(0, np_promedio - 3 * error_std)
    
    puntos_fuera = [i for i, d in enumerate(defectuosos) if d > lcs_np or d < lci_np]
    
    return {
        "defectuosos": defectuosos,
        "np_promedio": round(np_promedio, 4),
        "p": round(p, 4),
        "lcs": round(lcs_np, 4),
        "lci": round(lci_np, 4),
        "puntos_fuera": puntos_fuera,
        "n_subgrupos": n_subgrupos,
        "tam_subgrupo": tam_subgrupo
    }


def calcular_grafico_c(defectos: List[int]) -> Dict:
    """
    Calcula grafico de control C (numero de defectos)
    
    Args:
        defectos: lista con numero de defectos en cada subgrupo
    
    Returns:
        diccionario con datos del grafico
    """
    n_subgrupos = len(defectos)
    c_promedio = np.mean(defectos)
    
    if c_promedio <= 0:
        return {"error": "El promedio de defectos debe ser positivo"}
    
    error_std = np.sqrt(c_promedio)
    lcs_c = c_promedio + 3 * error_std
    lci_c = max(0, c_promedio - 3 * error_std)
    
    puntos_fuera = [i for i, c in enumerate(defectos) if c > lcs_c or c < lci_c]
    
    return {
        "defectos": defectos,
        "c_promedio": round(c_promedio, 4),
        "lcs": round(lcs_c, 4),
        "lci": round(lci_c, 4),
        "puntos_fuera": puntos_fuera,
        "n_subgrupos": n_subgrupos
    }


def calcular_grafico_u(defectos: List[int], unidades: List[int]) -> Dict:
    """
    Calcula grafico de control U (numero de defectos por unidad)
    
    Args:
        defectos: lista con numero de defectos en cada subgrupo
        unidades: lista con numero de unidades en cada subgrupo
    
    Returns:
        diccionario con datos del grafico
    """
    if len(defectos) != len(unidades):
        return {"error": "Las listas deben tener la misma longitud"}
    
    n_subgrupos = len(defectos)
    u_valores = [d / u if u > 0 else 0 for d, u in zip(defectos, unidades)]
    u_promedio = sum(defectos) / sum(unidades) if sum(unidades) > 0 else 0
    
    if u_promedio <= 0:
        return {"error": "El promedio de defectos por unidad debe ser positivo"}
    
    limites_superiores = []
    limites_inferiores = []
    
    for u in unidades:
        if u > 0:
            error_std = np.sqrt(u_promedio / u)
            lcs = u_promedio + 3 * error_std
            lci = max(0, u_promedio - 3 * error_std)
        else:
            lcs = lci = 0
        limites_superiores.append(lcs)
        limites_inferiores.append(lci)
    
    puntos_fuera = [i for i, u in enumerate(u_valores) if u > limites_superiores[i] or u < limites_inferiores[i]]
    
    return {
        "u_valores": [round(u, 4) for u in u_valores],
        "u_promedio": round(u_promedio, 4),
        "lcs": [round(l, 4) for l in limites_superiores],
        "lci": [round(l, 4) for l in limites_inferiores],
        "puntos_fuera": puntos_fuera,
        "n_subgrupos": n_subgrupos
    }


def calcular_diagrama_pareto(defectos: Dict[str, int], umbral: float = 0.80) -> Dict:
    """
    Calcula diagrama de Pareto
    
    Args:
        defectos: diccionario con {tipo_defecto: cantidad}
        umbral: porcentaje acumulado para identificar factores vitales
    
    Returns:
        diccionario con datos del diagrama
    """
    if not defectos:
        return {"error": "No hay datos de defectos"}
    
    sorted_items = sorted(defectos.items(), key=lambda x: x[1], reverse=True)
    total = sum(defectos.values())
    
    tipos = [item[0] for item in sorted_items]
    cantidades = [item[1] for item in sorted_items]
    porcentajes = [(c / total * 100) for c in cantidades]
    porcentajes_acumulados = []
    acumulado = 0
    
    for p in porcentajes:
        acumulado += p
        porcentajes_acumulados.append(acumulado)
    
    # Identificar factores vitales (regla 80/20)
    factores_vitales = [i for i, p in enumerate(porcentajes_acumulados) if p <= umbral * 100]
    if factores_vitales:
        factores_vitales = list(range(max(factores_vitales) + 1))
    
    return {
        "tipos": tipos,
        "cantidades": cantidades,
        "porcentajes": [round(p, 2) for p in porcentajes],
        "porcentajes_acumulados": [round(p, 2) for p in porcentajes_acumulados],
        "total_defectos": total,
        "factores_vitales": factores_vitales,
        "num_factores_vitales": len(factores_vitales)
    }


def normalidad_ks(datos: List[float]) -> Dict:
    """
    Realiza la prueba de normalidad de Kolmogorov-Smirnov
    """
    if len(datos) < 2:
        return {"error": "Se necesitan al menos 2 observaciones"}
    
    statistic, p_value = stats.kstest(datos, 'norm', args=(np.mean(datos), np.std(datos, ddof=1)))
    
    return {
        "estadistico": round(statistic, 6),
        "p_valor": round(p_value, 6),
        "es_normal": p_value > 0.05,
        "interpretacion": "Los datos siguen una distribucion normal (KS)" if p_value > 0.05 
                         else "Los datos NO siguen una distribucion normal (KS)"
    }


def normalidad_anderson_darling(datos: List[float]) -> Dict:
    """
    Realiza la prueba de normalidad de Anderson-Darling
    """
    if len(datos) < 3:
        return {"error": "Se necesitan al menos 3 observaciones"}
    
    result = stats.anderson(datos)
    
    es_normal = result.statistic < result.critical_values[2]  # 5% significance level
    
    return {
        "estadistico": round(result.statistic, 6),
        "valores_criticos": [round(vc, 6) for vc in result.critical_values],
        "niveles_significancia": [15, 10, 5, 2.5, 1],
        "es_normal": es_normal,
        "interpretacion": "Los datos siguen una distribucion normal (Anderson-Darling)" if es_normal 
                         else "Los datos NO siguen una distribucion normal (Anderson-Darling)"
    }
