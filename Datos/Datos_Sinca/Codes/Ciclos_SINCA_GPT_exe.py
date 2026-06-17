# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 11:39:45 2025

@author: felip
"""
import pandas as pd
from Ciclos_SINCA_GPT import plot_all_cycles

#%% Importamos datos horarios de HCNM por estación 

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
HCNM = pd.read_csv(path+'HCNM_mod_df.csv',index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])

# Cortamos datos entre 2019 y 2023
d1 = pd.to_datetime('2019-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
HCNM = HCNM.loc[d1:d2]

#%% Ejecutamos

#%% Ciclos sin normalizar, compartiendo eje y

# Diario
plot_cycle(HCNM, freq=None, shared_y=True)

# Semanal
plot_cycle(HCNM, freq='D', shared_y=True)

# Anual
plot_cycle(HCNM, freq='ME', shared_y=True)

#%% Ciclos sin normalizar, sin compartir eje y

# Diario
plot_cycle(HCNM, freq=None, shared_y=False)

# Semanal
plot_cycle(HCNM, freq='D', shared_y=False)

# Anual
plot_cycle(HCNM, freq='ME', shared_y=False)

#%% Ciclos normalizados

# Diario
plot_cycle(HCNM, freq=None, normalize=True, shared_y=True)

# Semanal
plot_cycle(HCNM, freq='D', normalize=True, shared_y=True)

# Anual
plot_cycle(HCNM, freq='ME', normalize=True, shared_y=True)

#%% Ploteamos todos los ciclos

plot_all_cycles(HCNM, normalize=False, shared_y=True)


