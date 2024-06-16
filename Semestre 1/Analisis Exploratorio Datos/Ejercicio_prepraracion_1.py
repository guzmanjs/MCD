

#Importar librerias necesarias

import pandas as pd
import matplotlib as plot
import numpy as np


#Cargar el archivo

filename = "https://raw.githubusercontent.com/lvmeninnovations/datasets/main/crispdm/auto.csv"

# Lista de encabezados o nombres de los atributos
headers = ["factor-riesgo","perdida-promedio-anual","fabricante","tipo-combustible","aspiracion", "num-puertas","estilo-carroceria",
         "traccion","ubicacion-motor","distancia-entre-ejes", "longitud","anchura","altura","peso-vacio","tipo-motor",
         "num-cilindros", "tamano-motor","sistema-combustible","calibre","carrera","relacion-compresion","caballos-fuerza",
         "pico-rpm","millas_por_galon_ciudad","millas_por_galon_carretera","precio"]

# Leer el archivo CSV

df = pd.read_csv(filename, names = headers)

#Entender la estructura del dataset
df.info()

# Para ver cómo luce el dataset, utilizamos el método head().
df.head()

#Reemplazar ? por NaN
df.replace('?', np.nan, inplace=True)

df.head()


