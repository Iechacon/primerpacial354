# -*- coding: utf-8 -*-
"""ejercicio2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JaqwakR_iM-O6L-0VAKwWUS1nny5sqC1

**2.      Selección un datatset tabular de al menos 1000 columnas, 14 filas. Si elige imágenes igualmente puede convertir la imagen en datos tabulares de NxM. De esta selección indique cual es la clase o si no tiene.**
El dataset utilizado en estos momentos tiene los datos de personas que tienen estrés al dormir, tiene 13 columnas y 1000 datos las columnas que tiene son:
* Edad
* Estado civil
* Género
* IMC (índice de masa corporal)
* Frecuencia de ronquidos
* Frecuencia respiratoria
* Temperatura corporal
* Movimiento de las extremidades
* Oxígeno en la sangre
* Movimiento ocular
* Horas de sueño
* Frecuencia cardiaca
* Nivel de estrés

Como se puede notar, este dataset es uno supervisado, por lo tanto, tiene su clase, que sería nivel de estrés, ya que con este, se sabe el nivel de estrés y se puede clasificar de manera finita, ya que sólo hay 5 niveles de estrés: , 1, 2, 3, 4. Y este ayudará al modelo a que sepa analizar y poder clasificar de manera eficiente el nivel de estrés de una persona.


**Complemente con lo siguiente:**

**a. Sin el uso de librerías en Python programe el percentil y cuartil de cada columna. Que distribución se puede aplicar en su caso normal, Bernoulli, gaussiana, poisson, otros. Indique la razón de su uso graficando con matplotlib.**
"""

from urllib.request import DataHandler
from google.colab import drive
drive.mount("/content/drive")
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('/content/drive/MyDrive/parcial1/nivelestres.csv')
mapa_genero = {'Male': 0, 'Female': 1}
if 'gender' in data.columns:
    data['gender'] = [mapa_genero[val] if val in mapa_genero else val for val in data['gender']]

# a. Sin el uso de librerías en Python programe el percentil y cuartil de cada columna.
#Que distribución se puede aplicar en su caso normal, Bernoulli, gaussiana, poisson, otros. Indique la razón de su uso graficando con matplotlib.
# Función para calcular el percentil de una lista de números

# Función para calcular el percentil manualmente
def calcular_percentil(lista, percentil):
    lista_ordenada = sorted(lista)
    k = (len(lista_ordenada) - 1) * percentil / 100
    f = int(k)
    c = f + 1 if f < len(lista_ordenada) - 1 else f
    if f == c:
        return lista_ordenada[int(k)]
    else:
        return lista_ordenada[f] + (k - f) * (lista_ordenada[c] - lista_ordenada[f])

# Función para calcular cuartiles manualmente
def calcular_cuartiles(lista):
    Q1 = calcular_percentil(lista, 25)
    Q2 = calcular_percentil(lista, 50)
    Q3 = calcular_percentil(lista, 75)
    return Q1, Q2, Q3

columnas_relevantes = ['sleeping hours', 'respiration rate', 'heart rate']
datos_relevantes = data[columnas_relevantes]
for columna in datos_relevantes.columns:
    valores = [x for x in data[columna] if pd.notnull(x)]
    Q1, Q2, Q3 = calcular_cuartiles(valores)
    print(f"Cuartiles de {columna} - Q1: {Q1}, Mediana: {Q2}, Q3: {Q3}")
    P10 = calcular_percentil(valores, 10)
    P90 = calcular_percentil(valores, 90)
    print(f"Percentil 10: {P10}, Percentil 90: {P90} \n")

for columna, valores in datos_relevantes.items():
    # Filtrar solo los valores numéricos para graficar histogramas
    valores_numericos = [v for v in valores if isinstance(v, (int, float))]

    # Crear un histograma
    if len(valores_numericos) > 0:
        plt.figure(figsize=(3, 2))
        plt.hist(valores_numericos, bins=10, edgecolor='black', alpha=0.7)
        plt.title(f'Distribución de la columna: {columna}')
        plt.xlabel(columna)
        plt.ylabel('Frecuencia')
        plt.show()
#Distribución Bernoulli: marital status, gender
#Distribución Poisson: snoring rate, eye movement, limb movement, stress level
#Distribución Normal: age, respiration rate, body temperature, blood oxygen, heart rate, bmi,
#Distribución Exponencial: sleeping hours

