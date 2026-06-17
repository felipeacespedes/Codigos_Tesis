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
import cartopy
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
# import cartopy.feature as cfeature
import matplotlib.ticker as mticker
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
region = [-71.6, -71.4, -32.95, -32.7] 
data = np.arange(0,len(Dic['Estaciones'])*5,5)
Lon = Dic['Lon']
Lat = Dic['Lat']

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
fig, ax = plt.subplots(figsize=(7,8), subplot_kw={'projection':\
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
    # mpatches.Patch(color='gray', label=''),
    mpatches.Patch(color='yellow', label='Zonas Urbanas'),
    mpatches.Patch(color='green', label='Zonas Industriales'),
    # Add more legend handles for each feature you want in the legend
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


# Estaciones y sus nombres
sc = ax.scatter(Lon, Lat, s=130, c=colors, cmap=cmap, transform=\
                ccrs.Geodetic(),edgecolors='black',zorder=5)
                #,norm=norm)
ei = 0
for e in Dic['Abreviación_Estaciones']:
    ax.text(Lon[ei],Lat[ei]+0.005,e, fontsize=15,zorder=6)
    ei = ei+1
del e, ei

# Agregamos colorbar
cbar = fig.colorbar(sc, extend='both', label='bla', aspect=15, shrink=0.8)
# fig.colorbar(pl.cm.ScalarMappable(norm, cmap), extend='both')


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

fig.tight_layout()

del  cbar, cmap, colors, data, city_coords, city_names, gl, ax, fig, sc\
    , legend_handles, region, Lon, Lat, lon, lat, name
    
# Listo!

#%% Ahora, por  fin, ploteamos estadíasticos

# qué hacer:
    # Percentiles
    # valores máximos en epidsodios
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
        
# Discretize the colorbar into 5 sections
num_sections = 10
cbar_locator = pl.ticker.MaxNLocator(nbins=num_sections + 1)

# Colormap
colors = PD
cmap = plt.colormaps.get_cmap('Reds')

# Create a BoundaryNorm to discretize the colorbar
norm = pl.colors.BoundaryNorm(np.linspace(0, 0.5, num_sections + 1)\
                               ,cmap.N, clip=True)

# Create a ScalarMappable object
sc_mappable = pl.cm.ScalarMappable(cmap=cmap, norm=norm)
sc_mappable.set_array(colors)


# Create the colorbar
cbar = fig.colorbar(sc_mappable, ax=ax, extend='max', label='HCNM [ppm]'\
                    , aspect=15, shrink=0.9)


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
ax.set_title('Promedio de razón de mezcla horaria de HCNM para horas de "día".'\
          ,pad=15,fontsize=13)

fig.tight_layout()

del  cbar, cmap, cbar_locator, colors, city_coords, city_names, gl, ax\
    , fig, sc, legend_handles, region, Lon, Lat, lon, lat, name, Est_pd, PD\
    , sc_mappable, num_sections


#%% Promedio de noche

# diccionario con promedios nocturnos
Est_pn = {}
PN = np.empty(9)
ei = 0

for e in Dic['Estaciones']:
    Est_pn[e] = Est[e]['HCNM'].loc[(Est[e].index.hour >= 20) |\
                                   (Est[e].index.hour < 8)].mean()
    PN[ei] = Est_pn[e]
    ei = ei + 1
    
del e, ei
    
# Input
region = [-71.6, -71.4, -32.95, -32.7] 
Lon = Dic['Lon']
Lat = Dic['Lat']

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
    mpatches.Patch(color='green', label='Zonas Industriales'),
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

# Discretize the colorbar into 5 sections
num_sections = 10
cbar_locator = pl.ticker.MaxNLocator(nbins=num_sections + 1)

# Colormap
colors = PN
cmap = pl.cm.get_cmap('Reds', num_sections)

# Create a BoundaryNorm to discretize the colorbar
norm = pl.colors.BoundaryNorm(np.linspace(0, 0.5, num_sections + 1)\
                               ,cmap.N, clip=True)

# Create a ScalarMappable object
sc_mappable = pl.cm.ScalarMappable(cmap=cmap, norm=norm)
sc_mappable.set_array(colors)


# Create the colorbar
cbar = fig.colorbar(sc_mappable, ax=ax, extend='max', label='HCNM [ppm]'\
                    , aspect=15, shrink=0.9)


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

plt.title('Promedio de razón de mezcla horaria de HCNM para horas de "noche".'\
          ,pad=15,fontsize=13)

fig.tight_layout()

#%% Función para mapas

def create_map(ax, Lon, Lat, colors, cmap, num_sections,LL,RL,fig):
    # Set extent
    region = [-71.6, -71.4, -32.95, -32.7]
    ax.set_extent(region)

    # Regiones (linea de costa)
    ax.add_feature(reg, alpha=0.8, linewidth=.8, facecolor='gray' \
                   ,edgecolor='black',zorder=1)
    
    # Zonas urbanas
    ax.add_feature(urb, alpha=0.9, linewidth=.8, facecolor='yellow' \
                   ,edgecolor='black', zorder=2)
    
    # Zonas Industriales
    ax.add_feature(zi, alpha=0.9, linewidth=.8, facecolor='green' \
                   ,edgecolor='black', zorder=3)
        
    # Nombramos cada una de las zonas 
    legend_handles = [
        mpatches.Patch(color='yellow', label='Zonas Urbanas'),
        mpatches.Patch(color='green', label='Zonas Industriales')
        ]

    # Set up gridlines
    gl = ax.gridlines(draw_labels=True, dms=False, alpha=0.5, zorder=4,
                      x_inline=False, y_inline=False, crs=ccrs.PlateCarree()\
                          , linewidth=0.5)
    gl.top_labels = False
    gl.left_labels = LL
    gl.right_labels = RL
    # Set label style to display coordinates in decimal format
    gl.xformatter = cartopy.mpl.gridliner.LONGITUDE_FORMATTER
    gl.yformatter = cartopy.mpl.gridliner.LATITUDE_FORMATTER
    gl.xlocator = mticker.FixedLocator([-71.60, -71.55, -71.50, -71.45\
                                        , -71.40])

    # Estaciones y sus nombres
    sc = ax.scatter(Lon, Lat, s=130, c=colors, cmap=cmap, transform=\
                    ccrs.Geodetic(),edgecolors='black',zorder=5)
    
    ei = 0
    for e in Dic['Abreviación_Estaciones']:
        ax.text(Lon[ei],Lat[ei]+0.004,e, fontsize=10,zorder=6)
        ei = ei+1
    del e, ei
    
    # Nombramos cada una de las zonas 
    legend_handles = [
        mpatches.Patch(color='yellow', label='Zonas Urbanas'),
        mpatches.Patch(color='green', label='Zonas Industriales')
        ]
    # Add legend to the plot
    ax.legend(handles=legend_handles, loc='upper left')


    # Add city markers and names
    city_names = ['Concón', 'Quintero', 'Puchuncaví']
    city_coords = [(-71.541875, -32.936387), (-71.533682, -32.771999)\
                   , (-71.486326, -32.731778)]
    add = 0
    for name, (lon, lat) in zip(city_names, city_coords):
        # ax.scatter(lon, lat, s=100, marker='v', label=name\
        #            , color='red', transform=ccrs.PlateCarree()
        #            , alpha=1, zorder=5, edgecolors='black')
        if name == 'Puchuncaví':
            add = 0.023
        ax.text(lon - 0.04 - add, lat , name, color='black', fontsize=10\
                , transform=ccrs.PlateCarree())
    # Add a or b to figure
    if fig == '':
        ax.text(-71.415,-32.713,fig,color='black', fontsize=13\
                , transform=ccrs.PlateCarree())
        
    else:
        ax.text(-71.415,-32.713,fig+')',color='black', fontsize=13\
            , transform=ccrs.PlateCarree())

    return sc

#%% Figura con 2 mapas: promedios de día y noche
import sys
# diccionario con promedio de día y de noche
Est_pd = {}
PD = np.empty(9)
Est_pn = {}
PN = np.empty(9)
ei = 0

for e in Dic['Estaciones']:
    # promedio de día
    Est_pd[e] = Est[e]['HCNM'].loc[(8 <= Est[e].index.hour) & \
                                    (Est[e].index.hour < 20)].mean()
    PD[ei] = Est_pd[e]
    # promedio de noche
    Est_pn[e] = Est[e]['HCNM'].loc[(Est[e].index.hour >= 20) |\
                                   (Est[e].index.hour < 8)].mean()
    PN[ei] = Est_pn[e]
    ei = ei+1
del e, ei

# vemos qué chucha es PD
print(PD)
sys.exit()

# Definimos Lat y Lon a partir de el diccionario inicial
Lon = Dic['Lon']
Lat = Dic['Lat']

# Set up the subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7)\
                        , gridspec_kw={'width_ratios': [1, 1.25]}\
                        , subplot_kw={'projection': ccrs.PlateCarree()})
    
# Parametros
num_sections = 10
cmap =  plt.colormaps.get_cmap('Reds')
v_inf = 0
v_sup = 0.5


# Create maps for PD and PN
sc1 = create_map(ax1, Lon, Lat, PD, cmap, num_sections, True, False, 'a')
sc2 = create_map(ax2, Lon, Lat, PN, cmap, num_sections, False, False, 'b')


# Create a BoundaryNorm to discretize the colorbar
norm = pl.colors.BoundaryNorm(np.linspace(v_inf, v_sup, num_sections + 1)\
                               ,cmap.N, clip=True)

# Create a ScalarMappable object
sc_mappable = pl.cm.ScalarMappable(cmap=cmap, norm=norm)
sc_mappable.set_array(PN)


# Create the shared colorbar
cbar = fig.colorbar(sc_mappable, ax=ax2, extend='max', label='HCNM [ppm]'\
                    , aspect=15, shrink=0.85)
    
# Adjust layout
fig.tight_layout()
# fig.subplots_adjust(wspace=-0.3)
# fig.sup_title('Promedios')

# Show the plot
plt.show()


# Diferencia entre Noche y Día

Dif_ND = PN-PD

print([min(Dif_ND),max(Dif_ND)])

fig, ax = plt.subplots(figsize=(8,8), subplot_kw={'projection':\
                                                  ccrs.PlateCarree()})
# Parametros
num_sections = 8
cmap =  plt.colormaps.get_cmap('RdBu')
v_inf = -0.8
v_sup = 0.8

# Create maps for difference between PN and PD
sc = create_map(ax, Lon, Lat, Dif_ND, cmap, num_sections, True, False, '')

# Create a BoundaryNorm to discretize the colorbar
norm = pl.colors.BoundaryNorm(np.linspace(v_inf, v_sup, num_sections + 1)\
                               ,cmap.N, clip=True)

# Create a ScalarMappable object
sc_mappable = pl.cm.ScalarMappable(cmap=cmap, norm=norm)
sc_mappable.set_array(Dif_ND)


# Create the shared colorbar
cbar = fig.colorbar(sc_mappable, ax=ax, extend='both', label='HCNM [ppm]'\
                    , aspect=15, shrink=0.85)
    
# Adjust layout
fig.tight_layout()
# fig.subplots_adjust(wspace=-0.3)
# fig.sup_title('Promedios')

# Show the plot
plt.show()


del  cmap, cbar, Lon, Lat, Est_pd, PD, Est_pn, PN\
     , fig, sc1, sc2, sc_mappable, ax1, ax2, num_sections\
     , ax, v_inf, v_sup, Dif_ND

#%% Figura con 2 mapas: Promedios Verano vs Invierno

# diccionario con promedio de día Verano y Invierno
Est_pv = {}
PV = np.empty(9)
Est_pi = {}
PI = np.empty(9)
ei = 0

for e in Dic['Estaciones']:
    # promedio de día
    Est_pv[e] = Est[e]['HCNM'].loc[( Est[e].index.month <= 4) | \
                                    (Est[e].index.month >= 11)].mean()
    PV[ei] = Est_pv[e]
    # promedio de noche
    Est_pi[e] = Est[e]['HCNM'].loc[(Est[e].index.month >=5 ) |\
                                   (Est[e].index.month <= 10)].mean()
    PI[ei] = Est_pi[e]
    ei = ei+1
del e, ei

# Definimos Lat y Lon a partir de el diccionario inicial
Lon = Dic['Lon']
Lat = Dic['Lat']

# Set up the subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7)\
                        , gridspec_kw={'width_ratios': [1, 1.25]}\
                        , subplot_kw={'projection': ccrs.PlateCarree()})
    
