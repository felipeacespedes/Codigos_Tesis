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
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import datetime
import numpy as np
import Ciclos_SINCA_GPT as cs
import sys
# sys.exit()

COLOR_MAP = sns.color_palette("Set2", 18)

ls_og = [
     ('densely dashed',        (0, (5, 1))),
     ('dashed',                (0, (5, 3))),
     ('loosely dashed',        (0, (5, 10))),
     
     ('densely dotted',        (0, (1, 0.5))),
     ('dotted',                (0, (1, 2))),
     ('loosely dotted',        (0, (1, 5))),
     
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

#%% Importamos datos y cortamos entre 2019 y 2023

# Fechas
d1 = pd.to_datetime('2019-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')

# T59
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
T59 = pd.read_csv(path+'serie_T59full.csv', index_col='date',
                  parse_dates=True, infer_datetime_format = True )
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
                  usecols=['date','ts','p','mslp','hr','rg','u','v','wd','ws'])
DMC = DMC.loc[d1:d2]

# Principal
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/Principal/'
Princ = pd.read_csv(path+'Principal.csv',index_col='date',parse_dates=True,
                    usecols=['date','t_inv','t10','u10','v10','wd10','ws10'])
Princ = Princ.loc[d1:d2]

#%% Juntamos Datos

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
DMC = DMC.rename(columns={'ts':'t_dmc','u':'u_dmc','v':'v_dmc',
                          'p':'p_dmc','hr':'hr_dmc','mslp':'mslp_dmc',
                          'rg':'r_dmc','wd':'wd_dmc','ws':'ws_dmc',
                           })
Princ = Princ.rename(columns={'t10':'t_princ','t_inv':'inv_princ',
                              'wd10':'wd_princ','ws10':'ws_princ',
                              'u10':'u_princ','v10':'v_princ'})

#%% Datos horarios ##

DF_h = pd.concat([HCNM,CO,SO2,MP25,MP10,NO2,NO,O3,U,V,WS,WD,DMC,Princ], axis=1)

#%% Datos horario sin anomalía ##

# Fechas
d1 = pd.to_datetime('2023-05-21 00:00:00')
d2 = pd.to_datetime('2023-05-26 23:00:00')

# Con mediana: hay mejores resultados para promedios diarios!!
DF_met_ha = DF_h[DF_h.columns[-27:len(DF_h.columns)]].copy()
DF_met_ha = DF_met_ha.resample('H').mean()

# Quitamos ciclo anual y semianual
df = DF_met_ha.copy()
df = df.asfreq('H').interpolate()
for var in DF_met_ha.columns:
    # Extraemos señal
    y = df[var].values
    N = len(y)

    # Apply FFT
    fft_vals = np.fft.fft(y)
    freqs = np.fft.fftfreq(N, d=1)  # d=1 since data is daily
    
    # Identify the frequencies corresponding to annual and semiannual cycles
    # 1 cycle per 365 days → frequency = 1/365
    # 2 cycles per 365 days → frequency = 2/365
    
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
    DF_met_ha[var] = y - seasonal_cycle + y.mean()
    
    # # Subtract to get anomaly-removed (detrended) signal
    # anomaly_filtered = y - seasonal_cycle + y.mean()
    # # Add back to the DataFrame
    # df['seasonal_cycle'] = seasonal_cycle
    # df['anomaly_filtered'] = anomaly_filtered
    # # Plot
    # plot = [var,'seasonal_cycle','anomaly_filtered']
    # df.loc[d1:d2,plot].plot(figsize=(15, 5),
    #                         title='Original vs. Seasonal Cycle vs. Anomaly')
    # plt.tight_layout()
    # plt.show()
del df
####################
#%% Datos diarios ##

# Con mediana: hay mejores resultados para promedios diarios!!
DMC = DMC.resample('D').quantile(0.5)
HCNM = HCNM.resample('D').quantile(0.5)
CO = CO.resample('D').quantile(0.5)
SO2 = SO2.resample('D').quantile(0.5)
MP25 = MP25.resample('D').quantile(0.5)
MP10 = MP10.resample('D').quantile(0.5)
NO2 = NO2.resample('D').quantile(0.5)
NO = NO.resample('D').quantile(0.5)
O3 = O3.resample('D').quantile(0.5)
U = U.resample('D').quantile(0.5)
V = V.resample('D').quantile(0.5)
WS = WS.resample('D').quantile(0.5)
Princ = Princ.resample('D').quantile(0.5)
# Juntamos
DF_d = pd.concat([T59,HCNM,CO,SO2,MP25,MP10,NO2,NO,O3,U,V,WS,DMC,Princ], axis=1)
DF_met_da = pd.concat([T59['T59'],U,V,WS,DMC,Princ], axis=1)

#%% Datos diarios sin anomalía ##

df = DF_met_da.copy()
df = df.asfreq('D').interpolate()

