# -*- coding: utf-8 -*-
"""ejercicio5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xPhMJY0Fhz2tD7MBleWKlGQo59A0wm08
"""

from google.colab import drive
drive.mount("/content/drive")
import pandas as pd
data = pd.read_csv('/content/drive/MyDrive/parcial1/nivelestres.csv')

# Conectar Google Drive y leer el archivo CSV
from google.colab import drive
import pandas as pd

# Montar Google Drive
drive.mount("/content/drive")

# Leer el archivo desde la ubicación especificada en Google Drive
data = pd.read_csv('/content/drive/MyDrive/parcial1/nivelestres.csv')

# Paso 1: Definir funciones para Normalización y Penalizaciones L1 y L2

def normalizar_columna(columna):
    min_val = min(columna)
    max_val = max(columna)
    return [(x - min_val) / (max_val - min_val) if max_val != min_val else 0 for x in columna]

def calcular_penalizacion_l1(coeficientes, lambd=0.05):
    l1_penalizacion = lambd * sum(abs(w) for w in coeficientes)
    return l1_penalizacion

def calcular_penalizacion_l2(coeficientes, lambd=0.05):
    l2_penalizacion = lambd * sum(w**2 for w in coeficientes)
    return l2_penalizacion

columnas_continuas = [
    'age', 'bmi', 'snoring rate', 'respiration rate', 'body temperature',
    'limb movement', 'blood oxygen', 'eye movement', 'sleeping hours', 'heart rate'
]

data_filled = data[columnas_continuas].fillna(data.median(numeric_only=True))

data_normalized = pd.DataFrame()
for col in columnas_continuas:
    if col in data_filled.columns:
        valores_columna = [float(x) for x in data_filled[col]]
        data_normalized[col] = normalizar_columna(valores_columna)

print("\nPrimeras filas del DataFrame Normalizado:")
print(data_normalized.head())

coeficientes = [0.5, -0.8, 0.3, 0.6, -0.2, 0.7, -0.1, 0.4, -0.3, 0.9]

l1_penalizacion = calcular_penalizacion_l1(coeficientes, lambd=0.05)
l2_penalizacion = calcular_penalizacion_l2(coeficientes, lambd=0.05)

print(f"\nPenalización L1: {l1_penalizacion}")
print(f"Penalización L2: {l2_penalizacion}")