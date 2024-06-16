#1. PREGUNTA SMART
#¿Cuáles son el top 5 de los países con más gasto per cápita en medicinas en los últimos 10 años según el % del total de gasto en salud?


# Importo las librerías requeridas
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

#3. Importo el dataset y analizo su estructura
ruta_archivo = "D:\OneDrive - Tecnoquimicas\99. PERSONAL\Formación\Maestria\Semestre 1\Analisis Exploratorio Datos\Clase 5\CATEGORIA_COMPRAS.csv"
ruta_archivo_2=
df = pd.read_csv(ruta_archivo)
df.head()
df.shape
df.info()

#3.1. Creo una lista para las etiquetas de columnas en español

headers = ['Pais', 'Año', '%GastoSalud','%PIB','PIBPC','CodigoPais', 'GastoTotal']
df.columns = headers
df.head(10)
#3.2. Resumen estádistico de las variables
df.describe()
plt.hist(df['Año'])

p