for var in DF_met_da.columns:
    if var == 'T59':
        continue
    # Extraemos señal
    y = df[var].values
    N = len(y)

    # Apply FFT
    fft_vals = np.fft.fft(y)
    freqs = np.fft.fftfreq(N, d=1)  # d=1 since data is daily
    
    # Identify the frequencies corresponding to annual and semiannual cycles
    # 1 cycle per 365 days → frequency = 1/365
    # 2 cycles per 365 days → frequency = 2/365
    
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
    DF_met_da[var] = y - seasonal_cycle + y.mean()
    
    # # Subtract to get anomaly-removed (detrended) signal
    # anomaly_filtered = y - seasonal_cycle + y.mean()
    # # Add back to the DataFrame
    # df['seasonal_cycle'] = seasonal_cycle
    # df['anomaly_filtered'] = anomaly_filtered
    # plot = [var,'seasonal_cycle','anomaly_filtered']
    # df[plot].plot(figsize=(15, 5),title='Original vs. Seasonal Cycle vs. Anomaly')
    # plt.tight_layout()
    # plt.show()

del df
#%% Dato diario pero en casos

# Seleccionamos de 7 a 21 horas
DF_dhh = DF_h.copy()
mask =  (DF_h.index.hour < 7) | (21 < DF_h.index.hour)
DF_dhh.loc[mask] = np.nan
DF_dhh = DF_dhh.resample('D').mean()
DF_dhh = pd.concat([T59,DF_dhh], axis=1)

# Seleccionamos de 21 a 7 horas
DF_dhnh = DF_h.copy()
mask =  (DF_h.index.hour > 7) & (21 > DF_h.index.hour)
DF_dhnh.loc[mask] = np.nan
DF_dhnh = DF_dhnh.resample('D').mean()
DF_dhnh = pd.concat([T59,DF_dhnh], axis=1)

# Seleccionamos horas de mañana
DF_dhm = DF_h.copy()
mask =  (DF_h.index.hour < 5) | (10 < DF_h.index.hour)
DF_dhm.loc[mask] = np.nan
DF_dhm = DF_dhm.resample('D').mean()
DF_dhm = pd.concat([T59,DF_dhm], axis=1)

#%% Vemos comunas de intoxicados

# Obtenemos días con más intoxicados
data = T59.copy()
mask_int = (data['T59'] != 0)
data = data.loc[mask_int]
data = data.sort_values(by='T59',ascending=False).iloc[0:-3,:]

# Guardamos índices por comuna
mask_Q = (T59['Comuna'] == 'Quintero')
mask_P = (T59['Comuna'] == 'Puchuncaví')
mask_QP = (T59['Comuna'] == 'Quintero y Puchuncaví')

# Hist
data['Comuna'].hist(figsize=(7,5),grid=True)
plt.title('Histograma casos por comuna')
plt.tight_layout()

#########################################
#########################################
#%%######### SCATTERPLOTS ###############
#########################################
#########################################

#%% Vemos Scatter entre variables y T59

# Columnas y Filas
C = 6
F = 3
data = DF_dhh.copy()

fig, axs = plt.subplots(F,C,figsize=(24,10),layout='constrained',sharey=True)
props = dict(boxstyle='round', facecolor='lightgrey', alpha=0.5)

plot = [
        ['hr_dmc','p_dmc','mslp_dmc'],
        ['t_dmc','inv_princ','r_dmc'],
        ['ws_dmc','u_dmc','v_dmc'],
        ['ws_princ','u_princ','v_princ'],
        ['ws_VE','u_VE','v_VE'],
        ['ws_CQ','u_CQ','v_CQ'],
        ]

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

for c in range(C):
    for f in range(F):
        # definimos x
        x = plot[c][f]
        #ploteamos
        corr = "%.2f" % data[['T59',x]].corr().loc['T59',x]
        sns.scatterplot(data,x=x,y='T59',ax=axs[f,c])
        axs[f,c].grid(alpha=0.5)
        axs[f,c].text(0.75, 0.95, r'$\rho$='+corr, transform=axs[f,c].transAxes,
                      fontsize=10,verticalalignment='top', bbox=props)
        axs[f,c].set_xlabel(x, fontweight='bold')
        
# Main
fig.suptitle('Scatter Plots de variables diarias v/s T59 (serie diaria total)',
             fontsize=14)

#%% Vemos Scatter entre variables y T59 tomando solo días con intoxicados

data = DF_dhm.copy()

## Hacemos Nan días sin intoxicados
mask =  (data['T59'] <= 80)
data.loc[mask] = np.nan