# Parametros
num_sections = 10
cmap =  plt.colormaps.get_cmap('Reds')
v_inf = 0
v_sup = 0.5


# Create maps for PD and PN
sc1 = create_map(ax1, Lon, Lat, PV, cmap, num_sections, True, False, 'a')
sc2 = create_map(ax2, Lon, Lat, PI, cmap, num_sections, False, False, 'b')


# Create a BoundaryNorm to discretize the colorbar
norm = pl.colors.BoundaryNorm(np.linspace(v_inf, v_sup, num_sections + 1)\
                               ,cmap.N, clip=True)

# Create a ScalarMappable object
sc_mappable = pl.cm.ScalarMappable(cmap=cmap, norm=norm)
sc_mappable.set_array(PI)


# Create the shared colorbar
cbar = fig.colorbar(sc_mappable, ax=ax2, extend='max', label='HCNM [ppm]'\
                    , aspect=15, shrink=0.85)
    
# Adjust layout
fig.tight_layout()
# fig.subplots_adjust(wspace=-0.3)
# fig.sup_title('Promedios')

# Show the plot
plt.show()

# Diferencia entre Invierno y Verano


Dif_IV = PI-PV

print([min(Dif_IV),max(Dif_IV)])

fig, ax = plt.subplots(figsize=(8,8), subplot_kw={'projection':\
                                                  ccrs.PlateCarree()})
