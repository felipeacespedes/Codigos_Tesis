# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 13:47:42 2025

@author: felip
"""
import geopandas as gpd

#%% Importamos librerías
import Plot_Maps_profe as pm
import Plot_Maps_profe_pygmt as pmp
import Plot_Maps_mio_pygmt as pmm
import pandas as pd
#%% Definimos variables

le = ['Ventanas','Quintero','Concón']

#%% Cargamos df de datos modificados
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
nc = path+'QUINTERO.nc'

#%%  plot con pygmt para profe
pmp.map_topo_pygmt('C:/Users/felip/Desktop/mapa_EGU.png')

#%% plot con pygmt para mi
pmm.map_topo_pygmt('C:/Users/felip/Desktop/mapa_intro.png')

#%% Exploración de archivos IDE

# Todos los archivos descargados de IDE son solo para CQP!

## Termoelectricas:
# path_t = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/IDE/'\
#             +'Termoeléctricas.dbf'
# t = gpd.read_file(path_t)

## Almacenamiento de Combustibles: Se muestra quien almacena qué gases!
## , además de las ubicaciones de interés para COVs (Petroleo-Gas)
# path_t = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/IDE/'\
#             +'Almacenamiento_de_Combustibles.dbf'
# t = gpd.read_file(path_t)

## Terminal Maritimos:
# path_t = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/IDE/'\
#             +'Terminal_Marítimo.dbf'
# t = gpd.read_file(path_t)

## Oleoducto
# path_t = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/IDE/'\
#             +'Oleoducto.dbf'
# t = gpd.read_file(path_t)

## Gasoducto
# path_t = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/IDE/'\
#             +'Gasoducto.dbf'
# t = gpd.read_file(path_t)

#%% Archivos no IDE

## Red Vial:
# path_t = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Red_Vial/'\
#             +'redvial2019.shp'
# t = gpd.read_file(path_t)
# Reproyectar a WGS84 lat/lon
# t = t.to_crs("EPSG:4326")
# t = t[(t['Cod_Region']==5)&(t['Clase_Ruta']==1)]
