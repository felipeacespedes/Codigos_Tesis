# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:35:52 2024

@author: felip

Código para inspeccionar datos de contaminantes básicos de Centro Quintero
"""

# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
from import_var import import_var

#%% Importamos datos contaminantes

# Creamos df para contaminantes

CQ_df = pd.DataFrame(index = pd.date_range('2018-01-01 00:00:00',
                                           '2023-12-31 23:00:00',
                                           freq='H'))
# HCNM [ppm]
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_SINCA/'
HCNM = pd.read_csv(path+'HCNM_mod_lod_df.csv')
HCNM['date'] = pd.to_datetime(HCNM['date'])
HCNM = HCNM.set_index('date')
CQ_df['HCNM'] = HCNM['Centro_Quintero']*1000
del path, HCNM

# CH4 [ppm]
CQ_df['CH4'] = import_var('Centro_Quintero', 'Cont', 'CH4',
                          '2018-01-01','2023-12-31')*1000
# HCT [ppm]
CQ_df['HCT'] = import_var('Centro_Quintero', 'Cont', 'HCT',
                          '2018-01-01','2023-12-31')*1000
# O3 [ppb]
CQ_df['O3'] = import_var('Centro_Quintero', 'Cont', 'O3',
                          '2018-01-01','2023-12-31')
# NO [ppb]
CQ_df['NO'] = import_var('Centro_Quintero', 'Cont', 'NO',
                          '2018-01-01','2023-12-31')
# NO2 [ppb]
CQ_df['NO2'] = import_var('Centro_Quintero', 'Cont', 'NO2',
                          '2018-01-01','2023-12-31')
# CO [ppm]
CQ_df['CO'] = import_var('Centro_Quintero', 'Cont', 'CO',
                          '2018-01-01','2023-12-31')*1000
# MP25 [ug/m3]
CQ_df['MP25'] = import_var('Centro_Quintero', 'Cont', 'MP25',
                          '2018-01-01','2023-12-31')
# MP10[ug/m3]
CQ_df['MP10'] = import_var('Centro_Quintero', 'Cont', 'MP10',
                          '2018-01-01','2023-12-31')
#SO2 [ppb]
CQ_df['SO2'] = import_var('Centro_Quintero', 'Cont', 'SO2',
                          '2018-01-01','2023-12-31')
# ws [m/s]
CQ_df['ws'] = import_var('Centro_Quintero', 'Meteo', 'Vel',
                          '2018-01-01','2023-12-31')
# wd [°]
CQ_df['wd'] = import_var('Centro_Quintero', 'Meteo', 'Dir',
                          '2018-01-01','2023-12-31')

#%% Guardamos

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/' 
CQ_df.to_csv(path+'CQ_ContMet1823_OpenAirFormat.csv'\
               , sep=';',index_label='date'\
               , date_format='%d/%m/%Y %H:%M:%S')
    
