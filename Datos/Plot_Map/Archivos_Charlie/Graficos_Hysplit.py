# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 13:32:15 2023

@author: cr2_usuario
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import LineCollection

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# %% Funciones

def plot_traj(trajgroup, proj = ccrs.PlateCarree(), 
              extent=None, proj_ext=ccrs.PlateCarree(),
              ocean=False, land=False, coastlines=False,
              add_centroid=False, add_x0=False, 
              ticks=None, title=None, cmap=None,
              figsize=[6,4], save=False, namefig=None):
    
    # 
    fig, axs = plt.subplots(subplot_kw=dict(projection=proj), figsize=figsize)
    
    # Zoom in
    if extent is not None:
        axs.set_extent(extent, crs=proj_ext)
    
    # Add map features
    if ocean: 
        axs.add_feature(cfeature.OCEAN, alpha=.7)
    if land: 
        axs.add_feature(cfeature.LAND, alpha=0.4, facecolor="gray", zorder=1)  # Grayscale colors can be set using 0 (black) to 1 (white)
    if coastlines: 
        axs.coastlines(resolution='50m', color='black', linewidth=.3, zorder=2)
    
    # Add lat/lon gridlines every 20° to the map
    # dgx = 20
    # dgy = 10
    # gl = axs.gridlines(xlocs=np.arange(-180, 180, dgx), ylocs=np.arange(-90, 90, dgy), 
    #                    zorder=5, draw_labels=False, linestyle='dashed')
    # gl.top_labels = False
    # gl.bottom_labels = True
    # gl.right_labels = False
    # gl.xformatter = LONGITUDE_FORMATTER
    # gl.yformatter = LATITUDE_FORMATTER
    # gl.xlabel_style = {'size': 12, 'color': 'k', 'weight':'bold'}
    # gl.ylabel_style = {'size': 12, 'color': 'k', 'weight':'bold'}
    
    # Añadir ticks
    if ticks is not None:
        axs.set_xticks(ticks[0], crs=ccrs.PlateCarree())
        axs.set_yticks(ticks[1], crs=ccrs.PlateCarree())
        axs.tick_params(axis='both', which='major', labelsize=10)
        
    lon_formatter = LongitudeFormatter(zero_direction_label=True, dms=True, auto_hide=False)
    lat_formatter = LatitudeFormatter(dms=True, auto_hide=False)
    axs.xaxis.set_major_formatter(lon_formatter)
    axs.yaxis.set_major_formatter(lat_formatter)
    
    axs.tick_params(axis="both", length=8)
    
    # Plots
    k = 0
    for p in trajgroup.index.drop_duplicates():
        df1 = trajgroup.loc[p]
        for d in df1.Launch_Datetime.drop_duplicates():
            df2 = df1[df1.Launch_Datetime == d]
            x = df2['Longitude']
            y = df2['Latitude']

            axs.plot(x, y, color=cmap[k], linewidth=.9, zorder=7)
            
        k += 1

    if add_centroid:
        centroide = centroide_traj(trajgroup)
        axs.plot(centroide['Longitude'], centroide['Latitude'], color='r', 
                 linewidth=3, zorder=8)
        
    if add_x0:
        axs.scatter(x[0], y[0], c='m', s=500, marker="*", zorder=20)


    if title is not None:
        axs.set_title(title, fontsize=14, weight='bold')
    
    
    if save == True:
        fig.savefig(namefig+'.png', dpi=600)

    return fig, axs






def plot_traj_var(trajgroup, var, fig, position=(1,1,1), format_cb=None, 
                  add_title=None, save=False, namefig=None, add_x0=True):
    
    proj = ccrs.PlateCarree()
    
    axs = fig.add_subplot(position[0], position[1], position[2], projection=proj)
    # fig, axs = plt.subplots(subplot_kw=dict(projection=proj), figsize=[6,4])
    
    # Zoom in
    extent = [-150, -59, -70, -9]
    axs.set_extent(extent)
    
    # Add map features
    axs.add_feature(cfeature.OCEAN, alpha=.7)
    axs.add_feature(cfeature.LAND, alpha=1)  # Grayscale colors can be set using 0 (black) to 1 (white)
    axs.coastlines(resolution='50m', color='black', linewidth=.3, zorder=2)
    
    # Add lat/lon gridlines every 20° to the map
    dgx = 20
    dgy = 10
    gl = axs.gridlines(xlocs=np.arange(-180, 180, dgx), ylocs=np.arange(-90, 90, dgy), 
                       zorder=5, draw_labels=True, linestyle='dashed')
    gl.top_labels = False
    gl.bottom_labels = True
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 12, 'color': 'k', 'weight':'bold'}
    gl.ylabel_style = {'size': 12, 'color': 'k', 'weight':'bold'}
    
    
    dt_launch = trajgroup.index.drop_duplicates()
    
    for dti in dt_launch:
        
        df = trajgroup.loc[dti]
        
        
        x = df['Longitude']
        y = df['Latitude']
        z = df[var]
    
        if format_cb == None:
            min_z = min(z)
            max_z = max(z)
            cmap = 'viridis'
            cbar_tit = ''
        else:
            min_z = format_cb['min_z']
            max_z = format_cb['max_z']
            cmap = format_cb['cmap']
            cbar_tit = format_cb['cb_tit']
        
        # Create a set of line segments so that we can color them individually
        # This creates the points as a N x 1 x 2 array so that we can stack points
        # together easily to get the segments. The segments array for line collection
        # needs to be (numlines) x (points per line) x 2 (for x and y)
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(min_z, max_z, clip=True)
        lc = LineCollection(segments, cmap=cmap, norm=norm, zorder=7)
        # Set the values used for colormapping
        lc.set_array(z)
        lc.set_linewidth(2)
        line = axs.add_collection(lc)
        
    if add_x0:
        axs.scatter(x[0], y[0], c='m', s=500, marker="*", zorder=10)

    if add_title != None:
        axs.set_title(add_title, fontsize=14, weight='bold')
    
    cb = fig.colorbar(line, ax=fig.axes, shrink=0.7)
    cb.ax.set_ylabel(cbar_tit, fontsize=13)
    
    if save == True:
        fig.savefig(namefig+'.png', dpi=600)

    return axs


def centroide_traj(trajgroup):
    
    df = trajgroup[['Timestep','Latitude', 'Longitude']]
    
    centroide = df.groupby('Timestep').mean()
    
    return centroide

