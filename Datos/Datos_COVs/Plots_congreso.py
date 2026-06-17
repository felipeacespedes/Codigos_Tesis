# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 17:46:36 2024

@author: felip
"""

# Importamos librerías
import matplotlib.pyplot as plt
import pandas as pd
from Ternario_functs import COV_Ternary_tod_sb, COV_Ternary_tod_cb\
                            ,COV_Ternary_wd_sb, COV_Ternary_wd_cb

#%% Importamos Datos

# COVs PTR-MS-TOF
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
file = 'datos_inv/inv_data_1min.csv' #1min
COV = pd.read_csv(path+file,delimiter=';')
COV['date'] = pd.to_datetime(COV['date'],format='%d/%m/%Y %H:%M:%S')
COV['date'] = pd.to_datetime(COV['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV = COV.set_index('date')
COV_m = COV.copy() # copiamos minutario
COV = COV.resample('H').mean()
# Guardamos hora inicial y final de COV para cortar HCNM
Ti = COV.index[0]; Tf = COV.index[-1]

del path, file
#%% Creamos plot con 3 series de tiempo y 6 plot ternario

# La idea es plotear en 3 ejes:
    # 1. 3 series de tiempo y leyenda
    # 2. 3 plot ternarios wd y colorbar wd
    # 3. 3 plot ternarios tod y colorbar tod
    
#%% fila 1: series de tiempo

# Definimos COVs de interes
cov_ec = ['Benzene', 'Methanol', 'Ethyl.benzene_Xylenes','Propene_Cyclopropane',
          'Acetaldehyde','Toluene','Butenes','Acetone_propanal']

# Creamos figura
fig, axs = plt.subplots(1,3,sharey=True,figsize=(20,6))

## Serie 1: 12-09
date_1 = pd.to_datetime('2022-09-12 00:00:00')
date_2 = pd.to_datetime('2022-09-12 14:00:00')
# Ploteamos
COV_m.loc[date_1:date_2,cov_ec].plot(ax = axs[0],grid=True,ylim=(0,200),
                                     ylabel='ppb',label=None)

axs[0].set_title('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
          +date_2.strftime('%Y-%m-%d, %H:%M.'))
    
## Serie 2: 04-10
date_1 = pd.to_datetime('2022-10-03 23:00:00')
date_2 = pd.to_datetime('2022-10-04 14:00:00')
# Ploteamos
COV_m.loc[date_1:date_2,cov_ec].plot(ax = axs[1],grid=True,ylim=(0,200),
                                     ylabel='ppb',label=None)
axs[1].set_title('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
          +date_2.strftime('%Y-%m-%d, %H:%M.'))

## Serie 3: 07-10
date_1 = pd.to_datetime('2022-10-07 00:00:00')
date_2 = pd.to_datetime('2022-10-07 13:00:00')
# Ploteamos
COV_m.loc[date_1:date_2,cov_ec].plot(ax = axs[2],grid=True,ylim=(0,200),
                                     ylabel='ppb',label='_nolegend_')
axs[2].set_title('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
          +date_2.strftime('%Y-%m-%d, %H:%M.'))

fig.tight_layout()

#%% fila 2: 3 plot ternarios tod 

# Creamos figura
fig = plt.figure(figsize=(20,6))

## Ternario 1: 12-09
ax1 = plt.subplot(1,3,1, projection='ternary')
COV_Ternary_tod_sb(COV_m,'2022-09-12 00:00:00','2022-09-12 14:00:00', ax1)

## Ternario 2: 04-10
ax2 = plt.subplot(1,3,2, projection='ternary')
COV_Ternary_tod_sb(COV_m,'2022-10-03 23:00:00','2022-10-04 14:00:00', ax2)

## Ternario 3: 07-10
ax3 = plt.subplot(1,3,3, projection='ternary')
sc = COV_Ternary_tod_sb(COV_m,'2022-10-07 00:00:00','2022-10-07 13:00:00',ax3)

## Colorbar:
COV_Ternary_tod_cb(ax3,fig,sc)

plt.tight_layout(pad=1.4)

#%% fila 3: 3 plot ternarios wd

# Creamos figura
fig = plt.figure(figsize=(20,6))

## Ternario 1: 12-09
ax1 = plt.subplot(1,3,1, projection='ternary')
COV_Ternary_wd_sb(COV_m,'2022-09-12 00:00:00','2022-09-12 14:00:00', ax1)

## Ternario 2: 04-10
ax2 = plt.subplot(1,3,2, projection='ternary')
COV_Ternary_wd_sb(COV_m,'2022-10-03 23:00:00','2022-10-04 14:00:00', ax2)

## Ternario 3: 07-10
ax3 = plt.subplot(1,3,3, projection='ternary')
sc = COV_Ternary_wd_sb(COV_m,'2022-10-07 00:00:00','2022-10-07 13:00:00',ax3)

## Colorbar:
COV_Ternary_wd_cb(ax3,fig,sc)

plt.tight_layout(pad=1.8)

#%% Ahora juntamos las 3 figuras

# Figura y subfiguras
fig = plt.figure(figsize=(20,17))
subfigs = fig.subfigures(3, 1)

## fila 1: series de tiempo ##

# Definimos COVs de interes
cov_ec = ['Benzene', 'Methanol', 'Ethyl.benzene_Xylenes','Propene_Cyclopropane',
          'Acetaldehyde','Toluene','Butenes','Acetone_propanal']

# Creamos figura
axs = subfigs[0].subplots(1,3)#, sharey=True)

## Serie 1: 12-09
date_1 = pd.to_datetime('2022-09-12 00:00:00')
date_2 = pd.to_datetime('2022-09-12 14:00:00')
# Ploteamos
COV_m.loc[date_1:date_2,cov_ec].plot(ax = axs[0],grid=True,ylim=(0,50),
                                     ylabel='[ppb]')

axs[0].set_title('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
          +date_2.strftime('%Y-%m-%d, %H:%M.'))
axs[0].annotate('a)',xy=(-0.13, 1.04), xycoords='axes fraction',
                weight='bold',size=13)
    
## Serie 2: 04-10
date_1 = pd.to_datetime('2022-10-03 23:00:00')
date_2 = pd.to_datetime('2022-10-04 14:00:00')
# Ploteamos
COV_m.loc[date_1:date_2,cov_ec].plot(ax = axs[1],grid=True,ylim=(0,115),
                                     ylabel='[ppb]')
axs[1].set_title('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
          +date_2.strftime('%Y-%m-%d, %H:%M.'))

## Serie 3: 07-10
date_1 = pd.to_datetime('2022-10-07 00:00:00')
date_2 = pd.to_datetime('2022-10-07 13:00:00')
# Ploteamos
COV_m.loc[date_1:date_2,cov_ec].plot(ax = axs[2],grid=True,ylim=(0,185),
                                     ylabel='[ppb]')
axs[2].set_title('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
          +date_2.strftime('%Y-%m-%d, %H:%M.'))


## fila 2: 3 plot ternarios tod ##

# Ternario 1: 12-09
ax1 = subfigs[1].add_subplot(1,3,1, projection='ternary')
COV_Ternary_tod_sb(COV_m,'2022-09-12 00:00:00','2022-09-12 14:00:00', ax1)
ax1.annotate('b)',xy=(-0.16, 1.04), xycoords='axes fraction',
             weight='bold',size=13)

# Ternario 2: 04-10
ax2 = subfigs[1].add_subplot(1,3,2, projection='ternary')
COV_Ternary_tod_sb(COV_m,'2022-10-03 23:00:00','2022-10-04 14:00:00', ax2)

# Ternario 3: 07-10
ax3 = subfigs[1].add_subplot(1,3,3, projection='ternary')
sc = COV_Ternary_tod_sb(COV_m,'2022-10-07 00:00:00','2022-10-07 13:00:00',ax3)

# Colorbar:
COV_Ternary_tod_cb(ax3,fig,sc)


## fila 3: 3 plot ternarios wd ##

## Ternario 1: 12-09
ax1 = subfigs[2].add_subplot(1,3,1, projection='ternary')
COV_Ternary_wd_sb(COV_m,'2022-09-12 00:00:00','2022-09-12 14:00:00', ax1)
ax1.annotate('c)',xy=(-0.16, 1.04), xycoords='axes fraction',
             weight='bold',size=13)

## Ternario 2: 04-10
ax2 = subfigs[2].add_subplot(1,3,2, projection='ternary')
COV_Ternary_wd_sb(COV_m,'2022-10-03 23:00:00','2022-10-04 14:00:00', ax2)

## Ternario 3: 07-10
ax3 = subfigs[2].add_subplot(1,3,3, projection='ternary')
sc = COV_Ternary_wd_sb(COV_m,'2022-10-07 00:00:00','2022-10-07 13:00:00',ax3)

## Colorbar:
COV_Ternary_wd_cb(ax3,subfigs[2],sc)

plt.subplots_adjust(left = 0.05, top = 0.9, right = 0.91, bottom = 0.15,
                    hspace = 0.8, wspace = 0.12)

#%% Plotear varianzas de COVs

COV_m.std().sort_values(ascending=False).plot.bar(figsize=(10,7),zorder=2)
plt.title('COVs sorted by std, invierno 2022')
plt.ylabel('ppb')
plt.grid(zorder=0)
plt.tight_layout()

#%%

COV_m.loc[:,COV_m.std()>0.3]

