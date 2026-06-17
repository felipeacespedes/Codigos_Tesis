# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 17:04:00 2025

@author: felip
"""

import pandas as pd
import numpy as np
from import_var import import_var, import_var_col

#%%  Cargamos contaminantes de interes

est = ['Ventanas','Centro_Quintero','Concón']
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/'
Fi = '2018-01-01'
Ff = '2023-12-31'
date = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

#%% CO

# Creamos DF
CO = pd.DataFrame(columns=est)
CO['date'] = date
CO = CO.set_index('date')
# Estaciones a dejar con nan
nan = ['Ventanas','Concón']
# Importamos datos
for e in est:
    if e in nan:
        continue
    CO[e] = import_var(e,'Cont','CO',Fi,Ff)
# Rellenamos con Nan
for e in nan:
    CO[e] = np.nan

#%% SO2

# Creamos DF
SO2 = pd.DataFrame(columns=est)
SO2['date'] = date
SO2 = SO2.set_index('date')
# Estaciones a dejar con nan
nan = []
# Importamos datos
for e in est:
    if e in nan:
        continue
    SO2[e] = import_var(e,'Cont','SO2',Fi,Ff)

# Rellenamos con Nan
# for e in nan:
#     SO2[e] = np.nan

#%% MP25

# Creamos DF
MP25 = pd.DataFrame(columns=est)
MP25['date'] = date
MP25 = MP25.set_index('date')
# Estaciones a dejar con nan
nan = []
# Importamos datos
for e in est:
    if e in nan:
        continue
    MP25[e] = import_var(e,'Cont','MP25',Fi,Ff)

# Rellenamos con Nan
# for e in nan:
#     MP25[e] = np.nan

#%% MP10

# Creamos DF
MP10 = pd.DataFrame(columns=est)
MP10['date'] = date
MP10 = MP10.set_index('date')
# Estaciones a dejar con nan
nan = []
# Importamos datos
for e in est:
    if e in nan:
        continue
    MP10[e] = import_var(e,'Cont','MP10',Fi,Ff)

# Rellenamos con Nan
# for e in nan:
#     MP10[e] = np.nan

#%% NO2

# Creamos DF
NO2 = pd.DataFrame(columns=est)
NO2['date'] = date
NO2 = NO2.set_index('date')
# Estaciones a dejar con nan
nan = ['Concón']
# Importamos datos
for e in est:
    if e in nan:
        continue
    NO2[e] = import_var(e,'Cont','NO2',Fi,Ff)

# Rellenamos con Nan
for e in nan:
    NO2[e] = np.nan

#%% NO

# Creamos DF
NO = pd.DataFrame(columns=est)
NO['date'] = date
NO = NO.set_index('date')
# Estaciones a dejar con nan
nan = ['Concón']
# Importamos datos
for e in est:
    if e in nan:
        continue
    NO[e] = import_var(e,'Cont','NO',Fi,Ff)

# Rellenamos con Nan
for e in nan:
    NO[e] = np.nan
    
#%% O3

# Creamos DF
O3 = pd.DataFrame(columns=est)
O3['date'] = date
O3 = O3.set_index('date')
# Estaciones a dejar con nan
nan = ['Concón']
# Importamos datos
for e in est:
    if e in nan:
        continue
    O3[e] = import_var(e,'Cont','O3',Fi,Ff)

# Rellenamos con Nan
for e in nan:
    O3[e] = np.nan
    
#%% Guardamos

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Contaminantes/'
CO.to_csv(path+'CO_df.csv')
SO2.to_csv(path+'SO2_df.csv')
MP25.to_csv(path+'MP25_df.csv')
MP10.to_csv(path+'MP10_df.csv')
NO2.to_csv(path+'NO2_df.csv')
NO.to_csv(path+'NO_df.csv')
O3.to_csv(path+'O3_df.csv')
