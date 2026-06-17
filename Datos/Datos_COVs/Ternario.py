# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 09:24:42 2024

@author: felip

Código para plotear graficos ternarios acorde a concentraciones relativas 
entre Etilbenceno-Tolueno-Xilenos
"""

# Librerías

import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
import numpy as np
from Ternario_functs import COV_TimeSeries, COV_Ternary_tod\
    , COV_Ternary_wd, COV_Ternary_LongPeriod_tod\
    , COV_Ternary_ColoredPeriods


#%% Importamos datos

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
# file = 'datos_ver/ver_data_1min.csv'; freq = '1m'
# file = 'datos_inv/inv_data_1min.csv'; freq = '1m'
file = 'datos_inv/inv_data_5min.csv'; freq = '5m'

COV = pd.read_csv(path+file,delimiter=';')
COV['date'] = pd.to_datetime(COV['date'],format='%d/%m/%Y %H:%M:%S')
COV['date'] = pd.to_datetime(COV['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV = COV.set_index('date')

#%% Planificación

# La idea es plotear fechas en específico. Las fechas relevantes dentro
# de el periodo de interés (27/08/22 al 23/11/22) son:
    # - 31/08/22
    # - 02/09/22
    
#%% Ploteamos los 2 días de interés

# n debe ser de acuerdo a cuandos periodos se logran aclanzar de 30 minutos!

#%% Ploteamos 31/08/22
Fi = '2022-08-31 06:00:00'
Ff = '2022-08-31 10:00:00'
vmin = 6; vmax = 10; n = 4
# COV_TimeSeries(COV, Fi, Ff)
COV_Ternary_tod(COV, Fi, Ff, vmin, vmax, n, '1m',True)
# COV_Ternary_wd(COV, Fi, Ff)

#%% Ploteamos 02/09/22
Fi = '2022-09-02 08:00:00'
Ff = '2022-09-02 12:00:00'
vmin = 8; vmax = 12; n = 8
COV_TimeSeries(COV, Fi, Ff)
COV_Ternary_tod(COV, Fi, Ff, vmin, vmax, n, '1m')
# COV_Ternary_wd(COV, Fi, Ff)

#%% Ploteamos días enteros  

# 31/08 todo el día 
Fi = '2022-08-31 00:00:00'
Ff = '2022-08-31 23:59:00'
vmin = 0; vmax = 23; n = 23
COV_TimeSeries(COV, Fi, Ff)
COV_Ternary_tod(COV, Fi, Ff, vmin, vmax, n, '1m')

# 02/09 todo el día 
Fi = '2022-09-02 00:00:00'
Ff = '2022-09-02 23:59:00'
vmin = 0; vmax = 23; n = 23
COV_TimeSeries(COV, Fi, Ff)
COV_Ternary_tod(COV, Fi, Ff, vmin, vmax, n, '1m')


#%% Ploteamos periodo completo marcando hora del día 

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
file = 'voc_min_UTC_4.csv'; freq = '1m'
# file = 'voc_5min_UTC_meteo.csv'; freq = '5m'

COV = pd.read_csv(path+file,delimiter=';')
COV['date'] = pd.to_datetime(COV['date'],format='%d/%m/%Y %H:%M:%S')
COV['date'] = pd.to_datetime(COV['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV = COV.set_index('date')


# Definimos fechas de inicio y fin
Fi = '2022-08-27 00:06:00'
Ff = '2022-09-23 00:00:00'
COV_Ternary_LongPeriod_tod( COV, Fi, Ff, freq)

#%% Ploteamos periodo completo marcando episodios de contamiación

# Definimos periodos a plotear en color

# invierno:
# Fi = ['2022-08-31 06:00:00','2022-09-02 08:00:00']
# Ff = ['2022-08-31 10:00:00','2022-09-02 12:00:00']
# Fi = ['2022-09-12 04:00:00','2022-10-04 02:00:00','2022-10-04 20:00:00']
# Ff = ['2022-09-12 10:00:00','2022-10-04 10:00:00','2022-10-05 04:00:00']
# Fi = ['2022-09-12 04:00:00']
# Ff = ['2022-09-12 10:00:00']
# Fi = ['2022-10-04 05:00:00']
# Ff = ['2022-10-04 08:00:00']
Fi = ['2022-10-04 20:00:00']
Ff = ['2022-10-05 04:00:00']
COV_Ternary_ColoredPeriods( COV, Fi, Ff, freq, True )

# verano 
# Fi = ['2022-01-11 07:00:00']#,'2022-01-18 21:00:00']
# Ff = ['2022-01-11 08:00:00']#,'2022-01-19 09:00:00']
# # Fi = ['2022-01-21 23:00:00']
# # Ff = ['2022-01-22 08:30:00']
# COV_Ternary_ColoredPeriods( COV, Fi, Ff, freq, True)

#%% Leemos los datos del csv NILU

# importamos 
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
NILU = pd.read_csv(path+'Tabla_NILU_BTEX_2.csv',delimiter=';')

NILU['mop-xylenes'] = NILU['mp-xylene']+NILU['o-xylene']

NILU.head()

ax1 = NILU[['benzene','toluene','ethylbenzene','mop-xylenes']]\
    .plot(xticks=NILU.index, rot=45, figsize=(13,7), ylabel='ng/m3'\
          ,xlabel='Lugar', lw=0, marker='o'\
          ,title='Valores de BTEXs por lugar en informe NILU')
ax1.set_xticklabels(NILU.place,size=10)
ax1.grid()
plt.tight_layout()

NILU['E/E+Xs'] = NILU['ethylbenzene']/(NILU['ethylbenzene']+NILU['mop-xylenes'])
NILU['T/B'] = NILU['toluene']/NILU['benzene']

ax1 = NILU['T/B'].plot(xticks=NILU.index, rot=45, figsize=(13,7), ylabel='ng/m3'\
          ,xlabel='Lugar', lw=0, marker='o'\
          ,title='Valores de T/B por lugar en informe NILU')
ax1.set_xticklabels(NILU.place,size=10)
ax1.grid()
plt.tight_layout()

#%% Se toman los valores simliares a 8A y 9A

lug_sim = ['1A','2A','3A','4A','6A','7A','8A','9A','15A','16A']

razon_E = []

for i in NILU.index:
    if NILU.iloc[i,3] in lug_sim:
        print(NILU.iloc[i,3])
        print(NILU.iloc[i,13])
        razon_E.append(NILU.iloc[i,13])
        
print(np.mean(razon_E)) # 0.15896128445225186
print(np.std())
#%% Episodio 21/01/2022

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_ver/'
file = 'voc_min_UTC_4.csv'; freq = '1m'

COV = pd.read_csv(path+file,delimiter=';')
COV['date'] = pd.to_datetime(COV['date'],format='%d/%m/%Y %H:%M:%S')
COV['date'] = pd.to_datetime(COV['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV = COV.set_index('date')


Fi = ['2022-01-21 22:45:00','2022-01-22 03:00:00','2022-01-22 06:30:00']
Ff = ['2022-01-22 01:45:00','2022-01-22 05:00:00','2022-01-22 08:30:00']

COV_Ternary_ColoredPeriods( COV, Fi, Ff, freq, False)

#%% Ver si se puede plotear peaks de campaña con tod y wd

# Creamos lista de peaks de interés en campaña
Pi = ['2022-09-12 04:00:00', '2022-10-04 05:00:00', '2022-10-04 20:00:00'\
      ,'2022-10-12 23:00:00','2022-10-23 20:00:00','2022-10-31 21:00:00']
Pf = ['2022-09-12 10:00:00', '2022-10-04 08:00:00', '2022-10-05 04:00:00'\
      ,'2022-10-13 09:00:00','2022-10-24 09:00:00','2022-11-01 09:00:00']


dire= 'C:/Users/felip/Desktop/Avances/8/Linea_Central_Tesis/'

### TOD y Wd ###
for i in range(len(Pi)):
    COV_TimeSeries(COV, Pi[i], Pf[i],dire+'TS/',str(i))
    # COV_Ternary_tod(COV, Pi[i], Pf[i], '5min', dire+'TOD/', str(i)+'_tod')
    # COV_Ternary_wd(COV, Pi[i], Pf[i], dire+'Wd/', str(i)+'_wd')




