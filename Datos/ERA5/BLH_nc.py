# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 15:14:46 2025

@author: felip
"""

from netCDF4 import Dataset, num2date
import pandas as pd
import matplotlib.pyplot as plt

#%% Import data

# [-71.55,-32.83]: 2018-2023
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/ERA5/BLH_2018-2023_6h.nc'
nc_file = Dataset(path)

#%% Exploramos

# Variables
nc_file.variables

# Lat Lon date
Lat =  nc_file['latitude'][:]
Lon =  nc_file['longitude'][:]
valid_time =  nc_file['valid_time'][:]
units =  nc_file.variables['valid_time'].getncattr('units')
cal = nc_file.variables['valid_time'].getncattr('calendar')
date = num2date(valid_time,units=units,calendar=cal,
                only_use_cftime_datetimes=False)

# BLH
BLH =  nc_file['blh'][:,0,0].tolist()

# Creamos DF
BLH_df = pd.DataFrame(columns=['BLH'],index=pd.to_datetime(date))
BLH_df['BLH'] = BLH

#%% Ploteamos

d1 = pd.to_datetime('2022-09-01 00:00:00')
d2 = pd.to_datetime('2022-10-31 23:00:00')
BLH_df.loc[d1:d2].plot(grid=True, figsize=(20,7), title='BLH',ylabel='m',
                       ylim=(0,1000))
plt.tight_layout()

#%% Guardamos .csv
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/ERA5/'
BLH_df.to_csv(path+'BLH_ERA5.csv',index_label='date')

