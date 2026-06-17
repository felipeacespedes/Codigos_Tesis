# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 10:36:19 2024

@author: felip

Código para inspección de datos nefo
"""
# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from netCDF4 import Dataset

#%% Info Relevante

# -La frecuencia temporal es cada 16 segundos.

#%% Importamos datos

# Probamos importando 1 día
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Nefo/octubre_puchu/'
## L1
# nc_file = Dataset(path+'L1_320117_202209120000_Puchuncavi.nc')
# L2
nc_file = Dataset(path+'L2_320117_202210070000_Puchuncavi.nc')
## L3
# nc_file = Dataset(path+'L3_DEFAULT_320117_202210070000'+
#                   '_1_360_1_3120_10_30_4000_3_0_1_500_1000_4000_60_'+
#                   'Puchuncavi.nc')



# Extraemos variables de interes
time= nc_file['time'][:]
date_stamp = nc_file['date_stamp'][:]
range_h = nc_file['range'][:]
# cloud_status = nc_file['cloud_status'][:]
cloud_data = nc_file['cloud_data'][:]
## L1
# data = nc_file['rcs_910'][:]
## L2
data = nc_file['profile_data'][:]
## L3
# data = nc_file['Bs_profile_data'][:]
# data = nc_file['Ng_profile_data'][:]
# data = nc_file['Ec_profile_data'][:]

# mean_layer_height = nc_file['Mean_Layer_Height'][:]
# bl_height_length = nc_file['bl_height_length'][:]

#%% Procesamiento datos Nefo

# Profe Ricardo dice que valores menores a 0 deben setearse a 0 y  mayores 
# a 3000 deben setearse a 3000.

# Menores a 0
data[data <= 0] = 0 

# Mayores a 3000
data[data >= 3000] = 3000 

#%% Let's build a DataFrame!

# 16 seg
NEFO = pd.DataFrame(index=pd.to_datetime(date_stamp[:,0]))
NEFO[['CloudData0','CloudData1','CloudData2']] = cloud_data
# NEFO['CloudStatus'] = cloud_status
# NEFO['MeanLayerHeight'] = mean_layer_height
# NEFO['BLHeightLength'] = bl_height_length

# # 30 seg
# NEFO_30s = NEFO.resample('30s').mean()

# # 1 min
# NEFO_1m = NEFO.resample('1min').mean()


#%% Let's plot!
#%% Serie de timepo 3 rangos de espectros de retrodispersión

# NEFO.plot(subplots=True,figsize=(10,5),grid=True,linewidth=1.5)
# NEFO['MeanLayerHeight'].plot(figsize=(20,10),grid=True, marker='o',linewidth=1)
# plt.ylim(0,1200)
# plt.xlim(NEFO.index[0],NEFO.index[-1])
# plt.tight_layout()

#%% Contourf de espectro de retrodispersión

fig,(ax,cax) = plt.subplots(1,2,figsize=(10,5),
                            gridspec_kw={'width_ratios': [40, 1]})
# ax: contourf de retrodisersión
CT = ax.contourf(pd.to_datetime(date_stamp[:,0]),range_h,data.transpose(),
                 cmap='jet',levels=np.arange(0,3001,250))
# NEFO['CloudData0'].plot(figsize=(10,5),grid=True, marker='*',
#                         linewidth=0,ax=ax)#*0.3048

ax.set_ylim(0,1200)
ax.set_ylabel('Altura [m]')
ax.set_xlabel('Hora [s]')
ax.grid(visible=True,axis='both',alpha=0.7)
# cax: colorbar de contourf
cbar = plt.colorbar(CT, cax=cax, label = 
                    r'Insensidad $[10^{5} srad \cdot km]^{-1}$',pad=0.1)
# norm = colors.Normalize(vmin=0, vmax=3000)
# sm = plt.cm.ScalarMappable(norm=norm, cmap = CT.cmap)
# sm.set_array([])
# cbar = plt.colorbar(sm, cax=cax, ticks=CT.levels,
#                     label = r'Insensidad $[srad \cdot km]^{-1}$',pad=0.1)


fig.suptitle('Señal de Retrodispersión '+
             pd.to_datetime(date_stamp[0,0]).strftime('%Y-%m-%d'))
fig.tight_layout()