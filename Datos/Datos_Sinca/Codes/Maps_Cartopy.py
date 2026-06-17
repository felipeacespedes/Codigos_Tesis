# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 16:07:34 2023

@author: felip
"""

# Importamos librerías
import cartopy
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as pl
import numpy as np
import pandas as pd
import os.path
from import_var import import_var

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

Dic['Unidades_Cont'] = ['ppb','ppm','ppm','ppm','ppm',r'$\mu g/m^{3}$',
                        r'$\mu g/m^{3}$']

Dic['Variables_Meteo'] = ['Velocidad','Dirección']

Dic['Unidades_Meteo'] = ['m/s','°']

Dic['Variables'] = ['SO2','CH4','HCNM','HCT','CO','MP25','MP10' \
                    ,'Velocidad','Dirección']

# por ahora usamos el periodo que sabemos que esta relativamente bien
Fi = '2018-01-01'
Ff = '2023-12-31'

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
        
del v, e, nan

#%% Importamos mapas vectoriales de la BCN y KML de Zona Industrial

## BCN
# Regiones
path_reg = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Regiones/'+\
            'Regional.shp'
reg = ShapelyFeature(Reader(path_reg).geometries(), ccrs.Mercator.GOOGLE)

# Zonas Urbanas
path_urb = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Areas_Pobladas/'+\
            'Areas_Pobladas.shp'
urb = ShapelyFeature(Reader(path_urb).geometries(), ccrs.Mercator.GOOGLE)

# Zona Industrial
path_zi = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/py/'\
            +'Zona_Industrial.shp'
zi = ShapelyFeature(Reader(path_zi).geometries(), ccrs.PlateCarree())

del path_reg, path_urb, path_zi

#%% Promedio de día

# diccionario con promedio de día
Est_pd = {}
PD = np.empty(9)
ei = 0

for e in Dic['Estaciones']:
    Est_pd[e] = Est[e]['HCNM'].loc[(8 <= Est[e].index.hour) & \
                                    (Est[e].index.hour < 20)].mean()
    PD[ei] = Est_pd[e]
    ei = ei+1
del e, ei
    
# Input
region = [-71.6, -71.4, -32.95, -32.7] 
Lon = Dic['Lon']
Lat = Dic['Lat']

# Método simple:
colors = PD

# Definimos figura y ejes
fig, ax = plt.subplots(figsize=(8,8), subplot_kw={'projection':\
                                                  ccrs.PlateCarree()})

# Definimos región
ax.set_extent(region)

# Regiones (linea de costa)
ax.add_feature(reg, alpha=0.8, linewidth=.8, facecolor='gray' \
               ,edgecolor='black',zorder=1)

# Zonas urbanas
ax.add_feature(urb, alpha=0.5, linewidth=.8, facecolor='yellow' \
               ,edgecolor='black', zorder=2)

# Zonas Industriales
ax.add_feature(zi, alpha=0.5, linewidth=.8, facecolor='green' \
               ,edgecolor='black', zorder=3)
    
# Nombramos cada una de las zonas 
legend_handles = [
    mpatches.Patch(color='yellow', label='Zonas Urbanas'),
    mpatches.Patch(color='green', label='Zonas Industriales')
    ]
    
# Añadimos nombres de ciudades
city_names = ['Concón', 'Quintero', 'Puchuncaví']
city_coords = [(-71.541875, -32.936387) \
              ,(-71.533682, -32.771999) \
              ,(-71.486326, -32.731778)]

# Add city markers
for name, (lon, lat) in zip(city_names, city_coords):
    ax.scatter(lon, lat, s=100, marker='v', label=name, color='red'\
               , transform=ccrs.PlateCarree(), alpha=1, zorder=5 \
               , edgecolors='black')

    # Add city names as text
    ax.text(lon-0.03, lat+0.005, name, color='black', fontsize=13\
            , transform=ccrs.PlateCarree())
        



# Create a ScalarMappable object
cmap = pl.colormaps.get_cmap('Reds')
sc_mappable = plt.cm.ScalarMappable(cmap=cmap)
sc_mappable.set_array(colors)
sc_mappable.set_clim(0, 0.5)  # Set the range for the colorbar

# Create the colorbar discretized into 5 sections
num_sections = 5
cbar = fig.colorbar(sc_mappable, ax=ax, extend='max', label='HCNM [ppm]'\
                    , aspect=15, shrink=0.9)
cbar.set_ticks(np.linspace(0, 0.5, num_sections + 1))

# Optionally, you can set custom tick labels
# cbar.set_ticklabels(['0.0', '0.1', '0.2', '0.3', '0.4', '0.5'])


# Estaciones y sus nombres
sc = ax.scatter(Lon, Lat, s=130, c=colors, cmap=cmap, transform=\
                ccrs.Geodetic(),edgecolors='black',zorder=5)

ei = 0
for e in Dic['Abreviación_Estaciones']:
    ax.text(Lon[ei],Lat[ei]+0.005,e, fontsize=15,zorder=6)
    ei = ei+1
del e, ei


# Agregamos gridlines
gl = ax.gridlines(draw_labels=True, dms=False,alpha=0.5, zorder=4\
                  , x_inline=False, y_inline=False,crs=ccrs.PlateCarree())
gl.top_labels = False
gl.right_labels = False
# Set label style to display coordinates in decimal format
gl.xformatter = cartopy.mpl.gridliner.LONGITUDE_FORMATTER
gl.yformatter = cartopy.mpl.gridliner.LATITUDE_FORMATTER

# Add legend to the plot
ax.legend(handles=legend_handles, loc='upper left')

# Set title
ax.set_title('Promedio de razón de mezcla horaria de HCNM para horas de "día"'\
          ,pad=15,fontsize=13)

fig.tight_layout()

plt.show()


del   cmap, colors, city_coords, city_names, gl, ax\
    , fig, sc, legend_handles, region, Lon, Lat, lon, lat, name, Est_pd, PD\
    # , sc_mappable
