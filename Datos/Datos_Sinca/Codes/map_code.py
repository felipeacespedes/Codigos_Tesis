# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 19:10:11 2023

@author: felip
"""

import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.pyplot as plt
import matplotlib as pl
import numpy as np
# import pandas as pd


#%% We define a dictionary to save the meteo stations to display with cartopy

# Diccionario
Dic = {}

# Station names
Dic['Estaciones'] = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura' \
                     ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo']

# Station short names
Dic['Abreviación_Estaciones'] = ['VE','LM','CQ','LO' \
                                 ,'SU','JV','CC','GA','CO']

# Latitudes of stations
Dic['Lat'] = [-32.741822,-32.764257,-32.787721,-32.794914,-32.801052
              ,-32.935160,-32.924531,-32.915544,-32.929497]

# Longitudes of stations
Dic['Lon'] = [-71.480928,-71.454400,-71.532226,-71.496420,-71.483406
              ,-71.525804,-71.515441,-71.481469,-71.440576]

#%% Now we load the shapefiles, or convert them from kml, if thats the case

# loading of regions (states)
path_reg = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Regiones/'+\
            'Regional.shp'
reg = ShapelyFeature(Reader(path_reg).geometries(), ccrs.Mercator.GOOGLE)

# loading of urban zones
path_urb = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Areas_Pobladas/'+\
            'Areas_Pobladas.shp'
urb = ShapelyFeature(Reader(path_urb).geometries(), ccrs.Mercator.GOOGLE)


# now we load the converted shapefile 
path_zi = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/py/'\
            +'Zona_Industrial.shp'


zi = ShapelyFeature(Reader(path_zi).geometries(), ccrs.PlateCarree())

#%% Now, let's plot it using cartopy

# Input
region = [-71.6, -71.4, -32.95, -32.7]
data = np.arange(0,len(Dic['Estaciones'])*5,5)
lon = Dic['Lon']
lat = Dic['Lat']

# Color Map
cmap = pl.colormaps.get_cmap('hsv')
colors = data

# Definimos figura y ejes
fig, ax = plt.subplots(figsize=(7,8), subplot_kw={'projection': ccrs.PlateCarree()})

# Definimos región
ax.set_extent(region)

# Regions (linea de costa)
ax.add_feature(reg, alpha=0.4, linewidth=.8, facecolor="gray", edgecolor='black',
                zorder=1)
# Urban zones
ax.add_feature(urb, alpha=0.2, linewidth=.8, facecolor="yellow", edgecolor='black',
                zorder=2)


# Industrial zones 
ax.add_feature(zi, alpha=1, linewidth=.8, facecolor="green", edgecolor='black',
                zorder=4)



# adding of stations as scatter points
sc = ax.scatter(lon, lat, s=130, c=colors, cmap=cmap, transform=ccrs.Geodetic()\
                ,edgecolors='black',zorder=5)
    
# adding names of stations as text beside of every scatter point
ei = 0
for e in Dic['Abreviación_Estaciones']:
    ax.text(lon[ei]-0.005,lat[ei]+0.005,e, fontsize=15,zorder=6)
    ei = ei+1
del e, ei

# adding colorbar
fig.colorbar(sc, extend='both', label='bla')

# adding gridlines
gr = ax.gridlines(draw_labels=True, dms=True,alpha=0.5, zorder=4)
gr.top_labels = False
gr.right_labels = False