# Parametros
num_sections = 6
cmap =  plt.colormaps.get_cmap('RdBu')
v_inf = -0.6
v_sup = 0.6

# Create maps for difference between PN and PD
sc = create_map(ax, Lon, Lat, Dif_IV, cmap, num_sections, True, False, '')

# Create a BoundaryNorm to discretize the colorbar
norm = pl.colors.BoundaryNorm(np.linspace(v_inf, v_sup, num_sections + 1)\
                               ,cmap.N, clip=True)

# Create a ScalarMappable object
sc_mappable = pl.cm.ScalarMappable(cmap=cmap, norm=norm)
sc_mappable.set_array(Dif_IV)


# Create the shared colorbar
cbar = fig.colorbar(sc_mappable, ax=ax, extend='both', label='HCNM [ppm]'\
                    , aspect=15, shrink=0.85)
    
# Adjust layout
fig.tight_layout()
# fig.subplots_adjust(wspace=-0.3)
# fig.sup_title('Promedios')

# Show the plot
plt.show()

del  cmap, cbar, Lon, Lat, Est_pv, PV, Est_pi, PI\
    , fig, sc1, sc2, sc_mappable, ax1, ax2, num_sections, Dif_IV


#%% 
# # Por estación:
# # Importamos variables de contaminantes a dataframe de cada estación
# for e in range(len(le)):
#     Est[le[e]] = pd.DataFrame({'T': T})
#     Est[le[e]] = Est[le[e]].set_index('T')
#     for v in range(len(lv)):
#         file_c = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
#         +'Estaciones/'+le[e]+'/Cont/'+lv[v]+'.csv'
#         file_m = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
#         +'Estaciones/'+le[e]+'/Meteo/'+lv[v]+'.csv'
#         if os.path.isfile(file_c) == True:
#             Est[le[e]][lv[v]] = import_var(\
#                 le[e],'Cont',lv[v],Fi,Ff)
                
