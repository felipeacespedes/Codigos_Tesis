# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 12:15:14 2024

@author: felip

Code created to try suggestions made by Pai
"""

#%% Importamos librerías
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#%% Definimos variables a utilizar

# Importamos HCNM, HCNM_m y HCNM_m_lod
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
HCNM = pd.read_pickle(path+'HCNM_orig_df.pkl')
HCNM_m = pd.read_pickle(path+'HCNM_mod_df.pkl')
HCNM_m_lod = pd.read_pickle(path+'HCNM_mod_lod_df.pkl')

# Fechas inicial y final
Fi = '2018-01-01'
Ff = '2023-12-31'

# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

# Estación
Est = 'Ventanas'

# Estaciones de interés
Est_ls = ['Ventanas','Centro_Quintero','Concón','Gaviotas','Colmo']


#%% Evaluamos la autocorrelación de HCNM para ver tamaño de ventana
lag = 10
lags = np.arange(-lag,lag+1,1)
acorr_df = pd.DataFrame(columns=HCNM.columns.values,index=lags)

# Evaluate autocorrelation with NaN values handled

for e in HCNM.columns.values:
    for l in lags:
        # Extract the series for the specific column and drop NaN values
        series_data = HCNM_m_lod[e].dropna()
        
        # Calculate autocorrelation for the lag
        acorr_df.loc[l, e] = series_data.autocorr(lag=l)

# Plot the autocorrelation
fig, ax = plt.subplots(figsize=(8, 6))
for e in HCNM.columns.values:
    ax.plot(lags, 1-acorr_df.loc[:, e], label=e)

ax.legend()
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
ax.set_title('Autocorrelation for Different Series and Lags')
plt.xlim(0,10)
plt.grid()
plt.show()


#%% Aplicamos media mobil a datos horarios

# Probameremos diferentes tamaños de ventana
window_size = 5
 
# Get the window of series
# of observations of specified window size
windows = HCNM_m_lod.rolling(window_size, center=True)
 
# Create a series of moving
# averages of each window
HCNM_ma = windows.mean()

# Serie Original
i = T.get_loc('2019-01-01 00:00:00')
f = T.get_loc('2019-02-01 23:00:00')
y_min = 0
y_max = 0.2
fig = plt.figure(figsize=(10,7))
# Serie Horaria Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],HCNM_m_lod[Est][i:f],zorder=2)
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Horaria Original '+Est)
plt.xticks(rotation=20)
plt.grid()
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],HCNM_ma[Est][i:f],zorder=2)
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Horaria '+Est+', aplicando Media Movil WZ=5')
plt.xticks(rotation=20)
plt.grid()
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Calculamos promedios diarios 

# T diario
Td = T[::24]

# Creamos DFs de estaciones para series diarias (Daily Average)
HCNM_pd = pd.DataFrame({'T': Td})
HCNM_pd = HCNM_pd.set_index('T')
HCNM_pd_ma = pd.DataFrame({'T': Td})
HCNM_pd_ma = HCNM_pd_ma.set_index('T') 

# Resampleamos a promedios diarios el dataframe de cada estación
for e in HCNM.columns.values:
    # resampleo de serie modificada
    HCNM_pd[e] = HCNM_m_lod[e].resample('24H').mean()
    # resampleo de serie modificada y con ma
    HCNM_pd_ma[e] = HCNM_ma[e].resample('24H').mean()

# probamos day of year
dias = HCNM_pd[0:365].index.dayofyear

#%% Aplicamos media mobil a datos diarios 

# Probameremos diferentes tamaños de ventana
window_size = 100
 
# Get the window of series
# of observations of specified window size
windows = HCNM_pd.rolling(window_size, center=True)
 
# Create a series of moving
# averages of each window
HCNM_ma_pd = windows.mean()

# Serie Original
i = Td.get_loc('2018-01-01 00:00:00')
f = Td.get_loc('2023-12-31 00:00:00')
y_min = 0
y_max = 0.3
fig = plt.figure(figsize=(20,10))
# Serie Original diaria
ax1 = plt.subplot(2,1,1)
ax1.plot(Td[i:f],HCNM_pd[Est][i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(Td[i],Td[f])
ax1.set_title('Serie Diaria Original '+Est)
plt.xticks(rotation=20)
plt.grid()
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(Td[i:f],HCNM_ma_pd[Est][i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(Td[i],Td[f])
ax2.set_title('Serie Diaria '+Est+', aplicando Media Movil WZ=100')
plt.xticks(rotation=20)
plt.grid()
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()



#%% Calculamos ciclos anuales con promedios diarios

# diccionario con ciclo anual para cada estación y contaminante/variable 
HCNM_ca = pd.DataFrame(columns=HCNM.columns.values,index=np.arange(1,366,1))
HCNM_ca_ma = pd.DataFrame(columns=HCNM.columns.values,index=np.arange(1,366,1))

for e in HCNM.columns.values:
    for d in range(365):
        HCNM_ca.loc[d+1,e] = HCNM_pd[e]\
            .loc[(HCNM_pd[e].index.dayofyear==d+1)].mean()
        HCNM_ca_ma.loc[d+1,e] = HCNM_pd_ma[e]\
            .loc[(HCNM_pd[e].index.dayofyear==d+1)].mean()


# ahora ploteamos todas las estaciones para la variable HCNM
for e in Est_ls:
    plt.figure(figsize=(20,10))
    HCNM_ca[e].plot(style='-',title=e,label='Serie')
    HCNM_ca_ma[e].plot(style='-',label='Serie MA')
    plt.legend()
    plt.grid()

#%% Calculamos promedios mensuales
 
# Creamos DFs de estaciones para series diarias (Daily Average)
HCNM_pm = pd.DataFrame({'T': T})
HCNM_pm = HCNM_pm.set_index('T')
HCNM_pm_ma = pd.DataFrame({'T': T})
HCNM_pm_ma = HCNM_pm_ma.set_index('T') 

# Resampleamos a promedios mensuales el dataframe de cada estación
for e in HCNM.columns.values:
    # resampleo de serie modificada
    HCNM_pm[e] = HCNM_m_lod[e].resample('M').mean()
    # resampleo de serie modificada y con ma
    HCNM_pm_ma[e] = HCNM_ma[e].resample('M').mean()


# # probamos day of year↑
# mes = HCNM_pm[0:12].index.month

#%% Calculamos ciclos anuales con promedios mensuales

# Dataframe con ciclo anual para cada estación y contaminante/variable 
HCNM_ca = pd.DataFrame(columns=HCNM.columns.values,index=np.arange(1,13,1))
HCNM_ca_ma = pd.DataFrame(columns=HCNM.columns.values,index=np.arange(1,13,1))

for e in HCNM.columns.values:
    for m in range(12):
        HCNM_ca.loc[m+1,e] = HCNM_pm[e]\
            .loc[(HCNM_pm[e].index.month==m+1)].mean()
        HCNM_ca_ma.loc[m+1,e] = HCNM_pm_ma[e]\
            .loc[(HCNM_pm[e].index.month==m+1)].mean()
        
# ahora ploteamos todas las estaciones para la variable HCNM
for e in Est_ls:
    plt.figure(figsize=(20,10))
    HCNM_ca[e].plot(style='-',title=e,label='Serie')
    HCNM_ca_ma[e].plot(style='-',label='Serie MA')
    plt.legend()
    plt.grid()


#%% Calculamos ciclo semanal con promedios diarios y media mobil

# Dataframe con ciclo semanal para cada estación y contaminante 
HCNM_cs = pd.DataFrame(columns=HCNM.columns.values,index=np.arange(1,8,1))
HCNM_cs_ma = pd.DataFrame(columns=HCNM.columns.values,index=np.arange(1,8,1))

for e in Est_ls:
    for d in range(7):
        HCNM_cs.loc[d+1,e] = \
            HCNM_pd[e].loc[(HCNM_pd[e].index.dayofweek==d)].mean()
        HCNM_cs_ma.loc[d+1,e] = \
            HCNM_pd_ma[e].loc[(HCNM_pd_ma[e].index.dayofweek==d)].mean()

# ahora ploteamos todas las estaciones para la variable HCNM
for e in Est_ls:
    plt.figure(figsize=(20,10))
    HCNM_cs[e].plot(style='-',title=e,label='Serie')
    HCNM_cs_ma[e].plot(style='-',label='Serie MA')
    plt.legend()
    plt.grid()
    
#%% Calculamos ciclo diario ustilizando media mobil

# ahora creamos ciclo diario

# horas = T[0:24].hour

# Datarfame con ciclo diario para cada estación y contaminante/variable 
HCNM_cd = pd.DataFrame(columns=HCNM.columns.values,index=np.arange(0,24,1))
HCNM_cd_ma = pd.DataFrame(columns=HCNM.columns.values,index=np.arange(0,24,1))

for e in Est_ls:
    for h in range(24):
        HCNM_cd.loc[h,e] = HCNM_m_lod.loc[(HCNM_m_lod.index.hour==h),e].mean()
        HCNM_cd_ma.loc[h,e] = HCNM_ma.loc[(HCNM_ma.index.hour==h),e].mean()

# ahora ploteamos todas las estaciones para la variable HCNM
for e in Est_ls:
    plt.figure(figsize=(20,10))
    HCNM_cd[e].plot(style='-',title=e,label='Serie')
    HCNM_cd_ma[e].plot(style='-',label='Serie MA')
    plt.legend()
    plt.grid()
        
        
        
        