"""**b. De al menos tres columnas seleccionadas por usted indique que datos son relevantes de estas, grafique la misma (puede ser dispersión o mapa de calor, otros), indique al menos 4 características por columna seleccionada.**

1. Horas de sueño (sleeping hours):
El sueño juega un papel crucial en la regulación del estrés. Un menor número de horas de sueño se ha asociado con niveles más altos de cortisol (la hormona del estrés) y una mayor susceptibilidad a sufrir episodios de ansiedad o tensión. La falta de sueño impide que el cuerpo se recupere adecuadamente, afectando la capacidad de manejar situaciones estresantes. Y esta variable puede ser un fuerte predictor de niveles de estrés elevados o bajos, ya que existe una relación inversa entre la cantidad de horas de sueño y el nivel de estrés.
2. Frecuencia respiratoria (respiration rate):
La frecuencia respiratoria aumenta cuando una persona está estresada. Es una respuesta fisiológica directa del cuerpo ante situaciones de tensión o ansiedad.
La respiración rápida y superficial es un indicador de la activación del sistema nervioso simpático (la respuesta de “lucha o huida”), lo que es típico en estados de estrés agudo. Se espera que un aumento en la frecuencia respiratoria se correlacione con niveles más altos de estrés, lo que hace de esta variable un predictor clave.
3. Frecuencia cardiaca (heart rate):
La frecuencia cardíaca se eleva en respuesta a eventos estresantes. Un ritmo cardíaco acelerado indica que el cuerpo está en un estado de alerta o ansiedad. El corazón responde rápidamente a los niveles elevados de estrés al bombear más sangre para preparar al cuerpo para enfrentar una situación estresante. Un aumento en la frecuencia cardíaca puede ser un predictor directo de la presencia de estrés, especialmente si se observan picos anormales durante el sueño o en reposo.
"""

import seaborn as sns

# Seleccionar las columnas relevantes para la predicción del nivel de estrés
columnas_relevantes = ['sleeping hours', 'respiration rate', 'heart rate']
datos_relevantes = data[columnas_relevantes]

# Calcular la matriz de correlación entre las variables seleccionadas
matriz_correlacion = datos_relevantes.corr()

# Crear el mapa de calor
plt.figure(figsize=(8, 6))
sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Mapa de calor de correlación: Horas de sueño, Frecuencia Respiratoria, Frecuencia Cardiaca")
plt.show()

"""*Características de las tres columnas:*
1. Horas de Sueño (sleeping hours):
* La cantidad de horas que una persona duerme afecta directamente su bienestar general y niveles de estrés.
* Aunque el dataset mide solo horas, la calidad es un indicador indirecto que puede ser inferido del tiempo total de sueño.
* Si las horas de sueño están por debajo de cierto umbral (generalmente 7-8 horas), se pueden identificar posibles riesgos de estrés elevado.
* Cambios significativos en la cantidad de horas de sueño pueden indicar problemas de salud o estrés.

2. Frecuencia Respiratoria (respiration rate):
* La frecuencia respiratoria en reposo refleja el estado de relajación o estrés del cuerpo.
* La frecuencia respiratoria tiende a aumentar durante episodios de ansiedad o estrés.
* Un ritmo de respiración regular es indicador de una buena condición de salud, mientras que irregularidades podrían correlacionarse con estrés.
* Durante el sueño, la frecuencia respiratoria tiende a disminuir, y variaciones significativas pueden indicar niveles elevados de estrés.

3. Frecuencia Cardiaca (heart rate):
* Un ritmo cardíaco bajo en reposo indica un buen estado de salud, mientras que un ritmo elevado podría estar relacionado con ansiedad o estrés.
* La frecuencia cardíaca aumenta en situaciones de estrés o alerta, lo cual es un indicador fisiológico directo del estrés.
* Una alta variabilidad en la frecuencia cardíaca puede indicar problemas de salud o niveles de estrés inusualmente altos.
* La frecuencia cardíaca debería disminuir durante el sueño. Si esto no ocurre, puede ser un indicador de estrés o mala calidad del sueño.


**c. Obteniendo la media, mediana, moda con el uso de librerías, grafique un diagrama de cajas-bigote de al menos 3 columnas. Explique el resultado.**

*Sleeping Hours:*
Presenta varios valores atípicos (outliers) en el extremo inferior (personas con pocas horas de sueño). La caja está sesgada hacia abajo, indicando que la mayoría duerme pocas horas.

*Respiration Rate:*
La caja es simétrica, lo que sugiere una distribución normal de la frecuencia respiratoria. No se observan muchos outliers, indicando que los datos están en rangos típicos.

*Heart Rate:*
La distribución es más compacta con algunos outliers. La mediana es menor a la media, lo que podría indicar una ligera asimetría hacia valores altos.

*Resultado:*
El diagrama de cajas y las medidas centrales muestran que el sleeping hours tiene un comportamiento inusual, con muchos valores atípicos y una moda en 0. La frecuencia respiratoria y la frecuencia cardíaca están mejor distribuidas, con formas más típicas y menos valores extremos.
"""

#Calculamos las medidas de tendencia central (media, mediana, moda) para cada columna
medias = datos_relevantes.mean()
medianas = datos_relevantes.median()
modas = datos_relevantes.mode().iloc[0]

# Mostrar resultados
print("Medidas de Tendencia Central:")
print(f"Medias:\n{medias}\n")
print(f"Medianas:\n{medianas}\n")
print(f"Modas:\n{modas}\n")

# 4. Crear el diagrama de cajas (boxplot) para visualizar la distribución de las columnas seleccionadas
plt.figure(figsize=(5, 3))  # Tamaño de la figura
sns.boxplot(data=datos_relevantes)  # Crear el boxplot con seaborn
plt.title("Diagrama de Cajas-Bigote para Sleeping Hours, Respiration Rate y Heart Rate")
plt.ylabel('Valor')
plt.xlabel('Características')
plt.show()
