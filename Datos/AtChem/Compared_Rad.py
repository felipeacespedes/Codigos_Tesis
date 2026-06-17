# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 15:23:47 2025

@author: felip
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Importamos datos

# Path 
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/datos_DMC/'


#%% Radiación
R = pd.read_csv(path+'R/radiacion_2019_2023.csv', sep=';', header=0,
                usecols=[3,4], parse_dates=True,index_col='date',
                names=['date','rg'])
R = R.loc[~R.index.duplicated(),:]
R = R.shift(periods=-4,freq='h')# pasamos a UTC-4

R_m = R.resample('min').asfreq().interpolate(method='akima')

# R = R.resample('h').mean()

#############
#%% 12-09 ###

#%% Día nublado: 12-09

d1 = pd.to_datetime('2022-09-11 22:00:00')
d2 = pd.to_datetime('2022-09-12 23:59:00')
R_m.loc[d1:d2,'rg'].plot(figsize=(10,5), grid=True,ylim=(-20,1100))
plt.tight_layout()


#%% Día despejado: 09-09

d1 = pd.to_datetime('2022-09-08 22:00:00')
d2 = pd.to_datetime('2022-09-09 23:59:00')
R_m.loc[d1:d2,'rg'].plot(figsize=(10,5), grid=True,ylim=(-20,1100))
plt.tight_layout()


#%% Dividimos

# df diferencias
d1 = pd.to_datetime('2022-09-11 22:00:00')
d2 = pd.to_datetime('2022-09-12 23:59:00')
R_diff = pd.DataFrame(index=pd.date_range(d1,d2,freq='min'))

# R cloudy
d1 = pd.to_datetime('2022-09-11 22:00:00')
d2 = pd.to_datetime('2022-09-12 23:59:00')
R_diff['rc'] = R_m.loc[d1:d2,'rg'].values+1

# R sunny
d1 = pd.to_datetime('2022-09-08 22:00:00')
d2 = pd.to_datetime('2022-09-09 23:59:00')
R_diff['rs'] = R_m.loc[d1:d2,'rg'].rolling(window=30,center=True).mean().values+1


# R division
R_diff['rd'] = R_diff['rc']/R_diff['rs']
R_diff[['rc','rs']] = R_diff[['rc','rs']]-1

#%% Ploteamos división subplot

R_diff.plot(figsize=(10,10), grid=True,subplots=True)
plt.tight_layout()

#%% Ploteamos división mismo plot

R_diff[['rc','rs']].plot(figsize=(10,10), grid=True)
plt.tight_layout()

#############
#%% 04-10 ###

#%% Día nublado: 04-10

d1 = pd.to_datetime('2022-10-04 22:00:00')
d2 = pd.to_datetime('2022-10-03 23:59:00')
R_m.loc[d1:d2,'rg'].plot(figsize=(10,5), grid=True,ylim=(-20,1100))
plt.tight_layout()

#%% Día despejado: 

d1 = pd.to_datetime('2022-10-08 22:00:00')
d2 = pd.to_datetime('2022-10-09 23:59:00')
R_m.loc[d1:d2,'rg'].plot(figsize=(10,5), grid=True,ylim=(-20,1100))
plt.tight_layout()

#%% Dividimos

# df diferencias
d1 = pd.to_datetime('2022-10-03 22:00:00')
d2 = pd.to_datetime('2022-10-04 23:59:00')
R_diff = pd.DataFrame(index=pd.date_range(d1,d2,freq='min'))

# R cloudy
d1 = pd.to_datetime('2022-10-03 22:00:00')
d2 = pd.to_datetime('2022-10-04 23:59:00')
R_diff['rc'] = R_m.loc[d1:d2,'rg'].values+1

# R sunny
d1 = pd.to_datetime('2022-10-08 22:00:00')
d2 = pd.to_datetime('2022-10-09 23:59:00')
R_diff['rs'] = (R_m.loc[d1:d2,'rg'].rolling(window=30,center=True).mean().values*0.98)+1


# R division
R_diff['rd'] = R_diff['rc']/R_diff['rs']
R_diff[['rc','rs']] = R_diff[['rc','rs']]-1

#%% Ploteamos división suplot

R_diff.plot(figsize=(10,10), grid=True,subplots=True)
plt.tight_layout()

#%% Ploteamos división mismo plot

R_diff[['rc','rs']].plot(figsize=(10,10), grid=True)
plt.tight_layout()