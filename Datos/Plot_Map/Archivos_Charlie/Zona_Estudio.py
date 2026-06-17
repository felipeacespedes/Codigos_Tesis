#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 11:32:47 2021

Crear mapa para propuesta Quintero-Puchuncavi

@author: chopa
"""

# %% Import librerias

import geopandas as gpd
import pygmt

import fiona
fiona.drvsupport.supported_drivers['KML'] = 'rw'

# %% Cargar archivos

# DEM
fn_dem = "s33_w072_1arc_v3.tif"
# Zona urbana
fn_zurb = "../Chile_shp/Areas_Pobladas/Areas_Pobladas.shp"
# Zona industrial
fn_zi = "Zona_Industrial.kml"
ruta_fig = 'Mapas/'

# %% Cargar y plotear topografia
# Zoom a zona de estudi
zoom = [-71.65, -71.35, -32.97, -32.65]

fig = pygmt.Figure()
# pygmt.config(COLOR_BACKGROUND="cadetblue1")
# pygmt.makecpt(cmap="geo", series=[0, 900, 1], output ="cmap.cpt")

# Cargar topografia del USGS
# grid = pygmt.datasets.load_earth_relief(resolution="01s", region=zoom)
# fig.grdimage(grid=grid, projection="Q6c", frame=["xa0.1f0.05", "ya0.1f0.05"], cmap=True) #M10c

# Usar imagen .tif
fig.grdimage(grid=fn_dem, projection="Q6c", frame=["xa0.1f0.05", "ya0.1f0.05"], 
             region=zoom, cmap="cmap.cpt")

# Añadir barra de colores
with pygmt.config(FONT="10", FONT_HEADING="10" ):
    fig.colorbar(frame='a200f100+l"Topografía [m]"', #cmap="cmap.cpt", 
                 position="g-71.35/-32.65+o0.7/-0.4c+w5.6c+h", box=True)

# %% Añadir rosa y escala

with pygmt.config(FONT_LABEL=7, FONT_ANNOT_PRIMARY=7):
    fig.basemap(rose="g-71.62/-32.68+f1+l,,,N+w0.7c", 
                map_scale="g-71.38/-32.945+w4+f+lkm")

# %% Cargar y plotear zonas urbanas

zu = gpd.read_file(fn_zurb)
# Reproyectar a WGS84 lat/lon
zu= zu.to_crs("EPSG:4326")

# Filtrar para Quintero, Puchuncavi y Concon
zu = zu[(zu['comuna'] == 'Quintero') | (zu['comuna'] == 'PUCHUNCAVI') | (zu['comuna'] == 'Concón')]

fig.plot(data=zu, pen="1p,blue", label="Zona Urbana (Q-P-C)")

# %% Cargar y plotear zonas industriales

zi = gpd.read_file(fn_zi, driver='KML')

fig.plot(data=zi, fill="red", pen="1p,red", label="Zona Industrial")

# %% Estaciones HCNM y SO2

lon_hcnm = [-71.481481, -71.515479, -71.524749, -71.439825,
            -71.532226, -71.49642, -71.483406,
            -71.454509, -71.480832]
lat_hcnm = [-32.915616, -32.924756, -32.934929, -32.920837,
            -32.787721, -32.794914, -32.801052,
            -32.764345, -32.741815]

fig.plot(x=lon_hcnm, y=lat_hcnm, fill="white", style="c0.16c", pen="0.8p", 
          label="Estaciones SINCA con HCNM y SO2")

# %% Estaciones SO2

lon_so2 = [-71.535264, -71.436308,
           -71.407326, -71.474214]
lat_so2 = [-32.772511, -32.807605,
           -32.718731, -32.748276]

fig.plot(x=lon_so2, y=lat_so2, fill="dimgray", style="c0.16c", pen="0.8p", 
          label="Estaciones SINCA con SO2")

# %% Sensores SMA

lon_sma = [-71.477784, -71.509125, -71.494577, -71.485148]
lat_sma = [-32.750812, -32.766655, -32.780912, -32.766276]

fig.plot(x=lon_sma, y=lat_sma, fill="yellow", style="c0.16c", pen="0.8p", 
          label="Sensores SMA")

# %% Nombres ciudades

fig.text(x=-71.6, y=-32.91, text="Concón", font="8p,Helvetica-Bold,black", justify="ML")
fig.text(x=-71.645, y=-32.75, text="Quintero-Puchuncaví", font="8p,Helvetica-Bold,black", justify="ML")

# %% Leyenda

with pygmt.config(FONT_ANNOT_PRIMARY=10):
    fig.legend(box=True, position="g-71.35/-32.97+o0.3/0c")

# %% Guardar imagen

fig.show(method="external")
fig.savefig(ruta_fig+"Mapa_Quintero.png", dpi=600)