#         elif os.path.isfile(file_m) == True:
#             Est[le[e]][lv[v]] = import_var(\
#                 le[e],'Meteo',lv[v],Fi,Ff)
#         else:
#             Est[le[e]][lv[v]] = nan
            
#         del file_c, file_m

# # Por variable:
# # Importamos variables de contaminantes a dataframe de cada estación
# Var = {}
# for v in range(len(lv)):
#     Var[lv[v]] = pd.DataFrame({'T': T})
#     Var[lv[v]] = Var[lv[v]].set_index('T')
#     for e in range(len(le)):
#         file_c = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
#         +'Estaciones/'+le[e]+'/Cont/'+lv[v]+'.csv'
#         file_m = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
#         +'Estaciones/'+le[e]+'/Meteo/'+lv[v]+'.csv'
#         if os.path.isfile(file_c) == True:
#             Var[lv[v]][le[e]] = import_var(\
#                 le[e],'Cont',lv[v],Fi,Ff)
                
#         elif os.path.isfile(file_m) == True:
#             Var[lv[v]][le[e]] = import_var(\
#                 le[e],'Meteo',lv[v],Fi,Ff)
#         else:
#             Var[lv[v]][le[e]] = nan
            
#         del file_c, file_m

#%% Ciclos de HCNM

