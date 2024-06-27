import csv
import numpy as np

def parametros_desde_csv(nombre_archivo):
    """Obtiene una tupla de tres vectores de numpy desde un archivo csv

    Dos vectores de igual longitud se leen del archivo 'csv' que corresponden
    a las coordenadas de 'x' e 'y' de una serie de puntos.
    Los puntos se ordenan automáticamente de manera creciente, y se genera
    un error si hay dos puntos repetidos.

    El tercer valor leído es una tupla de tres números que corresponden
    con dos valores extremos y una cuenta de valores de muestras 'x'
    para calcular las ordenadas respectivas de esos puntos para una función"""

    try:
        with open(nombre_archivo, newline="") as archivo:
            lector = iter(csv.reader(archivo))
            valores_x = np.array([float(x) for x in next(lector)])
            valores_y = np.array([float(x) for x in next(lector)])
            intervalo = (float(x) for x in next(lector))
    except OSError as e:
        raise type(e)("No se pudo leer el archivo") from e
    except StopIteration as e:
        raise ValueError("No hay suficientes datos en el archivo") from e

    if len(valores_x) != len(valores_y):
        raise ValueError("La cantidad de coordenadas 'x' e 'y' no coinciden")
    if len(intervalo) != 3:
        raise ValueError("El intervalo debe ser de tres valores")

    return (valores_x, valores_y, np.linspace(*intervalo))

def ordenar_por_iesimo(secuencias, indice):
    if indice < 0 and indice >= len(secuencias):
        raise IndexError("Índice fuera de rango (0:%d): %d"
                         % (len(secuencias), indice))

    referencia = secuencias[indice]
    largo = len(referencia)
    for i in range(largo - 1):
        valores = [secuencia[largo - 1] for secuencia in secuencias]
        comparado = valores[indice]
        for j in range(largo - 1, i, -1):
            for secuencia in secuencias:
                secuencia[j] = secuencia[j - 1]
            if comparado < referencia[j]:
                for k, secuencia in enumerate(secuencias):
                    secuencia[j - 1] = valores[k]

    pass  # Falta esto
            
