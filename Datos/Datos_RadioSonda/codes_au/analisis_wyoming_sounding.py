#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 23:43:08 2023

@author: au
"""

import pandas as pd
import numpy as np

# Define el rango de fechas para el cual tienes archivos
fecha_inicio = "20210101"
fecha_fin = "20211231"
formato_fecha = "%Y%m%d"

# Define los niveles de presión predeterminados
pres_levels = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350,
               300, 250, 225, 200, 175, 150, 125, 100]

# Define las variables de los datos
col_names = ["HGHT", "TEMP", "DWPT", "RELH", "MIXR", "DRCT", "SKNT", "THTA", "THTE", "THTV"]

# Función para leer e interpolar datos de radiosonda para una fecha específica
def procesar_datos_radiosonda(fecha_str):
    archivo = f"{fecha_str}_12.txt"

    try:
        with open(archivo, 'r') as f:
            lines = f.readlines()
            data_start = None
            for i, line in enumerate(lines):
                if "PRES   HGHT   TEMP" in line:
                    data_start = i + 3
                    break

        df = pd.read_csv(archivo, skiprows=data_start, delim_whitespace=True,
                         names=["PRES", "HGHT", "TEMP", "DWPT", "RELH", "MIXR",
                                "DRCT", "SKNT", "THTA", "THTE", "THTV"],
                         na_values=['*****', '99999', 'NaN', 'NaN*', ''])

        dfi = pd.DataFrame({"PRES": pres_levels})
        for col in col_names:
            dfi[col] = df[col].interpolate(method="linear", limit_area="inside")  # Interpolación lineal con relleno

        return dfi  # Devuelve el DataFrame con los datos interpolados
    except FileNotFoundError:
        # Si el archivo no existe, devuelve un DataFrame con NaNs para este día
        n_levels = len(pres_levels)
        data = np.full((n_levels, len(col_names)), np.nan)
        return pd.DataFrame(data, columns=col_names)

# Itera sobre todas las fechas y procesa los datos
rango_fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')
lista_datos_interpolados = []

for fecha in rango_fechas:
    fecha_str = fecha.strftime(formato_fecha)
    datos_interpolados = procesar_datos_radiosonda(fecha_str)
    lista_datos_interpolados.append(datos_interpolados)

# Concatenar los DataFrames en una sola tabla (DataFrame)
df_datos_interpolados = pd.concat(lista_datos_interpolados, keys=rango_fechas, axis=0)
df_datos_interpolados.index.names = ['Fecha', 'Nivel']

# df_datos_interpolados tendrá el DataFrame con los datos interpolados para cada día del año y cada nivel de presión.
#%%

# Obtener una lista de fechas únicas
fechas_unicas = df_datos_interpolados.index.get_level_values('Fecha').unique()

# Obtener el número de niveles de presión
num_niveles = len(pres_levels)

# Crear la matriz tridimensional solo para la variable TEMP
matriz_temp = np.zeros((len(fechas_unicas), num_niveles))

# Llenar la matriz con los datos de la variable TEMP del DataFrame df_datos_interpolados
for idx, fecha in enumerate(fechas_unicas):
    datos_fecha = df_datos_interpolados.loc[fecha]
    matriz_temp[idx, :] = datos_fecha["TEMP"].values

# Ahora tienes la matriz tridimensional "matriz_temp" con los datos interpolados solo para la variable TEMP
print(matriz_temp)

#%%

import matplotlib.pyplot as plt

# Definir las etiquetas de los ejes (fechas y niveles de presión)
etiquetas_fechas = fechas_unicas.strftime('%m-%d')
etiquetas_niveles = pres_levels


# Crear la figura y el gráfico contourf
fig, ax = plt.subplots(figsize=(10, 8))
contour_plot = ax.contourf(etiquetas_fechas, etiquetas_niveles
                           ,matriz_temp.T
                           ,cmap='seismic'
                           ,levels=np.linspace(-20, 20, 11)
                           ,extend='both')


"""
# Crear la figura y el gráfico contourf
fig, ax = plt.subplots(figsize=(10, 8))
contour_plot = ax.contourf(etiquetas_fechas, etiquetas_niveles
                           ,matriz_temp.T
                           ,cmap='jet'
                           ,levels=np.linspace(273, 323, 101)
                           ,extend='both')
"""

# Etiquetas de los ejes
ax.set_xticks(etiquetas_fechas[::15])  # Mostrar cada 15 fechas para evitar superposición
ax.set_xticklabels(etiquetas_fechas[::15], rotation=45, ha='right')
ax.set_xlabel('Fechas')

# Invertir el eje 'y'
ax.invert_yaxis()

# Configurar el eje 'y' en escala logarítmica
ax.set_yscale('log')

# Etiquetas del eje 'y' cada 100 hPa
etiquetas_niveles_cada_100 = list(range(1000, 0, -100))  # Desde 1000 hasta 100 hPa en orden descendente
ax.set_yticks(etiquetas_niveles_cada_100)
ax.set_yticklabels(etiquetas_niveles_cada_100)

ax.set_ylabel('Presión (hPa)')
ax.set_title('Radiosondeos Punta Arenas - 2021')

# Agregar una barra de colores para interpretar los valores
cbar = plt.colorbar(contour_plot, ax=ax)
cbar.set_label('T(°C)')

# Añadir las grillas en cada xtick
plt.grid(which='both')

plt.show()