# Tratamiento datos HCNM:
# Eliminamos todos los datos que sean menores a LOD = 0.05 ppm
# y los reemplazamos por Nan

for e in Dic['Estaciones']:
    Est[e]['HCNM'].loc[(Est[e]['HCNM'] < 0.05)] = np.nan
del e



# Creamos diccionario de estaciones para series diarias
Est_d= {}

# Resampleamos a promedios diarios el dataframe de cada estación
for e in range(len(Dic['Estaciones'])):
    Est_d[Dic['Estaciones'][e]] = pd.DataFrame({'T': T})
    Est_d[Dic['Estaciones'][e]] = Est_d[Dic['Estaciones'][e]].set_index('T')
    Est_d[Dic['Estaciones'][e]] = Est[Dic['Estaciones'][e]].resample('D')\
                                                                    .mean()

del e

# Quitamos 29 de febrero

for e in Dic['Estaciones']:
    Est_d[e] = Est_d[e].loc[~((Est_d[e].index.month==2) \
                              & (Est_d[e].index.day==29))]
    Est_d[e].sort_index(inplace=True)
del e

# creamos matriz de días
dias = Est_d['Centro_Quintero'][0:365].index.dayofyear

# función para plotear con facilidad 
def func(ax, data, color, position, label):  
    if data.name == 'HCNM':
        line = ax.plot(data.index, data.values, color=color, zorder=3\
                       , linewidth=2, label=label)
        ax.spines[position].set_color(color)
    else:
        line = ax.plot(data.index, data.values, color=color, zorder=2\
                       , alpha=0.7, label=label)
        ax.spines[position].set_color(color)

    for pos in ['left', 'right']:
        if pos != position:
            ax.spines[pos].set_visible(False)

    return line[0]

#%% Estacional:

# diccionario con ciclo anual para cada estación y contaminante/variable 
Est_ca = {}

for e in Dic['Estaciones']:
    Est_ca[e] = pd.DataFrame({'T':dias})
    Est_ca[e] = Est_ca[e].set_index('T')
    for d in range(365):
        Est_ca[e].loc[d+1,Dic['Variables']] = \
            Est_d[e].loc[(Est_d[e].index.dayofyear==d+1)].mean()

del e


