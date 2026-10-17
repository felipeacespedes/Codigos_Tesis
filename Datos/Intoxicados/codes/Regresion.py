# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 12:30:09 2025

@author: felip
"""
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import datetime
import numpy as np
import Ciclos_GPT as cs
import sys
import os
import ClimatologicalDailyCycle as cdc
import Regresion_Funcs as rf

COLOR_MAP = sns.color_palette("Set2", 18)

ls_og = [
     ('densely dashed',        (0, (4, 1))),
     ('dashed',                (0, (4, 4))),
     ('loosely dashed',        (0, (4, 10))),
     
     ('densely dotted',        (0, (1, 2))),
     ('dotted',                (0, (1, 4))),
     ('loosely dotted',        (0, (1, 6))),
     
     ('densely dashdotted',    (0, (3, 1, 1, 1))),
     ('dashdotted',            (0, (3, 4, 1, 4))),
     ('loosely dashdotted',    (0, (3, 7, 1, 7))),

     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1))),
     ('dashdotdotted',         (0, (3, 4, 1, 4, 1, 4))),
     ('loosely dashdotdotted', (0, (3, 7, 1, 7, 1, 7))),
     ]
ls = []
for i in range(len(ls_og)):
    ls.append(ls_og[i][1])
del ls_og

# Path de datos
path_data = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/data/'

#%% Importamos datos y cortamos entre 2019 y 2023

# Fechas
d1 = pd.to_datetime('2019-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')

# T59
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
T59 = pd.read_csv(path+'serie_T59full.csv', index_col='date',
                  parse_dates=True)
T59 = T59.loc[d1:d2,['T59','Comuna']]

# SINCA HCNM
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
HCNM = pd.read_csv(path+'HCNM_mod_df.csv',
                   index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero','Concón'])
HCNM = HCNM.loc[d1:d2]

# SINCA Contaminantes
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Contaminantes/'
CO = pd.read_csv(path+'CO_df.csv',index_col='date',parse_dates=True,
                 usecols=['date','Ventanas','Centro_Quintero','Concón'])
SO2 = pd.read_csv(path+'SO2_df.csv',index_col='date',parse_dates=True,
                  usecols=['date','Ventanas','Centro_Quintero','Concón'])
MP25 = pd.read_csv(path+'MP25_df.csv',index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero','Concón'])
MP10 = pd.read_csv(path+'MP10_df.csv',index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero','Concón'])
NO2 = pd.read_csv(path+'NO2_df.csv',index_col='date',parse_dates=True,
                  usecols=['date','Ventanas','Centro_Quintero','Concón'])
NO = pd.read_csv(path+'NO_df.csv',index_col='date',parse_dates=True,
                 usecols=['date','Ventanas','Centro_Quintero','Concón'])
O3 = pd.read_csv(path+'O3_df.csv',index_col='date',parse_dates=True,
                 usecols=['date','Ventanas','Centro_Quintero','Concón'])

CO = CO.loc[d1:d2]
SO2 = SO2.loc[d1:d2]
MP25 = MP25.loc[d1:d2]
MP10 = MP10.loc[d1:d2]
NO2 = NO2.loc[d1:d2]
NO = NO.loc[d1:d2]
NOx = NO + NO2
O3 = O3.loc[d1:d2]


# SINCA Viento
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
WD = pd.read_csv(path+'WD_df.csv',
                   index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero','Concón'])
WS = pd.read_csv(path+'WS_df.csv',
                   index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero','Concón'])
WD = WD.loc[d1:d2]
WS = WS.loc[d1:d2]
U = (-1)*np.sin(np.deg2rad(WD))*WS
V = (-1)*np.cos(np.deg2rad(WD))*WS

# DMC
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/datos_DMC/'
DMC = pd.read_csv(path+'DMC_h.csv',index_col='date',parse_dates=True,
                  usecols=['date','ts','td','p','slp','hr','rg','u','v','wd','ws'])
DMC = DMC.loc[d1:d2]

# Principal
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/Principal/'
Princ = pd.read_csv(path+'Principal.csv',index_col='date',parse_dates=True,
                    usecols=['date','t_inv_30','t10','u10','v10','wd10','ws10',
                             't40','u40','v40','wd40','ws40',
                             ])
Princ = Princ.loc[d1:d2]

# Quintero
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/Quintero/'
Quint = pd.read_csv(path+'Quintero.csv',index_col='date',parse_dates=True,
                    usecols=['date','u10','v10','wd10','ws10'])
Quint = Quint.loc[d1:d2]

# Importamos datos de altura de capa límita por ERA5 en [-71.55,-32.83]
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/ERA5/'
ERA5 = pd.read_csv(path+'MET_ERA5.csv',index_col='date',parse_dates=True)
ERA5 = ERA5.shift(periods=-4,freq='h')# pasamos a UTC-4
ERA5 = ERA5.loc[d1:d2]

#%% Cambiamos nombres a variables a utilizar

# Especificamos nombres
HCNM = HCNM.rename(columns={'Ventanas':'HCNM_VE','Centro_Quintero':'HCNM_CQ',
                      'Concón':'HCNM_CC'})
CO = CO.rename(columns={'Ventanas':'CO_VE','Centro_Quintero':'CO_CQ',
                        'Concón':'CO_CC'})
SO2 = SO2.rename(columns={'Ventanas':'SO2_VE','Centro_Quintero':'SO2_CQ',
                          'Concón':'SO2_CC'})
MP25 = MP25.rename(columns={'Ventanas':'MP25_VE','Centro_Quintero':'MP25_CQ',
                            'Concón':'MP25_CC'})
MP10 = MP10.rename(columns={'Ventanas':'MP10_VE','Centro_Quintero':'MP10_CQ',
                            'Concón':'MP10_CC'})
NO2 = NO2.rename(columns={'Ventanas':'NO2_VE','Centro_Quintero':'NO2_CQ',
                          'Concón':'NO2_CC'})
NO = NO.rename(columns={'Ventanas':'NO_VE','Centro_Quintero':'NO_CQ',
                        'Concón':'NO_CC'})
NOx = NOx.rename(columns={'Ventanas':'NOx_VE','Centro_Quintero':'NOx_CQ',
                        'Concón':'NOx_CC'})
O3 = O3.rename(columns={'Ventanas':'O3_VE','Centro_Quintero':'O3_CQ',
                          'Concón':'O3_CC'})
U = U.rename(columns={'Ventanas':'u_VE','Centro_Quintero':'u_CQ',
                      'Concón':'u_CC'})
V = V.rename(columns={'Ventanas':'v_VE','Centro_Quintero':'v_CQ',
                      'Concón':'v_CC'})
WS = WS.rename(columns={'Ventanas':'ws_VE','Centro_Quintero':'ws_CQ',
                      'Concón':'ws_CC'})
WD = WD.rename(columns={'Ventanas':'wd_VE','Centro_Quintero':'wd_CQ',
                      'Concón':'wd_CC'})
DMC = DMC.rename(columns={'ts':'t_dmc','td':'td_dmc','u':'u_dmc','v':'v_dmc',
                          'p':'p_dmc','hr':'hr_dmc','slp':'slp_dmc',
                          'rg':'r_dmc','wd':'wd_dmc','ws':'ws_dmc'})
Princ = Princ.rename(columns={'t10':'t_princ','t40':'t40_princ','t_inv_30':'ies_princ',
                              'wd10':'wd_princ','ws10':'ws_princ','u10':'u_princ','v10':'v_princ',
                              'wd40':'wd40_princ','ws40':'ws40_princ','u40':'u40_princ','v40':'v40_princ'})
Quint = Quint.rename(columns={'wd10':'wd_quint','ws10':'ws_quint',
                              'u10':'u_quint','v10':'v_quint'})
ERA5 = ERA5.rename(columns={'u10':'u_era5','v10':'v_era5','ws10':'ws_era5',
                            'd2m':'td_era5','t2m':'t_era5','hr2m':'hr_era5',
                            'sp':'p_era5','blh':'blh_era5'})

#%% Datos horarios ##

# Juntamos variables
DF_h = pd.concat([HCNM,CO,SO2,MP25,MP10,NO2,NO,NOx,O3,U,V,WS,WD,DMC,Princ,Quint,ERA5], axis=1)

# Creamos diferenical de presión
DF_h['slp_dmc_diff'] = DMC['slp_dmc'].rolling(window=12,center=True).mean()\
                                    .diff(periods=-3)*(-1)
# DF a 6h por datos ERA5 (NO LO ESTOY USANDO)
DF_6h = DF_h.resample('6h',offset='2h').asfreq()
DF_6h.iloc[0,:] = DF_6h.iloc[4,:]

## Seleccionamos los datos de contaminantes y meteo ##
# A contaminantes se les restará ciclo anual y semianual por fft:
cont = pd.concat([HCNM,CO,SO2,MP25,MP10,NO2,NO,NOx,O3], axis=1).columns.tolist()
# A variables meteo se les aplicará una resta de el promedio movil
# horario (según hora del día) de +-45 días, intentando replicar 
# analisis estacional movil para todo el año:
met = pd.concat([U,V,WS,WD,DMC,Princ,Quint,ERA5], axis=1).columns.tolist()

# creamos columna booleana para evento
# mask = (T59['T59']>0)
# mask = mask.astype(int).asfreq('h',method='ffill')
# DF_h['evento'] = mask
# DF_h['T59'] = T59['T59'].asfreq('h',method='ffill')

# Guardamos
DF_h.index.names = ['date']
DF_h.to_csv(path_data+'DF_h.csv')


#####################################################
#%% Datos horarios Anomalía Anual-Semianual a cont ##

# Quitamos ciclo anual y semianual por fft a CONTAMINANTES
DF_ha = DF_h.copy()
df = DF_ha[cont].copy()
for var in df.columns.values:
    
    if var in ['T59','Comuna']:
        continue
    
    series = df[var]

    # Skip if all NaN
    if series.isna().all():
        continue
    
    # If the series starts with NaNs, find the first valid index
    first_valid = series.first_valid_index()
    series = series.loc[first_valid:]  # cut off leading NaNs
    
    # Now fill possible gaps inside (but not at the start)
    series = series.interpolate()

    # Extraemos señal
    y = series.values
    N = len(y)

    # Apply FFT
    fft_vals = np.fft.fft(y)
    freqs = np.fft.fftfreq(N, d=1/24)  # d=1 since data is daily 
    
    # Find the closest matching indices for annual and semiannual
    annual_freq = 1 / 365
    semiannual_freq = 2 / 365

    # Indices for positive frequencies
    pos_freqs = freqs[:N//2]
    annual_idx = np.argmin(np.abs(pos_freqs - annual_freq))
    semiannual_idx = np.argmin(np.abs(pos_freqs - semiannual_freq))
    
    # Zero out all but the 0th, annual, and semiannual frequencies
    fft_filtered = np.zeros_like(fft_vals)
    fft_filtered[0] = fft_vals[0]  # Keep the mean
    fft_filtered[annual_idx] = fft_vals[annual_idx]
    fft_filtered[-annual_idx] = fft_vals[-annual_idx]
    fft_filtered[semiannual_idx] = fft_vals[semiannual_idx]
    fft_filtered[-semiannual_idx] = fft_vals[-semiannual_idx]

    
    # Inverse FFT to get the anomaly signal (seasonal cycle)
    seasonal_cycle = np.fft.ifft(fft_filtered).real
    
    # Reemplazamos serie filtrada por ciclo anual y semianual
    DF_ha.loc[series.index, var] = y - seasonal_cycle
    
del df

######################################################################
#%% Datos 6-horarios Anomalía Anual-Semianual ###### NO CORRER !!! ###



# Quitamos ciclo anual y semianual
DF_6ha = DF_6h.copy()
df = DF_6ha.copy()
df = df.asfreq('6h').interpolate()
for var in df.columns.values:
    # Extraemos señal
    y = df[var].values
    N = len(y)


    # Apply FFT
    fft_vals = np.fft.fft(y)
    freqs = np.fft.fftfreq(N, d=6/24)  # d=1 since data is daily
    
    # Find the closest matching indices for annual and semiannual
    annual_freq = 1 / 365
    semiannual_freq = 2 / 365
    
    # Indices for positive frequencies
    pos_freqs = freqs[:N//2]
    annual_idx = np.argmin(np.abs(pos_freqs - annual_freq))
    semiannual_idx = np.argmin(np.abs(pos_freqs - semiannual_freq))
    
    # Zero out all but the 0th, annual, and semiannual frequencies
    fft_filtered = np.zeros_like(fft_vals)
    fft_filtered[0] = fft_vals[0]  # Keep the mean
    fft_filtered[annual_idx] = fft_vals[annual_idx]
    fft_filtered[-annual_idx] = fft_vals[-annual_idx]
    fft_filtered[semiannual_idx] = fft_vals[semiannual_idx]
    fft_filtered[-semiannual_idx] = fft_vals[-semiannual_idx]
    
    # Inverse FFT to get the anomaly signal (seasonal cycle)
    seasonal_cycle = np.fft.ifft(fft_filtered).real
    
    # Reemplazamos serie filtrada por ciclo anual y semianual
    DF_6ha[var] = y - seasonal_cycle
    
del df

#########################################################################
#%% Climatological Daily Cycle: Anomalía Anual-Semianual-Diaria a met ###

# Quitamos ciclo diario estacional centrado en +-45 días a variables meteo 

# Seleccionamos variables meteo
df = DF_ha[met].copy()
df = df.asfreq('h').interpolate()  # 'h' o '6h'
for var in df.columns:
    # Calculamos cdc con ventana ±45-días (3 meses) y computamos anomalía
    DF_ha[var] =  df[var] - cdc.build_cdc_vect(df, col=var, window_days=45)
    
for c in ['_VE','_CQ','_CC','_princ','40_princ','_quint','_dmc']:
    DF_ha['wd'+c] = np.rad2deg(np.arctan2(-1*(DF_ha['u'+c]/DF_ha['ws'+c]),
                                         -1*(DF_ha['v'+c]/DF_ha['ws'+c])))% 360
# Agragamos diferenical de presión
DF_ha["slp_dmc_diff"] = DF_ha["slp_dmc"].rolling(window=12,center=True).mean()\
                                    .diff(periods=-3)*(-1)  
                                    

# Hacemos nan valores que no son datos de ERA5
mask = (DF_ha.index.hour != 2) & (DF_ha.index.hour != 8) &\
       (DF_ha.index.hour != 14) & (DF_ha.index.hour != 20)
DF_ha.loc[mask,ERA5.columns] = float('nan')
    
# Guardamos
# DF_ha.index.names = ['date']
# DF_ha.to_csv(path_data+'DF_ha.csv')

# Agregamos slp_dms_diff a met
met.append('slp_dmc_diff')

    
################################
#%% Datos diarios y en casos ###

# Los archivos originales (DF_d.csv y DF_dhm.csv) se dejarán con la media
# en contaminantes, además se dejará un archivo del tipo "_ContMean" para ambos 

#####################
### Datos Diarios ###
DF_d = pd.DataFrame([], columns=DF_h.columns).astype(DF_h.dtypes)
DF_d[met] = DF_h[met].resample('D').mean()
DF_d[cont] = DF_h[cont].resample('D').mean()
DF_d = pd.concat([T59,DF_d], axis=1)

# resampleamos wd en base a U y V
for c in ['_VE','_CQ','_CC','_princ','40_princ','_quint','_dmc']:
    DF_d['wd'+c] = np.rad2deg(np.arctan2(-1*(DF_d['u'+c]/DF_d['ws'+c]),
                                         -1*(DF_d['v'+c]/DF_d['ws'+c])))% 360

# Guardamos
# DF_d.index.names = ['date']
# DF_d.to_csv(path_data+'DF_d.csv')

#################################
### Dato diario pero en casos ###


# Seleccionamos de Horas Hábiles: 07 a 21 horas
DF_dhh = DF_h.copy()
mask =  (DF_h.index.hour < 7) | (21 < DF_h.index.hour)
DF_dhh.loc[mask] = np.nan
DF_dhh[met] = DF_dhh[met].resample('D').mean()
DF_dhh[cont] = DF_dhh[cont].resample('D').mean()
DF_dhh = DF_dhh.resample('D').asfreq()
DF_dhh = pd.concat([T59,DF_dhh], axis=1)

# Seleccionamos de Horas No Hábiles: 22 a 06 horas
DF_dhnh = DF_h.copy()
DF_dhnh.index = DF_dhnh.index + pd.Timedelta(hours=2)
mask = (DF_dhnh.index.hour > 8) 
DF_dhnh.loc[mask] = np.nan
DF_dhnh[met] = DF_dhnh[met].resample('D').mean()
DF_dhnh[cont] = DF_dhnh[cont].resample('D').mean()
DF_dhnh = DF_dhnh.resample('D').asfreq()
DF_dhnh = DF_dhnh.iloc[:-1]
DF_dhnh = pd.concat([T59, DF_dhnh], axis=1)


# Seleccionamos Horas de Mañana: 05 a 11
DF_dhm = DF_h.copy()
mask =  (DF_h.index.hour < 5) | (11 < DF_h.index.hour)
DF_dhm.loc[mask] = np.nan
DF_dhm[met] = DF_dhm[met].resample('D').mean()
DF_dhm[cont] = DF_dhm[cont].resample('D').mean()
DF_dhm = DF_dhm.resample('D').asfreq()
DF_dhm = pd.concat([T59,DF_dhm], axis=1)

# resampleamos wd en base a U y V
for c in ['_VE','_CQ','_CC','_princ','40_princ','_quint','_dmc']:
    DF_dhh['wd'+c] = np.rad2deg(np.arctan2(-1*(DF_dhh['u'+c]/DF_dhh['ws'+c]),
                                         -1*(DF_dhh['v'+c]/DF_dhh['ws'+c])))% 360
    DF_dhnh['wd'+c] = np.rad2deg(np.arctan2(-1*(DF_dhnh['u'+c]/DF_dhnh['ws'+c]),
                                         -1*(DF_dhnh['v'+c]/DF_dhnh['ws'+c])))% 360
    DF_dhm['wd'+c] = np.rad2deg(np.arctan2(-1*(DF_dhm['u'+c]/DF_dhm['ws'+c]),
                                         -1*(DF_dhm['v'+c]/DF_dhm['ws'+c])))% 360
    
# Guardamos DF_dhm
# DF_dhm['T59'] = T59['T59']
# DF_dhm.index.names = ['date']
# DF_dhm.to_csv(path_data+'DF_dhm.csv')


#########################################
#%% Datos diarios Anomalía y en casos ###


# Los archivos originales (DF_da.csv y DF_dhma.csv) se dejarán con la media
# en contaminantes, además se dejará un archivo del tipo "_ContMean" para ambos 

#######################
### Anomalía diaria ###
DF_da = pd.DataFrame([], columns=DF_ha.columns).astype(DF_ha.dtypes)
DF_da[met] = DF_ha[met].resample('D').mean()
DF_da[cont] = DF_ha[cont].resample('D').mean()
DF_da = pd.concat([T59,DF_da], axis=1)

# resampleamos wd en base a U y V
for c in ['_VE','_CQ','_CC','_princ','40_princ','_quint','_dmc']:
    DF_da['wd'+c] = np.rad2deg(np.arctan2(-1*(DF_da['u'+c]/DF_da['ws'+c]),
                                         -1*(DF_da['v'+c]/DF_da['ws'+c])))% 360


#####################################
### Anomalía diaria pero en casos ###

# DF_da, DF_dca = rf.anomalia_d(DF_d)
# DF_dhha, brp = rf.anomalia_d(DF_dhh)
# DF_dhnha, brp = rf.anomalia_d(DF_dhnh)
# DF_dhma, brp = rf.anomalia_d(DF_dhm)

# Seleccionamos de Horas Hábiles: 07 a 21 horas
DF_dhha = DF_ha.copy()
mask =  (DF_ha.index.hour < 7) | (21 < DF_ha.index.hour)
DF_dhha.loc[mask] = np.nan
DF_dhha[met] = DF_dhha[met].resample('D').mean()
DF_dhha[cont] = DF_dhha[cont].resample('D').mean()
DF_dhha = DF_dhha.resample('D').asfreq()
DF_dhha = pd.concat([T59,DF_dhha], axis=1)

# Seleccionamos de Horas No Hábiles: 22 a 06 horas
DF_dhnha = DF_ha.copy()
DF_dhnha.index = DF_dhnha.index + pd.Timedelta(hours=2)
mask = (DF_dhnha.index.hour > 8) 
DF_dhnha.loc[mask] = np.nan
DF_dhnha[met] = DF_dhnha[met].resample('D').mean()
DF_dhnha[cont] = DF_dhnha[cont].resample('D').mean()
DF_dhnha = DF_dhnha.resample('D').asfreq()
DF_dhnha = DF_dhnha.iloc[:-1]
DF_dhnha = pd.concat([T59, DF_dhnha], axis=1)


# Seleccionamos Horas de Mañana: 05 a 11
DF_dhma = DF_ha.copy()
mask =  (DF_ha.index.hour < 5) | (11 < DF_ha.index.hour)
DF_dhma.loc[mask] = np.nan
DF_dhma[met] = DF_dhma[met].resample('D').mean()
DF_dhma[cont] = DF_dhma[cont].resample('D').mean()
DF_dhma = DF_dhma.resample('D').asfreq()
DF_dhma = pd.concat([T59,DF_dhma], axis=1)

# resampleamos wd en base a U y V
for c in ['_VE','_CQ','_CC','_princ','40_princ','_quint','_dmc']:
    DF_dhha['wd'+c] = np.rad2deg(np.arctan2(-1*(DF_dhha['u'+c]/DF_dhha['ws'+c]),
                                         -1*(DF_dhha['v'+c]/DF_dhha['ws'+c])))% 360
    DF_dhnha['wd'+c] = np.rad2deg(np.arctan2(-1*(DF_dhnha['u'+c]/DF_dhnha['ws'+c]),
                                         -1*(DF_dhnha['v'+c]/DF_dhnha['ws'+c])))% 360
    DF_dhma['wd'+c] = np.rad2deg(np.arctan2(-1*(DF_dhma['u'+c]/DF_dhma['ws'+c]),
                                         -1*(DF_dhma['v'+c]/DF_dhma['ws'+c])))% 360


# Guardamos
# DF_da.index.names = ['date']
# DF_da.to_csv(path_data+'DF_da.csv')
# DF_dhma['T59'] = T59['T59']
# DF_dhma.index.names = ['date']
# DF_dhma.to_csv(path_data+'DF_dhma.csv')

# del brp
#%% Vemos comunas de intoxicados

# Mínimo de intoxicados a utilizar
N_intc = 1

# Obtenemos días con más intoxicados
data = T59.copy()
mask_int = (data['T59'] >= N_intc)
data = data.loc[mask_int]
data = data.sort_values(by='T59',ascending=False)

# Guardamos índices por comuna
mask_Q = (T59['Comuna'] == 'Quintero') & (T59['T59'] >= N_intc)
mask_P = (T59['Comuna'] == 'Puchuncaví') & (T59['T59'] >= N_intc)
mask_QP = (T59['Comuna'] == 'Quintero y Puchuncaví') & (T59['T59'] >= N_intc)


#########################################
#########################################
#%%######### SCATTERPLOTS ###############
#########################################
#########################################

###########################################
#%% Vemos Scatter entre variables y T59 ###


# Columnas y Filas
C = 8
F = 3
var = 'T59'
data = DF_dhh.copy()

fig, axs = plt.subplots(F,C,figsize=(22,10),layout='constrained',sharey=True)
props = dict(boxstyle='round', facecolor='lightgrey', alpha=0.5)

# plot = [
#         ['blh_era5','p_dmc','r_dmc'],
#         ['ies_princ','t_dmc','hr_dmc'],
#         ['ws_dmc','u_dmc','v_dmc'],
#         ['ws_princ','u_princ','v_princ'],
#         ['ws_VE','u_VE','v_VE'],
#         ['ws_CQ','u_CQ','v_CQ'],
#         ]

plot = [
        ['HCNM_VE','HCNM_CQ','HCNM_CC'],
        ['MP25_VE','MP25_CQ','MP25_CC'],
        ['MP10_VE','MP10_CQ','MP10_CC'],
        ['CO_VE','CO_CQ','CO_CC'],
        ['SO2_VE','SO2_CQ','SO2_CC'],
        ['NO2_VE','NO2_CQ','NO2_CC'],
        ['NO_VE','NO_CQ','NO_CC'],
        ['O3_VE','O3_CQ','O3_CC'],
        ]

for c in range(C):
    for f in range(F):
        # definimos x
        x = plot[c][f]
        #ploteamos
        corr = "%.2f" % data[[var,x]].corr().loc[var,x]
        sns.scatterplot(data,x=x,y=var,ax=axs[f,c])
        axs[f,c].grid(alpha=0.5)
        axs[f,c].text(0.75, 0.95, r'$\rho$='+corr, transform=axs[f,c].transAxes,
                      fontsize=10,verticalalignment='top', bbox=props)
        axs[f,c].set_xlabel(x, fontweight='bold')
        
# Main
fig.suptitle(f'Scatter Plots de variables diarias v/s {var} (serie diaria total)',
             fontsize=14)

#############################################################################
#%% Vemos Scatter entre variables y T59 tomando solo días con intoxicados ###

data = DF_d.copy()

## Hacemos Nan días sin intoxicados
mask =  (data['T59'] <= 80)
data.loc[mask] = np.nan

# Columnas y Filas
C = 6; F = 3; fs=(20,10)
plot = [
        ['hr_dmc','p_dmc','r_dmc'],
        ['t_dmc','u_dmc','v_dmc'],
        ['ies_princ','u_princ','v_princ'],
        ['HCNM_VE','u_VE','v_VE'],
        ['HCNM_CQ','u_CQ','v_CQ'],
        ['HCNM_CC','u_CC','v_CC']]

# Columnas y Filas
# C = 8; F = 3; fs=(24,10)
# plot = [
#         ['HCNM_VE','HCNM_CQ','HCNM_CC'],
#         ['MP25_VE','MP25_CQ','MP25_CC'],
#         ['MP10_VE','MP10_CQ','MP10_CC'],
#         ['CO_VE','CO_CQ','CO_CC'],
#         ['SO2_VE','SO2_CQ','SO2_CC'],
#         ['NO2_VE','NO2_CQ','NO2_CC'],
#         ['NO_VE','NO_CQ','NO_CC'],
#         ['O3_VE','O3_CQ','O3_CC'],
#         ]

fig, axs = plt.subplots(F,C,figsize=fs,layout='constrained',sharey=True)
props = dict(boxstyle='round', facecolor='lightgrey', alpha=0.5)
for c in range(C):
    for f in range(F):
        # definimos x
        x = plot[c][f]
        #ploteamos
        corr = "%.2f" % data[['T59',x]].corr().loc['T59',x]
        sns.scatterplot(data,x=x,y='T59',ax=axs[f,c])
        axs[f,c].grid(alpha=0.5)
        axs[f,c].text(0.75, 0.95, r'$\rho$ ='+corr, transform=axs[f,c].transAxes,
                      fontsize=10,verticalalignment='top', bbox=props)
        axs[f,c].set_xlabel(x, fontweight='bold')
# Main
fig.suptitle('Scatter Plots de variables diarias v/s T59 (solo días con intoxicaciones)',
             fontsize=14)

#####################################
#%% Scatters de diferente comunas ###

#### Columnas, Filas y horas
LP = ['M']
# LP = ['V','V2']
# LP = ['C','C2']
# LP = ['Q']
LH = ['TD', 'HH', 'HNH', 'HM']
var = 'T59'
#####

### Comparamos tratamiento de datos ###
# variante = 'Normal'; Perc = True; corr = False
# variante = 'Anomalia'; Perc = True; corr = False
# variante = 'Mar-Oct'
V = ['Normal','Anomalia']

# Iteramos por Plot y Hora:
for variante in V:
    Perc = True; corr = False
    for P in LP:
        for H in LH:
            # Definimos variables por casos
            if P == 'M': # Meteo
                plot = [
                        ['blh_era5','ies_princ','r_dmc','ws_dmc'],
                        ['slp_dmc','slp_dmc_diff','t_dmc','hr_dmc'],
                        ]
                C = 4
                F = 2
                W = 10
                L = 5
                plot = list(map(list, zip(*plot)))
                
            elif P == 'V': # Vientos 1
                plot = [
                        ['ws_VE','wd_VE','u_VE','v_VE'],
                        ['ws_princ','wd_princ','u_princ','v_princ'],
                        ['ws_dmc','wd_dmc','u_dmc','v_dmc'],
                        ['ws_CQ','wd_CQ','u_CQ','v_CQ'],
                        ]
                C = 4
                F = 4
                W = 10
                L = 10
                plot = list(map(list, zip(*plot)))
                
            elif P == 'V2': # Vientos 2
                plot = [
                        ['ws40_princ','wd40_princ','u40_princ','v40_princ'],
                        ['ws_quint','wd_quint','u_quint','v_quint'],
                        ['ws_CC','wd_CC','u_CC','v_CC'],
                        ]
                C = 4
                F = 3
                W = 10
                L = 7.5
                plot = list(map(list, zip(*plot)))
                
            elif P == 'C':
                plot = [
                        ['HCNM_VE','HCNM_CQ','SO2_VE','SO2_CQ'],
                        ['MP25_VE','MP25_CQ','NO2_VE','NO2_CQ'],
                        ['MP10_VE','MP10_CQ','NO_VE','NO_CQ'],
                        ['CO_VE','CO_CQ','O3_VE','O3_CQ'],
                        ]
                C = 4
                F = 4
                W = 10
                L = 10
                
            elif P == 'C2': # Contaminantes
                plot = [
                        ['HCNM_VE','HCNM_CQ','HCNM_CC'],
                        ['MP25_VE','MP25_CQ','MP25_CC'],
                        ['MP10_VE','MP10_CQ','MP10_CC'],
                        ['SO2_VE','SO2_CQ','SO2_CC'],
                        ]
                C = 4
                F = 3
                W = 10
                L = 7.5
                
            elif P == 'Q':
                # plot = [
                #         ['blh_era5','ies_princ','ws_dmc','CO_VE'],
                #         ['r_dmc','slp_dmc','slp_dmc_diff','hr_dmc'],
                #         ['HCNM_CQ','NO_CQ','NO2_CQ','O3_CQ'],
                #         ['SO2_CQ','CO_CQ','MP25_CQ','MP10_CQ']
                #         ]
                plot = [
                        ['HCNM_CQ','NO_CQ','NO2_CQ','O3_CQ'],
                        ['SO2_CQ','MP25_CQ','MP10_CQ','CO_CQ'],
                        ['ies_princ','blh_era5','hr_dmc','r_dmc'],
                        ['ws_dmc','u_dmc','v_dmc','slp_dmc'],
                        ['t_dmc','u_princ','v_CC','slp_dmc_diff'],
                        ]
                cont_Q = ['HCNM_CQ','NO_CQ','NO2_CQ','O3_CQ',
                        'SO2_CQ','CO_CQ','MP25_CQ','MP10_CQ']
                C = 5
                F = 4
                W = 12.5
                L = 10
                # plot = list(map(list, zip(*plot)))
                
            elif P == 'KM':
                plot = [
                        ['HCNM_CQ','MP25_CQ'],
                        ['ies_princ','ws_dmc']
                        ]
                cont_Q = ['HCNM_CQ','NO_CQ','NO2_CQ','O3_CQ',
                        'SO2_CQ','CO_CQ','MP25_CQ','MP10_CQ']
                C = 2
                F = 2
                W = 2.5*C
                L = 2.5*F
                # plot = list(map(list, zip(*plot)))
        
        
            if H == 'HH': # Horario Hábil
                data = DF_dhh.copy() if variante!='Anomalia' else DF_dhha.copy()
                data['CO_VE'] = DF_d['CO_VE']
                h = 'horas hábiles (07 a 21)'
            elif H == 'HNH': # Horario No Hábil
                data = DF_dhnh.copy() if variante!='Anomalia' else DF_dhnha.copy()
                data['CO_VE'] = DF_d['CO_VE']
                h = 'horas no hábiles (22 a 06)'
            elif H == 'HM': # Horas Mañana
                data = DF_dhm.copy() if variante!='Anomalia' else DF_dhma.copy()
                data['CO_VE'] = DF_d['CO_VE']
                h = 'horas de mañana (05 a 11)'
            elif H == 'TD': # Todo Día
                data = DF_d.copy() if variante!='Anomalia' else DF_da.copy()
                data['CO_VE'] = DF_d['CO_VE']
                h = 'día completo'
                
            # sys.exit()
            # Nos aseguramos de que existan las columnas T59 y Comuna
            data['T59'] = T59['T59']
            data['Comuna'] = T59['Comuna']
        
            
            ## Seleccionamos y hacemos nan meses que no utilizaremos para ciclo diario
            if variante == 'Mar-Oct':
                mask_mes = (DF_d.index.month<3)|(DF_d.index.month>10)
                data.loc[mask_mes] = float('nan')
                
            
        
            fig, axs = plt.subplots(F,C,figsize=(W,L),layout='constrained',sharey=True)
            
            for c in range(C):
                for f in range(F):
                    # Definimos x
                    x = plot[c][f]
                    if corr == True:
                        corr_Q = "%.2f" % data.loc[mask_Q,[x,var]].corr().loc[var,x]
                        corr_P = "%.2f" % data.loc[mask_P,[x,var]].corr().loc[var,x]
                        corr_QP = "%.2f" % data.loc[mask_QP,[x,var]].corr().loc[var,x]
                        corr_int =  "%.2f" % data.loc[mask_int,[x,var]].corr().loc[var,x]
                        label_Q = r'$\rho_{Q}$='+str(corr_Q)
                        label_P = r'$\rho_{P}$='+str(corr_P)
                        label_QP = r'$\rho_{QP}$='+str(corr_QP)
                        label_int = r'$\rho_{Tot}$='+str(corr_int)
                    else:
                        label_Q = 'Q'
                        label_P = 'P'
                        label_QP = 'QP'
                        label_int = 'Tot.'
                        
                    # Creamos axi en base a C y F
                    if C == 1:
                        axi = axs[f]
                    elif F == 1:
                        axi = axs[c]
                    else:
                        axi = axs[f,c]
                        
                    # Ploteamos
                    sc=100
                    sns.scatterplot(data[mask_Q],x=x,y=var,ax=axi,color='b',
                                    marker='.',label=label_Q,
                                    s=sc, edgecolor='k',linewidth=0.15,zorder=2)
                    sns.scatterplot(data[mask_QP],x=x,y=var,ax=axi,color='r',
                                    marker='.',label=label_QP,
                                    s=sc, edgecolor='k',linewidth=0.15,zorder=2)
                    if len(data.loc[mask_P,[x,var]]) > 5:
                        sns.scatterplot(data[mask_P],x=x,y=var,ax=axi,color='gold',
                                        marker='.',label=label_P,
                                        s=sc, edgecolor='k',linewidth=0.15,zorder=2)
                    ## Totales en el fondo (gris) ##
                    # sns.scatterplot(data[mask_int],x=x,y=var,ax=axi,color='grey',
                    #                 label=label_int, zorder=1,
                    #                 s=70, alpha=0.6, edgecolor='grey',linewidth=0.1)
    
                    axi.grid(alpha=0.5)
                    axi.set_xlabel(x, fontweight='bold',fontsize=13.5)
                    axi.set_ylabel('N° Intx.',fontsize=13.5)
                    
                    
                    # Leyenda solo en primer plot en caso de no indicar corr
                    if corr == False and c==C-1 and f==0 and P !='C': 
                        axi.legend(loc='upper left', fontsize=10, framealpha=0.4,
                                        handlelength=1)
                    elif corr == False and c!=C-1 or f!=0: 
                        axi.legend_=None
                    elif corr == True:
                        axi.legend(loc='upper left', fontsize=6, framealpha=0.4,
                                        handlelength=1) 
                    
                    # Sacar ticks y labels de vacío
                    if x == 'CO_VE':
                        axi.set_xlabel(None)
                        axi.set_ylabel(None)
                        axi.set_xticklabels([])
                        axi.tick_params(axis='both', length=0, labelbottom=False)
                        axi.grid(False)
                    # Q sentence
                    Q_c = (P=='Q' and x in cont_Q)
                    # Legenda en ax de CO_VE para percentiles
                    if x == 'CO_VE' and Perc == True:
                        le = [
                            Line2D([0], [0], color='tab:blue',ls=ls[1],alpha=0.35,label='Percentil 25'),
                            Line2D([0], [0], color='grey',ls=ls[1],alpha=0.7, label='Mediana'),
                            Line2D([0], [0], color='tab:red',ls=ls[1],alpha=0.35,label='Percentil 75'),
                            Line2D([0], [0], color='tab:red',ls=ls[5],alpha=0.45,label='Percentil 90'),
                            Line2D([0], [0], color='tab:red',ls=ls[4],alpha=0.45,label='Percentil 95'),
                            Line2D([0], [0], color='tab:red',ls=ls[3],alpha=0.45,label='Percentil 99')
                            ]
                        le = le if P[0] in ['C','Q'] else le[0:len(le)-3]
                        axi.legend(handles=le[::-1],framealpha=1,
                                        fontsize=10,handlelength=7,loc='center')
    
                    # Mediana Total y percentiles
                    elif Perc == True and x[0:2]!='wd':
                        axi.axvline(data[x].quantile(0.25),c='tab:blue',ls=ls[1],alpha=0.3, zorder=0)
                        axi.axvline(data[x].quantile(0.50),c='grey',ls=ls[1],alpha=0.7, zorder=0)
                        axi.axvline(data[x].quantile(0.75),c='tab:red',ls=ls[1],alpha=0.3, zorder=0)
                        if P == 'C' or Q_c:
                            axi.axvline(data[x].quantile(0.90),c='tab:red',ls=ls[5],alpha=0.4, zorder=0)
                            axi.axvline(data[x].quantile(0.95),c='tab:red',ls=ls[4],alpha=0.4, zorder=0)
                            axi.axvline(data[x].quantile(0.99),c='tab:red',ls=ls[3],alpha=0.4, zorder=0)
                        
                        
                    # xlim en casos
                    if x[0] == 'u':
                        axi.set_xlim(-2.5,2.5)
                    elif x[0] == 'v':
                        axi.set_xlim(-5.2,5.2)
                    elif x[0:2] == 'ws':
                        axi.set_xlim(-0.2,5.4)
                    elif x[0:2] == 'wd':
                        axi.set_xlim(-0.2,360.2)
                    # elif x == 'p_dmc':
                    #     axi.set_xlim(1010,1030)
                    
                    if variante == 'Anomalia':
                        # xlim en casos
                        if x[0] == 'u':
                            axi.set_xlim(-2.5,2.5)
                        elif x[0] == 'v':
                            axi.set_xlim(-5.2,5.2)
                        elif x[0:2] == 'ws':
                            axi.set_xlim(-4,4)
                        elif x[0:2] == 'wd':
                            axi.set_xlim(-0.2,360.2)
                    # Ticks label size        
                    axi.tick_params('both',labelsize=11.5)
        
            # Main
            if P == 'KM' and variante == 'Anomalia':
                fig.suptitle(f'Anomalías diarias v/s Intoxicados, '+\
                             # ' (días con min. '+str(N_intc)+' intx.)'+\
                             h,fontsize=15)
            elif variante == 'Anomalia':
                fig.suptitle(f'Anomalías diarias v/s Intoxicados'+\
                             # ' (días con min. '+str(N_intc)+' intx.)'+\
                             ', '+h,fontsize=15)
    
            else:
                fig.suptitle(f'Variables diarias v/s Intoxicados'+\
                             # ' (días con min. '+str(N_intc)+' intx.)'+\
                             ', '+h,fontsize=15)
            # Guardamos
            if P in ['C2','V2']:
                path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados'+\
                        '/Sección 2/ScatterPlots/'+P[0]+'/'+variante+'/'+P+'/'
            elif P == 'KM':
                path = 'C:/Users/felip/Desktop/U/Tesis/Simposio_CR2/figs/'
            else:
                path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados'+\
                        '/Sección 2/ScatterPlots/'+P+'/'+variante+'/'
            # Chequeamos existencia de directorio
            if not os.path.exists(path[0:len(path)-1]):
                os.makedirs(path[0:len(path)-1])
                print(f"Directorio '{path[0:len(path)-1]}' fue creado.")
            fig.savefig(path+'ScatterPlots_'+P+'_'+H+'_'+variante+'.png', dpi=300)


#########################################
#########################################
#%%########### REGRESIONES ##############
#########################################
#########################################

#######################################
#%% Seleccionamos la serie completa ###
#######################################

########################################################
#%% Regresión Lineal Simple por variable: Coef. y R2 ###
##  HORAS PREVIAS DE A 1 HORA !!



variables = [
    
            # 'ies_princ','t_dmc','hr_dmc','slp_dmc','r_dmc',
            # 'ws_VE','ws_princ','ws_dmc','ws_CQ',
            
            # 'u_princ','v_princ',
            # 'u_dmc','v_dmc',
            # 'u_VE','v_VE',
            # 'u_CQ','v_CQ',
        
        
            'HCNM_CQ','CO_CQ','SO2_CQ','NO2_CQ','NO_CQ','O3_CQ',
            'MP25_CQ','MP10_CQ',
        
            # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
            # 'MP25_VE','MP10_VE',

            ]
Hi = 12
vcb = 10
N_int = 30

# Corremos
dias = np.ones(24+Hi)
resultados = {}  # diccionario para guardar coef y R2 por variable
for var in variables:
    coef_list = []
    r2_list = []
    dias_validos = []
    
    for i in range(-Hi, 24):
        if var[0].isupper():    
            data = DF_h[[var]].copy()
        else:
            data = DF_ha[[var]].copy()

        # Seleccionamos horas
        if i<0:
            data = data.shift(periods=-i)
            hi = 0
        else:
            hi = i
        mask = (data.index.hour != hi)            
        data.loc[mask] = np.nan
        data = data.resample('D').mean()
        data['T59'] = T59['T59']
        
        ######################################
        ### Hacemos 0 datos a no utilizar: ###    
        # Nos quedamos días sin intoxicados o con menos de cierto N 
        # mask =  (T59['T59'] <= N_int)
        ## Nos quedamos solo con eventos en Quintero
        mask = (T59['Comuna'] != 'Quintero')|(T59['T59'] <= N_int)
        ## Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
        # mask = (T59['Comuna'] == 'Puchuncaví')|(T59['T59'] <= N_int)
        ## Nos quedamos solo con eventos en Puchuncaví
        # mask = (T59['Comuna'] != 'Puchuncaví')|(T59['T59'] <= N_int)
        ## Nos quedamos con eventos en Quintero y Puchuncaví
        # mask = (T59['Comuna'] != 'Quintero y Puchuncaví')|(T59['T59'] <= N_int)
        ## Hacemos Nan los datos seleccionados:
        data.loc[mask,'T59'] = 0
        data_T59 = data['T59']
        ########################################
        
        # estandarizamos
        data = (data - data.mean()) / data.std()
        data['T59'] = data_T59#T59['T59'] # incluimos T59 sin estandarizar
        # Corremos regresión lineal
        df_var = data.copy()
        df_var = df_var[['T59', var]].dropna()
        dias[i] = len(df_var)
        if len(df_var) < 5:
            coef_list.append(np.nan)
            r2_list.append(np.nan)
            dias_validos.append(0)
            continue

        X = sm.add_constant(df_var[[var]])
        y = df_var['T59']
        model = sm.OLS(y, X).fit()
        
        coef_list.append(model.params[var])
        r2_list.append(model.rsquared)
        dias_validos.append(len(df_var))

    df_result = pd.DataFrame({
        'Hora': list(range(-Hi, 24)),
        'Coef': coef_list,
        'R2': r2_list,
        'N': dias_validos
    }).set_index('Hora')
    
    resultados[var] = df_result
    

## Ploteamos ##
n_vars = len(variables)
fig = plt.figure(figsize=(15, n_vars * 2), layout='constrained')
gs = fig.add_gridspec(n_vars, 1)  # 1 columna, n filas

# Para capturar los valores de coeficientes (para colorbar)
heatmaps = []

for i, var in enumerate(variables):
    df = resultados[var]
    ax = fig.add_subplot(gs[i, 0])  # Solo un eje por fila

    # Heatmap (sin colorbar por ahora)
    hm = sns.heatmap(
        df[['Coef']].T, cmap='bwr', vmin=-vcb, vmax=vcb,
        ax=ax, cbar=False, xticklabels=True, yticklabels=[var],
        linewidths=0.05, linecolor='gray'
    )
    heatmaps.append(hm)
    
    ax.axvline(x=Hi, color='k', ls='--', lw=1.5)
    ax.set_xticks(np.arange(0.5, 24.5 + Hi, 1))
    ax.set_xticklabels(list(range(-Hi, 24)), rotation=0)
    ax.set_yticklabels([var], rotation=90, fontsize=13,fontweight='bold')
    ax.set_xlabel(None)


    # R²
    ax2 = ax.twinx()
    ax2.plot(np.arange(0.5, 24.5 + Hi, 1), df['R2'], marker='o',
             color='k', lw=1.5, alpha=0.6)
    ax2.set_ylim(0, 0.5)
    ax2.set_ylabel('R²', fontsize=10, rotation=270, labelpad=15)
    ax2.grid(axis='y',linestyle='--', linewidth=0.5,alpha=0.5)
    ax2.set_xlabel(None)

# === Añadir colorbar global ===
# Tomamos el último heatmap y su mapeo de color
norm = mpl.colors.Normalize(vmin=-vcb, vmax=vcb)
cm = plt.cm.ScalarMappable(cmap='bwr', norm=norm)
cm.set_array([])

# Agregamos al costado derecho
cbar = fig.colorbar(cm, ax=[fig.axes[i*2] for i in range(n_vars)],  # solo los axes de coef
                    orientation='vertical', aspect=30, pad=0.01)
cbar.set_label('Coeficiente del modelo', fontsize=12)

# Título principal
fig.suptitle(
    f'Regresiones lineales simples por variable, Serie total'
    f',{Hi} horas previas, de a 1 hora',
    fontsize=15
)
fig.supxlabel('Hora')


#################################################
#%% Seleccionamos solo días con Intoxiaciones ###
#################################################

########################################################
#%% Regresión Lineal Simple por variable: Coef. y R2 ###
##  HORAS PREVIAS DE A 1 HORA !!



variables = [
    
            # 'ies_princ','t_dmc','hr_dmc','slp_dmc','r_dmc',
            # 'ws_VE','ws_princ','ws_dmc','ws_CQ',
            
            # 'u_princ','v_princ',
            # 'u_dmc','v_dmc',
            # 'u_VE','v_VE',
            # 'u_CQ','v_CQ',
        
        
            'HCNM_CQ','CO_CQ','SO2_CQ','NO2_CQ','NO_CQ','O3_CQ',
            'MP25_CQ','MP10_CQ',
        
            # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
            # 'MP25_VE','MP10_VE',

            ]
Hi = 12
vcb = 100
N_int = 1


# Corremos
dias = np.ones(24+Hi)
resultados = {}  # diccionario para guardar coef y R2 por variable
for var in variables:
    coef_list = []
    r2_list = []
    dias_validos = []
    
    for i in range(-Hi, 24):
        # Seleccionamos DF a utilizar
        if var[0].isupper():    
            data = DF_h[[var]].copy()
        else:
            data = DF_ha[[var]].copy()
        # Calculamos promedio diario, en caso de ser horas de día previo
        # se corre la serie para que la hora quede en el día
        if i<0:
            data = data.shift(periods=-i)
            hi = 0
        else:
            hi = i
        mask = (data.index.hour != hi)            
        data.loc[mask] = np.nan
        data = data.resample('D').mean()
        data['T59'] = T59['T59']
        
        ########################################
        ### Hacemos Nan datos a no utilizar: ###    
        # Nos quedamos días sin intoxicados o con menos de cierto N 
        # mask =  (data['T59'] <= N_int)
        ## Nos quedamos solo con eventos en Quintero
        # mask = (T59['Comuna'] != 'Quintero')|(data['T59'] <= N_int)
        ## Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
        mask = (T59['Comuna'] == 'Puchuncaví')|(data['T59'] <= N_int)
        ## Nos quedamos solo con eventos en Puchuncaví
        # mask = (T59['Comuna'] != 'Puchuncaví')|(data['T59'] <= N_int)
        ## Nos quedamos con eventos en Quintero y Puchuncaví
        # mask = (T59['Comuna'] != 'Quintero y Puchuncaví')|(data['T59'] <= N_int)
        ## Hacemos Nan los datos seleccionados:
        data.loc[mask] = np.nan
        data_T59 = data['T59']
        ########################################
        
        # Estandarizamos datos
        data = (data - data.mean()) / data.std()
        data['T59'] = data_T59 # Usamos T59 sin estandarizar
        
        ### Corremos Regresión Lineal ###
        df_var = data.copy()
        df_var = df_var[['T59', var]].dropna()
        dias[i] = len(df_var)
        if len(df_var) < 5:
            coef_list.append(np.nan)
            r2_list.append(np.nan)
            dias_validos.append(0)
            continue

        X = sm.add_constant(df_var[[var]])
        y = df_var['T59']
        model = sm.OLS(y, X).fit()
        
        coef_list.append(model.params[var])
        r2_list.append(model.rsquared)
        dias_validos.append(len(df_var))

    df_result = pd.DataFrame({
        'Hora': list(range(-Hi, 24)),
        'Coef': coef_list,
        'R2': r2_list,
        'N': dias_validos
    }).set_index('Hora')
    
    resultados[var] = df_result
    

## Ploteamos ##
n_vars = len(variables)
fig = plt.figure(figsize=(15, n_vars * 2), layout='constrained')
gs = fig.add_gridspec(n_vars, 1)  # 1 columna, n filas

# Para capturar los valores de coeficientes (para colorbar)
heatmaps = []

for i, var in enumerate(variables):
    df = resultados[var]
    ax = fig.add_subplot(gs[i, 0])  # Solo un eje por fila

    # Heatmap (sin colorbar por ahora)
    hm = sns.heatmap(
        df[['Coef']].T, cmap='bwr', vmin=-vcb, vmax=vcb,
        ax=ax, cbar=False, xticklabels=True, yticklabels=[var],
        linewidths=0.05, linecolor='gray'
    )
    heatmaps.append(hm)
    
    ax.axvline(x=Hi, color='k', ls='--', lw=1.5)
    ax.set_xticks(np.arange(0.5, 24.5 + Hi, 1))
    ax.set_xticklabels(list(range(-Hi, 24)), rotation=0)
    ax.set_yticklabels([var], rotation=90, fontsize=13,fontweight='bold')
    ax.set_xlabel(None)


    # R²
    ax2 = ax.twinx()
    ax2.plot(np.arange(0.5, 24.5 + Hi, 1), df['R2'], marker='o',
             color='k', lw=1.5, alpha=0.6)
    ax2.set_ylim(0, 1)
    ax2.set_ylabel('R²', fontsize=10, rotation=270, labelpad=15)
    ax2.grid(axis='y',linestyle='--', linewidth=0.5,alpha=0.5)
    ax2.set_xlabel(None)

# === Añadir colorbar global ===
# Tomamos el último heatmap y su mapeo de color
norm = mpl.colors.Normalize(vmin=-vcb, vmax=vcb)
cm = plt.cm.ScalarMappable(cmap='bwr', norm=norm)
cm.set_array([])

# Agregamos al costado derecho
cbar = fig.colorbar(cm, ax=[fig.axes[i*2] for i in range(n_vars)],  # solo los axes de coef
                    orientation='vertical', aspect=30, pad=0.01)
cbar.set_label('Coeficiente del modelo', fontsize=12)

# Título principal
fig.suptitle(
    f'Regresiones lineales simples por variable, Casos con Intoxicaciones'
    f' ≥ {N_int} ({dias.max()} días),{Hi} horas previas, de a 1 hora',
    fontsize=15
)
fig.supxlabel('Hora')

########################################################
#%% Regresión Lineal Simple por variable: Coef. y R2 ###
### HORAS PREVIAS DE A 3 HORAS !!

variables = [
    
            'ies_princ','blh_era5','t_dmc','hr_dmc','slp_dmc','r_dmc',
            'ws_VE','ws_princ','ws_dmc','ws_CQ',
            
            # 'u_princ','v_princ',
            # 'u_dmc','v_dmc',
            # 'u_VE','v_VE',
            # 'u_CQ','v_CQ',
        
        
            # 'HCNM_CQ','CO_CQ','SO2_CQ','NO2_CQ','NO_CQ','O3_CQ',
            # 'MP25_CQ','MP10_CQ',
        
            # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
            # 'MP25_VE','MP10_VE',

            ]
Hi = 12
vcb = 100
N_int = 0

# Corremos
dias = np.ones(24+Hi)
resultados = {}  # diccionario para guardar coef y R2 por variable
for var in variables:
    coef_list = []
    r2_list = []
    dias_validos = []

    for i in range(-Hi, 24):
        # Seleccionamos DF a utilizar
        if var[0].isupper() or var == 'r_dmc':    
            data = DF_h[[var]].copy()
        else:
            data = DF_ha[[var]].copy()
        # Calculamos promedio diario, en caso de ser horas de día previo
        # se corre la serie para que la hora quede en el día
        if i <= 0:
            data = data.shift(periods=-i+1)
            hi = 1
        elif i == 23:
            data = data.shift(periods=-1)
            hi = 22
        else:
            hi = i
            
        mask = (data.index.hour < hi-1) | (data.index.hour > hi+1)
        data.loc[mask] = np.nan
        data = data.resample('D').mean()
        data['T59'] = T59['T59']
        
        ########################################
        ### Hacemos Nan datos a no utilizar: ###    
        # Nos quedamos días sin intoxicados o con menos de cierto N 
        mask =  (data['T59'] <= N_int)
        ## Nos quedamos solo con eventos en Quintero
        # mask = (T59['Comuna'] != 'Quintero')|(data['T59'] <= N_int)
        ## Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
        # mask = (T59['Comuna'] == 'Puchuncaví')|(data['T59'] <= N_int)
        ## Nos quedamos solo con eventos en Puchuncaví
        # mask = (T59['Comuna'] != 'Puchuncaví')|(data['T59'] <= N_int)
        ## Nos quedamos con eventos en Quintero y Puchuncaví
        # mask = (T59['Comuna'] != 'Quintero y Puchuncaví')|(data['T59'] <= N_int)
        ## Hacemos Nan los datos seleccionados:
        data.loc[mask] = np.nan
        data_T59 = data['T59']
        ########################################
        
        # Estandarizamos datos
        data = (data - data.mean()) / data.std()
        data['T59'] = data_T59 # Usamos T59 sin estandarizar
        
        ### Corremos Regresión Lineal ###
        df_var = data.copy()
        df_var = df_var[['T59', var]].dropna()
        dias[i] = len(df_var)
        if len(df_var) < 5:
            coef_list.append(np.nan)
            r2_list.append(np.nan)
            dias_validos.append(0)
            continue

        X = sm.add_constant(df_var[[var]])
        y = df_var['T59']
        model = sm.OLS(y, X).fit()
        
        coef_list.append(model.params[var])
        r2_list.append(model.rsquared)
        dias_validos.append(len(df_var))

    df_result = pd.DataFrame({
        'Hora': list(range(-Hi, 24)),
        'Coef': coef_list,
        'R2': r2_list,
        'N': dias_validos
    }).set_index('Hora')
    
    resultados[var] = df_result
    

## Ploteamos ##
n_vars = len(variables)
fig = plt.figure(figsize=(15, n_vars * 2), layout='constrained')
gs = fig.add_gridspec(n_vars, 1)  # 1 columna, n filas

# Para capturar los valores de coeficientes (para colorbar)
heatmaps = []

for i, var in enumerate(variables):
    df = resultados[var]
    ax = fig.add_subplot(gs[i, 0])  # Solo un eje por fila

    # Heatmap (sin colorbar por ahora)
    hm = sns.heatmap(
        df[['Coef']].T, cmap='bwr', vmin=-vcb, vmax=vcb,
        ax=ax, cbar=False, xticklabels=True, yticklabels=[var],
        linewidths=0.05, linecolor='gray'
    )
    heatmaps.append(hm)
    
    ax.axvline(x=Hi, color='k', ls='--', lw=1.5)
    ax.set_xticks(np.arange(0.5, 24.5 + Hi, 1))
    ax.set_xticklabels(list(range(-Hi, 24)), rotation=0)
    ax.set_yticklabels([var], rotation=90, fontsize=13,fontweight='bold')
    ax.set_xlabel(None)


    # R²
    ax2 = ax.twinx()
    ax2.plot(np.arange(0.5, 24.5 + Hi, 1), df['R2'], marker='o',
             color='k', lw=1.5, alpha=0.6)
    ax2.set_ylim(0, 1)
    ax2.set_ylabel('R²', fontsize=10, rotation=270, labelpad=15)
    ax2.grid(axis='y',linestyle='--', linewidth=0.5,alpha=0.5)
    ax2.set_xlabel(None)

# === Añadir colorbar global ===
# Tomamos el último heatmap y su mapeo de color
norm = mpl.colors.Normalize(vmin=-vcb, vmax=vcb)
cm = plt.cm.ScalarMappable(cmap='bwr', norm=norm)
cm.set_array([])

# Agregamos al costado derecho
cbar = fig.colorbar(cm, ax=[fig.axes[i*2] for i in range(n_vars)],  # solo los axes de coef
                    orientation='vertical', aspect=30, pad=0.01)
cbar.set_label('Coeficiente del modelo', fontsize=12)

# Título principal
fig.suptitle(
    f'Regresiones lineales simples por variable, Casos con Intoxicaciones'
    f' ≥ {N_int} ({dias.max()} días),{Hi} horas previas, ventanas de 3 horas',
    fontsize=15
)
fig.supxlabel('Hora')


#########################################
#########################################
#%%######### Ciclos Diarios #############
#########################################
#########################################

# Modificar ciclos para discriminar por comuna o cantidad de intoxicados
# y uso de datos sin ciclo anual y semianual


#%% Calculamos Ciclos diarios

# Seleccionamos variables
# top_dias=12
N_int = 1
# df = DF_met_ha.copy()
df = DF_h.copy()
var =  [
            # 'ies_princ','t_dmc','hr_dmc','slp_dmc','r_dmc',
            # 'ws_VE','ws_princ','ws_dmc','ws_CQ',
            
            # 'u_princ','v_princ',
            # 'u_dmc','v_dmc',
            # 'u_VE','v_VE',
            # 'u_CQ','v_CQ',
        
            'HCNM_CQ','CO_CQ','SO2_CQ','NO2_CQ','NO_CQ','O3_CQ',
            'MP25_CQ','MP10_CQ',
        
            # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
            # 'MP25_VE','MP10_VE',
        ]


## Obtenemos días con más intoxicados
data = T59.copy()
mask_int = (data['T59'] != 0)
data = data.loc[mask_int]
data = data.sort_values(by='T59',ascending=False)


## Seleccionamos días con más de cierto Nde intoxicados
mask =  (T59['T59'] >= N_int)

# Nos quedamos solo con eventos en Quintero
# mask = (T59['Comuna'] == 'Quintero')&(T59['T59'] >= N_int)

# Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
# mask = (T59['Comuna'] != 'Puchuncaví')&(T59['T59'] >= N_int)

# Nos quedamos solo con eventos en Puchuncaví
# mask = (T59['Comuna'] == 'Puchuncaví')&(T59['T59'] >= N_int)

# Nos quedamos con eventos en Quintero y Puchuncaví
# mask = (T59['Comuna'] == 'Quintero y Puchuncaví')&(T59['T59'] <= N_int)



i = 0
for v in var:
    color = COLOR_MAP[i % len(COLOR_MAP)]
    fig, ax = plt.subplots(figsize=(20, 10.5))
    
    # Obtenemos valores de ciclo diarios para variable
    median, q10, q25, q75, q90 = cs.get_cycle_data(DF_h[v],
                                                   'H',[lambda x: x.hour])
    # Ploteamos ciclo diarios 
    x = median.index
    ax.fill_between(x, q10.values, q90.values, color=color, alpha=0.2)
    ax.fill_between(x, q25.values, q75.values, color=color, alpha=0.3)
    ax.plot(x, median.values, marker='o', color=color)
    legend_elements = [
        Line2D([0], [0], color=color, marker='o', label='Mediana'),
        Patch(facecolor=color, alpha=0.3, label='pctl. 25–75'),
        Patch(facecolor=color, alpha=0.2, label='pctl. 10–90')
        ]
    
    ## Ploteamos días con más intoxicaciones
    # for d in range(len(T59.loc[mask])):
    #     if d < len(ls):
    #         ils=d
    #     elif d > len(ls):
    #         ils=d-len(ls)
    #     t1 = data.index[d]
    #     t2 = t1 + datetime.timedelta(hours=23)
    #     alp = 0.6
    #     ax.plot(x,df.loc[t1:t2,v], color='grey',alpha=alp,ls='-',lw=0.3,
    #             zorder=0)

        
    ## Ploteamos días seleccionados con intoxicaciones
    for d in range(len(T59.loc[mask])):
        if d < len(ls):
            ils=d
        elif d > len(ls):
            ils=d-len(ls)
        t1 = data.index[d]
        t2 = t1 + datetime.timedelta(hours=23)
        alp = 0.6
        ax.plot(x,df.loc[t1:t2,v], color='k',alpha=alp,ls=ls[ils],zorder=0)
        legend_elements.append(Line2D([0], [0], color='k',alpha=alp,ls=ls[d],
                                      label=str(t1)[0:-9]+': '+
                                      str(int(data.iloc[d,0]))+' intx.'))
    
    
    ax.set_title(f"Ciclo diario {v}", fontsize=15, weight='bold')
    ax.set_xlabel('Hora')
    ax.set_ylabel(f"{v}", rotation=90,
                  labelpad=10, fontsize=15, weight='bold')
    ax.legend(handles=legend_elements,framealpha=0.6,fontsize=7,
              handlelength=7)
    ax.grid(True)
    ax.set_xticks(range(0, 24)[::2])
    
    # fig.suptitle(title, fontsize=18)
    # plt.subplots_adjust(top=0.93)
    plt.tight_layout()
    plt.show()
    i = i+1
    
#%% Ciclo diario de día N con día N+1 y N-1

# Seleccionamos variables
# top_dias=12
N_int = 80
# df = DF_met_6ha.copy()
df = DF_h.copy()
var =  [
            # 'blh_era5',
            'ies_princ','t_dmc','hr_dmc','p_dmc','r_dmc',
            'wd_dmc','ws_dmc',
            # 'blh_era5','t_era5','hr_era5','p_era5','ws_era5'
            # 'p_dmc','p_era5',
            # 't_dmc','t_era5',
            # 'hr_dmc','hr_era5',
            
            
            # 'ws_VE','ws_princ',
            # 'ws_dmc','ws_CQ',
            # 'ws_era5',
            
            # 'u_VE','v_VE',
            # 'u_princ','v_princ',
            # 'u_dmc','v_dmc',
            # 'u_CQ','v_CQ',
            # 'u_era5','v_era5',
            

            # 'HCNM_CQ','NO2_CQ','NO_CQ','O3_CQ',
            # 'MP25_CQ','MP10_CQ','CO_CQ','SO2_CQ',
        
            # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
            # 'MP25_VE','MP10_VE',
        ]


## Hacemos nan meses que no utilizaremos para ciclo diario
mask = (df.index.month<4)|(df.index.month>7)
df.loc[mask] = float('nan')


## Obtenemos días con más intoxicados
# data = T59.copy()
# mask_int = (data['T59'] != 0)
# data = data.loc[mask_int]
# data = data.sort_values(by='T59',ascending=False)

## Seleccionamos días con más de cierto Nde intoxicados
mask =  (T59['T59'] >= N_int)

# Nos quedamos solo con eventos en Quintero
# mask = (T59['Comuna'] == 'Quintero')&(T59['T59'] >= N_int)

# Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
# mask = (T59['Comuna'] != 'Puchuncaví')&(T59['T59'] > N_int)

# Nos quedamos solo con eventos en Puchuncaví
# mask = (T59['Comuna'] == 'Puchuncaví')&(T59['T59'] >= N_int)

# Nos quedamos con eventos en Quintero y Puchuncaví
# mask = (T59['Comuna'] == 'Quintero y Puchuncaví')&(T59['T59'] >= N_int)

dias = T59.loc[mask].index.astype(str).values
print(dias)
# dias = [ts.strftime('%Y/%m/%d %H:%M') for ts in dias_exp]
ic = 0
for v in var:
    if df.index.freqstr == '6h':
        hd = 4
        freq = '6h'
        delta = 4
        x = np.arange(2,74,6)

    elif df.index.freqstr == 'h':    
        hd = 24
        freq = 'h'
        delta = 6
        x = np.arange(0,72,1)
    df_prom = pd.DataFrame(columns=dias,index=list(range(hd*3)))
    color = COLOR_MAP[ic % len(COLOR_MAP)]
    fig, ax = plt.subplots(figsize=(20, 10.5))
    
    # Obtenemos valores de ciclo diarios para variable
    median, q10, q25, q75, q90 = cs.get_cycle_data(df[v],freq,
                                                   [lambda x: x.hour])
    # Tomamos concatenamos 3 días
    median = pd.concat([median,median,median], ignore_index=True)
    q10 = pd.concat([q10,q10,q10], ignore_index=True)
    q25 = pd.concat([q25,q25,q25], ignore_index=True)
    q75 = pd.concat([q75,q75,q75], ignore_index=True)
    q90 = pd.concat([q90,q90,q90], ignore_index=True)
    # Ploteamos ciclo diarios 
    # x = median.index
    ax.fill_between(x, q10.values, q90.values, color=color, alpha=0.2)
    ax.fill_between(x, q25.values, q75.values, color=color, alpha=0.3)
    ax.plot(x, median.values, marker='o', color=color)
    legend_elements = [
        Line2D([0], [0], color=color, marker='o', label='Mediana'),
        Patch(facecolor=color, alpha=0.3, label='pctl. 25–75'),
        Patch(facecolor=color, alpha=0.2, label='pctl. 10–90')
        ]
    ## Ploteamos días con más intoxicaciones
    for d in range(len(dias)):
        # if d==1 or d==2:
        #     c='tab:red';lw = 1
        # else:
        c='grey';lw = 0.5
        t = pd.to_datetime(dias[d])
        t1 = t - datetime.timedelta(hours=24)
        t2 = t + datetime.timedelta(hours=47)
        df_prom.loc[:,dias[d]] = df.loc[t1:t2,v].astype(float).values
        ax.plot(x,df.loc[t1:t2,v], color=c,alpha=0.6,ls='-',lw=lw,
                zorder=0)
 
    ## Ploteamos días seleccionados con intoxicaciones
    # for d in range(len(dias)):
    #     if d < len(ls):
    #         ils=d
    #     elif d > len(ls):
    #         ils=d-len(ls)
    #     t = pd.to_datetime(dias[d])
    #     t1 = t - datetime.timedelta(hours=24)
    #     t2 = t + datetime.timedelta(hours=47)
    #     df_prom.loc[:,dias[d]] = df.loc[t1:t2,v].astype(float).values
    #     alp = 0.6
    #     ax.plot(x,df.loc[t1:t2,v], color='k',alpha=alp,ls=ls[ils],zorder=0)
    #     legend_elements.append(Line2D([0], [0], color='k',alpha=alp,ls=ls[d],
    #                                   label=str(t)[0:-9]+': '+
    #                                   str(int(data.iloc[d,0]))+' intx.'))
    
    ## Ploteamos media y mediana de días con más intoxicados
    ax.plot(x,df_prom.quantile(q=0.5,axis=1),color='grey',ls='-',lw=2,marker='o',
            zorder=2)
    ax.plot(x,df_prom.mean(axis=1),color='darkgrey',ls='-',lw=2,marker='o',
            zorder=2)
    legend_elements.append(Line2D([0],[0],color='grey',ls='-',lw=2,marker='o',
                           label='Mediana intxs.'))
    legend_elements.append(Line2D([0],[0],color='darkgrey',ls='-',lw=2,marker='o',
                           label='Media intxs.'))
    ax.set_title(f"Ciclo diario {v}, días N-1, N y N+1", 
                 fontsize=15, weight='bold')
    ax.set_xlabel('Hora')
    ax.set_ylabel(f"{v}", rotation=90,
                  labelpad=10, fontsize=15, weight='bold')
    ax.legend(handles=legend_elements,framealpha=0.6,fontsize=7,
              handlelength=7,loc='upper right')
    ax.grid(True)
    ax.set_xticks(range(0, 24*3)[::delta])
    ax.set_xticklabels(range(-24, 48)[::delta])
    for i in [0,24,48,72]: ax.axvline(x=i, color='k', ls='--',lw=2)
    props = dict(boxstyle='round', facecolor='lightgrey', alpha=0.5)
    ax.text(0.18,0.95,'Día N-1', bbox=props,
            transform=ax.transAxes,fontsize=15,verticalalignment='top')
    ax.text(0.5,0.95,'Día N', bbox=props,
            transform=ax.transAxes,fontsize=15,verticalalignment='top')
    ax.text(0.8,0.95,'Día N+1', bbox=props,
            transform=ax.transAxes,fontsize=15,verticalalignment='top')
    if v == 'p_dmc':
        ax.set_ylim(1010,1025)
    elif v == 'v_dmc':
        ax.set_ylim(-8,8)
    elif v[0:4] == 'HCNM':
        ax.set_ylim(-0.2,2)
    elif v[0:3] == 'SO2':
        ax.set_ylim(-2,50)
    plt.tight_layout()
    plt.show()
    
    ic = ic+1
    
###############################################    
#%% Ciclo diario de día N con día N+1 y N-1 ###
############## SUBPLOTS #######################

## Seleccionamos variables
# top_dias=12
N_int = 1
df_h = DF_h.copy()
df_6h = DF_6h.copy()

## Hacemos nan meses que no utilizaremos para ciclo diario
mask_h = (df_h.index.month<4)|(df_h.index.month>9)
mask_6h = (df_6h.index.month<4)|(df_6h.index.month>9)
df_h.loc[mask_h] = float('nan')
df_6h.loc[mask_6h] = float('nan')


#### Categoría #####
# CAT = ['met1','met2','ws','wd','u','v','cont-CQ1','cont-CQ2','cont-VE1','cont-VE2']
CAT = ['met1','met2']

for c in CAT:

    ## Met1 ##
    if c == 'met1':
        cat = c
        var = ['blh_era5','ies_princ','t_dmc']
    
    ## Met2 ##
    elif c == 'met2':
        cat = c
        var = ['hr_dmc','slp_dmc','r_dmc']
    
    ## ws ##
    elif c == 'ws':
        cat = c
        var = ['ws_VE','ws_princ','ws_dmc','ws_CQ']
    
    ## wd ##
    elif c == 'wd':
        cat = c 
        var = ['wd_VE','wd_princ','wd_dmc','wd_CQ']     
    
    ## u ##
    elif c == 'u':
        cat = c
        var = ['u_VE','u_princ','u_dmc','u_CQ']
    
    ## v ##
    elif c == 'v':
        cat = c
        var = ['v_VE','v_princ','v_dmc','v_CQ'] 
    
    ## Contaminantes CQ1 ##
    elif c == 'cont-CQ1':
        cat = c      
        var = ['HCNM_CQ','NO2_CQ','NO_CQ','O3_CQ']
    
    ## Contaminantes CQ2 ##
    elif c == 'cont-CQ2':
        cat = c     
        var = ['CO_CQ','SO2_CQ','MP25_CQ','MP10_CQ']
    
    ## Contaminantes VE1 ##
    elif c == 'cont-VE1':
        cat = c
        var = ['HCNM_VE','NO2_VE','NO_VE','O3_VE']
    
    ## Contaminantes VE2 ##
    elif c == 'cont-VE2':
        cat = c
        var = ['SO2_VE','MP25_VE','MP10_VE']
    
    ## Comparación DMC-ERA5 ##
    # cat = 'comp-DMC-ERA5'
    # var = ['p_dmc','p_era5','t_dmc','t_era5','hr_dmc','hr_era5']
    
        
    
    
    
    
    ## Obtenemos días con más intoxicados
    # data = T59.copy()
    # mask_int = (data['T59'] != 0)
    # data = data.loc[mask_int]
    # data = data.sort_values(by='T59',ascending=False)
    
    #### N de intoxicados y comunas #####
    
    ## Seleccionamos días con más de cierto Nde intoxicados
    # mask =  (T59['T59'] >= N_int)
    
    # Nos quedamos solo con eventos en Quintero
    # mask = (T59['Comuna'] == 'Quintero')&(T59['T59'] >= N_int)
    
    # Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
    mask = (T59['Comuna'] != 'Puchuncaví')&(T59['T59'] >= N_int)
    
    # Nos quedamos solo con eventos en Puchuncaví
    # mask = (T59['Comuna'] == 'Puchuncaví')&(T59['T59'] >= N_int)
    
    # Nos quedamos con eventos en Quintero y Puchuncaví
    # mask = (T59['Comuna'] == 'Quintero y Puchuncaví')&(T59['T59'] >= N_int)
    
    ## Definimos días 
    dias = T59.loc[mask].index.astype(str).values
    # dias = [ts.strftime('%Y/%m/%d %H:%M') for ts in dias_exp]
    print(dias)
    ic = 0
    fig, ax = plt.subplots(len(var),1, figsize=(12, 4*len(var)),sharex=True)
    for v in var:
        if v[-4:len(v)]=='era5':
            hd = 4
            freq = '6h'
            delta = 4
            x = np.arange(2,74,6)
            df = df_6h.copy()
    
        else:    
            hd = 24
            freq = 'h'
            delta = 6
            x = np.arange(0,72,1)
            df = df_h.copy()
        
        # Dataframe de promedios de var
        df_prom = pd.DataFrame(columns=dias,index=list(range(hd*3)))
    
        # Obtenemos valores de ciclo diarios para variable
        median, q10, q25, q75, q90 = cs.get_cycle_data(df[v],freq,
                                                       [lambda x: x.hour])
        # Tomamos concatenamos 3 días
        median = pd.concat([median,median,median], ignore_index=True)
        q10 = pd.concat([q10,q10,q10], ignore_index=True)
        q25 = pd.concat([q25,q25,q25], ignore_index=True)
        q75 = pd.concat([q75,q75,q75], ignore_index=True)
        q90 = pd.concat([q90,q90,q90], ignore_index=True)
        # Ploteamos ciclo diarios
        color = COLOR_MAP[ic % len(COLOR_MAP)]
        ax[ic].fill_between(x, q10.values, q90.values, color=color, alpha=0.2)
        ax[ic].fill_between(x, q25.values, q75.values, color=color, alpha=0.3)
        ax[ic].plot(x, median.values, marker='o', color=color)
        legend_elements = [
            Line2D([0], [0], color=color, marker='o', label='Mediana'),
            Patch(facecolor=color, alpha=0.3, label='pctl. 25–75'),
            Patch(facecolor=color, alpha=0.2, label='pctl. 10–90')
            ]
        ## Ploteamos días con más intoxicaciones
        for d in range(len(dias)):
            c='grey';lw = 0.5
            t = pd.to_datetime(dias[d])
            t1 = t - datetime.timedelta(hours=24)
            t2 = t + datetime.timedelta(hours=47)
            df_prom.loc[:,dias[d]] = df.loc[t1:t2,v].astype(float).values
            ax[ic].plot(x,df.loc[t1:t2,v], color=c,alpha=0.5,ls='-',lw=lw,
                    zorder=0)
     
        ## Ploteamos días seleccionados con intoxicaciones
        # for d in range(len(dias)):
        #     if d < len(ls):
        #         ils=d
        #     elif d > len(ls):
        #         ils=d-len(ls)
        #     t = pd.to_datetime(dias[d])
        #     t1 = t - datetime.timedelta(hours=24)
        #     t2 = t + datetime.timedelta(hours=47)
        #     df_prom.loc[:,dias[d]] = df.loc[t1:t2,v].astype(float).values
        #     alp = 0.6
        #     ax[ic].plot(x,df.loc[t1:t2,v], color='k',alpha=alp,ls=ls[ils],zorder=0)
        #     legend_elements.append(Line2D([0], [0], color='k',alpha=alp,ls=ls[d],
        #                                   label=str(t)[0:-9]+': '+
        #                                   str(int(data.iloc[d,0]))+' intx.'))
        
        ## Ploteamos media y mediana de días con más intoxicados
        ax[ic].plot(x,df_prom.quantile(q=0.5,axis=1),color='grey',ls='-',lw=2,marker='o',
                    zorder=2)
        ax[ic].plot(x,df_prom.mean(axis=1),color='darkgrey',ls='-',lw=2,marker='o',
                    zorder=2)
        legend_elements.append(Line2D([0],[0],color='grey',ls='-',lw=2,marker='o',
                               label='Mediana intxs.'))
        legend_elements.append(Line2D([0],[0],color='darkgrey',ls='-',lw=2,marker='o',
                               label='Media intxs.'))
        if ic ==len(var)-1:
            ax[ic].set_xlabel('Hora')
        ax[ic].set_ylabel(f"{v}", rotation=90,
                      labelpad=10, fontsize=15, weight='bold')
        ax[ic].legend(handles=legend_elements,framealpha=0.6,fontsize=7,
                  handlelength=2,loc='upper right')
        ax[ic].grid(True)
        ax[ic].set_xticks(range(0, 24*3)[::delta])
        ax[ic].set_xticklabels(range(-24, 48)[::delta])
        for i in [0,24,48,72]: ax[ic].axvline(x=i, color='k', ls='--',lw=2)
        props = dict(boxstyle='round', facecolor='lightgrey', alpha=0.5)
        ax[ic].text(0.18,0.95,'Día N-1', bbox=props,
                transform=ax[ic].transAxes,fontsize=10,verticalalignment='top')
        ax[ic].text(0.5,0.95,'Día N', bbox=props,
                transform=ax[ic].transAxes,fontsize=10,verticalalignment='top')
        ax[ic].text(0.8,0.95,'Día N+1', bbox=props,
                transform=ax[ic].transAxes,fontsize=10,verticalalignment='top')
        if v == 'p_dmc':
            ax[ic].set_ylim(1010,1025)
        elif v == 'HCNM_CQ':
            ax[ic].set_ylim(-0.2,2)
        elif v == 'blh_era5':
            ax[ic].set_ylim(-2,800)
        elif v == 'HCNM_VE':
            ax[ic].set_ylim(-0.1,1)
        elif v[0:3] == 'SO2':
            ax[ic].set_ylim(-2,50)
    
        # Sumamos 1 a ic
        ic = ic+1
        
    # Settings fig
    fig.suptitle("Ciclo diario Abril-Julio 2019-2023, días N-1, N y N+1", 
                  fontsize=15, weight='bold',y=0.993)
    fig.tight_layout()
    path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 2/CicloDiario/'
    fig.savefig(path + f'/CicloDiario_{cat}_min'+str(N_int)+'intx.png', dpi=300)

######################################################
######################################################
#%%### Promedios diarios previos y posteriores  ######
######################################################
######################################################

# Con el fin de ver la evolución de promedios diarios previos y posteriores
# se plotearán estos

## Intoxicados y días:
N_int = 50
N_d = 5

## Definimos df data
data = DF_d.copy()
# data = DF_met_da.copy()

# Nos quedamos solo con eventos con más de cierto N de intoxicados
# mask =  (T59['T59'] >= N_int)

# Nos quedamos solo con eventos en Quintero
# mask = (T59['Comuna'] == 'Quintero')&(T59['T59'] >= N_int)

# Nos quedamos con eventos en Quintero y Quintero-Puchuncaví
mask = (T59['Comuna'] != 'Puchuncaví')&(T59['T59'] >= N_int)

# Nos quedamos solo con eventos en Puchuncaví
# mask = (T59['Comuna'] == 'Puchuncaví')&(T59['T59'] >= N_int)

# Nos quedamos con eventos en Quintero-Puchuncaví
# mask = (T59['Comuna'] == 'Quintero y Puchuncaví')&(T59['T59'] >= N_int)

# data.loc[mask,'T59'] = float('nan')
# len_d = data['T59'].count()
# dias = data.sort_values(by='T59',ascending=False).index[0:len_d]

dias = T59.loc[mask].index
print(T59.loc[mask])

var = [
        'HCNM_CQ',
        # 'CO_CQ',
        # 'SO2_CQ',
        # 'MP25_CQ',
        # 'MP10_CQ',
        # 'NO2_CQ',
        # 'NO_CQ',
        # 'O3_CQ',
        
        # 'blh_era5',
        # 't_era5','hr_era5','p_era5',

        # 'ws_era5','u_era5','v_era5',
        # 'ies_princ',
        # 't_princ',
        # 't_dmc','hr_dmc','p_dmc',
        # 'v_dmc',
        
        # 'r_dmc',
        # 'u_dmc','v_dmc','u_princ','v_princ',
        # 'ws_princ','ws_dmc',
        # 'wd_VE','wd_princ','wd_dmc','wd_CQ','wd_CC',
        # 'u_VE','u_princ','u_dmc','u_CQ',
        # 'v_VE','v_princ','v_dmc','v_CQ',
        ]

dias_exp = []
# dias = dias_exp
 
for v in var:
    df_var = pd.DataFrame(columns=dias,index=list(range(-N_d,N_d+1)))
    df_var.index.name = 'Día'
    # Seleccionamos días previos-posteriores
    for d in dias:
        t = pd.to_datetime(d)
        t1 = t - datetime.timedelta(days=N_d)
        t2 = t + datetime.timedelta(days=N_d)
        df_var.loc[-N_d:N_d,d] = data.loc[t1:t2,v].values

    # Calculamos promedios de días
    df_media = df_var.mean(axis=1)
    df_mediana = df_var.quantile(0.5,axis=1, numeric_only=False)
    
    # Pasamos dataframe a formato largo
    df_melted = pd.melt(df_var.reset_index(), id_vars=['Día'],
                        var_name='Variable', value_name=v)
    
    # Ploteamos
    sns.set_style('whitegrid') 
    fig, ax = plt.subplots(figsize=(15, 10),layout='constrained')
    
    for d in dias:
        # ax.plot(df_var.index+N_d,df_var[d],c='grey',lw=0.3,alpha=0.7,zorder=0)

        if df_var[d][0]<=df_mediana[0]:
            ax.plot(df_var.index+N_d,df_var[d],c='grey',lw=0.3,alpha=0.7,zorder=0)
        else:
            ax.plot(df_var.index+N_d,df_var[d],c='red',lw=0.5,alpha=0.7,zorder=0)
            print(str(d)+' = '+str(int(T59.loc[d,'T59']))+',  '+\
                  str(T59.loc[d,'Comuna']))
            dias_exp.append(d)
        
    ax.plot(df_media.index+N_d, df_media,c='dimgrey',lw=2,alpha=1,zorder=2,
            marker='o',label='Media')
    ax.plot(df_mediana.index+N_d, df_mediana,c='steelblue',lw=3,alpha=1,
            zorder=3,marker='o', label='Mediana')
    # sns.boxplot(x='Día', y=v, data=df_melted, ax=ax)
    # sns.violinplot(x='Día', y=v, data=df_melted, ax=ax, inner='quart',
    #                fill=False,zorder=1)
    sns.stripplot(x='Día', y=v, data=df_melted, ax=ax, zorder=1,
                  jitter=False, color='grey', alpha=0.5)
    
    ax.set_title('Boxplot promedios diarios de días con mín. '+str(N_int)
                  +' intx. ('+str(len(dias))+' días), mostrando los '+str(N_d)+
                  ' días previos y posteriores')
    ax.set_xlabel('Día',fontweight='bold')
    ax.set_ylabel(v,fontweight='bold')

######################################################
######################################################
#%%### Promedios diarios previos y posteriores  ######
######################################################
################## SUBPLOTS ##########################

# Con el fin de ver la evolución de promedios diarios previos y posteriores
# se plotearán estos

## Intoxicados y días:
N_int = 80
N_d = 5

## Definimos df data
data = DF_d.copy()

#### Categoría #####
CAT = ['met1','met2','ws','wd','u','v','cont-CQ1','cont-CQ2','cont-VE1','cont-VE2']
for c in CAT:

    ## Met1 ##
    if c == 'met1':
        cat = c
        var = ['blh_era5','ies_princ','t_dmc']
    
    ## Met2 ##
    elif c == 'met2':
        cat = c
        var = ['hr_dmc','p_dmc','r_dmc']
    
    ## ws ##
    elif c == 'ws':
        cat = c
        var = ['ws_VE','ws_princ','ws_dmc','ws_CQ']
    
    ## wd ##
    elif c == 'wd':
        cat = c 
        var = ['wd_VE','wd_princ','wd_dmc','wd_CQ']     
    
    ## u ##
    elif c == 'u':
        cat = c
        var = ['u_VE','u_princ','u_dmc','u_CQ']
    
    ## v ##
    elif c == 'v':
        cat = c
        var = ['v_VE','v_princ','v_dmc','v_CQ'] 
        
    
    ## Contaminantes CQ1 ##
    elif c == 'cont-CQ1':
        cat = c      
        var = ['HCNM_CQ','NO2_CQ','NO_CQ','O3_CQ']
    
    ## Contaminantes CQ2 ##
    elif c == 'cont-CQ2':
        cat = c     
        var = ['CO_CQ','SO2_CQ','MP25_CQ','MP10_CQ']
    
    ## Contaminantes VE1 ##
    elif c == 'cont-VE1':
        cat = c
        var = ['HCNM_VE','NO2_VE','NO_VE','O3_VE']
    
    ## Contaminantes VE2 ##
    elif c == 'cont-VE2':
        cat = c
        var = ['SO2_VE','MP25_VE','MP10_VE']
    
    ## Comparación DMC-ERA5 ##
    # cat = 'comp-DMC-ERA5'
    # var = ['p_dmc','p_era5','t_dmc','t_era5','hr_dmc','hr_era5']
    
    #### N de intoxicados y comunas #####
    
    # Nos quedamos solo con eventos con más de cierto N de intoxicados
    mask =  (T59['T59'] >= N_int)
    
    # Nos quedamos solo con eventos en Quintero
    # mask = (T59['Comuna'] == 'Quintero')&(T59['T59'] >= N_int)
    
    # Nos quedamos con eventos en Quintero y Quintero-Puchuncaví
    # mask = (T59['Comuna'] != 'Puchuncaví')&(T59['T59'] >= N_int)
    
    # Nos quedamos solo con eventos en Puchuncaví
    # mask = (T59['Comuna'] == 'Puchuncaví')&(T59['T59'] >= N_int)
    
    # Nos quedamos con eventos en Quintero-Puchuncaví
    # mask = (T59['Comuna'] == 'Quintero y Puchuncaví')&(T59['T59'] >= N_int)
    
    # Definimos días a plotear
    dias = T59.loc[mask].index
    # dias = dias_exp
    # print(dias)
    
    # Ploteamos
    ic = 0
    sns.set_style('whitegrid') 
    fig, ax = plt.subplots(len(var),1, figsize=(6, 2*len(var)),sharex=True)
    for v in var:
        df_var = pd.DataFrame(columns=dias,index=list(range(-N_d,N_d+1)))
        df_var.index.name = 'Día'
        # Seleccionamos días previos-posteriores
        for d in dias:
            t = pd.to_datetime(d)
            t1 = t - datetime.timedelta(days=N_d)
            t2 = t + datetime.timedelta(days=N_d)
            df_var.loc[-N_d:N_d,d] = data.loc[t1:t2,v].values
    
        # Calculamos promedios de días
        df_media = df_var.mean(axis=1)
        df_mediana = df_var.quantile(0.5,axis=1, numeric_only=False)
        
        # Pasamos dataframe a formato largo
        df_melted = pd.melt(df_var.reset_index(), id_vars=['Día'],
                            var_name='Variable', value_name=v)
    
        
        for d in dias:
                ax[ic].plot(df_var.index+N_d,df_var[d],c='grey',lw=0.3,alpha=0.6,zorder=0)
            
        ax[ic].plot(df_media.index+N_d, df_media,c='dimgrey',lw=2,alpha=1,zorder=2,
                marker='o',label='Media')
        ax[ic].plot(df_mediana.index+N_d, df_mediana,c='steelblue',lw=3,alpha=1,
                zorder=3,marker='o', label='Mediana')
        # sns.boxplot(x='Día', y=v, data=df_melted, ax=ax[ic])
        # sns.violinplot(x='Día', y=v, data=df_melted, ax=ax[ic], inner='quart',
        #                 fill=False,zorder=1)
        sns.stripplot(x='Día', y=v, data=df_melted, ax=ax[ic], zorder=1,
                      jitter=False, color='grey', alpha=0.4,s=3)
        ax[ic].axvline(N_d,ls='--',color='lightgrey',alpha=0.5,zorder=0)
        ax[ic].set_ylabel(v,fontweight='bold',fontsize=12)
        if v != var[0]:
            ax[ic].legend_ = None
        if len(var) == ic+1:
            ax[ic].set_xlabel('Día',fontweight='bold')
        ic = ic + 1
        
    # Settings fig
    fig.suptitle(f'Valores diarios de {N_d} días prev/post, mín. '+str(N_int)
                  +' intx. ('+str(len(dias))+' días)', 
                  fontsize=9,y=0.984)
    fig.tight_layout()
    path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 2/ValoresDiarios/min'+str(N_int)+'intx/'
    fig.savefig(path + f'ValoresDiarios_{cat}_min'+str(N_int)+'intx.png', dpi=300)
    
###############################################
###############################################
#%%######       Plots extras       ############
###############################################
###############################################

#%% Scatter entre 2 variables

# Variables''
x = 'O3_VE'
y = 'ws_princ'
# Figura
fig, ax = plt.subplots(figsize=(8,6),layout='constrained')
props = dict(boxstyle='round', facecolor='lightgrey', alpha=0.5)
corr = "%.2f" % DF_d[[x,y]].corr().loc[y,x]
sns.scatterplot(DF_d,x=x,y=y,ax=ax)
ax.grid(alpha=0.5)
ax.text(0.9, 0.95, r'$\rho$='+corr, transform=ax.transAxes,
              fontsize=10,verticalalignment='top', bbox=props)
ax.set_xlabel(x, fontweight='bold')
ax.set_ylabel(y, fontweight='bold')
fig.suptitle('Scatter Plots de variables diarias '+x+' y '+y,
             fontsize=14)


#%% Comparamos scatters de estación con intoxicaciones en comuna

# Estación y variables
mask_com = mask_Q
est='VE'
x = 'HCNM_'+est
y = 'T59'
data = DF_dhh.copy()
# Figura
fig, ax = plt.subplots(figsize=(8,8),layout='constrained')
props = dict(boxstyle='round', facecolor='lightgrey', alpha=0.5)

# Scatter Total intoxicados
corr_int = "%.2f" % data.loc[mask_int,[x,y]].corr().loc[y,x]
sns.scatterplot(data[mask_int],x=x,y=y,ax=ax,color='b')
# Scatter comuna
corr_com = "%.2f" % data.loc[mask_com,[x,y]].corr().loc[y,x]
sns.scatterplot(data[mask_com],x=x,y=y,ax=ax, color='m')

ax.grid(alpha=0.5)
ax.text(0.85,0.95,r'$\rho_{comuna}$='+str(corr_com)+'\n'+\
                 r'$\rho_{total}$='+str(corr_int)
        , transform=ax.transAxes,fontsize=10,verticalalignment='top',
        bbox=props)
ax.set_xlabel(x, fontweight='bold')
ax.set_ylabel(y, fontweight='bold')
fig.suptitle('Scatter Plots de variables diarias '+x+' y '+y,
             fontsize=14)

#%% Subplots series de tiempo

# Fechas


# 72
# d1 = pd.to_datetime('2022-06-17 00:00:00')
# d2 = pd.to_datetime('2022-06-17 23:00:00')

# 20
# d1 = pd.to_datetime('2022-06-24 00:00:00')
# d2 = pd.to_datetime('2022-06-24 23:00:00')

# 41
# d1 = pd.to_datetime('2022-08-11 00:00:00')
# d2 = pd.to_datetime('2022-08-11 23:00:00')


# 04-10
d1 = pd.to_datetime('2022-10-04 00:00:00')
d2 = pd.to_datetime('2022-10-04 23:00:00')


# data = DF_h.copy()
data = pd.read_csv(path_data+'DF_h.csv', index_col='date', parse_dates=True)
# data['slp_dmc_diff'] = data['slp_dmc'].diff() 
# data['slp_dmc_rm'] = data['slp_dmc'].rolling(window=13,center=True).mean()
# data['slp_dmc_rmdiff'] = data['slp_dmc_rm'].diff()
# data['T59'] = T59['T59'].asfreq('h')
# mask = data['T59']<10
# data.loc[mask,'T59'] = 0
# data.loc[mask,'Comuna'] = float('nan')
# Variables
variables = [
            'SO2_CQ','MP25_CQ','MP10_CQ',
            # 'CO_CQ',
            # 'NO_CQ','NO2_CQ','O3_CQ',
            
            'blh_era5','ies_princ','slp_dmc',
            'u_dmc','v_dmc','ws_dmc',
            'u_princ','v_princ','hr_dmc'
            'u_CC','v_CC','t_CC'
            
            # 'HCNM_VE','HCNM_CQ','HCNM_CC',
            
            # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
            # 'MP25_VE','MP10_VE',
    
            # 'blh_era5','ies_princ','t_dmc','hr_dmc','slp_dmc','slp_dmc_diff','r_dmc','ws_dmc',
            # 'ws_VE','ws_princ','ws_dmc','ws_CQ',


            # 'r_dmc','t_dmc','slp_dmc','slp_dmc_diff','slp_dmc_rm','slp_dmc_rmdiff'
            # 'u_princ','v_princ','slp_dmc','slp_dmc_diff',
            # 'u_VE','v_VE',
            # 'u_princ','v_princ',
            # 'u_dmc','v_dmc',
            # 'u_CQ','v_CQ',
            
            # 'T59',

            ]

# Ploteamos
n_var = len(variables)
ax = data.loc[d1:d2,variables].plot(subplots=True, layout=(n_var,1)\
                                    ,grid=True, figsize=(5,1*n_var), 
                                    marker='.', lw=1,ms=3, sharex=True,
                                    title=d1.strftime('%d-%m-%Y'))
plt.tight_layout()
# path para guardar figuras
# path_fig = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 2/Clusters/DiaPeakTruncado/'
# # Chequeamos existencia de directorio
# if not os.path.exists(path_fig[0:len(path_fig)-1]):
#     os.makedirs(path_fig[0:len(path_fig)-1])
#     print(f"Directorio '{path_fig[0:len(path_fig)-1]}' fue creado.")
# plt.savefig(path_fig+'Dia_'+d1.strftime('%y%m%d')+'.png', dpi=300)


#%% Plot para 04-10

# 04-10
d1 = pd.to_datetime('2022-10-03 00:00:00')
d2 = pd.to_datetime('2022-10-06 00:00:00')

# importamos DF_h
data = pd.read_csv(path_data+'DF_h.csv', index_col='date', parse_dates=True)

# Variables
variables = [
            'SO2_CQ','MP25_CQ','MP10_CQ',
            
            'blh_era5','ies_princ','slp_dmc',
            'u_dmc','v_dmc','ws_dmc',
            'u_princ','v_princ','hr_dmc',
            'u_CC','v_CC','t_dmc'

            ]
    
# Creamos figura
fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(15, 10), sharex=True)
axes = axes.flatten() # Aplanamos para iterar más facil 
cmap = plt.get_cmap('tab10') # cmap tab para 10 colores

cols = data.loc[date_1:date_2, variables].columns
# Iteramos por variables
for i, col in enumerate(cols):
    # usamos operador % para iterar de 0 a 9
    color_index = i % 10
    series_to_plot = data.loc[d1:d2, col].dropna()
    series_to_plot.plot(ax=axes[i], grid=True, legend=True,
                        color=cmap(color_index))
    if col[0] in ['u','v']:
        axes[i].set_ylim(-5,5)

    
plt.tight_layout()
# path para guardar figuras
path_fig = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 3/1/'
plt.savefig(path_fig+'Series_extra_'+d1.strftime('%m-%d-%H%M')+'_a_'+
            d2.strftime('%m-%d-%H%M')+'.png',dpi=300)

#%% 

data_test = data.loc[d1:d2, variables]


#%% Boxplots de HCNM por comuna y total


date_1 = pd.to_datetime('01-01-2021',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2023',format='%d-%m-%Y')
data = DF_d[date_1:date_2].copy()
var = 'blh_era5'
fig, ax = plt.subplots(1,2,figsize=(11,7),sharey=True,width_ratios=[2,1])

meanprops={"marker":"D", "markerfacecolor":"white","zorder":3,
           "markeredgecolor":"black","markersize":"8"}

# ax[0]
sns.boxplot(data=data,y=var,x='Comuna',ax=ax[0],palette='Set1',zorder=1,
            showfliers=False, showmeans=True,linewidth=2,meanprops=meanprops)
# sns.violinplot(data=data,y='T59',x='Comuna',ax=ax[0],
#                palette='Set1',linewidth=3,fill=False,inner='quart',
#                inner_kws=dict(color="k",linewidth=2))
sns.stripplot(data=data,y=var,x='Comuna',ax=ax[0],zorder=2,
              palette='Set1',edgecolor="gray", size=6, linewidth=1)
ax[0].grid(zorder=0,alpha=0.5)
ax[0].set_title('Casos por comuna', fontweight='bold')

# ax[1]
mask = (data['T59']>=0)
sns.boxplot(data=data[mask],y=var,ax=ax[1],zorder=1,showfliers=False,linewidth=2,
            color='darkorange',showmeans=True,meanprops=meanprops)
# sns.violinplot(data=data,y='T59',ax=ax[1],color='darkorange',linewidth=3,
#               fill=False,inner='quart',inner_kws=dict(color="k",linewidth=1.5))
sns.stripplot(data=data[mask],y=var,ax=ax[1],zorder=2,color='darkorange',
             edgecolor="gray", size=6, linewidth=1)
ax[1].grid(zorder=0,alpha=0.5)
ax[1].set_title('Casos totales', fontweight='bold')
ax[1].set_xticklabels(['Total'])
# ax[1].set_ylim(-0.01,7)

# fig
fig.suptitle(f'Boxplots {var} entre 2021-2023',fontsize=14)
fig.tight_layout()

#%% Scatter matrix

# df = pd.concat([T59,DF_d],axis=1)
# df["slp_dmc_diff"] = df["slp_dmc"].diff()
# df = df[df['T59']>0]

cols = ['T59','Comuna','slp_dmc_diff',
        # 'ies_princ',
        #'t_princ','t40_princ',
        # 't_dmc','hr_dmc','r_dmc','slp_dmc','slp_dmc_diff',
        # 'blh_era5',
        
        # 'ws_VE','ws_princ','ws40_princ',
        # 'ws_dmc','ws_CQ','ws_quint','ws_CC',
        
        # 'ws_dmc',
        
        # 'u_VE','v_VE',
        # 'u_princ','v_princ',
        # 'u40_princ','v40_princ',
        # 'u_dmc','v_dmc',
        # 'u_CQ','v_CQ',
        # 'u_quint','v_quint',
        # 'u_CC','v_CC',
    
        'HCNM_CQ',
        'CO_CQ',
        'SO2_CQ',
        'NO2_CQ','NO_CQ','O3_CQ',
        'MP25_CQ','MP10_CQ',
    
        # 'HCNM_VE',
        # 'SO2_VE',
        # 'NO2_VE','NO_VE','O3_VE',
        # 'MP25_VE','MP10_VE',
        
        # 'HCNM_CC',
        # 'MP25_CC','MP10_CC','SO2_CC'
        ]


sns.set_theme(style="ticks")
sns.pairplot(df[cols],hue='Comuna')

# g = sns.pairplot(df[cols], diag_kind="kde")
# g.map_lower(sns.kdeplot, levels=4, color=".2")


