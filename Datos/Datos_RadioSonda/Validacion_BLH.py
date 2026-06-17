# -*- coding: utf-8 -*-
"""
Created on Thu May 28 15:46:56 2026

@author: felip
"""

import pandas as pd

#%% Importamos datos y cortamos entre 2019 y 2023

# Fechas
d1 = pd.to_datetime('2022-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')

# Importamos datos de altura de capa límita por ERA5 en [-71.55,-32.83]
path = '/run/media/felipe/78C43BD9C43B9878/Users/felip/Desktop/U/Tesis/Datos/ERA5/'
ERA5 = pd.read_csv(path+'MET_ERA5.csv',index_col='date',parse_dates=True)
ERA5 = ERA5.shift(periods=-4,freq='h')# pasamos a UTC-4
ERA5 = ERA5.loc[d1:d2]
ERA5 = ERA5.iloc[1:len(ERA5.index)-1:2]

# Importamos datos de BLH con radiosonda
path = '/run/media/felipe/78C43BD9C43B9878/Users/felip/Desktop/U/Tesis/Datos/Datos_RadioSonda/' 
RS = pd.read_csv(path+'BLH.txt',index_col='date',parse_dates=True)
RS = RS[1:len(RS)]
RS.index = RS.index + pd.Timedelta(hours=-4)

#%% Creamos DF con datos de era y rs

BLH = pd.DataFrame(columns=['ERA5','RS'],index=RS.index)
BLH['ERA5'] = ERA5['blh']
BLH['RS'] = RS['BLH']

#%% Ploteamos 


# Fechas
d1 = pd.to_datetime('2022-03-01 00:00:00')
d2 = pd.to_datetime('2022-05-01 23:00:00')
BLH.loc[d1:d2].plot(figsize=(10,5), grid=True,lw=0,marker='.')
