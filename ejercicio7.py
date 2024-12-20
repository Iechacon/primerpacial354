# -*- coding: utf-8 -*-
"""ejercicio7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eKjc1j4DMqGl-uFaWziJolk5K2kWbBrt
"""
####################################################33
#a. Con DEAP
pip install deap


from deap import base, creator, tools, algorithms
import random

# Definir la estructura del problema de maximización del fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Configurar el toolbox
toolbox = base.Toolbox()

# Atributos y población
toolbox.register("attr_int", random.randint, 0, 1)  # Atributo para crear bits (0 y 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=8)  # Crear individuos de 8 bits
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Función de evaluación
def funcion_evaluacion(individual):
    # Convertir de binario a decimal
    decimal_value = int("".join(map(str, individual)), 2)
    try:
        return (decimal_value ** (2 * decimal_value) - 1.0),
    except OverflowError:
        return float('-inf'),

toolbox.register("evaluate", funcion_evaluacion)

# Definir operadores genéticos personalizados (cruce en un punto específico y mutación en un bit específico)
def custom_crossover(ind1, ind2, punto_de_cruce):
    """
    Realiza cruce en un punto específico.
    """
    # Realizar el cruce en el punto especificado
    ind1[punto_de_cruce:], ind2[punto_de_cruce:] = ind2[punto_de_cruce:], ind1[punto_de_cruce:]
    return ind1, ind2

def custom_mutation(individual, indice_mutacion):
    """
    Realiza la mutación en un bit específico.
    """
    # Invertir el bit en el índice especificado
    individual[indice_mutacion] = 1 - individual[indice_mutacion]
    return individual,

# Registrar operadores personalizados en el toolbox
toolbox.register("mate", custom_crossover, punto_de_cruce=3)  # Cruzar en el tercer índice
toolbox.register("mutate", custom_mutation, indice_mutacion=4)  # Mutar en el cuarto índice
toolbox.register("select", tools.selTournament, tournsize=3)

# Crear la población inicial
poblacion_inicial = toolbox.population(n=12)

# Algoritmo evolutivo con operadores específicos para cada generación
NGEN = 3  # Número de generaciones

# Definir diferentes puntos de cruce y mutación para cada generación
puntos_de_cruce = [3, 4, 2]  # Puntos de cruce por generación
puntos_de_mutacion = [4, 6, 5]  # Puntos de mutación por generación

for gen in range(NGEN):
    print(f"\n--- Generación {gen + 1} ---")
    
    # Cambiar el punto de cruce y mutación para esta generación
    toolbox.unregister("mate")
    toolbox.unregister("mutate")
    toolbox.register("mate", custom_crossover, punto_de_cruce=puntos_de_cruce[gen])
    toolbox.register("mutate", custom_mutation, indice_mutacion=puntos_de_mutacion[gen])
    
    # Evaluar la población actual
    fitnesses = list(map(toolbox.evaluate, poblacion_inicial))
    for ind, fit in zip(poblacion_inicial, fitnesses):
        ind.fitness.values = fit

    # Selección de la próxima generación
    offspring = toolbox.select(poblacion_inicial, len(poblacion_inicial))
    offspring = list(map(toolbox.clone, offspring))

    # Aplicar cruzamiento y mutación según las probabilidades
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.5:  # Probabilidad de cruce 50%
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < 0.2:  # Probabilidad de mutación 20%
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Evaluar individuos con fitness no calculado
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Reemplazar la población actual por la descendencia
    poblacion_inicial[:] = offspring

    # Mostrar resultados de la generación actual
    print(f"Evaluaciones: {[ind.fitness.values[0] for ind in poblacion_inicial]}")
    print(f"Individuos: {[int(''.join(map(str, ind)), 2) for ind in poblacion_inicial]}")


#########################################################################
#b. Sin DEAP
# Definir la población inicial según la imagen proporcionada
poblacion_inicial = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

# Definir la función de evaluación f(x) = x^(2x) - 1
def funcion_evaluacion(x):
    try:
        return x ** (2 * x) - 1
    except OverflowError:  # Controlar errores por valores grandes
        return float('inf')

