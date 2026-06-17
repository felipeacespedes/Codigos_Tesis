# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 12:10:10 2024

@author: felip

Código para crear Master dataframe para campaña de invierno que incluya los
COVs a resolusión 5m, datos meteo a 5m y datos SINCA a 1h
"""
# Importamos librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from import_var import import_var
#%% Importamos datos

## COVs
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
file = 'inv_data_5min.csv'
COV_5m = pd.read_csv(path+file,delimiter=';')
COV_5m['date'] = pd.to_datetime(COV_5m['date'],format='%d/%m/%Y %H:%M:%S')
COV_5m['date'] = pd.to_datetime(COV_5m['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV_5m = COV_5m.set_index('date')

## Meteo
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
file = 'inv_data_5min.csv'
MET_5m = pd.read_csv(path+file,delimiter=';',usecols=['date','p','t',
                                                      'rh','ws','wd','sr'])
MET_5m['date'] = pd.to_datetime(MET_5m['date'],format='%d/%m/%Y %H:%M:%S')
MET_5m['date'] = pd.to_datetime(MET_5m['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
MET_5m = MET_5m.set_index('date')


## SINCA
CQ_1h = pd.DataFrame(index = pd.date_range('2022-08-27 00:00:00',
                                           '2022-11-03 23:00:00',
                                           freq='h'))
# CH4 [ppm]->[ppb]
CQ_1h['CH4'] = import_var('Centro_Quintero', 'Cont', 'CH4',
                          '2022-08-27','2022-11-03')*1000
# O3 [ppb]
CQ_1h['O3'] = import_var('Centro_Quintero', 'Cont', 'O3',
                          '2022-08-27','2022-11-03')
# NO [ppb]
CQ_1h['NO'] = import_var('Centro_Quintero', 'Cont', 'NO',
                          '2022-08-27','2022-11-03')
# NO2 [ppb]
CQ_1h['NO2'] = import_var('Centro_Quintero', 'Cont', 'NO2',
                          '2022-08-27','2022-11-03')
# CO [ppm] -> [ppb]
CQ_1h['CO'] = import_var('Centro_Quintero', 'Cont', 'CO',
                          '2022-08-27','2022-11-03')*1000
# SO2 [ppb]
CQ_1h['SO2'] = import_var('Centro_Quintero', 'Cont', 'SO2',
                          '2022-08-27','2022-11-03')

# Aplicamos interpolación por Akima
MET_5m = MET_5m.resample('5min').asfreq().interpolate(method='akima')
CQ_1h = CQ_1h.resample('5min').asfreq().interpolate(method='akima')

del path, file
#%% data MET

# Fechas
d1 = pd.to_datetime('2022-09-11 00:00:00')
d2 = pd.to_datetime('2022-09-12 23:00:00')
MET_5m.loc[d1:d2,['p','t','rh']].plot(subplots=True,figsize=(10,10),grid=True)
plt.tight_layout()

#%% data CQ

# Fechas
d1 = pd.to_datetime('2022-09-11 00:00:00')
d2 = pd.to_datetime('2022-09-12 23:00:00')
CQ_1h.loc[d1:d2,['SO2','O3','NO','NO2','CO','CH4']].plot(subplots=True,figsize=(10,20),grid=True)
plt.tight_layout()

#%% Creamos Master Data Frame y vamos rellenando

# Creamos DF de resolución 1 minuto para toda la campaña
Mdf_5m = pd.DataFrame(index = pd.date_range('2022-08-27 00:00:00',
                                           '2022-11-03 23:00:00',
                                           freq='5min'))

#%% Ingresamos COVs con nombres tal cual

Mdf_5m[COV_5m.columns] = COV_5m

#%% Ingresamos variables SINCA

# Contaminantes básicos
Mdf_5m = Mdf_5m.join(CQ_1h[['CH4','O3','NO','NO2','CO','SO2']])

#%% Ingresamos variables Meteo

# Vientos,Temperatura, Presión, Humedad Relativa y Radiación
Mdf_5m[MET_5m.columns] = MET_5m

#%% Guardamos
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
Mdf_5m.to_csv(path+'MasterDF_inv_data_5m.csv',sep=';',
              index_label='date', date_format='%d/%m/%Y %H:%M:%S')