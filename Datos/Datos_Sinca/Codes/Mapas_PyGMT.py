# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:16:01 2023

@author: felip

Código para plotear mapas vectoriales con la librería PyGMT

"""
# Importamos librerías

import pygmt as pg
# Prueba pygmt:
# pg.test()
# en la prueba hubieron algunos errores, pero según:
# https://forum.generic-mapping-tools.org/t/about-pygmt-test/598
# , no deberían ser problema para datos con datos vectoriales

import cartopy.crs as ccrs
# import cartopy.feature as cf
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
# import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as pl
import numpy as np
import pandas as pd
from import_var import import_var
import os.path

# import fiona
# fiona.drvsupport.supported_drivers['KML'] = 'rw'


#%% Definimos diccionario con estaciones y coordenadas

# Diccionario
Dic = {}

Dic['Estaciones'] = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura' \
                     ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo']

Dic['Abreviación_Estaciones'] = ['VE','LM','CQ','LO' \
                                 ,'SU','JV','CC','GA','CO']

    
Dic['Lat'] = [-32.741822,-32.764257,-32.787721,-32.794914,-32.801052
              ,-32.935160,-32.924531,-32.915544,-32.929497]

Dic['Lon'] = [-71.480928,-71.454400,-71.532226,-71.496420,-71.483406
              ,-71.525804,-71.515441,-71.481469,-71.440576]
    
Dic['Variables_Cont'] = ['SO2','CH4','HCNM','HCT','CO','MP25','MP10']

Dic['Unidades_Cont'] = ['ppb','ppm','ppm','ppm','ppm']

Dic['Variables_Meteo'] = ['Velocidad','Dirección']

Dic['Unidades_Meteo'] = ['m/s','°']

Dic['Variables'] = ['SO2','CH4','HCNM','HCT','CO','MP25','MP10' \
                    ,'Velocidad','Dirección']

# por ahora usamos el periodo que sabemos que esta relativamente bien
Fi = '2020-01-01'
Ff = '2022-12-31'

# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

#%% Definimos variables en DFs

# Creamos diccionario de estaciones
Est = {}

# Creamos array con Nans para rellenar las variables que no existan
nan = np.empty(len(T)); nan[:] = np.nan

# Importamos variables de contaminantes a dataframe de cada estación
for e in range(len(Dic['Estaciones'])):
    Est[Dic['Estaciones'][e]] = pd.DataFrame({'T': T})
    Est[Dic['Estaciones'][e]] = Est[Dic['Estaciones'][e]].set_index('T')
    for v in range(len(Dic['Variables_Cont'])):
        file = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/'\
        +Dic['Estaciones'][e]+'/Cont/'+Dic['Variables_Cont'][v]+'.csv'
        if os.path.isfile(file) == True:
            Est[Dic['Estaciones'][e]][Dic['Variables_Cont'][v]] = import_var(\
                Dic['Estaciones'][e],'Cont',Dic['Variables_Cont'][v],Fi,Ff)
        else:
            Est[Dic['Estaciones'][e]][Dic['Variables_Cont'][v]] = nan
        del file
        
# Añadimos variables meteorológicas
for e in range(len(Dic['Estaciones'])):
    for v in range(len(Dic['Variables_Meteo'])):
        file = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/'\
        +Dic['Estaciones'][e]+'/Meteo/'+Dic['Variables_Meteo'][v][0:3]+'.csv'
        if os.path.isfile(file) == True:
            Est[Dic['Estaciones'][e]][Dic['Variables_Meteo'][v]] = import_var(\
            Dic['Estaciones'][e],'Meteo',Dic['Variables_Meteo'][v][0:3],Fi,Ff)
        
        else:
            Est[Dic['Estaciones'][e]][Dic['Variables_Meteo'][v]] = nan
        del file
        
del v, e

#%% Importamos mapas vectoriales de la BCN y KML de Zona Industrial

## BCN
# Regiones
path_reg = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Regiones/'+\
            'Regional.shp'
reg = ShapelyFeature(Reader(path_reg).geometries(), crs=ccrs.Mercator.GOOGLE)

# Zonas Urbanas
path_urb = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Areas_Pobladas/'+\
            'Areas_Pobladas.shp'
urb = ShapelyFeature(Reader(path_urb).geometries(), crs=ccrs.Mercator.GOOGLE)

# Nombres Geograficos: Toponimos
path_nom = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Toponimos/'+\
            'Toponimos.shp'
nom_reader = Reader(path_nom)
nom = ShapelyFeature(nom_reader.geometries(), crs=ccrs.Mercator.GOOGLE\
                     ,facecolor="black", edgecolor='black')

## KML: en este caso deberemos hacer una conversión de KML a ShapeFile

# zi_kml = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Archivos_Charlie/'\
#         +'Zona_Industrial.kml'
# zi_gdf = gpd.read_file(zi_kml, driver='KML')
# zi_sf = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial.shp'
# zi_gdf.to_file(zi_sf, driver='ESRI Shapefile')
# ahora si, cargamos el shapefile

path_zi = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/au/'\
            +'Zona_Industrial.shp'
zi_reader = Reader(path_zi)
zi = ShapelyFeature(zi_reader.geometries(), ccrs.PlateCarree()\
                            , facecolor="green", edgecolor='None')

#%% 1: Utilizamos PyGMT para plotear linea de costa.

fig = pg.Figure()
fig.coast(
    # Set the x-range from 10E to 20E and the y-range to 35N to 45N
    region=[-71.6, -71.4, -32.9, -32.7],
    projection="M12c",
    land="lightgray",
    water="white",
    borders="1/0.5p",
    shorelines="1/0.5p",
    frame="ag",
)
fig.show()

#%% 2: Usamos Cartopy para plotear linea de costa


# Limite del mapa
region = [-71.8, -71.4, -33.1, -32.7]

plt.figure()
cmap = plt.colormaps['tab10'](np.linspace(0,1,10))
cmap = cmap[[0,1,2,3,4,5,6,8,9]]

proj = ccrs.PlateCarree()
ax = plt.axes(projection=proj)

# Show only region
ax.set_extent(region)

# Make figure larger
plt.gcf().set_size_inches(10, 8)
    
# Añade linea de costa
ax.add_feature(reg, alpha=0.4, linewidth=.8, facecolor="gray", edgecolor='None',
                zorder=1)
ax.add_feature(reg, alpha=1, linewidth=.8, facecolor="None", edgecolor='black',
                zorder=8)
ax.add_feature(urb, alpha=0.4, linewidth=.8, facecolor="yellow", edgecolor='None',
                zorder=1)
ax.add_feature(urb, alpha=1, linewidth=.8, facecolor="None", edgecolor='white',
                zorder=8)
del region, cmap, proj, ax

#%% Ahora ploteamos las estaciones con valores en color, junto con una colorbar

# Primero hay que correr la sección de importación de mapas vectoriales

# Input
region = [-71.6, -71.4, -32.95, -32.7] #[-71.86, -71.2, -33.48, -32.63]
data = np.arange(0,len(Dic['Estaciones'])*5,5)
lon = Dic['Lon']
lat = Dic['Lat']

# Color Map
### Lo que tenía Charlie:
# cmap = pl.colors.ListedColormap(['blue', 'cyan', 'green', 'orange'])
# norm = pl.colors.BoundaryNorm([17, 27, 33, 47, 63], cmap.N) 
# cmap.set_under('black')
# cmap.set_over('red')
# colors = cmap(norm(data))
### Método simple:
cmap = pl.colormaps.get_cmap('hsv')
colors = data

# Definimos figura y ejes
fig, ax = plt.subplots(figsize=(7,8), subplot_kw={'projection': ccrs.PlateCarree()})

# Definimos región
ax.set_extent(region)

# Regiones (linea de costa)
ax.add_feature(reg, alpha=0.4, linewidth=.8, facecolor="gray", edgecolor='None',
                zorder=1)
ax.add_feature(reg, alpha=1, linewidth=.8, facecolor="None", edgecolor='black',
                zorder=2)
# Zonas urbanas
ax.add_feature(urb, alpha=0.2, linewidth=.8, facecolor="yellow", edgecolor='None',
                zorder=3)
ax.add_feature(urb, alpha=1, linewidth=.8, facecolor="None", edgecolor='white',
                zorder=4)
# Lugares: no se ven :(
# ax.add_feature(nom, alpha=1, linewidth=.8, facecolor="brown", edgecolor='None',
#                 zorder=5)
# ax.add_feature(nom, alpha=1, linewidth=.8, facecolor="None", edgecolor='white',
#                 zorder=6)
# Zona Industrial

# ax.add_feature(zi, alpha=1, linewidth=.8, facecolor="green", edgecolor='None',
#                 zorder=7)
# ax.add_feature(zi, alpha=1, linewidth=.8, facecolor="None", edgecolor='white',
#                 zorder=8)

# Estaciones y sus nombres
sc = ax.scatter(lon, lat, s=130, c=colors, cmap=cmap, transform=ccrs.Geodetic()\
                ,edgecolors='black',zorder=9)
            #,norm=norm)
ei = 0
for e in Dic['Abreviación_Estaciones']:
    ax.text(lon[ei]-0.005,lat[ei]+0.005,e, fontsize=15,zorder=10)
    ei = ei+1
del e, ei

# Agregamos colorbar
fig.colorbar(sc, extend='both', label='bla')
# fig.colorbar(pl.cm.ScalarMappable(norm, cmap), extend='both')

# Agregamos gridlines
gr = ax.gridlines(draw_labels=True, dms=True,alpha=0.5, zorder=4)
gr.top_labels = False
gr.right_labels = False

fig.tight_layout()


