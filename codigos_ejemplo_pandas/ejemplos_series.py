import pandas as pd
import numpy as np

#Si data es un ndarray entonces el vector de índices debe tener
# la misma longitud que el array de entrada, si no dará error.
print("SERIE: ")
serie_1 = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
print(serie_1)

# El atributo index guarda el vector de etiquetas para cada
# valor de la serie
print("Index:")
print(serie_1.index)

print("Keys: ")
print(serie_1.keys())

# El vector de valores está en el atributo values
print("Values: ")
print(serie_1.values)

# Si no se proporciona un vector de índices, entonces se crea
# uno automáticamente con los índices numéricos
print("Serie 2:")
serie_2 = pd.Series(np.random.rand(5))
print(serie_2)

# Array vs serie: la serie permite definir índices de forma explícita
# y no tienen por qué ser consecutivos
print("Serie 3:")
serie_3 = pd.Series([0.25, 0.5, 0.75, 1.0], index=[2, 5, 3, 7])
print(serie_3)

print("Serie diccionario:")
# Definición de una serie a partir de un diccionario
d = {'a': 1., 'b': 2., 'c': 3.0, 'd': 4. }
print(pd.Series(d))

# Si data es un diccionario, entonces si pasamos un vector de
# índices se usará para tomar los elementos del diccionario de
# datos que se correspondan con las etiquetas proporcionadas,
# en el mismo orden que indique el vector de índices
# En caso de que algún índice no tenga valor, pondrá NaN
print("Serie diccionario con indices explícitos:")
print(pd.Series(d, index = ['e', 'd', 'c', 'f', 'b', 'a']))

#Serie a partir de un valor escalar
print("Serie con escalar:")
print(pd.Series(3.5, index=['a', 'b', 'c', 'd']))

# Finalmente, también podemos poner un nombre a la serie de valores
# y de índices con los argumentos name e index.name
serie_2.name = "Serie 2"
serie_2.index.name = "Ordinal"
print(serie_2)

"""
#Ejemplo suma series
serie_A = pd.Series({'a':0.1, 'c':0.3, 'd':0.5, 'f':0.7})
print(serie_A)
serie_B = pd.Series({'a':0.8, 'b':0.4, 'd':0.6, 'e':0.1})
print(serie_B)
print(serie_A + serie_B)
"""