# Función para realizar cruce de individuos en un punto específico
def realizar_cruce(poblacion, punto_de_cruce):
    poblacion_cruzada = []
    for i in range(0, len(poblacion), 2):  # Iterar en pares
        padre1 = poblacion[i]
        padre2 = poblacion[i + 1] if i + 1 < len(poblacion) else poblacion[0]  # Evitar out of range
        # Realizar el cruce en el punto especificado
        hijo1 = padre1[:punto_de_cruce] + padre2[punto_de_cruce:]
        hijo2 = padre2[:punto_de_cruce] + padre1[punto_de_cruce:]
        poblacion_cruzada.extend([hijo1, hijo2])
    return poblacion_cruzada

# Función para realizar mutación en un punto específico
def realizar_mutacion(poblacion, indice_mutacion):
    poblacion_mutada = []
    for individuo in poblacion:
        lista_bits = list(individuo)
        # Mutar el bit en el índice especificado
        lista_bits[indice_mutacion] = '1' if lista_bits[indice_mutacion] == '0' else '0'
        poblacion_mutada.append(''.join(lista_bits))
    return poblacion_mutada

# Primera Generación
# Paso 1: Evaluar la función para cada valor de la población inicial
evaluaciones_gen1 = [funcion_evaluacion(x) for x in poblacion_inicial]

# Paso 2: Convertir cada valor de la población a su representación binaria de 8 bits
fenotipos_gen1 = [format(x, '08b') for x in poblacion_inicial]

# Paso 3: Realizar cruce y mutación para la primera generación (Punto de cruce: 3, Mutación: 4to bit)
cruce_gen1 = realizar_cruce(fenotipos_gen1, punto_de_cruce=3)
mutacion_gen1 = realizar_mutacion(cruce_gen1, indice_mutacion=3)
poblacion_final_gen1 = [int(ind, 2) for ind in mutacion_gen1]

# Segunda Generación (Usar la población final de la 1ra generación)
evaluaciones_gen2 = [funcion_evaluacion(x) for x in poblacion_final_gen1]
fenotipos_gen2 = [format(x, '08b') for x in poblacion_final_gen1]
# Realizar cruce y mutación para la segunda generación (Punto de cruce: 4, Mutación: 6to bit)
cruce_gen2 = realizar_cruce(fenotipos_gen2, punto_de_cruce=4)
mutacion_gen2 = realizar_mutacion(cruce_gen2, indice_mutacion=5)
poblacion_final_gen2 = [int(ind, 2) for ind in mutacion_gen2]

# Tercera Generación (Usar la población final de la 2da generación)
evaluaciones_gen3 = [funcion_evaluacion(x) for x in poblacion_final_gen2]
fenotipos_gen3 = [format(x, '08b') for x in poblacion_final_gen2]
# Realizar cruce y mutación para la tercera generación (Punto de cruce: 2, Mutación: 5to bit)
cruce_gen3 = realizar_cruce(fenotipos_gen3, punto_de_cruce=2)
mutacion_gen3 = realizar_mutacion(cruce_gen3, indice_mutacion=4)
poblacion_final_gen3 = [int(ind, 2) for ind in mutacion_gen3]

# Mostrar los resultados de cada generación
import pandas as pd

# Crear DataFrames para cada generación
df_gen1 = pd.DataFrame({
    'Poblacion Inicial': poblacion_inicial,
    'f(x)': evaluaciones_gen1,
    'Fenotipo (Binario)': fenotipos_gen1,
    'Cruce': cruce_gen1,
    'Mutacion': mutacion_gen1,
    'Poblacion Final (Decimal)': poblacion_final_gen1
})

df_gen2 = pd.DataFrame({
    'Poblacion Inicial': poblacion_final_gen1,
    'f(x)': evaluaciones_gen2,
    'Fenotipo (Binario)': fenotipos_gen2,
    'Cruce': cruce_gen2,
    'Mutacion': mutacion_gen2,
    'Poblacion Final (Decimal)': poblacion_final_gen2
})

df_gen3 = pd.DataFrame({
    'Poblacion Inicial': poblacion_final_gen2,
    'f(x)': evaluaciones_gen3,
    'Fenotipo (Binario)': fenotipos_gen3,
    'Cruce': cruce_gen3,
    'Mutacion': mutacion_gen3,
    'Poblacion Final (Decimal)': poblacion_final_gen3
})

print("Generacion 1:")
print(df_gen1)
print("\nGeneracion 2:")
print(df_gen2)
print("\nGeneracion 3:")
print(df_gen3)
