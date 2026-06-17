#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:20:47 2023

@author: au
"""

import pandas as pd
import matplotlib.pyplot as plt


import metpy.calc as mpcalc
#from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units


# Leer el archivo de texto y omitir las primeras líneas antes de los datos
archivo = "20220224_00.txt"  # Reemplaza "yyyymmdd" con la fecha correspondiente
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_RadioSonda/data/'
with open(path+archivo, 'r') as f:
    lines = f.readlines()
    data_start = None
    for i, line in enumerate(lines):
        if "PRES   HGHT   TEMP" in line:
            data_start = i + 3
            break

# Cargar los datos en un DataFrame de pandas
df = pd.read_csv(archivo, skiprows=data_start, sep='\\s+',
                 names=["PRES", "HGHT", "TEMP", "DWPT", "RELH", "MIXR",
                        "DRCT", "SKNT", "THTA", "THTE", "THTV"],
                 na_values=["*****", "99999", "NaN", "NaN", ""])

#%% Valores de presión para interpolar (reemplaza estos valores con los niveles deseados)
pres_levels = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350,
               300, 250, 225, 200, 175, 150, 125, 100]

# Función de interpolación cúbica
col_names = ["HGHT", "TEMP", "DWPT", "RELH", "MIXR", "DRCT", "SKNT", "THTA"]
dfi = pd.DataFrame({"PRES": pres_levels})
for col in col_names:
    dfi[col] = df[col].interpolate(method="linear", limit_area="inside")

#%% Plot Skew-T

# Change default to be better for skew-T
plt.rcParams['figure.figsize'] = (9, 9)


# We will pull the data out of the example dataset into individual variables and
# assign units.

p = dfi['PRES'].values * units.hPa
T = dfi['TEMP'].values * units.degC
Td = dfi['DWPT'].values * units.degC
wind_speed = dfi['SKNT'].values * units.knots
wind_dir = dfi['DRCT'].values * units.degrees
u, v = mpcalc.wind_components(wind_speed, wind_dir)

###########################################

skew = SkewT()

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot_barbs(p, u, v)

# Set some better labels than the default
skew.ax.set_xlabel('Temperature (\N{DEGREE CELSIUS})')
skew.ax.set_ylabel('Pressure (mb)')

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()
skew.ax.set_ylim(1000, 100)

# Show the plot
plt.show()

    