# comparamos la variable HCNM y MP25/CO
plt.style.use('default')
for e in Dic['Estaciones']:
    dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+e+'/Cont/CA/'
    if os.path.isdir(dire) == False:
        continue
    
    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Create a twin axis sharing the y-axis
    ax2 = ax.twinx()
    
    # Move the third axis a bit to the right
    ax3 = ax.twinx()
    ax3.spines['right'].set_position(("axes", 1.07))
    
    # Plot using the function and store line objects for the legend
    ln1 = func(ax, Est_ca[e]['HCNM'], 'blue', 'left', label=\
               Est_ca[e]['HCNM'].name)
    ln2 = func(ax2, Est_ca[e]['MP25'], 'orange', 'right', label=\
               Est_ca[e]['MP25'].name)
    ln3 = func(ax3, Est_ca[e]['CO'], 'green', 'right', label=\
               Est_ca[e]['CO'].name)
    
    # Set the color for the Y-axis ticks and labels for ax, ax2, and ax3
    ax.tick_params(axis='y', direction='in', labelcolor='blue',colors='blue')
    ax.set_ylabel(Est_ca[e]['HCNM'].name+' ['+Dic['Unidades_Cont'][2]+']'\
                  , color='blue')
    
    ax2.tick_params(axis='y', direction='in', labelcolor='orange'\
                    , colors='orange')
    ax2.set_ylabel(Est_ca[e]['MP25'].name+' ['+Dic['Unidades_Cont'][5]+']'\
                   , color='orange')
    
    ax3.tick_params(axis='y', direction='in', labelcolor='green'\
                    ,colors='green')
    ax3.set_ylabel(Est_ca[e]['HCNM'].name+' ['+Dic['Unidades_Cont'][4]+']'\
                   , color='green')
    

    # Legend
    leg = []
    leg.append(ln1)
    leg.append(ln2)
    leg.append(ln3)
    labs = [l.get_label() for l in leg]
    ax.legend(leg, labs, loc=0)
    
    # Other adjustments
    ax.grid(True, alpha=0.5)
    plt.title('Ciclo Estacional: HCNM vs MP25/CO, ' + e)
    plt.tight_layout()
    
    # Save or show the plot
    plt.savefig(dire + Est_ca[e]['HCNM'].name + '_vs_' + Est_ca[e]['MP25']\
                .name +'&' + Est_ca[e]['CO'].name + '_treated.png'\
                , bbox_inches='tight', dpi=300)
    plt.show()
    
# Delete unnecessary variables
del e, dire

#%% Semanal:

# Aplicamos mismo código aplicado a ciclo anual pero ahora por día de semana:
    
# diccionario con ciclo semanal para cada estación y contaminante/variable 
Est_cs = {}

for e in Dic['Estaciones']:
    Est_cs[e] = pd.DataFrame({'T':dias[0:7]})
    Est_cs[e] = Est_cs[e].set_index('T')
    for d in range(7):
        Est_cs[e].loc[d+1,Dic['Variables']] = Est_d[e].loc[(Est_d[e]\
                                            .index.dayofweek==d)].mean()
        
del e


# comparamos las variables HCNM y MP25/CO
plt.style.use('default')
for e in Dic['Estaciones']:
    dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/' + e + '/Cont/CS/'
    if not os.path.isdir(dire):
        continue
    
    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Create twin axes sharing the y-axis
    ax2 = ax.twinx()
    
    # Move the third axis a bit to the right
    ax3 = ax.twinx()
    ax3.spines['right'].set_position(("axes", 1.07))
    
    # Plot using the func function and store line objects for the legend
    ln1 = func(ax, Est_cs[e]['HCNM'], 'blue', 'left', label=\
               Est_cs[e]['HCNM'].name)
    ln2 = func(ax2, Est_cs[e]['MP25'], 'orange', 'right', label=\
               Est_cs[e]['MP25'].name)
    ln3 = func(ax3, Est_cs[e]['CO'], 'green', 'right', label=\
               Est_cs[e]['CO'].name)
    
    # Set the color for the Y-axis ticks and labels for ax, ax2, and ax3
    ax.tick_params(axis='y', direction='in', labelcolor='blue',colors='blue')
    ax.set_ylabel(Est_ca[e]['HCNM'].name+' ['+Dic['Unidades_Cont'][2]+']'\
                  , color='blue')
    
    ax2.tick_params(axis='y', direction='in', labelcolor='orange'\
                    , colors='orange')
    ax2.set_ylabel(Est_ca[e]['MP25'].name+' ['+Dic['Unidades_Cont'][5]+']'\
                   , color='orange')
    
    ax3.tick_params(axis='y', direction='in', labelcolor='green'\
                    ,colors='green')
    ax3.set_ylabel(Est_ca[e]['HCNM'].name+' ['+Dic['Unidades_Cont'][4]+']'\
                   , color='green')
    
    # Legend
    leg = []
    leg.append(ln1)
    leg.append(ln2)
    leg.append(ln3)
    labs = [l.get_label() for l in leg]
    ax.legend(leg, labs, loc=0)
    
    # Other adjustments
    ax.grid(True, alpha=0.5)
    plt.title('Ciclo Semanal: HCNM vs MP25/CO, ' + e)
    plt.tight_layout()
    
    # Save or show the plot
    plt.savefig(dire + Est_cs[e]['HCNM'].name + '_vs_' + Est_cs[e]['MP25']\
                .name +'&' + Est_cs[e]['CO'].name + '_treated.png'\
                    , bbox_inches='tight', dpi=300)
    plt.show()

