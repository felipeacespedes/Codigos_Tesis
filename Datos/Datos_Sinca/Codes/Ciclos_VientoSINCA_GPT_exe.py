# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 17:36:41 2025

@author: felip
"""

import pandas as pd
from Ciclos_VientoSINCA_GPT import plot_wind_cycles, plot_polar_wind_cycles,\
                                    plot_wind_direction_and_speed

#%% Importamos datos horarios de HCNM por estación 

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
WD = pd.read_csv(path+'WD_df.csv',index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])
WS = pd.read_csv(path+'WS_df.csv',index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])
# Cortamos DFs a periodo 2019-2023
d1 = pd.to_datetime('2019-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')

WD = WD.loc[d1:d2]
WS = WS.loc[d1:d2]

#%% Wind cycles como scatter
plot_wind_cycles(WD)

#%% Wind cycles como polar plot
plot_polar_wind_cycles(WD)

#%% Wind cycles como polar plot y con velocidad

# Diario
plot_wind_direction_and_speed(WD, WS, cycle='daily')
# Anual
plot_wind_direction_and_speed(WD, WS, cycle='yearly')
