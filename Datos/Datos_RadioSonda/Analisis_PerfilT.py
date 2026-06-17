# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:07:18 2026

@author: felip
"""

import pandas as pd
import matplotlib.pyplot as plt


import metpy.calc as mpcalc
#from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units


# Leer el archivo de texto y omitir las primeras líneas antes de los datos
archivo = "20220328_12.txt"  # Reemplaza "yyyymmdd" con la fecha correspondiente
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_RadioSonda/data/'
with open(path+archivo, 'r') as f:
    lines = f.readlines()
    data_start = None
    for i, line in enumerate(lines):
        if "PRES   HGHT   TEMP" in line:
            data_start = i + 3
            break

# Cargar los datos en un DataFrame de pandas
df = pd.read_csv(path+archivo, skiprows=data_start, sep='\\s+',
                 names=["PRES", "HGHT", "TEMP", "DWPT", "RELH", "MIXR",
                        "DRCT", "SKNT", "THTA", "THTE", "THTV"],
                 na_values=["*****", "99999", "NaN", "NaN", ""])

# df = df.iloc[0:len(df.index)-1,:]

#%% Creamos variables

# Variables
T = df['TEMP'].values * units.degC
Td = df['DWPT'].values * units.degC
H = df['HGHT'].values * units.meters

# Diferenciales T
d1_T = df['TEMP'].diff(periods=-1) / df['HGHT'].diff(periods=-1)
d2_T = d1_T.diff(periods=-1) / df['HGHT'].diff(periods=-1)

#%% Plot lineal T y Td

## Plot T ##
plt.figure(figsize=(8,7))
plt.plot(T,H)
plt.title('T: '+str(archivo))
plt.xlim(5,25)
plt.ylim(0,2000)
plt.grid()

## Plot Td ##
# plt.figure(figsize=(8,7))
# plt.plot(Td,H)
# plt.title('Td')
# plt.xlim(-25,15)
# plt.ylim(0,2000)
# plt.grid()

#%% Ploteamos diferencial de T

# Ploteamos T y Dif_T

# T
fig, ax1 = plt.subplots(figsize=(8,7))
c1 = 'tab:blue'
ax1.plot(H,T,label='T', color=c1)
ax1.set_ylabel('T [°C]', color=c1)
ax1.tick_params(axis='y', labelcolor=c1)
ax1.set_ylim(5,20)
ax1.set_xlim(0,1000)

# Diff_T
ax2 = ax1.twinx()
c2 = 'tab:orange'
ax2.plot(H,d1_T, color=c2)
ax2.set_ylabel('d1_T [°C]',color=c2)
ax2.tick_params(axis='y', labelcolor=c2)
# ax2.set_ylim(-10,10)
# ax2.set_xlim(0,2000)

# Diff_T
ax3 = ax1.twinx()
ax3.spines.right.set_position(("axes", 1.2))
c3 = 'tab:green'
ax3.plot(H,d2_T, color=c3)
ax3.set_ylabel('d2_T [°C]',color=c3)
ax3.tick_params(axis='y', labelcolor=c3)
# ax3.set_ylim(-10,10)
# ax3.set_xlim(0,3000)

plt.title('T, d1_T y d2_T')
plt.grid(axis='both',which='both')

#%% Calculo cambio positivo en pendiente

for i in range(len(H)):
    if d1_T[i] > 0:
        hi = H[i]
        print('BLH = '+str(hi))
        break
    elif i == len(H)-1: 
        print('No se encontró pendiente positiva')