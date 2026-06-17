# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 18:26:44 2025

@author: felip
"""

import pandas as pd
import matplotlib.pyplot as plt

#%% Importamos csv

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_lucas/'
DF = pd.read_csv(path+'data_ppb.csv',index_col='DATE',parse_dates=True)
DF.index = pd.to_datetime(DF.index.strftime('%Y-%m-%d %H:%M:%S'))

#%% Lists of compounds

comp_int=['X_Propene','CH3CHO',
          'X_C4H8','X_Acetone_Propanal',
          'X_MACR_MVK','X_Butanone_Butanal',
          'C5H8','HCHO','DMS',
          'NO','NO2','O3']

#%% Ploteamos

date_1 = pd.to_datetime('2021-12-20 00:00:00')
date_2 = pd.to_datetime('2021-12-25 00:00:00')

DF.loc[date_1:date_2,comp_int].plot(figsize=(20,10),grid=True,
                                    subplots=True,layout=(4,3))
plt.tight_layout()
