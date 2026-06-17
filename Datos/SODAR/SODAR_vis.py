# -*- coding: utf-8 -*-
"""
Created on Wed May 24 15:24:01 2023

@author: felip
"""

import numpy as np
# import matplotlib as pl
import matplotlib.pyplot as plt
import pandas as pd


#%% Importamos datos SODAR (1 día): entrar a carpeta SODAR

dia = '220912'

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/SODAR/RawSodar/'
f = pd.read_table(path+dia+'.txt',skiprows=10,na_values='*')

# '220825' '220904' '221006'
# print(f)

#%% Ordenamos datos de dirección de viento por altura y tiempo

Dir = np.transpose(pd.to_numeric(f.dir.values).reshape([96,98]))

Vel = np.transpose(pd.to_numeric(f.speed.values).reshape([96,98]))


#%% Creamos vector de fechas

# Creamos vector tiempo
t1 = '2022-'+dia[2:4]+'-'+dia[4:6]+' 00:15:00'



t2 = '2022-'+dia[2:4]+'-'+str(int(dia[4:6])+1)+' 00:00:00'

# t2 = '2022-09-01 00:00:00'
time_vec = np.squeeze(pd.date_range(start=t1, end=t2, freq='15min'))
del t1, t2

# chequeamos el largo de del vector fechas original
# time = f.time 

#%% Chequeamos si hay archivos que tengan menos de 96 datos 
# Esto ya que el 220825.txt tiene 95 datos temporales (le falta el 12:15)

# importamos lista con strings de días a usar en listas.txt
lista = np.array(pd.read_table('lista.txt',dtype=str,header=None
                           ,skipinitialspace=True).iloc[:,0])

largo = np.empty([len(lista)])

for i in range(len(lista)):
    largo[i] = pd.read_table('RawSodar/'+lista[i]+'.txt',skiprows=11).size
    
print(sum(largo != 94080)) # hay 3 días con menos datos
n = largo != 94080 # vector booleano con días que tienen menos datos
print(lista[n]) # ['220825' '220904' '221006']

#%% Creamos corrección para días con menos de 9408 datos [96 datos 15m y 98 niveles]

# Tomamos día de referencia que sabemos que tiene todos los datos 
# y tomamos las columnas "time" y "z": '220826'
ref = pd.read_table('RawSodar/220826.txt',skiprows=10,
                    na_values='*',usecols=['time','z'])



#%% Ploteamos días

# Altura
zi = 18


# definimos  x e y para meshgrid y Z cómo el campo:
# x
x = time_vec
# y
y = pd.to_numeric(f.z.values[0:zi])

# X e Y
X, Y = np.meshgrid(x, y)

# Dirección:
Z1 = Dir[0:zi,:]

# Velocidad:
Z2 = Vel[0:zi,:]



fig, (ax1,ax2) = plt.subplots(2,1,layout='constrained',
                              figsize=(10, 6))

# Dirección
CS1 = ax1.contourf(X,Y,Z1,50,cmap='hsv',origin='lower')

ax1.set_title('Perfil dirección viento horizontal para día '+dia[4:6]+'/'+
              dia[2:4]+'/'+dia[0:2])
ax1.set_xlabel('Hora')
ax1.set_ylabel('Altura [m]')
ax1.set_xticks([time_vec[11],time_vec[23],time_vec[35],
                time_vec[47],time_vec[59],time_vec[71],
                time_vec[83],time_vec[95]])
ax1.set_xticklabels(['03:00','06:00','09:00','12:00'
                     ,'15:00','18:00','21:00','00:00'], rotation = 15)
ax1.grid(color='gray',linestyle='--',linewidth=0.5)

# Colorbar
cbar1 = fig.colorbar(CS1)
cbar1.ax.set_ylabel('Dirección de viento [°]')

# Velocidad
levels = np.linspace(0,15,16)
CS2 = ax2.contourf(X,Y,Z2,levels=levels, cmap='Reds', origin='lower',
                   extend='max')

ax2.set_title('Perfil velocidad de viento horizontal para día '+dia[4:6]+'/'+
              dia[2:4]+'/'+dia[0:2])
ax2.set_xlabel('Hora')
ax2.set_ylabel('Altura [m]')
ax2.set_xticks([time_vec[11],time_vec[23],time_vec[35]
                ,time_vec[47],time_vec[59],time_vec[71]
                ,time_vec[83],time_vec[95]])
ax2.set_xticklabels(['03:00','06:00','09:00','12:00'
                     ,'15:00','18:00','21:00','00:00'], rotation = 15)
ax2.grid(color='gray',linestyle='--',linewidth=0.5)


# Colorbar
cbar2 = fig.colorbar(CS2)
cbar2.ax.set_ylabel('Velocidad [m/s]')

#%% Vamos a probar el approach de ChatGPT

dia = '220904'

# '220825' '220904' '221006'

# Load data
df = pd.read_table('RawSodar/'+dia+'.txt',skiprows=10,na_values='*')

# Assuming `time` column is in datetime format
df['time'] = pd.to_datetime(df['time'])

# Define the full range for `time`, starting from 00:15 to exclude 00:00 of the current day
start_time = df['time'].min().replace(hour=0, minute=15)
end_time = start_time + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)
full_time_range = pd.date_range(start=start_time, end=end_time, freq='15T')

# Define the full range for `z`
z_levels = np.arange(30, 1010, 10)  # 30 to 1000 meters in steps of 10

# Create a complete grid of time and z
full_index = pd.MultiIndex.from_product([full_time_range, z_levels], names=['time', 'z'])
full_df = pd.DataFrame(index=full_index).reset_index()

# Merge with your original dataframe
merged_df = pd.merge(full_df, df, on=['time', 'z'], how='left')

# Save or work with `merged_df` as needed
print(merged_df.head())







