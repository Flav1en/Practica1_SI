import pandas as pd
import numpy as np

# Concatenación simple de Series con la función pd.concat()
ser_1 = pd.Series(['A','B','C'], index=[1,2,3])
ser_2 = pd.Series(['D','E','F'], index=[4,5,6])
print("SER_1")
print(ser_1)

print("SER_2")
print(ser_2)

print("Concat ser_1 y ser_2")
ser_1_2 = pd.concat([ser_1, ser_2])
print(ser_1_2)

# Concatenación simple de DataFrame con pd.concat()
dict_1 = {'A': ['A0', 'A1'],
     'B': ['B0', 'B1']}

df_1 = pd.DataFrame(dict_1)
print("DF_1")
print(df_1)

dict_2 = {'C': ['C0', 'C1'],
     'D': ['D0', 'D1']}
df_2 = pd.DataFrame(dict_2)
print("DF_2")
print(df_2)

# Concatenación con missing
print("Concatenación con valores chungos: ")
df_1_2 = pd.concat([df_1, df_2], axis=0)
print(df_1_2)
print("Concatenación SIN valores chungos: ")
df_1_2 = pd.concat([df_1, df_2], axis=1)
print(df_1_2)

# Ejemplo de pd.merge() con dos DataFrame
dict_1 = {'empleado': ['Ana', 'Juan', 'María', 'Carlos'],
       'dpto.': ['Contabilidad', 'RRHH', 'Marketing', 'RRHH']}
df_1 = pd.DataFrame(dict_1)
dict_2 = {'empleado': ['Ana', 'Juan', 'María', 'Carlos'],
       'ext.': [6895, 6745, 6855, 6746]}
df_2 = pd.DataFrame(dict_2)
df_1_2 = pd.merge(df_1, df_2)
print("Opearción de MERGE: ")
print(df_1_2)

# Ejemplo de join() con dos DataFrame
dict_1 = {'dpto.': ['Contabilidad', 'RRHH', 'Marketing', 'RRHH']}
dict_2 = {'ext.': [6895, 6745, 6855, 6746]}
df_1 = pd.DataFrame(dict_1, index=['Ana', 'Juan', 'María', 'Carlos'])
df_2 = pd.DataFrame(dict_2, index=['Ana', 'Juan', 'María', 'Carlos'])
print("Opearción de JOIN: ")
print(df_1.join(df_2))