# Columnas y Filas
C = 6; F = 3; fs=(20,10)
plot = [
        ['hr_dmc','p_dmc','r_dmc'],
        ['t_dmc','u_dmc','v_dmc'],
        ['inv_princ','u_princ','v_princ'],
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

#%% Scatter entre 2 variables

# Estación y variables
est='CQ'
x = 'HCNM_'+est
y = 'MP25_'+est
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

#%% Scatters de diferente comunas

#### Columnas, Filas y horas
P = 'M' # [C, M]
LH = ['TD', 'HH', 'HNH', 'HM']
#####

for H in LH:   
    # Definimos variables por casos
    if P == 'M': # Meteo
        C = 6
        F = 3
        W = 20
        L = 10
        plot = [
                ['hr_dmc','p_dmc','mslp_dmc'],
                ['r_dmc','t_dmc','inv_princ'],
                ['ws_dmc','u_dmc','v_dmc'],
                ['ws_princ','u_princ','v_princ'],
                ['ws_VE','u_VE','v_VE'],
                ['ws_CQ','u_CQ','v_CQ'],
                ]
    elif P == 'C': # Contaminantes
        C = 4
        F = 4
        W = 13
        L = 12
        plot = [
                ['HCNM_VE','HCNM_CQ','SO2_VE','SO2_CQ'],
                ['MP25_VE','MP25_CQ','NO2_VE','NO2_CQ'],
                ['MP10_VE','MP10_CQ','NO_VE','NO_CQ'],
                ['CO_VE','CO_CQ','O3_VE','O3_CQ'],
                ]
    
    if H == 'HH': # Horario Hábil 
        data = DF_dhh.copy()
        h = 'horas hábiles (07 a 21)'
    elif H == 'HNH': # Horario No Hábil
        data = DF_dhnh.copy()
        h = 'horas no hábiles (22 a 06)'
    elif H == 'HM': # Horas Mañana
        data = DF_dhm.copy()
        h = 'horas de mañana (04 a 10)'
    elif H == 'TD': # Todo Día
        data = DF_d.copy()
        h = 'día completo'
    

    fig, axs = plt.subplots(F,C,figsize=(W,L),layout='constrained',sharey=True)
    
    for c in range(C):
        for f in range(F):
            # definimos x
            x = plot[c][f]
            corr_Q = "%.2f" % data.loc[mask_Q,[x,'T59']].corr().loc['T59',x]
            corr_P = "%.2f" % data.loc[mask_P,[x,'T59']].corr().loc['T59',x]
            corr_QP = "%.2f" % data.loc[mask_QP,[x,'T59']].corr().loc['T59',x]
            corr_int =  "%.2f" % data.loc[mask_int,[x,'T59']].corr().loc['T59',x]
            #ploteamos
            sns.scatterplot(data[mask_Q],x=x,y='T59',ax=axs[f,c],color='b',
                            marker='*',label='Q,  '+r'$\rho$='+str(corr_Q))
            sns.scatterplot(data[mask_P],x=x,y='T59',ax=axs[f,c],color='r',
                            marker='*',label='P,  '+r'$\rho$='+str(corr_P))
            sns.scatterplot(data[mask_QP],x=x,y='T59',ax=axs[f,c],color='orange',
                            marker='*',label='QP, '+r'$\rho$='+str(corr_QP))
            sns.scatterplot(data[mask_int],x=x,y='T59',ax=axs[f,c],color='grey',
                            label='Total, '+r'$\rho$='+str(corr_int), zorder=0)
    
            axs[f,c].grid(alpha=0.5)
            axs[f,c].set_xlabel(x, fontweight='bold')
            axs[f,c].legend(loc='upper left', fontsize=8, framealpha=0.4)
    # Main
    fig.suptitle('Scatter Plots de variables diarias v/s T59 '+\
                 '(solo días con intoxicaciones), segregando por comuna, '+h,
                 fontsize=14)
    fig.show()


#########################################
#########################################
#%%########### REGRESIONES ##############
#########################################
#########################################

#%% Aplicamos regresión con promedios diarios

# Copiamos DF
df = DF_d.copy()

# Drop missing values from relevant columns
var = ['inv_princ','u_princ','v_princ',
       't_dmc','u_dmc','v_dmc',
       'hr_dmc','p_dmc','r_dmc',
       'HCNM_VE','u_VE','v_VE',
       'HCNM_CQ','u_CQ','v_CQ',
       'HCNM_CC','u_CC','v_CC']

df_var = df[['T59'] + var].dropna()

X = df_var[var]
y = df_var['T59']

# Add intercept
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()
print(f"R²: {model.rsquared:.3f}")
print(model.summary())

#######################################################
#%% Probamos modelo usando diferentes horas del día ###

# Creamos Dataframe para guardar datos de modelo
cols = ['R2',
        'inv_princ',
        't_dmc',
        'hr_dmc',
        'p_dmc',
        'r_dmc',
        'u_princ','v_princ',
        'u_dmc','v_dmc',
        'u_VE','v_VE',
        'u_CQ','v_CQ',
        # 'HCNM_VE','HCNM_CQ',
        # 'MP25_VE','MP25_CQ',
        # 'MP10_VE','MP10_CQ',
        # 'CO_CQ',
        # 'SO2_VE','SO2_CQ',
        # 'NO2_VE','NO2_CQ',
        # 'NO_VE','NO_CQ',
        # 'O3_VE','O3_CQ',
        ]

OLS_df = pd.DataFrame(columns=cols, index=range(24))

# Iteramos por hora del día
for i in range(24):
       
    # Tomamos solo hora de interés
    data = DF_h.copy()
    mask =  (data.index.hour != i)
    data.loc[mask] = np.nan
    
    # Promediamos y adjuntamos datos de intoxicados
    data = data.resample('D').mean()

    # Estandarizamos
    data = (data-data.mean())/data.std()
    data['T59'] = T59['T59'] # redefinimos intoxicados sin estandar.
    
    ## Corremos modelo ##
    
    # Copiamos DF
    df = data.copy()
    
    # Drop missing values from relevant columns
    var = cols[1:len(cols)]
    df_var = df[['T59'] + var].dropna()
    
    X = df_var[var]
    y = df_var['T59']
    
    # Add intercept
    X = sm.add_constant(X)
    
    # Fit the model
    model = sm.OLS(y, X).fit()
    
    # Guardamos performance de modelo
    # print('model h='+str(i))
    # print(model.rsquared)
    # print(model.params.values[1:len(cols)])

    OLS_df.loc[i,var] = model.params.values[1:len(cols)]
    OLS_df.loc[i,'R2'] = model.rsquared 

OLS_df = OLS_df.apply(pd.to_numeric)
    
# Ploteamos heatmap

# Ploteamos
fig , axs = plt.subplots(2,figsize = (20,10.5), layout='constrained',
                         gridspec_kw={'height_ratios': [3, 1]})

### Heatmap ###
var = cols[1:len(cols)];v = 3
sns.heatmap(OLS_df[var].transpose(),cmap ='bwr',
            linewidths = 0.08,vmin=-v,vmax=v, ax = axs[0])

axs[0].set_yticklabels(OLS_df[var].columns.values,rotation=45, size=6,
                       fontweight='bold')
axs[0].set_ylabel('Coeficientes')

# Colorbar
colorbar = axs[0].collections[0].colorbar
fig.get_layout_engine().set(w_pad=0.2, h_pad=0.2)

### R2 ###
sns.lineplot(OLS_df['R2'], ax=axs[1])
axs[1].set_xticks(range(24))
axs[1].set_xticklabels(range(24),rotation=0)
axs[1].set_xlabel('Hora')
axs[1].set_ylabel('R2')
axs[1].set_xlim(-0.5,23.5)
axs[1].grid()   

fig.suptitle('Coeficientes y R2 según hora del día (serie diaria total)')
fig.get_layout_engine().set(w_pad=0.2, h_pad=0.06)


#################################################
#%% Seleccionamos solo días con Intoxiaciones ###
#################################################

#######################################################
#%% Probamos modelo usando diferentes horas del día ###

# Creamos Dataframe para guardar datos de modelo
cols = ['R2',
        'inv_princ',
        't_dmc',
        'hr_dmc',
        'p_dmc',
        'r_dmc',
        'u_princ','v_princ',
        'u_dmc','v_dmc',
        'u_VE','v_VE',
        'u_CQ','v_CQ',
        # 'HCNM_VE','HCNM_CQ',
        # 'MP25_VE','MP25_CQ',
        # 'MP10_VE','MP10_CQ',
        # 'CO_CQ',
        # 'SO2_VE','SO2_CQ',
        # 'NO2_VE','NO2_CQ',
        # 'NO_VE','NO_CQ',
        # 'O3_VE','O3_CQ',
        ]

N_int = 20    
OLS_itx = pd.DataFrame(columns=cols, index=range(24))

# Probamos largo de df_var
dias = np.ones(24)

# Iteramos por hora del día
for i in range(24):

    # Tomamos solo hora de interés
    data = DF_h.copy()
    mask =  (data.index.hour != i)
    data.loc[mask] = np.nan
    
    
    # Promediamos y adjuntamos datos de intoxicados
    data = data.resample('D').mean()
    data['T59'] = T59['T59']
    
    # Hacemos Nan días sin intoxicados (y días con menos de 10)
    mask =  (data['T59'] <= N_int)
    data.loc[mask] = np.nan
    data_T59 = data['T59'] # guardamos datos no estandarizados
    
    # Estandarizamos
    data = (data-data.mean())/data.std()
    data['T59'] = data_T59 # redefinimos intoxicados sin estandar.
    
    ## Corremos modelo ##
    
    # Copiamos DF
    df = data.copy()
    
    # Drop missing values from relevant columns
    var = cols[1:len(cols)]
    df_var = df[['T59'] + var].dropna()
    
    X = df_var[var]
    y = df_var['T59']
    
    # Add intercept
    X = sm.add_constant(X)
    
    # Fit the model
    model = sm.OLS(y, X).fit()
    
    # Guardamos performance de modelo
    # print('model h='+str(i))
    # print(model.rsquared)
    # print(model.params.values[1:len(cols)])

    OLS_itx.loc[i,var] = model.params.values[1:len(cols)]
    OLS_itx.loc[i,'R2'] = model.rsquared
    dias[i] = len(df_var)

OLS_itx = OLS_itx.apply(pd.to_numeric)

# Ploteamos heatmap
fig , axs = plt.subplots(2,figsize = (20,10.5), layout='constrained',
                         gridspec_kw={'height_ratios': [3, 2]})

### Heatmap ###
var = cols[1:len(cols)]; v = 60
sns.heatmap(OLS_itx[var].transpose(),cmap ='bwr',linecolor='black',
            linewidths = 0.08,vmin=-v,vmax=v, ax = axs[0])

axs[0].set_yticklabels(OLS_itx[var].columns.values,rotation=45, size=6,
                       fontweight='bold')
axs[0].set_ylabel('Coeficientes')

# Colorbar
colorbar = axs[0].collections[0].colorbar


### R2 ###
sns.lineplot(OLS_itx['R2'], ax=axs[1],marker='o')
axs[1].set_xticks(range(24))
axs[1].set_xticklabels(range(24),rotation=0)
axs[1].set_xlabel('Hora')
axs[1].set_ylabel('R2')
axs[1].set_xlim(-0.5,23.5)
axs[1].grid() 

fig.suptitle('Coeficientes y R2 según hora del día '+
             '(solo días con intoxicaciones, N = '+str(int(dias.max()))+' días)')
fig.get_layout_engine().set(w_pad=0.2, h_pad=0.06)
# fig.subplots_adjust(top=0.1)

#########################################
#%% Correr desde horas previas al día ###

# Creamos Dataframe para guardar datos de modelo
cols = ['R2',
        # 'inv_princ',
        # 't_dmc',
        # 'hr_dmc',
        # 'p_dmc',
        # 'r_dmc',
        # 'ws_dmc',
        # 'u_princ','v_princ',
        # 'u_dmc','v_dmc',
        # 'u_VE','v_VE',
        # 'u_CQ','v_CQ',
        
        'HCNM_CQ',
        'CO_CQ',
        'SO2_CQ',
        'NO2_CQ','NO_CQ','O3_CQ',
        
        # 'HCNM_VE',
        # 'SO2_VE',
        # 'NO2_VE','NO_VE','O3_VE',
        
        # 'MP25_VE','MP25_CQ',
        # 'MP10_VE','MP10_CQ',
        ]

# Parametros
Hi = 12
vcb = 150
N_int = 50

# Probamos largo de df_var
dias = np.ones(24+Hi)
OLS_itx = pd.DataFrame(columns=cols, index=range(24+Hi))

# Iteramos por hora del día
for i in range(-Hi,24):

    # Tomamos solo hora de interés, ahora con ventana 3 horas
    data = DF_h.copy()
    if i<0:
        data = data.shift(periods=-i)
        hi = 0
    else:
        hi = i
    mask = (data.index.hour != hi)
    data.loc[mask] = np.nan
    # sys.exit()
    # Promediamos y adjuntamos datos de intoxicados
    data = data.resample('D').mean()
    data['T59'] = T59['T59']
    
    # Hacemos Nan días sin intoxicados o con menos de cierto N 
    # mask =  (data['T59'] <= N_int)
    
    # Nos quedamos solo con eventos en Quintero
    # mask = (T59['Comuna'] != 'Quintero')|(data['T59'] <= N_int)
    
    # Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
    mask = (T59['Comuna'] == 'Puchuncaví')|(data['T59'] <= N_int)

    # Nos quedamos solo con eventos en Puchuncaví
    # mask = (T59['Comuna'] != 'Puchuncaví')|(data['T59'] <= N_int)
    
    # Nos quedamos con eventos en Quintero y Puchuncaví
    # mask = (T59['Comuna'] != 'Quintero y Puchuncaví')|(data['T59'] <= N_int)

    
    data.loc[mask] = np.nan
    data_T59 = data['T59'] # guardamos datos no estandarizados
    # sys.exit()
    # Estandarizamos
    data = (data-data.mean())/data.std()
    data['T59'] = data_T59 # redefinimos intoxicados sin estandar.
    
    ## Corremos modelo ##
    
    # Copiamos DF
    df = data.copy()
    
    # Drop missing values from relevant columns
    var = cols[1:len(cols)]
    df_var = df[['T59'] + var].dropna()
    
    X = df_var[var]
    y = df_var['T59']
    
    # Add intercept
    X = sm.add_constant(X)
    
    # Fit the model
    model = sm.OLS(y, X).fit()

    OLS_itx.loc[i+Hi,var] = model.params.values[1:len(cols)]
    OLS_itx.loc[i+Hi,'R2'] = model.rsquared
    dias[i] = len(df_var)

OLS_itx = OLS_itx.apply(pd.to_numeric)

# Ploteamos
fig , axs = plt.subplots(2,figsize = (20,10.5), layout='constrained',
                         gridspec_kw={'height_ratios': [3, 2]})

### Heatmap ###
var = cols[1:len(cols)]
sns.heatmap(OLS_itx[var].transpose(),cmap ='bwr',linecolor='black',
            linewidths = 0.08,vmin=-vcb,vmax=vcb, ax = axs[0],
            cbar_kws={'pad': 0.02})

axs[0].set_yticklabels(OLS_itx[var].columns.values,rotation=45, size=Hi,
                       fontweight='bold')
axs[0].set_ylabel('Coeficientes')
axs[0].xaxis.set_major_locator(ticker.IndexLocator(base=0.5,offset=0))
axs[0].set_xticks(np.arange(0.5,24.5+Hi,1))
axs[0].set_xticklabels(list(range(-Hi,24)),rotation=0)
axs[0].axvline(x=Hi, color='k', ls='--',lw=1.5)

# Colorbar
colorbar = axs[0].collections[0].colorbar

### R2 ###
sns.lineplot(OLS_itx['R2'], ax=axs[1],marker='o')
axs[1].set_xticks(list(range(24+Hi)))
axs[1].set_xticklabels(list(range(-Hi,24)),rotation=0)
axs[1].set_xlim(-0.5,23.5+Hi)
axs[1].axvline(x=Hi-0.5, color='k', ls='--',lw=1.5)
axs[1].set_xlabel('Hora')
axs[1].set_ylabel('R2')
axs[1].grid() 

fig.suptitle('Coeficientes y R2 según hora del día '+
             '(solo días con min='+str(N_int)+' intoxicaciones, N = '+
             str(int(dias.max()))+' días), usando '+str(Hi)+' horas previas')
fig.get_layout_engine().set(w_pad=0.2, h_pad=0.06)
# fig.subplots_adjust(top=0.1)

##################################################################
#%% Correr con ventanas de tiempo y desde horas previas al día ###

# Creamos Dataframe para guardar datos de modelo
cols = ['R2',
        # 'inv_princ',
        # 't_dmc',
        # 'hr_dmc',
        # 'p_dmc',
        # 'r_dmc',
        # 'u_princ','v_princ',
        # 'u_dmc','v_dmc',
        # 'u_VE','v_VE',
        # 'u_CQ','v_CQ',
        
        
        'HCNM_CQ',
        'CO_CQ',
        'SO2_CQ',
        'NO2_CQ',
        'NO_CQ',
        'O3_CQ',
        
        # 'HCNM_VE',
        # 'SO2_VE',
        # 'NO2_VE','NO_VE','O3_VE',
        
        # 'MP25_VE','MP25_CQ',
        # 'MP10_VE','MP10_CQ',
        ]
        
# Parametros
Hi = 12
vcb = 100
N_int = 50

# Creamos DFs
dias = np.ones(24+Hi)
OLS_itx = pd.DataFrame(columns=cols, index=range(24+Hi))

# Iteramos por hora del día
for i in range(-Hi,24):

    # Tomamos solo hora de interés, ahora con ventana 3 horas
    data = DF_h.copy()
    if i<=0:
        data = data.shift(periods=-i+1)
        hi = 1
    elif i==23:
        data = data.shift(periods=-1)
        hi = 22
    else:
        hi = i
    mask = (data.index.hour < hi-1)|(data.index.hour > hi+1)
    data.loc[mask] = np.nan
    # sys.exit()
    # Promediamos y adjuntamos datos de intoxicados
    data = data.resample('D').mean()
    data['T59'] = T59['T59']
    
    # Hacemos Nan días sin intoxicados o con menos de cierto N 
    # mask =  (data['T59'] <= N_int)
    
    # Nos quedamos solo con eventos en Quintero
    # mask = (T59['Comuna'] != 'Quintero')|(data['T59'] <= N_int)
    
    # Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
    mask = (T59['Comuna'] == 'Puchuncaví')|(data['T59'] <= N_int)

    # Nos quedamos solo con eventos en Puchuncaví
    # mask = (T59['Comuna'] != 'Puchuncaví')|(data['T59'] <= N_int)
    
    # Nos quedamos con eventos en Quintero y Puchuncaví
    # mask = (T59['Comuna'] != 'Quintero y Puchuncaví')|(data['T59'] <= N_int)

    
    data.loc[mask] = np.nan
    data_T59 = data['T59'] # guardamos datos no estandarizados
    # sys.exit()
    # Estandarizamos
    data = (data-data.mean())/data.std()
    data['T59'] = data_T59 # redefinimos intoxicados sin estandar.
    
    ## Corremos modelo ##
    
    # Copiamos DF
    df = data.copy()
    
    # Drop missing values from relevant columns
    var = cols[1:len(cols)]
    df_var = df[['T59'] + var].dropna()
    
    X = df_var[var]
    y = df_var['T59']
    
    # Add intercept
    X = sm.add_constant(X)
    
    # Fit the model
    model = sm.OLS(y, X).fit()

    OLS_itx.loc[i+Hi,var] = model.params.values[1:len(cols)]
    OLS_itx.loc[i+Hi,'R2'] = model.rsquared
    dias[i] = len(df_var)

OLS_itx = OLS_itx.apply(pd.to_numeric)

# Ploteamos
fig , axs = plt.subplots(2,figsize = (20,10.5), layout='constrained',
                         gridspec_kw={'height_ratios': [3, 2]})

### Heatmap ###
var = cols[1:len(cols)]
sns.heatmap(OLS_itx[var].transpose(),cmap ='bwr',linecolor='black',
            linewidths = 0.08,vmin=-vcb,vmax=vcb, ax = axs[0],
            cbar_kws={'pad': 0.02})

axs[0].set_yticklabels(OLS_itx[var].columns.values,rotation=45, size=13,
                       fontweight='bold')
axs[0].set_ylabel('Coeficientes')
axs[0].xaxis.set_major_locator(ticker.IndexLocator(base=0.5,offset=0))
axs[0].set_xticks(np.arange(0.5,24.5+Hi,1))
axs[0].set_xticklabels(list(range(-Hi,24)),rotation=0)
axs[0].axvline(x=Hi, color='k', ls='--',lw=1.5)

# Colorbar
colorbar = axs[0].collections[0].colorbar

### R2 ###
sns.lineplot(OLS_itx['R2'], ax=axs[1],marker='o')
axs[1].set_xticks(list(range(24+Hi)))
axs[1].set_xticklabels(list(range(-Hi,24)),rotation=0)
axs[1].set_xlim(-0.5,23.5+Hi)
axs[1].axvline(x=Hi-0.5, color='k', ls='--',lw=1.5)
axs[1].set_xlabel('Hora')
axs[1].set_ylabel('R2')
axs[1].grid() 

fig.suptitle('Coeficientes y R2 según hora del día '+
             '(solo días con min='+str(N_int)+' intoxicaciones, N = '+
             str(int(dias.max()))+' días), usando '+str(Hi)+
             ' horas previas y ventanas de 3 horas')
fig.get_layout_engine().set(w_pad=0.2, h_pad=0.06)
# fig.subplots_adjust(top=0.1)

########################################################
#%% Regresión Lineal Simple por variable: Coef. y R2 ###
##  HORAS PREVIAS DE A 1 HORA !!



variables = [
    
            'inv_princ','t_dmc','hr_dmc','mslp_dmc','r_dmc',
            'ws_VE','ws_princ','ws_dmc','ws_CQ',
            
            'u_princ','v_princ',
            'u_dmc','v_dmc',
            'u_VE','v_VE',
            'u_CQ','v_CQ',
        
        
            # 'HCNM_CQ','CO_CQ','SO2_CQ','NO2_CQ','NO_CQ','O3_CQ',
            # 'MP25_CQ','MP10_CQ',
        
            # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
            # 'MP25_VE','MP10_VE',

            ]
Hi = 12
vcb = 100
N_int = 50
dias = np.ones(24+Hi)
resultados = {}  # diccionario para guardar coef y R2 por variable

for var in variables:
    coef_list = []
    r2_list = []
    dias_validos = []
    
    for i in range(-Hi, 24):
        # data = DF_h[[var]].copy()
        data = DF_met_ha[[var]].copy()
        if i<0:
            data = data.shift(periods=-i)
            hi = 0
        else:
            hi = i
        mask = (data.index.hour != hi)            
        data.loc[mask] = np.nan
        data = data.resample('D').mean()
        data['T59'] = T59['T59']

        
        # Hacemos Nan días sin intoxicados o con menos de cierto N 
        # mask =  (data['T59'] <= N_int)
        
        # Nos quedamos solo con eventos en Quintero
        # mask = (T59['Comuna'] != 'Quintero')|(data['T59'] <= N_int)
        
        # Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
        mask = (T59['Comuna'] == 'Puchuncaví')|(data['T59'] <= N_int)

        # Nos quedamos solo con eventos en Puchuncaví
        # mask = (T59['Comuna'] != 'Puchuncaví')|(data['T59'] <= N_int)
        
        # Nos quedamos con eventos en Quintero y Puchuncaví
        # mask = (T59['Comuna'] != 'Quintero y Puchuncaví')|(data['T59'] <= N_int)
        
        data.loc[mask] = np.nan
        data_T59 = data['T59']
        
        data = (data - data.mean()) / data.std()
        data['T59'] = data_T59
        
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

    # if i == n_vars:
        # ax.xaxis.set_visible(False)
        # ax.set_xlabel(None)
        # ax.set_xlabel('Hora')
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
    
            # 'inv_princ','t_dmc','hr_dmc','mslp_dmc','r_dmc',
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
Hi = 23
vcb = 100
N_int = 50
dias = np.ones(24+Hi)
resultados = {}  # diccionario para guardar coef y R2 por variable

for var in variables:
    coef_list = []
    r2_list = []
    dias_validos = []
    
    for i in range(-Hi, 24):
        data = DF_h[[var]].copy()
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

        
        # Hacemos Nan días sin intoxicados o con menos de cierto N 
        # mask =  (data['T59'] <= N_int)
        
        # Nos quedamos solo con eventos en Quintero
        # mask = (T59['Comuna'] != 'Quintero')|(data['T59'] <= N_int)
        
        # Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
        mask = (T59['Comuna'] == 'Puchuncaví')|(data['T59'] <= N_int)

        # Nos quedamos solo con eventos en Puchuncaví
        # mask = (T59['Comuna'] != 'Puchuncaví')|(data['T59'] <= N_int)
        
        # Nos quedamos con eventos en Quintero y Puchuncaví
        # mask = (T59['Comuna'] != 'Quintero y Puchuncaví')|(data['T59'] <= N_int)
        
        data.loc[mask] = np.nan
        data_T59 = data['T59']
        
        data = (data - data.mean()) / data.std()
        data['T59'] = data_T59
        
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

    # if i == n_vars:
        # ax.xaxis.set_visible(False)
        # ax.set_xlabel(None)
        # ax.set_xlabel('Hora')
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
N_int = 80
# df = DF_met_ha.copy()
df = DF_h.copy()
var =  [
            # 'inv_princ','t_dmc','hr_dmc','mslp_dmc','r_dmc',
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
# N_int = 80
df = DF_met_ha.copy()
# df = DF_h.copy()
var =  [
            # 'inv_princ','t_dmc','hr_dmc','mslp_dmc','r_dmc',
            # 'ws_VE','ws_princ',
            # 'ws_dmc','ws_CQ',
            
            'u_VE','v_VE',
            'u_princ','v_princ',
            'u_dmc','v_dmc',
            'u_CQ','v_CQ',
        
            # 'HCNM_CQ','CO_CQ','SO2_CQ','NO2_CQ','NO_CQ','O3_CQ',
            # 'MP25_CQ','MP10_CQ',
        
            # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
            # 'MP25_VE','MP10_VE',
        ]


## Obtenemos días con más intoxicados
# data = T59.copy()
# mask_int = (data['T59'] != 0)
# data = data.loc[mask_int]
# data = data.sort_values(by='T59',ascending=False)


## Seleccionamos días con más de cierto Nde intoxicados
# mask =  (T59['T59'] >= N_int)

# Nos quedamos solo con eventos en Quintero
# mask = (T59['Comuna'] == 'Quintero')&(T59['T59'] >= N_int)

# Nos quedamos con eventos en Quintero y Quintero y Puchuncaví
# mask = (T59['Comuna'] != 'Puchuncaví')&(T59['T59'] >= N_int)

# Nos quedamos solo con eventos en Puchuncaví
# mask = (T59['Comuna'] == 'Puchuncaví')&(T59['T59'] >= N_int)

# Nos quedamos con eventos en Quintero y Puchuncaví
# mask = (T59['Comuna'] == 'Quintero y Puchuncaví')&(T59['T59'] <= N_int)

# dias = T59.loc[mask].index.astype(str).values
dias = [ts.strftime('%Y/%m/%d %H:%M') for ts in dias_exp]
ic = 0
for v in var:
    df_prom = pd.DataFrame(columns=dias,index=list(range(24*3)))
    color = COLOR_MAP[ic % len(COLOR_MAP)]
    fig, ax = plt.subplots(figsize=(20, 10.5))
    
    # Obtenemos valores de ciclo diarios para variable
    median, q10, q25, q75, q90 = cs.get_cycle_data(DF_h[v],
                                                   'H',[lambda x: x.hour])
    # Tomamos concatenamos 3 días
    median = pd.concat([median,median,median], ignore_index=True)
    q10 = pd.concat([q10,q10,q10], ignore_index=True)
    q25 = pd.concat([q25,q25,q25], ignore_index=True)
    q75 = pd.concat([q75,q75,q75], ignore_index=True)
    q90 = pd.concat([q90,q90,q90], ignore_index=True)
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
    for d in range(len(dias)):
        if d < len(ls):
            ils=d
        elif d > len(ls):
            ils=d-len(ls)
        t = pd.to_datetime(dias[d])
        t1 = t - datetime.timedelta(hours=24)
        t2 = t + datetime.timedelta(hours=47)
        df_prom.loc[:,dias[d]] = df.loc[t1:t2,v].astype(float).values

        alp = 0.6
        ax.plot(x,df.loc[t1:t2,v], color='grey',alpha=alp,ls='-',lw=0.5,
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
    
    ## Ploteamos media de días con más intoxicados
    ax.plot(x,df_prom.mean(axis=1),color='grey',ls='-',lw=1,marker='o',
            zorder=2)
    legend_elements.append(Line2D([0],[0],color='grey',ls='-',lw=1,marker='o',
                           label='Media intxs.'))
    ax.set_title(f"Ciclo diario {v}, días N-1, N y N+1", 
                 fontsize=15, weight='bold')
    ax.set_xlabel('Hora')
    ax.set_ylabel(f"{v}", rotation=90,
                  labelpad=10, fontsize=15, weight='bold')
    ax.legend(handles=legend_elements,framealpha=0.6,fontsize=7,
              handlelength=7,loc='upper right')
    ax.grid(True)
    ax.set_xticks(range(0, 72)[::6])
    ax.set_xticklabels(range(-24, 48)[::6])
    for i in [0,24,48,72]: ax.axvline(x=i, color='k', ls='--',lw=2)
    props = dict(boxstyle='round', facecolor='lightgrey', alpha=0.5)
    ax.text(0.18,0.95,'Día N-1', bbox=props,
            transform=ax.transAxes,fontsize=15,verticalalignment='top')
    ax.text(0.5,0.95,'Día N', bbox=props,
            transform=ax.transAxes,fontsize=15,verticalalignment='top')
    ax.text(0.8,0.95,'Día N+1', bbox=props,
            transform=ax.transAxes,fontsize=15,verticalalignment='top')
    plt.tight_layout()
    plt.show()
    ic = ic+1
    
######################################################
######################################################
#%%### Promedios diarios previos y posteriores ]######
######################################################
######################################################

# Con el fin de ver la evolución de promedios diarios previos y posteriores
# se plotearán estos

## Intoxicados y días:
N_int = 30
N_d = 5

## Definimos df data
data = DF_d.copy()
# data = DF_met_da.copy()

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
        # 'u_CQ','v_CQ',
        # 'ws_CQ',
        # 'inv_princ','t_princ',
        # 't_dmc','hr_dmc',
        # 'mslp_dmc',
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
    sns.violinplot(x='Día', y=v, data=df_melted, ax=ax, inner='quart',
                   fill=False,zorder=1)
    sns.stripplot(x='Día', y=v, data=df_melted, ax=ax, zorder=1,
                  jitter=False, color='grey', alpha=0.5)
    
    ax.set_title('Boxplot promedios diarios de días con mín. '+str(N_int)
                  +' intx. ('+str(len(dias))+' días), mostrando los '+str(N_d)+
                  ' días previos y posteriores')
    ax.set_xlabel('Día',fontweight='bold')
    ax.set_ylabel(v,fontweight='bold')


    
###############################################
###############################################
#%%######       Plots extras       ############
###############################################
###############################################


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
d1 = pd.to_datetime('2022-10-04 00:00:00')
d2 = pd.to_datetime('2022-10-04 23:00:00')

# Variables
data = DF_h.copy()
variables = [
    
            # 'inv_princ','t_dmc','hr_dmc','mslp_dmc','r_dmc',
            # 'ws_VE','ws_princ','ws_dmc','ws_CQ',
            'inv_princ','r_dmc',
            # 'u_VE','v_VE',
            # 'u_princ','v_princ',
            'u_dmc','v_dmc',
            'u_CQ','v_CQ',
        
            'HCNM_CQ','CO_CQ','SO2_CQ','NO2_CQ','NO_CQ','O3_CQ',
            'MP25_CQ','MP10_CQ',
        
            # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
            # 'MP25_VE','MP10_VE',

            ]

# Ploteamos
n_var = len(variables)
ax = data.loc[d1:d2,variables].plot(subplots=True, layout=(n_var,1)\
                                    ,grid=True, figsize=(10,1.5*n_var))
plt.tight_layout()



