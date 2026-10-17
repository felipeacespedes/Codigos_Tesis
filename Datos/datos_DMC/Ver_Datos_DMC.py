# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 19:09:34 2025

@author: felip
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Importamos datos

# Path 
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/datos_DMC/'

## freq
f = 'h'
# f = 'D'

#%% Temperatura
T = pd.read_csv(path+'T/temperatura_2019_2023.csv', sep=';', header = 0,
                usecols=[3,4,5], parse_dates=True, index_col='date',
                names = ['date','ts','td'])

T = T.loc[~T.index.duplicated(),:]
T = T.shift(periods=-4,freq='h')# pasamos a UTC-4
T = T.resample(f).mean()

#%% Presion y Humedad Relativa
HR_P = pd.read_csv(path+'HR_P/presion_humedadrelativa_2019_2023.csv', sep=';',
                    usecols=[3,4,5,8], parse_dates=True, index_col='date',
                    names = ['date','hr','p','slp'], header=0)



HR_P = HR_P.loc[~HR_P.index.duplicated(),:]
HR_P = HR_P.shift(periods=-4,freq='h')# pasamos a UTC-4

# filtro 5 std
for var in HR_P.columns:
    series = HR_P[var]
    
    # Compute mean and standard deviation
    mean = series.mean()
    std = series.std()
    
    # Define threshold (e.g., 3 standard deviations)
    threshold = 5
    
    # Find outliers
    zscore = (series - mean) / std
    outliers = np.abs(zscore) > threshold
    
    # Replace outliers with NaN
    HR_P.loc[outliers, var] = float('nan')




HR_P = HR_P.resample(f).mean()

#%%
yr = 22
d1 = pd.to_datetime(f'20{yr}-06-17 00:00:00')
d2 = pd.to_datetime(f'20{yr}-06-25 23:00:00')

HR_P.loc[d1:d2,['hr','p','slp']].plot(subplots=True,layout=(3,1),figsize=(10,5))
plt.tight_layout()


#%% Radiación
R = pd.read_csv(path+'R/radiacion_2019_2023.csv', sep=';', header=0,
                usecols=[3,4], parse_dates=True,index_col='date',
                names=['date','rg'])
R = R.loc[~R.index.duplicated(),:]
R = R.shift(periods=-4,freq='h')# pasamos a UTC-4
R = R.resample(f).mean()

#%%

d1 = pd.to_datetime('2022-09-08 22:00:00')
d2 = pd.to_datetime('2022-09-09 23:59:00')
R.loc[d1:d2,'rg'].plot(figsize=(10,5), grid=True,ylim=(-20,1100))
plt.tight_layout()


#%% Viento
V = pd.read_csv(path+'V/viento_2019_2023.csv', sep=';', header=0,
                usecols=[3,4,5], parse_dates=True, index_col='date',
                names = ['date','wd','ws'])
V = V.loc[~V.index.duplicated(),:]
V = V.shift(periods=-4,freq='h')# pasamos a UTC-4


# resampleamos dirección 
V_aux = V.copy()
V_aux['u'] = np.sin(np.deg2rad(V_aux['wd']))
V_aux['v'] = np.cos(np.deg2rad(V_aux['wd']))
V_aux = V_aux.resample(f).mean()

V_aux['rad'] = np.arctan2(V_aux['u'], V_aux['v'])
V_aux['deg'] = np.rad2deg(V_aux['rad']) % 360  # Wrap to 0–360°

# resampleamos 
V = V.resample(f).mean()
V['wd'] = V_aux['deg']

## U y V:
    
# Calculo en base a promedios horarios de wd (lo que hice originalmente)
V['u'] = (-1)*np.sin(np.deg2rad(V['wd']))*V['ws']/1.944
V['v'] = (-1)*np.cos(np.deg2rad(V['wd']))*V['ws']/1.944
V['ws'] = V['ws']/1.944



#%% Juntamos Datos 
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/datos_DMC/'
MET = pd.concat([V, T, HR_P, R], axis=1)
if f == 'h':
    MET.to_csv(path+'DMC_h.csv')
elif f == 'D':
    MET.to_csv(path+'DMC_d.csv')







#%% Codigo para cargar .pkl descargado con código import_dmc.py

# Path 
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Codes/'
DMC = pd.read_pickle(path+'DMC.pkl')
DMC.columns = ['date','ws', 'wd', 't', 'td','hr', 'p', 'mslp','r']
DMC = DMC.set_index(pd.to_datetime(DMC['date']))
DMC = DMC.drop(columns=['date'])
