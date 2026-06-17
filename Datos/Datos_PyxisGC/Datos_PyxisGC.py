# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:36:37 2024

@author: felip

Código para tratamiento y visualización de datos BTEX medidos por intrumentos
PyxisGC. Su LOD para Benceno es de <0,03 μg/m3 (0,01ppb). Esta red consiste en 
7 estaciones repartidas entre CQPV, que llevan midiendo desde el 26-03-2023.
"""
# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt

#%%  Importamos datos
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_PyxisGC/'
names = ['PU_CESA','PU_FLR','QU_ERF','QU_CAQsb','QU_CQ','CC_JIC','CO_EPC']
var_names = {'Benzene(ug/m3)': 'Benzene', 'Ethylbenzene(ug/m3)': 'Ethylbenzene',
             'Toluene(ug/m3)':'Toluene','Xilenos(ug/m3)':'Xilenos'}

for file in names:
    print(file)
    globals()[f'{file}'] = pd.read_csv(path+file+'.csv', sep=';')
    globals()[f'{file}']['date'] = pd.to_datetime(globals()[f'{file}']\
                                                  ['Fecha'] + ' ' + globals()\
                                                      [f'{file}']['Hora'])
    globals()[f'{file}'] = globals()[f'{file}'].set_index('date')
    globals()[f'{file}'] = globals()[f'{file}'].drop(columns=\
                                    ['Fecha','Hora','Unnamed: 6'])
    globals()[f'{file}'] = globals()[f'{file}'].rename(columns=var_names)
        
del file

#%% Creamos DF con razones T/B para todas las estaciones

B_df = pd.DataFrame(index = PU_CESA.index, columns = names)
T_df = pd.DataFrame(index = PU_CESA.index, columns = names)
E_df = pd.DataFrame(index = PU_CESA.index, columns = names)
X_df = pd.DataFrame(index = PU_CESA.index, columns = names)
TB_df = pd.DataFrame(index = PU_CESA.index, columns = names)
EX_df = pd.DataFrame(index = PU_CESA.index, columns = names)
for col in names:
    TB_df[col] = globals()[f'{col}']['Toluene']/globals()[f'{col}']['Benzene']
    EX_df[col] = globals()[f'{col}']['Ethylbenzene']/globals()[f'{col}']['Xilenos']
    B_df[col] = globals()[f'{col}']['Benzene']
    E_df[col] = globals()[f'{col}']['Ethylbenzene']
    T_df[col] = globals()[f'{col}']['Toluene']
    X_df[col] = globals()[f'{col}']['Xilenos']
del col
#%% Ploteamos razones TB

date_1 = pd.to_datetime('2023-05-01 00:00:00')
date_2 = pd.to_datetime('2023-06-01 00:00:00')

ax = TB_df.loc[date_1:date_2,:].plot(subplots=True, layout=(7,1)\
                                    , grid=True, figsize=(30,15),ylim=(-1,20))
plt.tight_layout()

#%% Ploteamos razones EX

date_1 = pd.to_datetime('2023-04-25 00:00:00')
date_2 = pd.to_datetime('2023-05-05 00:00:00')

ax = EX_df.loc[date_1:date_2,:].plot(subplots=True, layout=(7,1)\
                                    , grid=True, figsize=(10,15),ylim=(-1,20))
plt.tight_layout()

#%% Ploteamos variable

date_1 = pd.to_datetime('2023-05-23 00:00:00')
date_2 = pd.to_datetime('2023-05-23 23:00:00')

ax = X_df.loc[date_1:date_2,:].plot(subplots=True, layout=(7,1)\
                                    , grid=True, figsize=(10,15),ylim=(-1,50))
plt.tight_layout()

#%% Ploteamos estación

date_1 = pd.to_datetime('2024-08-01 00:00:00')
date_2 = pd.to_datetime('2024-08-30 00:00:00')

ax = QU_CQ.loc[date_1:date_2,:].plot(subplots=True, layout=(4,1)\
                                    , grid=True, figsize=(30,15),ylim=(-1,150))
plt.tight_layout()


