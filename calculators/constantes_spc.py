"""
Constantes estadisticas para graficos de control por variables
Tomadas de tablas de ANSI/ASQC B1

Cada constante depende del tamanio del subgrupo (n)
"""

CONSTANTES = {
    2: {"d2": 1.128, "c4": 0.7979, "A2": 1.880, "A3": 2.659, "B3": 0.000, "B4": 3.267, "D3": 0.000, "D4": 3.267},
    3: {"d2": 1.693, "c4": 0.8862, "A2": 1.023, "A3": 1.954, "B3": 0.000, "B4": 2.568, "D3": 0.000, "D4": 2.575},
    4: {"d2": 2.059, "c4": 0.9213, "A2": 0.729, "A3": 1.628, "B3": 0.000, "B4": 2.266, "D3": 0.000, "D4": 2.282},
    5: {"d2": 2.326, "c4": 0.9400, "A2": 0.577, "A3": 1.427, "B3": 0.000, "B4": 2.089, "D3": 0.000, "D4": 2.115},
    6: {"d2": 2.534, "c4": 0.9515, "A2": 0.483, "A3": 1.287, "B3": 0.030, "B4": 1.970, "D3": 0.029, "D4": 1.874},
    7: {"d2": 2.704, "c4": 0.9594, "A2": 0.419, "A3": 1.182, "B3": 0.118, "B4": 1.882, "D3": 0.113, "D4": 1.864},
    8: {"d2": 2.847, "c4": 0.9650, "A2": 0.373, "A3": 1.099, "B3": 0.185, "B4": 1.815, "D3": 0.179, "D4": 1.816},
    9: {"d2": 2.970, "c4": 0.9693, "A2": 0.337, "A3": 1.032, "B3": 0.239, "B4": 1.761, "D3": 0.232, "D4": 1.777},
    10: {"d2": 3.078, "c4": 0.9727, "A2": 0.308, "A3": 0.975, "B3": 0.284, "B4": 1.716, "D3": 0.276, "D4": 1.744},
}

def obtener_constante(n: int, constante: str) -> float:
    """
    Obtiene el valor de una constante para un tamanio de subgrupo
    
    Args:
        n: tamanio del subgrupo (2 a 10)
        constante: nombre de la constante (d2, c4, A2, etc)
    
    Returns:
        Valor de la constante
    """
    if n not in CONSTANTES:
        raise ValueError(f"Tamanio de subgrupo no valido: {n}. Debe estar entre 2 y 10")
    
    if constante not in CONSTANTES[n]:
        raise ValueError(f"Constante no valida: {constante}")
    
    return CONSTANTES[n][constante]
