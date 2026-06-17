# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 17:37:39 2025

@author: felip
"""
# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
import datetime
# import seaborn as sns
# from statsmodels.tsa.seasonal import seasonal_decompose, STL
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
# sns.set_style("darkgrid")

# plt.rc("figure", figsize=(16, 12))
# plt.rc("font", size=13)

#%% Importamos datos SINCA

#%% DF HCNM
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_SINCA/'
HCNM = pd.read_csv(path+'HCNM_mod_lod_df.csv') # mod_lod
HCNM['date'] = pd.to_datetime(HCNM['date'])
HCNM = HCNM.set_index('date')

#%%  Plot de resultados varios:
    
#%% Ciclo Anual:
    
# Aquí en la tesis se había mencionado una approach de descomposición STL 
# (Seasonal-Trend Loess decomposition), esto es, descomponer en señal estacio-
# nal, tendencia y residual. Esto no entrega el ciclo anual, sino que la señal
# estacional de la serie de tiempo 

#%%
# Definimos fechas 
date_1 = pd.to_datetime('2018-01-01 00:00:00')
date_2 = pd.to_datetime('2023-12-31 23:00:00')
# Estación a plotear
le = 'Colmo' #['Ventanas','Centro_Quintero','Concón','Gaviotas','Colmo']
data = HCNM.loc[date_1:date_2, le].resample('W').mean().ffill()
# data = data.squeeze()

#%% STL
stl = STL(data,period=52,seasonal=51).fit()
stl.plot()
plt.show()

#%% Seasonal decompose

sd = seasonal_decompose(data,model="additive",period=52)
sd.plot()
plt.show() 

#%% Serie de tiempo

#%% HCNM ###

# Definimos fechas 
date_1 = pd.to_datetime('2021-05-01 00:00:00')
date_2 = pd.to_datetime('2021-05-03 23:00:00')

est = 'Ventanas'
peak_3std = HCNM[est].quantile(0.998)
peak_99perc = HCNM[est].quantile(0.99)
peak_95perc = HCNM[est].quantile(0.95)
ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(16,8),ylim=(-0.1,2))
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('[ppm]')
plt.legend()
plt.title(est)
plt.tight_layout()