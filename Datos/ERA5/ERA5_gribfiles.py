# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 14:23:45 2025

@author: felip
"""
# importamos librerías
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%% Cargamos datos 

# Grib data
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/ERA5/'

# [-32.84,-71.56]: 2019-2023
# grib_data = xr.open_dataset(path+'MET_2019-2023_6h.grib',engine='cfgrib')

# [-32.76,-71.50]: 2018-2024
# grib_data = xr.open_dataset(path+'MET_2018-2024_6h.grib',engine='cfgrib')

# [-32.76,-71.50]: 2018-2024 2
grib_data = xr.open_dataset(path+'MET_2018-2024_6h_2.grib',engine='cfgrib')


#%% Juntamos datos

# Xarray to Dataframe
data_df = grib_data.to_dataframe()

# Seleccionamos columnas de interes
data_df['date'] = pd.DatetimeIndex(data_df['valid_time'],freq='6h')
data_df = data_df.set_index('date')
data_df = data_df.drop(columns=['number','step','surface','valid_time'])
data_df[data_df.columns] = data_df[data_df.columns].astype(float)

#%% t

data_df['t2m'].hist(figsize=(7,5),grid=True)
plt.title('Histograma t ERA5')
plt.tight_layout()

#%% td

data_df['d2m'].hist(figsize=(7,5),grid=True)
plt.title('Histograma td ERA5')
plt.tight_layout()

#%% Cambiamos unidades de t y td

# t:
data_df['t2m'] = data_df['t2m']-273.15
# td:
data_df['d2m'] = data_df['d2m']-273.15


#%% Calculamos hr en base a t y td

# hr: Ecuación August-Roche-Magnus
data_df['hr2m'] = 100*(np.exp((17.625*data_df['d2m'])/(243.04+data_df['d2m']))\
                 /np.exp((17.625*data_df['t2m'])/(243.04+data_df['t2m'])))
    
#%% Calculamos ws

# ws
data_df['ws10'] = np.sqrt((data_df['u10']**2)+(data_df['v10']**2))

#%% Presión de Pascales a HectoPascales

data_df['sp'] = data_df['sp']/100

#%% Guardamos

# Lat,Lon: 
data_df.to_csv(path+'MET_ERA5.csv',index_label='date')
