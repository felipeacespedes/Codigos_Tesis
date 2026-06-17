# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 17:31:38 2024

@author: felip

Código para crear archivos Constrained AtChem de variables Quimicas y Meteo.
"""
# Importamos librerías
import pandas as pd
from Crear_archivos_constrained import AtChem_ConstrainFile

# Importamos MasterDF
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
DATA = pd.read_csv(path+'MasterDF_inv_data_1m.csv',delimiter=';')
DATA['date'] = pd.to_datetime(DATA['date'],format='%d/%m/%Y %H:%M:%S')
DATA['date'] = pd.to_datetime(DATA['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
DATA = DATA.set_index('date')

#%% Creamos listas para crear archivos

## Compuestos que se ingresan completo:
# PTR
comp_PTc = ['Formaldehyde','Methanol','Acetaldehyde','Ethanol',
           'Dimethyl.sulfide', 'Isoprene', 'Benzene', 'Toluene', 
           'Phenol','Styrene','Cresol']
comp_ATc = ['HCHO','CH3OH','CH3CHO','C2H5OH','DMS','C5H8','BENZENE',
           'TOLUENE','PHENOL','STYRENE','CRESOL']


## Divisiones:
comp_PTd = ['Propene_Cyclopropane','Butenes','Acetone_propanal',
           'Acetic.acid_Glycolaldehyde','Methacrolein_MVK','Butanone_Butanal',
           'Ethyl.benzene_Xylenes','C9_Aromatics','Monoterpenes']
comp_ATd = ['C3H6',['BUT1ENE','MEPROPENE'],['CH3COCH3','C2H5CHO'],'CH3CO2H',
           ['MACR','MVK','PENT1ENE'],['MEK','C3H7CHO'],
           ['EBENZ','MXYL','PXYL','OXYL'],
           ['PBENZ','IPBENZ','TM123B','TM124B',
            'TM135B','OETHTOL','METHTOL','PETHTOL'],
           ['APINENE','BPINENE','LIMONENE']]
## Otros:

# SINCA
comp_SI = ['O3','NO','NO2','CH4','CO','SO2']
comp_AT = ['O3','NO','NO2','CH4','CO','SO2']

# Meteo
met_EM = ['t','rh']
met_AT = ['TEMP','RH']

#%% Creamos Archivos
date_1 = '2022-09-11 22:00:00'
date_2 = '2022-09-13 01:59:00'

#%% Completos
freq='min'
path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida 1/'\
        +'Input/constraints/species/'
for n in range(len(comp_PTc)):
    AtChem_ConstrainFile(DATA.loc[date_1:date_2,comp_PTc[n]],
                         comp_ATc[n],False,freq,path)

#%% Divididos
freq='min'
path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida 1/'\
        +'Input/constraints/species/'
for n in range(len(comp_PTd)):
    AtChem_ConstrainFile(DATA.loc[date_1:date_2,comp_PTd[n]]
                         ,comp_ATd[n],False,freq,path)
    
#%% SINCA
freq='60min'
path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida 1/'\
        +'Input/constraints/species/'
for n in range(len(comp_SI)):
    AtChem_ConstrainFile(DATA.loc[date_1:date_2,comp_SI[n]]
                         ,comp_AT[n],False,freq,path)

#%% Meteo
freq='5min'
path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida 1/'\
        +'Input/constraints/environment/'                                            
for n in range(len(met_EM)):
    AtChem_ConstrainFile(DATA.loc[date_1:date_2,met_EM[n]]
                         ,met_AT[n],True,freq,path)

#%% Test:

# Probamos con Methacrolein_MVK dividido en MACR, MVK y PENT1ENE:
path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida 1/Input/Species/'
AtChem_ConstrainFile(DATA.loc['2022-10-04 00:00:00':'2022-10-04 23:59:00'\
                              ,'Methacrolein_MVK']
                     ,['MACR','MVK','PENT1ENE'],False,'min',path)


