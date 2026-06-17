# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 13:46:57 2025

@author: felip
"""

# librerías
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib import colors

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import cartopy.feature as cfeature
import matplotlib.patches as mpatches
from netCDF4 import Dataset
import numpy as np

# urb = cfeature.NaturalEarthFeature('cultural', 'urban_areas', '10m', facecolor='none')
# zi = cfeature.NaturalEarthFeature('cultural', 'urban_areas', '10m', facecolor='none')  # Replace with your industrial area if different

# Importamos mapas vectoriales de la BCN y KML de Zona Industrial

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

Dic = {
    'Estaciones': ['Ventanas','Quintero','Concón'],
    'Abreviación_Estaciones': ['VE','QN','CC'],
    'Lon': [-71.515825,-71.535295,-71.485704],
    'Lat': [-32.936796,-32.772393,-32.741703]
}



######### Mapas topografía ##########
def custom_terrain():
    cmap = plt.get_cmap('terrain')
    colors_list = cmap(np.linspace(0.1, 0.9, 256))  # Cut extremes
    new_cmap = colors.LinearSegmentedColormap.from_list('custom_terrain', 
                                                        colors_list)
    return new_cmap

def custom_colormap():
    # Define blue color for zero or lesser values
    blue_color = (0.541, 0.722, 0.961)
    
    # Create a terrain colormap starting from green
    terrain_cmap = plt.cm.get_cmap('geo')
    terrain_colors = terrain_cmap(np.linspace(0.22, 1, 256))  # Start from green
    
    # Combine the blue color and the terrain colormap
    colors = [blue_color] + list(terrain_colors)
    cmap = mcolors.LinearSegmentedColormap.from_list('custom_colormap', colors, N=256)
    
    return cmap
  
    
def create_map_topo(ax, le, Lon, Lat, nc, dire):
    ##### Load NetCDF #####
    nc_file = Dataset(nc)
    x_range = nc_file['x_range'][:]
    y_range = nc_file['y_range'][:]
    spacing = nc_file['spacing'][:]
    z = nc_file['z'][:]

    x = np.arange(x_range[0], x_range[1], spacing[0])
    x = x[:len(x)-1]
    y = np.arange(y_range[0], y_range[1], spacing[1])[::-1]
    X, Y = np.meshgrid(x, y)
    z_data = z.reshape(len(y), len(x))

    ##### Map #####
    region = [-71.6, -71.4, -32.95, -32.7]
    ax.set_extent(region)

    ##### Custom Terrain Colormap #####
    cmap_c = custom_colormap()
    vmin, vmax = 0, 700
    levels = np.linspace(vmin, vmax, 50)

    ##### Topography #####
    c = ax.contourf(X, Y, z_data, cmap=cmap_c, levels=levels, extend='both', 
                    transform=ccrs.PlateCarree())

    # Linea de Costa
    ax.contour(X, Y, z_data, levels=[0.1], colors='black', linewidths=1\
                    , transform=ccrs.PlateCarree())

    ##### Urban and Industrial Areas #####
    ax.add_feature(urb, linewidth=2, facecolor='none', edgecolor='thistle', 
                   zorder=2)
    ax.add_feature(zi, linewidth=2, facecolor='none', edgecolor='olivedrab', 
                   zorder=3)

    ##### Stations #####
    sc = ax.scatter(Lon, Lat, s=130, c='white', edgecolors='black',
                    zorder=6, transform=ccrs.PlateCarree())
    for e in le:
        ei = Dic['Estaciones'].index(e)
        ax.text(Dic['Lon'][ei], Dic['Lat'][ei]+0.004, 
                Dic['Abreviación_Estaciones'][ei], fontsize=10,
                weight='bold', zorder=6, transform=ccrs.PlateCarree())

    ##### Colorbar inside plot #####
    cbaxes = ax.inset_axes([0.9, 0.15, 0.02, 0.4])  # [x, y, width, height]
    plt.colorbar(c, cax=cbaxes, orientation='vertical', 
                 ticks=np.linspace(vmin, vmax, 8))
    cbaxes.set_ylabel('Topography [m]')

    ##### Add Globe #####
    ax_globe = ax.inset_axes([0.65, -0.25, 0.3, 0.3], 
                             projection=ccrs.Orthographic(central_longitude=-60,
                                                          central_latitude=-30))
    ax_globe.stock_img()
    ax_globe.coastlines()
    ax_globe.set_global()

    # Add red arrow pointing to Chile
    ax_globe.plot([-71.5], [-32.8], marker='o', color='red', markersize=6,
                  transform=ccrs.PlateCarree())

    ##### Black and white frame #####
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_color('black')

    return sc


############# Función Est_maps_topo(): crea serie de mapas para df
def map_topo(le, nc, dire, dpii=600):
    """
    Plot topography with stations, urban/industrial areas, and insets.

    Parameters:
    - le: List of station names
    - Lon: List of longitudes
    - Lat: List of latitudes
    - nc: Path to NetCDF file
    - dire: Save path
    - dpii: Resolution of saved figure
    """

    # Create figure
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Create main map
    create_map_topo(ax, le, Dic['Lon'], Dic['Lat'], nc, dire)

    # Tight layout
    plt.tight_layout()
    plt.show()

    # Save high-quality output
    plt.savefig(dire+'Mapa_EGU.png', dpi=dpii, bbox_inches='tight', 
                pad_inches=0.2, transparent=False)
    plt.close()
