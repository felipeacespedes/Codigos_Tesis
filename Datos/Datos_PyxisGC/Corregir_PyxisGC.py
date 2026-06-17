# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 12:31:41 2024

Código para tratamiento de datos BTEX medidos por intrumentos PyxisGC.
Su LOD para Benceno es de <0,03 μg/m3 (0,01ppb). Esta red consiste en 
7 estaciones repartidas entre CQPV, que llevan midiendo desde el 26-03-2023.
"""
# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
from Corregir_PyxisGC_functs import Plot_per, Plot_dias, Plot_mes, Corr_ser\
                                    , LOD           
plt.style.use('bmh')
import pickle
# import numpy as np
# import datetime

#%%  Importamos datos
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_PyxisGC/'
est = ['PU_CESA','PU_FLR','QU_ERF','QU_CAQsb','QU_CQ','CC_JIC','CO_EPC']

# Creamos diccionario para rellenar con DFs originales
Py_og = {}


# Iteramos por nombre de estación
for file in est:
    print(file)
    globals()[f'{file}'] = pd.read_csv(path+file+'.csv', sep=';')
    globals()[f'{file}']['date'] = pd.to_datetime(globals()[f'{file}']\
                                                  ['Fecha'] + ' ' + globals()\
                                                      [f'{file}']['Hora'])
    globals()[f'{file}'] = globals()[f'{file}'].set_index('date')
    globals()[f'{file}'] = globals()[f'{file}'].drop(columns=\
                                    ['Fecha','Hora','Unnamed: 6'])
        
    # Quitamos el factor (ug/m3) de nombres de las columnas
    cols = globals()[f'{file}'].columns
    for c in cols: 
        globals()[f'{file}'] = globals()[f'{file}'].rename(columns={c:c[0:-7]})

    # Rellenamos diccionario
    Py_og[file] = globals()[f'{file}'].copy()

    # Borramos variable
    del globals()[f'{file}']
    
# Guardamos nombre de contaminantes
cont = Py_og['PU_CESA'].columns
    
del path, file, c, cols
#%% Agregar faltantes, quitar duplicados y crear copia para modificados

# Creamos serie de fechas a utilizar para el tratamiento de datos
Fi = Py_og['PU_FLR'].index[0]
Ff = Py_og['PU_FLR'].index[-1]
T = pd.date_range(Fi,Ff,freq='H')

# Cremaos diccionario para rellenar con dfs de mismas caracteristicas
# que originales, pero con valores Nan, para luego modiciar y aplicar LOD.
Py_ml = {}

# Iteramos por estaciones
for e in est:
    print(e+':')
    # Identificamos fechas faltantes
    faltantes = T.difference(Py_og[e].index)
    print('Faltantes: ')
    for f in faltantes: print(f)
    
    # Creamos df para fechas faltantes con indice datetime correspondiente
    faltantes_df = pd.DataFrame(index=faltantes, columns=Py_og[e].columns)

    # Concatenamos el df original con el nuevo y ordenamos
    Py_og[e] = pd.concat([Py_og[e], faltantes_df]).sort_index()
    
    # Identificamos duplicados
    duplicados = Py_og[e].index[Py_og[e].index.duplicated(keep='first')]
    print('Duplicados: ')
    for d in duplicados: print(d)
    
    # Quitamos y mantenemos el primero
    Py_og[e] = Py_og[e][~Py_og[e].index.duplicated(keep='first')]
    
    # Creamos copia pero con NAN
    Py_ml[e] = pd.DataFrame().reindex_like(Py_og[e])

del e, faltantes, faltantes_df, duplicados, Ff, Fi
#%% Convertir de ug/m3 a ppb

# Creamos DF con factores de conversión de ug/m3 a ppb
FC_uap = pd.DataFrame(index = Py_og['PU_CESA'].columns, columns=['factor'])
factor = [1/3.19, 1/4.34, 1/3.77, 1/4.34]; FC_uap.loc[:,'factor'] = factor
del factor

# Ahora iteramos por estación y por contaminante COV
for e in est:
    for c in cont:
        Py_og[e].loc[:,c] = Py_og[e].loc[:,c]*FC_uap.loc[c,'factor']
del e, c

# Guardamos archivo de datos originales en ppb
# OJO: que este es un diccionario con varios dataframesde estaciones
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_PyxisGC/'
with open(path+'Py_og_ppb.pkl', 'wb') as file:
    pickle.dump(Py_og, file)

#%% Creamos LOD para cada contaminante

# Creamos LOD en ppb por contaminante cómo columna de FC_uap
# ,sabiendo que el LOD es 0.03 ug/m3:
FC_uap['LOD'] = FC_uap['factor']*0.03

#%% Revisión por estación

# Se revisarán solo los datos de las estaciones que tienen una estación
# asociada (ubicación similar) en red SINCA.

# Estas son:
    #  SINCA   |   PyxisGC
    # --------------------
    #    VE    |   PU_FLR
    #    CQ    |   QU_CQ
    #    CC    |   CC_JIC
    #    CO    |   CO_EPC

#%% PU: Fundación Las Rosas

# Serie Original
FLR_og = Py_og['PU_FLR'].copy()

# Parametros
ymax=2

# Plotear periodo especifico
Plot_per('BETX', 'PU_FLR', FLR_og, FC_uap, T, '2023-04-01 00:00:00'
         , '2024-08-30 00:00:00', ymax, False, 'OG')

# Plotear n días desde fecha
# Plot_dias('BETX', 'PU_FLR', FLR_og, FC_uap, T, '2023-04-01', 1#+215
#           , ymax, False, 'OG')

# Plotear meses
# Plot_mes('BETX', 'PU_FLR', FLR_og, FC_uap, T, ymax, False, 'OG')

#%% modificamos

# [2023-12-20 - 2024-01-04]
FLR= Corr_ser('PU_FLR', FLR_og,'2023-12-20','12','2024-01-04','00')


#%% Revisamos corrección

# Parametros
ymax=2

# Plotear periodo especifico
Plot_per('BETX', 'PU_FLR', FLR, FC_uap, T, '2023-04-01 00:00:00'
         , '2024-08-30 00:00:00', ymax, False, 'OG')

# Plotear n días desde fecha
# Plot_dias('BETX', 'PU_FLR', FLR_og, FC_uap, T, '2023-04-01', 1#+215
#           , ymax, False, 'OG')

# Plotear meses
# Plot_mes('BETX', 'PU_FLR', FLR_og, FC_uap, T, ymax, False, 'OG')

#%% Aplicar LOD a serie y agregar a df 

# Aplicar LOD y agregar a df
Py_ml['Centro_Quintero'] = LOD(FLR,FC_uap)