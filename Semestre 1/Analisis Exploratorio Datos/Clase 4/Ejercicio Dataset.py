#1. Pregunta SMART
#Se trabaja con un dataset de Kaggle que reporta los gastos en medicinas per cápita anualmente por país
# ¿Cuál es el top 5 de los países con mayor gasto per cápita en medicinas desde el inicio del siglo?

#2. Importar las librerías

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

df_link = "D:\OneDrive - Tecnoquimicas\99. PERSONAL\Formación\Maestria\Semestre 1\Analisis Exploratorio Datos\Clase 4\Pharmaceutical Drug Spending by countries.csv"

df = pd.read_csv(df_link)