import pandas as pd
import numpy as np

# Definimos los datos de entrada de formas diferentes para ilustrar
# algunos de los posibles formatos admitidos

# En caso de introducir un solo valor para alguna columna, el valor
# se replica tantas veces como sea preciso para rellenar la columna
data_1 = {
    'year': [2010, 2011, 2012, 2013, 2014] * 2,
    'group': ['A'] * 5 + ['B'] * 5,
    'intake': (55.3, 55.4, 55.3, 55.5, 54.4, 56.6, 57.7, 55.4, 57.9, 56),
    'output': 1.1,
    'collate': np.array([15, 5, 10, 40, 20, 12, 12, 12, 12, 12]),
    'gender': "M"
}
df_1 = pd.DataFrame(data_1)

print("DF1:")
print(df_1)

print("Columnas DF1: ")
# Listado de columnas en el DataFrame
print(df_1.columns)

# Listado de índices de las filas
print(df_1.index)

# En caso de que haya columnas que no existan
# se rellena con marca de dato faltante 'NaN'
print("DF2: ")
df_2 = pd.DataFrame(df_1, columns=['collate', 'group', 'intake', 'genotype'])
print(df_2)

# A partir de una Serie
population_dict = {'California':36332521,'Texas':26448193,
                   'New York':19651127,'Florida':19552860,
                   'Illinois':12882135}
population = pd.Series(population_dict)
df_population = pd.DataFrame(population, columns=['population'])
print("DF a partir de una serie:")
print(df_population)

# A partir de dos Series, es decir, a partir de un diccionario de objetos Series
# Los datos faltantes siempre los marca como NaN
area_dict = {'California':423967,'Texas':695662,
             'New York':141297,'Illinois':149995}
area = pd.Series(area_dict)
df_states = pd.DataFrame({'population':population, 'area':area})
print("DF a partir de dos series:")
print(df_states)

# Array multidimensional de 3 filas y 2 columnas
print("Dataframe como contenedor de series:")
print(pd.DataFrame(np.random.rand(3,2), columns=['col1', 'col2'], index=['a', 'b', 'c']))