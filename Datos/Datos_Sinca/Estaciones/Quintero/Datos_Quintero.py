# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 12:52:40 2025

@author: felip
"""

import pandas as pd
import numpy as np

#%% Cargamos datos de estación Quintero
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/Quintero/'
WD10 = pd.read_csv(path+'WD10.csv',sep=';',usecols=[2], decimal=',')
WS10 = pd.read_csv(path+'WS10.csv',sep=';',usecols=[2], decimal=',')

date = pd.date_range(start='2018-01-01 01:00:00',
                     end='2023-12-31 23:00:00',freq='h')
Quintero = pd.DataFrame(data={
                               'wd10':WD10.iloc[:,0],'ws10':WS10.iloc[:,0],
                               'u10':(-1)*np.sin(np.deg2rad(WD10.iloc[:,0]))*WS10.iloc[:,0],
                               'v10':(-1)*np.cos(np.deg2rad(WD10.iloc[:,0]))*WS10.iloc[:,0],
                               })
Quintero = Quintero.set_index(date)

# Guardamos
Quintero.index.names = ['date']
Quintero.to_csv(path+'Quintero.csv')