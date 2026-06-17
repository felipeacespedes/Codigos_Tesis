# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 11:28:05 2023

@author: cr2_usuario
"""

# %% Cargar librerias

import numpy as np
import pandas as pd
import matplotlib as mpl
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from Graficos_Hysplit import plot_traj

# %% Cargar archivos

# Ruta de trayectorias
path = "C:/Users/cr2_usuario/Desktop/Quintero/Paper/BT_QUIN/"
# Ruta de limites regionales
path_reg = "C:/Users/cr2_usuario/Desktop/Quintero/Chile_shp/Regiones/Regional.shp"
# Ruta de figuras
path_fig = "C:/Users/cr2_usuario/Desktop/Quintero/Paper/Resultados/"

# Cargar trayectorias en 2 dfolds
dfold1 = pd.DataFrame()
dfold2 = pd.DataFrame()
k = 0
for p in range(1,10):
    # Cargar episodio 1
    fn = "QUIN_bt_ep1_P"+str(p)+"_100.csv"
    df = pd.read_csv(path+fn, sep=";", index_col=0, parse_dates=[1,3])
    df = df.loc[range(2,13,2)]
    df.reset_index(inplace=True)
    df = pd.concat([pd.DataFrame({"P":np.repeat("P"+str(p), len(df))}), df], axis=1)
    df.set_index("P", inplace=True)
    dfold1 = pd.concat([dfold1, df])
    
    # Cargar episodio 2
    fn = "QUIN_bt_ep2_P"+str(p)+"_100.csv"
    df = pd.read_csv(path+fn, sep=";", index_col=0, parse_dates=[1,3])
    df = df.loc[range(2,13,2)]
    df.reset_index(inplace=True)
    df = pd.concat([pd.DataFrame({"P":np.repeat("P"+str(p), len(df))}), df], axis=1)
    df.set_index("P", inplace=True)
    dfold2 = pd.concat([dfold2, df])
    
# %% Filtrar trayectorias hasta 4 horas

dfold1 = dfold1[dfold1.Timestep >= -4]
dfold2 = dfold2[dfold2.Timestep >= -4]
    
# %% Cargar shapefile

reg = ShapelyFeature(Reader(path_reg).geometries(), crs=ccrs.Mercator.GOOGLE)
# reg = reg.intersecting_geometries(zoom)
# %% Graficos

# Limite del mapa
zoom = [-71.86, -71.2, -33.48, -32.63]

lon_ticks = np.arange(-71.9, -71.1, 0.3) 
lat_ticks = np.arange(-33.4, -32.62, 0.2)

cmap = mpl.colormaps['tab10'](np.linspace(0,1,10))
cmap = cmap[[0,1,2,3,4,5,6,8,9]]

for i in [1,2]:
    if i == 1:
        fig, ax = plot_traj(dfold1, extent=zoom, ticks=[lon_ticks, lat_ticks], 
                            land=False, cmap=cmap, figsize=[5.5,6])
    else:
        fig, ax = plot_traj(dfold2, extent=zoom, ticks=[lon_ticks, lat_ticks], 
                            land=False, cmap=cmap, figsize=[5.5,6])
    
    # Añade linea de costa
    ax.add_feature(reg, alpha=0.4, linewidth=.8, facecolor="gray", edgecolor='None',
                    zorder=1)
    ax.add_feature(reg, alpha=1, linewidth=.8, facecolor="None", edgecolor='black',
                    zorder=8)
    
    # Guardar imagen
    fig.savefig(path_fig+"BT_QUIN_EP"+str(i)+"_4H.png", dpi=600)