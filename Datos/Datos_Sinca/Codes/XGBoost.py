# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 18:56:59 2023

@author: felip

Código para utilizar la librería xgboost con el fin de entrenar un algoritmo 
para corregir las series de tiempo de sinca, se quiere entrenar el algoritmo 
con series desde el 2019 al 2022, para agarrar ciclos estacionales, y entregar
indices de horas, semana y días del año
"""

import xgboost as xgb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from import_var import import_var
from sklearn.metrics import mean_squared_error
import seaborn as sns
color_pal = sns.color_palette()
plt.style.use('fivethirtyeight')
from sklearn.model_selection import TimeSeriesSplit


#%% Cargamos series de HCNM para 9 estaciones de red SINCA

# Diccionario
Dic = {}

Dic['Estaciones'] = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura','Sur' \
              ,'Junta_Vecinos','Concón','Gaviotas','Colmo']

    
Dic['Variables_Cont'] = ['SO2','CH4','HCNM','HCT','CO']

Dic['Unidades_Cont'] = ['ppb','ppm','ppm','ppm','ppm']

Dic['Variables_Meteo'] = ['Velocidad','Dirección']

Dic['Unidades_Meteo'] = ['m/s','°']

# Fechas
# Fi = '2018-01-01'
# Ff = '2023-07-31'
Fi = '2019-01-01'
Ff = '2022-12-31'

# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

# importamos HCNM entre 27/09/22 y 23/11/22
HCNM = pd.DataFrame({'T':T})
HCNM = HCNM.set_index('T')
for est in Dic['Estaciones']:
    HCNM[est] = import_var(est,'Cont','HCNM',Fi,Ff)
    
# we´ll also add a hour of day, day of week and day of year index to 
# notice any kind of weekly cycle

# h = pd.date_range('', '2017-01-08', freq='D').to_series()
# HCNM['hour'] = h.dt.dayofweek

# maybe is not necessary


#%% Ploteamos 
 
HCNM['Ventanas'].plot(figsize=(15,5),style='.')
HCNM['Ventanas'].plot(figsize=(15,5),kind='hist',bins=500)

# usaremos desde 2019

# chequeamos que no hayan outliers, para eso vemos qué datos se encuentran 
# bajo los 0.1 ppm

qu = HCNM.query('Ventanas < 0.1')

qu['Ventanas'].plot(figsize=(15,5),style='.')
qu['Ventanas'].plot(figsize=(15,5),kind='hist',bins=500)

# vamos a suponer que no pueden haber datos menores a 0.1
# pero debemos conferir esto con rodrigo

# así vamos a sacar los datos bajo los 0.1 ppm 
HCNM_01 = HCNM.query('Ventanas < 0.1').copy()
HCNM_01 = HCNM_01['Ventanas']

HCNM_01.plot(figsize=(15,5),style='.')
HCNM_01.plot(figsize=(15,5),kind='hist',bins=500)
#%% Ahora usamos time series split para hacer validación cruzada

# Para entrenar el algoritmo vamos a usar la fucnión timeseriessplit
# para decirle el tamaño de la muestra de entrenamiento y la cantidad
# de separaciones (splits)

tss = TimeSeriesSplit(n_splits=5, test_size=24*365*1, gap=24)

# nos aseguyramos de que el indice del data frame son las fechas en su orden
HCNM_01 = HCNM_01.sort_index()

#%%

# Intentamos trabajar con analisis armonico pero la verdad la resolusión de 
# es demasiado alta, asi que usaremos fft, debería ser lo mismo ??

#%% FFT para ver el espectro

# esto lo haremos en la serie sin aplicar el query, os ea que tenga todos los
# datos sin filtrar para dtos debajo del LOD 


from scipy.fft import fft, fftfreq

# Number of samples in normalized_tone
# sample rate in hz: 
SAMPLE_RATE = 1/3600 #Hz
DURATION = 60*60*24*365*4  # Segundos
N = int(SAMPLE_RATE * DURATION+24)

yf = fft(np.array(HCNM['Ventanas']))
xf = np.fft.fftfreq(len(HCNM['Ventanas']))#fftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()


#%% Probamos con librería StatsModels

# importamos librería y aplicamos código de artículo:
# https://medium.com/@khairulomar/deconstructing-time-series-using-fourier-transform-e52dd535a44e

from statsmodels.tsa.seasonal import seasonal_decompose
# reempalzamos Nans con media de HCNM['Ventanas']
data = HCNM['Ventanas'].replace(np.nan,HCNM['Ventanas'].mean())

# data = HCNM['Ventanas']
decomposition = seasonal_decompose(data, model='multiplicative')
trend    = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

trend.plot(figsize=(15,5))
seasonal.plot(figsize=(15,5))
residual.plot(figsize=(15,5))

# tira el error "This function does not handle missing values"
# chequeamos si tiene Nans, en caso de que si tenga debemos rellearn con 
# promedio de hora y día según ciclo estacional horario

# np.isnan(data)
# np.nansum(data)

np.count_nonzero(~np.isnan(HCNM['Ventanas']))

#%%
# reemplazamos Nans con promedio de serie
# for i in range(len(HCNM['Ventanas'])):
#     if np.isnan(HCNM['Ventanas'][i]) == True:
#             HCNM['Ventanas'][i] = np.mean(HCNM['Ventanas'])

#%% Rellenamos Nans con el promedio de la serie por ahora usando pandas

data = HCNM['Ventanas'].replace(np.nan,HCNM['Ventanas'].mean())
np.count_nonzero(np.isnan(data))


# HCNM = 