# Delete unnecessary variables
del e, dire


#%% Diario:

# vector de tiempo con 24 horas
horas = T[0:24].hour

# diccionario con ciclo diario para cada estación y contaminante/variable 
Est_cd = {}

for e in Dic['Estaciones']:
    Est_cd[e] = pd.DataFrame({'T':horas})
    Est_cd[e] = Est_cd[e].set_index('T')
    for h in range(24):
        Est_cd[e].loc[h,Dic['Variables']] = Est[e].loc[(Est[e].index.hour==h)]\
                                                        .mean()
del e

# comparamos las variables HCNM y MP25/CO
for e in Dic['Estaciones']:
    dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/' + e + '/Cont/CD/'
    if not os.path.isdir(dire):
        continue

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(12, 5))

    # Create twin axes sharing the y-axis
    ax2 = ax.twinx()

    # Move the third axis a bit to the right
    ax3 = ax.twinx()
    ax3.spines['right'].set_position(("axes", 1.07))

    # Plot using the func function and store line objects for the legend
    ln1 = func(ax, Est_cd[e]['HCNM'], 'blue', 'left'\
               , label=Est_cd[e]['HCNM'].name)
    ln2 = func(ax2, Est_cd[e]['MP25'], 'orange', 'right'\
               , label=Est_cd[e]['MP25'].name)
    ln3 = func(ax3, Est_cd[e]['CO'], 'green', 'right'\
               , label=Est_cd[e]['CO'].name)

    # Set the color for the Y-axis ticks and labels for ax, ax2, and ax3
    ax.tick_params(axis='y', direction='in', labelcolor='blue',colors='blue')
    ax.set_ylabel(Est_ca[e]['HCNM'].name+' ['+Dic['Unidades_Cont'][2]+']'\
                  , color='blue')
    
    ax2.tick_params(axis='y', direction='in', labelcolor='orange'\
                    , colors='orange')
    ax2.set_ylabel(Est_ca[e]['MP25'].name+' ['+Dic['Unidades_Cont'][5]+']'\
                   , color='orange')
    
    ax3.tick_params(axis='y', direction='in', labelcolor='green'\
                    ,colors='green')
    ax3.set_ylabel(Est_ca[e]['HCNM'].name+' ['+Dic['Unidades_Cont'][4]+']'\
                   , color='green')

    # Legend
    leg = []
    leg.append(ln1)
    leg.append(ln2)
    leg.append(ln3)
    labs = [l.get_label() for l in leg]
    ax.legend(leg, labs, loc=0)

    # Other adjustments
    ax.grid(True, alpha=0.5)
    plt.title('Ciclo Diario: HCNM vs MP25/CO, ' + e)
    plt.tight_layout()

    # Save or show the plot
    plt.savefig(dire + Est_cd[e]['HCNM'].name + '_vs_' + Est_cd[e]['MP25']\
                .name +'&' + Est_cd[e]['CO'].name + '_treated.png', \
                    bbox_inches='tight', dpi=300)
    plt.show()

# Delete unnecessary variables
del e, dire

#