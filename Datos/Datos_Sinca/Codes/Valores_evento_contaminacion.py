# -*- coding: utf-8 -*-
"""
Created on Tue May 20 13:13:33 2025

@author: felip
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
#%% Importamos datos horarios de HCNM por estación 

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'

HCNM = pd.read_csv(path+'HCNM_mod_lod_df.csv',# HCNM_mod_lod_df ó HCNM_orig_df
                   index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])
del path
#%%

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'

WD = pd.read_csv(path+'WD_df.csv',
                   index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])

WS = pd.read_csv(path+'WS_df.csv',
                   index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])
del path
#%% Definimos periodos de altas rm

#%% Lista con fechas

EC = [# marzo 2023
      '2023-03-14','2023-03-17','2023-03-23','2023-03-29','2023-03-30',
      '2023-03-31',
      # abril 2023
      '2023-04-03','2023-04-04',
      # mayo 2023
      '2023-05-23','2023-05-29','2023-05-30']

#%% Ploteamos por separado

# Lista de estaciones
le = ['Ventanas','Centro_Quintero']#,'Concón','Colmo']

for est in le:
    
    # 3 std = 99.8 th percentile (se conversó al comenzar la tesis con Rodrigo):
    peak_3std = HCNM[est].quantile(0.998)

    # 99 th percentile (extreme event according to Johnston 2011)
    peak_99perc = HCNM[est].quantile(0.99)

    # 95 th percentile (solo exploratorio, fue preguntado por Rodrigo):
    peak_95perc = HCNM[est].quantile(0.95)

    if est == 'Ventanas':
        ymax = 2
    elif est == 'Centro_Quintero':
        ymax = 6
    
    for date in EC:
        
        # Definimos fechas
        date_2 = pd.to_datetime(date+' 23:00:00')
        date_1 = date_2 - datetime.timedelta(hours=29)
        
        plt.figure()
        
        ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(14,7),
                                              ylim=(-0.01,ymax), marker='o')
        plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
                   .format(peak_3std), linestyle='dashed', color='m')
        plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
                   .format(peak_99perc), linestyle='dashed', color='g')
        plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
                   .format(peak_95perc), linestyle='dashed', color='c')
        plt.ylabel('HCNM [ppm]')
        plt.title('Valores de Cota Inferior de Razón de Mezcla para Evento de'\
                  +f' Contaminación por HCNM en {est}, Eventos 2023')
        plt.legend()
        plt.tight_layout()
del le, peak_3std, peak_95perc, peak_99perc, ymax, date_1, date_2, ax, est, date
#%% Ploteamos subplots

# Lista de estaciones
le = ['Ventanas','Centro_Quintero','Concón']

for date in EC:
    
    # Definimos fechas
    date_2 = pd.to_datetime(date+' 12:00:00')
    date_1 = date_2 - datetime.timedelta(hours=14)
    date_2 = date_2 + datetime.timedelta(hours=12)
    
    fig , ax = plt.subplots(3,1, figsize=(8,10), sharex=True)
    
    axi = 0    
    for est in le:
        
        # 3 std = 99.8 th percentile (se conversó al comenzar la tesis con Rodrigo):
        peak_3std = HCNM[est].quantile(0.998)

        # 99 th percentile (extreme event according to Johnston 2011)
        peak_99perc = HCNM[est].quantile(0.99)

        # 95 th percentile (solo exploratorio, fue preguntado por Rodrigo):
        peak_95perc = HCNM[est].quantile(0.95)

        if est == 'Ventanas':
            ymax = 1
        elif est == 'Centro_Quintero':
            ymax = 2.5
        elif est == 'Concón':
            ymax = 2
        elif est == 'Colmo':
            ymax = 1
        
        HCNM.loc[date_1:date_2,est].plot(ax = ax[axi],grid=True,
                                         ylim=(-0.01,ymax),marker='o')
        ax[axi].hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
                   .format(peak_3std), linestyle='dashed', color='m')
        ax[axi].hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
                   .format(peak_99perc), linestyle='dashed', color='g')
        ax[axi].hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
                   .format(peak_95perc), linestyle='dashed', color='c')
        ax[axi].set_ylabel('HCNM [ppm]')
        ax[axi].legend()
        axi = axi + 1
    fig.suptitle(date)
    fig.tight_layout()
del le, peak_3std, peak_95perc, peak_99perc, ymax, date_1, date_2, 
fig, ax, est, date
#%% Vientos 

#%% Dirección

le = ['Ventanas','Centro_Quintero','Concón']

for date in EC:
    
    # Definimos fechas
    date_2 = pd.to_datetime(date+' 23:00:00')
    date_1 = date_2 - datetime.timedelta(hours=29)
    date_2 = date_2 + datetime.timedelta(hours=13)
    
    fig , ax = plt.subplots(4,1, figsize=(8,14), sharex=True)
    axi = 0    
    for est in le:
        WD.loc[date_1:date_2,est].plot(ax = ax[axi],grid=True,lw=0,
                                         ylim=(0,360),marker='o',markersize=5)
        ax[axi].set_ylabel('Dirección [°]')
        ax[axi].legend()
        axi = axi + 1
    fig.suptitle(date)
    fig.tight_layout()

del le, date_1, date_2, fig, ax, axi, date, est
#%% Velocidad 

le = ['Ventanas','Centro_Quintero','Concón']

for date in EC:
    
    # Definimos fechas
    date_2 = pd.to_datetime(date+' 23:00:00')
    date_1 = date_2 - datetime.timedelta(hours=29)
    date_2 = date_2 + datetime.timedelta(hours=13)
    
    fig , ax = plt.subplots(4,1, figsize=(8,14), sharex=True)
    axi = 0    
    for est in le:
        WS.loc[date_1:date_2,est].plot(ax = ax[axi],grid=True,lw=1,
                                         ylim=(0,8),marker='o',markersize=5)
        ax[axi].set_ylabel('Velocidad [m/s]')
        ax[axi].legend()
        axi = axi + 1
    fig.suptitle(date)
    fig.tight_layout()
    
#####################################
#%% Comparación con intoxicaciones ##
#####################################
#%% Importamos datos T59

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'

T59 = pd.read_csv(path+'serie_T59full.csv', index_col='date',
                  parse_dates=True, infer_datetime_format = True )

#%% sumamos Ventanas y Centro Quintero

HCNM['VE+CQ'] = HCNM['Ventanas'] + HCNM['Centro_Quintero']

#%% Pasamos a resolución diario HCNM

HCNM_day = HCNM.resample('D').max()

#%% Correlación

# Creamos dataframe
date_1 = pd.to_datetime('2023-03-14 00:00:00')
date_2 = pd.to_datetime('2023-06-22 23:00:00')
HCNM_23 = HCNM_day.loc[date_1:date_2]
HCNM_23['T59'] = T59.loc[date_1:date_2,'T59']

# Vemos matriz de correlación
HCNM_23.corr(method='pearson')

# del HCNM_23
#%% Ploteamos periodo completo


le = ['Ventanas','Centro_Quintero']

    
# Definimos fechas
# date_1 = pd.to_datetime('2023-03-14 00:00:00')
# date_2 = pd.to_datetime('2023-06-22 23:00:00')
date_1 = pd.to_datetime('2023-05-23 00:00:00')
date_2 = pd.to_datetime('2023-06-08 00:00:00')

fig , ax = plt.subplots(3,1, figsize=(13,12), sharex=True)

axi = 0    
for est in le:
    
    # # 3 std = 99.8 th percentile (se conversó al comenzar la tesis con Rodrigo):
    # peak_3std = HCNM[est].quantile(0.998)

    # # 99 th percentile (extreme event according to Johnston 2011)
    # peak_99perc = HCNM[est].quantile(0.99)

    # # 95 th percentile (solo exploratorio, fue preguntado por Rodrigo):
    # peak_95perc = HCNM[est].quantile(0.95)

    if est == 'Ventanas':
        ymax = 1
    elif est == 'Centro_Quintero':
        ymax = 3
    elif est == 'Concón':
        ymax = 2
    
    HCNM.loc[date_1:date_2,est].plot(ax = ax[axi],grid=True,marker='o',
                                     ylim=(-0.01,ymax))
    # ax[axi].hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
    #            .format(peak_3std), linestyle='dashed', color='m')
    # ax[axi].hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
    #            .format(peak_99perc), linestyle='dashed', color='g')
    # ax[axi].hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
    #            .format(peak_95perc), linestyle='dashed', color='c')
    ax[axi].set_ylabel('HCNM [ppm]')
    ax[axi].legend()
    axi = axi + 1

# Intoxicados
T59.loc[date_1:date_2,'T59'].plot(ax = ax[2],grid=True,marker='o')
ax[2].set_ylabel('Intoxicados')
ax[2].legend()

fig.suptitle(str(date_1)+' a '+str(date_2))
fig.tight_layout()
del le

#########################################################
#%% Ploteamos periodo horario pero solo horas de mañana #
#########################################################

# Seleccionamos horas entre las a 6:00-11:00 para antes de 1 abril
# y las 7:00-12:00 a partir del 1 de abril

le = ['Ventanas','Centro_Quintero','Concón']

# Creamos dataframes para periodos de eventos 2023
date_1 = pd.to_datetime('2023-03-14 00:00:00')
date_2 = pd.to_datetime('2023-03-31 23:00:00')
HCNM_23_1 = HCNM.loc[date_1:date_2,le]
date_1 = pd.to_datetime('2023-04-01 00:00:00')
date_2 = pd.to_datetime('2023-06-22 23:00:00')
HCNM_23_2 = HCNM.loc[date_1:date_2,le]

# Hacemos nan horas no utiles antes del 1 de Abril
mask =  (HCNM_23_1.index.hour < 5) | (19 < HCNM_23_1.index.hour)
HCNM_23_1.loc[mask] = np.nan

# Hacemos nan horas no utiles después del 1 de Abril
mask =  (HCNM_23_2.index.hour < 6) | (20 < HCNM_23_2.index.hour)
HCNM_23_2.loc[mask] = np.nan

# Juntamos dataframes
date_1 = pd.to_datetime('2023-03-14 00:00:00')
date_2 = pd.to_datetime('2023-06-22 23:00:00')
HCNM_23 = HCNM.loc[date_1:date_2,le]

HCNM_23.loc[HCNM_23_1.index,le] = HCNM_23_1
HCNM_23.loc[HCNM_23_2.index,le] = HCNM_23_2

# sumamos Ventanas y Quintero
HCNM_23['VE+CQ'] = HCNM_23['Ventanas'] + HCNM_23['Centro_Quintero']

# Pasamos a resolución diario HCNM
HCNM_23_day = HCNM_23.resample('D').quantile(0.5)

#%% Correlación

# Creamos dataframe
date_1 = pd.to_datetime('2023-03-14 00:00:00')
date_2 = pd.to_datetime('2023-06-22 23:00:00')
HCNM_23_day['T59'] = T59.loc[date_1:date_2,'T59']

# sumamos Ventanas y Quintero
HCNM_23_day['VE+CQ'] = HCNM_23_day['Ventanas'] + HCNM_23_day['Centro_Quintero']

# Vemos matriz de correlación
HCNM_23_day.corr(method='pearson')

#%% Ploteamos

le = ['Ventanas','Centro_Quintero']
    
# Definimos fechas
date_1 = pd.to_datetime('2023-03-14 00:00:00')
date_2 = pd.to_datetime('2023-06-22 23:00:00')

fig , ax = plt.subplots(3,1, figsize=(13,12), sharex=True)

axi = 0    
for est in le:
    
    # # 3 std = 99.8 th percentile (se conversó al comenzar la tesis con Rodrigo):
    # peak_3std = HCNM[est].quantile(0.998)

    # # 99 th percentile (extreme event according to Johnston 2011)
    # peak_99perc = HCNM[est].quantile(0.99)

    # # 95 th percentile (solo exploratorio, fue preguntado por Rodrigo):
    # peak_95perc = HCNM[est].quantile(0.95)

    if est == 'Ventanas':
        ymax = 2
    elif est == 'Centro_Quintero':
        ymax = 2
    elif est == 'Concón':
        ymax = 2
    
    HCNM_23_day.loc[date_1:date_2,est].plot(ax = ax[axi],grid=True,marker='o',
                                     ylim=(-0.01,ymax))
    # ax[axi].hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
    #             .format(peak_3std), linestyle='dashed', color='m')
    # ax[axi].hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
    #             .format(peak_99perc), linestyle='dashed', color='g')
    # ax[axi].hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
    #             .format(peak_95perc), linestyle='dashed', color='c')
    ax[axi].set_ylabel('HCNM [ppm]')
    ax[axi].legend()
    axi = axi + 1

# Intoxicados
T59.loc[date_1:date_2,'T59'].plot(ax = ax[2],grid=True,marker='o')
ax[2].set_ylabel('Intoxicados')
ax[2].legend()

fig.suptitle(str(date_1)+' a '+str(date_2))
fig.tight_layout()
del le


