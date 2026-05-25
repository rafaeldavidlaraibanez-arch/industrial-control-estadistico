"""
Script para inicializar el proyecto con datos de ejemplo
Ejecutar: python init_demo.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database.engine import init_db, SessionLocal
from repository.producto_repository import ProductoRepository
from repository.analista_repository import AnalistaRepository
from repository.variable_repository import VariableRepository, AtributoRepository
from repository.muestra_repository import MuestraRepository, MedicionVariableRepository, MedicionAtributoRepository
import random
from datetime import datetime, timedelta
import numpy as np

def crear_datos_ejemplo():
    """Crea datos de ejemplo para demostración"""
    
    print("🚀 Inicializando base de datos...")
    init_db()
    print("✅ Base de datos inicializada")
    
    session = SessionLocal()
    
    try:
        # Crear repositorios
        prod_repo = ProductoRepository(session)
        analista_repo = AnalistaRepository(session)
        var_repo = VariableRepository(session)
        attr_repo = AtributoRepository(session)
        muestra_repo = MuestraRepository(session)
        med_var_repo = MedicionVariableRepository(session)
        med_attr_repo = MedicionAtributoRepository(session)
        
        print("\n📊 Creando productos...")
        
        # Crear productos
        productos = [
            {
                "nombre": "Tomate Roma",
                "tipo": "fruta",
                "variedad": "Roma",
                "unidad_medida": "kg",
                "descripcion": "Tomate fresco para mercado"
            },
            {
                "nombre": "Lechuga Crespa",
                "tipo": "hortaliza",
                "variedad": "Crespa",
                "unidad_medida": "unidades",
                "descripcion": "Lechuga hidropónica"
            },
            {
                "nombre": "Menta Fresca",
                "tipo": "planta_medicinal",
                "variedad": "Piperita",
                "unidad_medida": "kg",
                "descripcion": "Menta para infusiones"
            }
        ]
        
        productos_creados = []
        for p in productos:
            prod = prod_repo.crear(**p)
            productos_creados.append(prod)
            print(f"  ✅ {p['nombre']}")
        
        print("\n👤 Creando analistas...")
        
        # Crear analistas
        analistas_data = [
            {"nombre": "Carlos", "apellido": "Mendoza", "cargo": "Técnico en Calidad", "contacto": "carlos@empresa.com"},
            {"nombre": "María", "apellido": "García", "cargo": "Inspector", "contacto": "maria@empresa.com"},
            {"nombre": "Juan", "apellido": "López", "cargo": "Supervisor", "contacto": "juan@empresa.com"}
        ]
        
        analistas_creados = []
        for a in analistas_data:
            analista = analista_repo.crear(**a)
            analistas_creados.append(analista)
            print(f"  ✅ {a['nombre']} {a['apellido']}")
        
        print("\n📊 Creando variables...")
        
        # Crear variables para cada producto
        for i, prod in enumerate(productos_creados):
            if i == 0:  # Tomate
                variables = [
                    {
                        "nombre_variable": "Peso",
                        "tipo_dato": "continua",
                        "lcs": 300,
                        "lci": 200,
                        "valor_nominal": 250,
                        "tam_subgrupo": 5,
                        "unidad_medida": "g"
                    },
                    {
                        "nombre_variable": "Diámetro",
                        "tipo_dato": "continua",
                        "lcs": 85,
                        "lci": 75,
                        "valor_nominal": 80,
                        "tam_subgrupo": 5,
                        "unidad_medida": "mm"
                    }
                ]
            elif i == 1:  # Lechuga
                variables = [
                    {
                        "nombre_variable": "Tamaño",
                        "tipo_dato": "continua",
                        "lcs": 35,
                        "lci": 25,
                        "valor_nominal": 30,
                        "tam_subgrupo": 5,
                        "unidad_medida": "cm"
                    }
                ]
            else:  # Menta
                variables = [
                    {
                        "nombre_variable": "Humedad",
                        "tipo_dato": "continua",
                        "lcs": 95,
                        "lci": 85,
                        "valor_nominal": 90,
                        "tam_subgrupo": 5,
                        "unidad_medida": "%"
                    }
                ]
            
            for var_data in variables:
                var = var_repo.crear(
                    id_producto=prod.id_producto,
                    **var_data
                )
                print(f"  ✅ {prod.nombre}: {var_data['nombre_variable']}")
        
        print("\n📌 Creando atributos...")
        
        # Crear atributos
        for prod in productos_creados:
            atributos = [
                {
                    "nombre_atributo": "Defectos de forma",
                    "tipo_grafico": "P",
                    "tam_subgrupo": 50
                },
                {
                    "nombre_atributo": "Manchas",
                    "tipo_grafico": "C",
                    "tam_subgrupo": 50
                }
            ]
            
            for attr_data in atributos:
                attr = attr_repo.crear(
                    id_producto=prod.id_producto,
                    **attr_data
                )
                print(f"  ✅ {prod.nombre}: {attr_data['nombre_atributo']}")
        
        print("\n📝 Creando muestras y mediciones...")
        
        # Crear muestras con mediciones realistas
        np.random.seed(42)
        
        for prod_idx, prod in enumerate(productos_creados):
            variables = var_repo.obtener_por_producto(prod.id_producto)
            
            for var in variables:
                # Generar 50 subgrupos (250 observaciones)
                for subgrupo in range(1, 11):  # 10 subgrupos
                    # Generar valores realistas
                    if var.nombre_variable == "Peso":
                        valor_base = 250 + np.random.normal(0, 10)
                    elif var.nombre_variable == "Diámetro":
                        valor_base = 80 + np.random.normal(0, 2)
                    elif var.nombre_variable == "Tamaño":
                        valor_base = 30 + np.random.normal(0, 1.5)
                    else:  # Humedad
                        valor_base = 90 + np.random.normal(0, 2)
                    
                    muestra = muestra_repo.crear(
                        id_producto=prod.id_producto,
                        id_analista=random.choice(analistas_creados).id_analista,
                        num_subgrupo=subgrupo,
                        lote=f"LOTE-2024-{prod_idx:02d}{subgrupo:02d}",
                        origen=f"Parcela {random.choice(['A', 'B', 'C'])}"
                    )
                    
                    # Crear 5 observaciones
                    for obs in range(var.tam_subgrupo):
                        valor = valor_base + np.random.normal(0, 1)
                        med_var_repo.crear(
                            id_muestra=muestra.id_muestra,
                            id_variable=var.id_variable,
                            num_observacion=obs + 1,
                            valor=valor
                        )
                
                print(f"  ✅ {prod.nombre}: {var.nombre_variable} - 10 subgrupos")
        
        print("\n✨ Datos de ejemplo creados exitosamente!")
        print("\n📊 Resumen:")
        print(f"  - Productos: {len(productos_creados)}")
        print(f"  - Analistas: {len(analistas_creados)}")
        from models.variables import VariableConfig, AtributoConfig
        num_variables = session.query(VariableConfig).count()
        num_atributos = session.query(AtributoConfig).count()
        print(f"  - Variables: {num_variables}")
        print(f"  - Atributos: {num_atributos}")
        
        print("\n🚀 Para iniciar la aplicación:")
        print("   streamlit run streamlit_app.py")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        session.close()

if __name__ == "__main__":
    crear_datos_ejemplo()
