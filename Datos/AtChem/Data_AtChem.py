# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 17:31:24 2024

@author: felip

Ordenar datos para Atchem
"""
# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
from import_var import import_var

#%% Importamos datos
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/AtChem/Input_AtChem/'


## COVs
file = 'PTR/COVs_1min_CampañaInvierno2022.csv'
COV_1m = pd.read_csv(path+file,delimiter=';')
COV_1m['date'] = pd.to_datetime(COV_1m['date'],format='%d/%m/%Y %H:%M:%S')
COV_1m['date'] = pd.to_datetime(COV_1m['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV_1m = COV_1m.set_index('date')

## Meteo
file = 'PTR/MET_5min_CampañaInvierno2022.csv'
MET_5m = pd.read_csv(path+file,delimiter=';')
MET_5m['date'] = pd.to_datetime(MET_5m['date'],format='%d/%m/%Y %H:%M:%S')
MET_5m['date'] = pd.to_datetime(MET_5m['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
MET_5m = MET_5m.set_index('date')

## SINCA
CQ_1h = pd.DataFrame(index = pd.date_range('2022-08-27 00:00:00',
                                           '2022-11-03 23:00:00',
                                           freq='H'))
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

del path, file
#%% Creamos DF para Atchem y vamos rellenando

# Creamos DF de resolución 1 minuto para toda la campaña
AtChem_1m = pd.DataFrame(index = pd.date_range('2022-08-27 00:00:00',
                                           '2022-11-03 23:00:00',
                                           freq='1min'))

#%% Ingresamos variables Meteo

# Temperatura y Humedad Relativa
AtChem_1m[['TEMP','RH']] = MET_5m[['t','rh']]

#%% Ingresamos variables SINCA

# Contaminantes básicos
AtChem_1m = AtChem_1m.join(CQ_1h[['CH4','O3','NO','NO2','CO']])

#%% Ingresamos COVs

## Formaldehyde ##
AtChem_1m['HCHO'] = COV_1m['Formaldehyde']

## Methanol ##
AtChem_1m['CH3OH'] = COV_1m['Methanol']

## Propene/Cyclopropane ##
AtChem_1m['C3H6'] = COV_1m['Propene_Cyclopropane']

## Acetaldehyde ##
AtChem_1m['CH3CHO'] = COV_1m['Acetaldehyde']

## Ethanol ##
AtChem_1m['C2H5OH'] = COV_1m['Ethanol']

## Butenes ##
# separamos en:
# - 1-Butene
AtChem_1m['BUT1ENE'] = COV_1m['Butenes']*0.5
# - isobutene
AtChem_1m['MEPROPENE'] = COV_1m['Butenes']*0.5

## Acetone/Propanal ##
# separamos en:
# - Acetone
AtChem_1m['CH3COCH3'] = COV_1m['Acetone_propanal']*0.5
# - Propanal
AtChem_1m['C2H5CHO'] = COV_1m['Acetone_propanal']*0.5

## Acetic acid / Glicolaldehyde ##
# separamos en:
# - Acetic acid
AtChem_1m['CH3CO2H'] = COV_1m['Acetic.acid_Glycolaldehyde']*0.5
# - Glicolaldehyde
AtChem_1m['HOCH2CHO'] = COV_1m['Acetic.acid_Glycolaldehyde']*0.5

## Dimethyl sulfide ##
AtChem_1m['DMS'] = COV_1m['Dimethyl.sulfide']

## Isoprene ##
AtChem_1m['C5H8'] = COV_1m['Isoprene']

## Methacrolein/MVK ##
# separamos en:
# - Methacrolein
AtChem_1m['MACR'] = COV_1m['Methacrolein_MVK']*0.5
# - Glicolaldehyde
AtChem_1m['MVK'] = COV_1m['Methacrolein_MVK']*0.5

## Butanone/Butanal ##
# separamos en:
# - Butanone
AtChem_1m['MEK'] = COV_1m['Butanone_Butanal']*0.5
# - Butanal
AtChem_1m['C3H7CHO'] = COV_1m['Butanone_Butanal']*0.5

## Benzene ##
AtChem_1m['BENZENE'] = COV_1m['Benzene']

## Toluene ##
AtChem_1m['TOLUENE'] = COV_1m['Toluene']

## Phenol ##
AtChem_1m['PHENOL'] = COV_1m['Phenol']

## Styrene ##
AtChem_1m['STYRENE'] = COV_1m['Styrene']

## Ethylbenzene/Xylenes ##
# separamos en:
# - Ethylbenzene
AtChem_1m['EBENZ'] = COV_1m['Ethyl.benzene_Xylenes']*0.25
# - m-Xyleno
AtChem_1m['MXYL'] = COV_1m['Ethyl.benzene_Xylenes']*0.25
# - p-Xyleno
AtChem_1m['PXYL'] = COV_1m['Ethyl.benzene_Xylenes']*0.25
# - o-Xyleno
AtChem_1m['OXYL'] = COV_1m['Ethyl.benzene_Xylenes']*0.25

## Cresol ##
AtChem_1m['CRESOL'] = COV_1m['Cresol']

## C9 Aromatics ##
# separamos en:
AtChem_1m['PBENZ'] = COV_1m['C9_Aromatics']*0.125
AtChem_1m['IPBENZ'] = COV_1m['C9_Aromatics']*0.125
AtChem_1m['TM123B'] = COV_1m['C9_Aromatics']*0.125
AtChem_1m['TM124B'] = COV_1m['C9_Aromatics']*0.125
AtChem_1m['TM135B'] = COV_1m['C9_Aromatics']*0.125
AtChem_1m['OETHTOL'] = COV_1m['C9_Aromatics']*0.125
AtChem_1m['METHTOL'] = COV_1m['C9_Aromatics']*0.125
AtChem_1m['PETHTOL'] = COV_1m['C9_Aromatics']*0.125

## Monoterpenes ##
# separamos en:
AtChem_1m['APINENE'] = COV_1m['Monoterpenes']*(1/3)
AtChem_1m['BPINENE'] = COV_1m['Monoterpenes']*(1/3)
AtChem_1m['LIMONENE'] = COV_1m['Monoterpenes']*(1/3)

#%% Cortar y guardar el 4 de octubre

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/AtChem/Input_AtChem/'
date_1 = '2022-10-04 00:00:00'
date_2 = '2022-10-04 23:59:00'
AtChem_1m_0410 = AtChem_1m.loc[date_1:date_2,:]
AtChem_1m_0410.insert(0,'Sec', ((AtChem_1m_0410.index - AtChem_1m_0410.index\
                        .normalize()) / pd.Timedelta('1 second')).astype(int))
AtChem_1m_0410.to_csv(path+'AtChemInput_0410.csv',sep=';',
                      index_label='DATE', date_format='%Y-%m-%dT%H:%M:%SZ')

#%% Revisamos datos

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/AtChem/Input_AtChem/'
file = 'AtChemInput_0410.csv'
AtChem = pd.read_csv(path+file,delimiter=';')
AtChem = AtChem.set_index(pd.to_datetime(AtChem['DATE']))
AtChem_1h = AtChem.resample('1h').mean()

#%% Ploteamos
comp = ['NO','NO2','O3']
AtChem_1h[comp].plot(subplots=True,grid=True,figsize=(10,10))
plt.tight_layout()





















