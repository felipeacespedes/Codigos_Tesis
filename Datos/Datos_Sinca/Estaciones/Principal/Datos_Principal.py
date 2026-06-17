# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 12:35:40 2025

@author: felip
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Cargamos datos de estación Principal
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/Principal/'
T10 = pd.read_csv(path+'T10.csv',sep=';',usecols=[2], decimal=',')
T20 = pd.read_csv(path+'T20.csv',sep=';',usecols=[2], decimal=',')
T40 = pd.read_csv(path+'T40.csv',sep=';',usecols=[2], decimal=',')
WD10 = pd.read_csv(path+'WD10.csv',sep=';',usecols=[2], decimal=',')
WS10 = pd.read_csv(path+'WS10.csv',sep=';',usecols=[2], decimal=',')
WD40 = pd.read_csv(path+'WD40.csv',sep=';',usecols=[2], decimal=',')
WS40 = pd.read_csv(path+'WS40.csv',sep=';',usecols=[2], decimal=',')
date = pd.date_range(start='2018-01-01 01:00:00',
                     end='2023-12-31 23:00:00',freq='h')
Principal = pd.DataFrame(data={'t10':T10.iloc[:,0],'t20':T20.iloc[:,0],'t40':T40.iloc[:,0],
                               't_inv_30':(T40.iloc[:,0]-T10.iloc[:,0]),
                               't_inv_10':(T20.iloc[:,0]-T10.iloc[:,0]),
                               'wd10':WD10.iloc[:,0],'ws10':WS10.iloc[:,0],
                               'u10':(-1)*np.sin(np.deg2rad(WD10.iloc[:,0]))*WS10.iloc[:,0],
                               'v10':(-1)*np.cos(np.deg2rad(WD10.iloc[:,0]))*WS10.iloc[:,0],
                               'wd40':WD40.iloc[:,0],'ws40':WS40.iloc[:,0],
                               'u40':(-1)*np.sin(np.deg2rad(WD40.iloc[:,0]))*WS40.iloc[:,0],
                               'v40':(-1)*np.cos(np.deg2rad(WD40.iloc[:,0]))*WS40.iloc[:,0]
                               })
Principal = Principal.set_index(date)
#%% Exploramos variables

yr = 23
d1 = pd.to_datetime(f'20{yr}-05-15 00:00:00')
d2 = pd.to_datetime(f'20{yr}-05-31 23:00:00')
var = ['t10','t20','t40','t_inv_10','t_inv_30']#,'wd10','wd40','ws10','ws40']
Principal.loc[d1:d2,var].plot(subplots=True,layout=(5,1),figsize=(10,15))
plt.tight_layout()

#%% Exploramos inversiones


fig, axs = plt.subplots(2,1,figsize=(10,15))

axs[0].plot(Principal.loc[d1:d2].index,Principal.loc[d1:d2,var[4]],label=var[4])
axs[0].axhline(y=-0.294, color='red', linestyle='--')
# axs[0].axhline(y=-0.0098, color='red', linestyle='--')

axs[0].grid(True,alpha=0.6)
axs[0].legend()

axs[1].plot(Principal.loc[d1:d2].index,Principal.loc[d1:d2,var[3]],label=var[3])
axs[1].axhline(y=-0.098, color='red', linestyle='--')
# axs[1].axhline(y=-0.0098, color='red', linestyle='--')

axs[1].grid(True,alpha=0.6)
axs[1].legend()


fig.tight_layout()

#%% Guardamos
Principal.index.names = ['date']
Principal.to_csv(path+'Principal.csv')

#%% Resampleamos viento a diario
