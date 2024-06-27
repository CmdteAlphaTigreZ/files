from csv_es import *
from trazadores import *
from aproximantes import *
from sistema_ec_lineales import *
import matplotlib.pyplot as plt
import numpy as np

def graficar(puntos_x, puntos_y, muestras_x, muestras_y):
    plt.clf()
    plt.plot(puntos_x, puntos_y, "or", label="Puntos")
    plt.plot(muestras_x, muestras_y, "b", label="Función")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()

def main():
    print("Presione 'Enter' para seleccionar el valor predefinido.\n")
    
    nombre_archivo = input(
        "Indique el nombre de archivo para los trazadores (trazador.csv): ")
    if nombre_archivo == "":
        nombre_archivo = "trazador.csv"

    puntos_x, puntos_y, muestras_x = parametros_desde_csv(nombre_archivo)
    trazador = generar_trazador_cubico_sujeto_simbolico(puntos_x, puntos_y)
    muestras_y = np.array([trazador(x) for x in muestras_x])
    graficar(puntos_x, puntos_y, muestras_x, muestras_y)
    input("Presione 'Enter' para continuar...")

    nombre_archivo = input(
        "Indique el nombre de archivo para los aproximantes (aproximante.csv): ")
    if nombre_archivo == "":
        nombre_archivo = "aproximante.csv"

    puntos_x, puntos_y, muestras_x = parametros_desde_csv(nombre_archivo)
