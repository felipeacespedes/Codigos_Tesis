# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:26:37 2026

@author: felip
"""
#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import seaborn as sns
import numpy as np
import scipy.cluster.hierarchy as sch

path_data = 'C:/Users/felip/Desktop/U/Tesis/Datos/Paper_COVs/data/'
path_fig = 'C:/Users/felip/Desktop/U/Tesis/Datos/Paper_COVs/figs/'

#%% Importamos datos

# Datos COVs
CC_cov = pd.read_csv(path_data+'Serie_Concon_mean_30min.csv', index_col=0,
                     parse_dates=True).rename_axis('date')
QU_cov = pd.read_csv(path_data+'Serie_Quintero_mean_30min.csv', index_col=0, 
                     parse_dates=True).rename_axis('date')
VE_cov = pd.read_csv(path_data+'Serie_Ventanas_mean_30min.csv', index_col=0, 
                     parse_dates=True).rename_axis('date')

# Datos Contaminantes Criterio y Meteo Supersitios
CC_ss = pd.read_csv(path_data+'Serie_SS_Concon_mean_30min.csv', index_col=0, 
                    parse_dates=True).rename_axis('date')
QU_ss = pd.read_csv(path_data+'Serie_SS_Quintero_mean_30min.csv', index_col=0, 
                    parse_dates=True).rename_axis('date')
VE_ss = pd.read_csv(path_data+'Serie_SS_Ventanas_mean_30min.csv', index_col=0, 
                    parse_dates=True).rename_axis('date')

#%% Quitamos compuestos no utilizados

drop = []
for col in CC_cov.columns:
    if (col in ['Formaldehido', 'Metanol', 'Isopreno', 'Propeno']):
        drop.append(col)
    elif (col[-2:len(col)] == '_2') and col not in ['Isopreno_2', 'Propeno_2']:
        drop.append(col)

   
CC_cov = CC_cov.drop(columns=drop)
QU_cov = QU_cov.drop(columns=drop)
VE_cov = VE_cov.drop(columns=drop)

#%% Quitamos variables meteo

drop = []
for col in CC_ss.columns:
    if col in ['RH', 'VelV', 'DirV', 'H2S','NOx']:
        drop.append(col) 

CC_ss = CC_ss.drop(columns=drop)
QU_ss = QU_ss.drop(columns=drop)
VE_ss = VE_ss.drop(columns=drop)

#%% Juntamos DFs

CC = CC_cov.join(CC_ss)
QU = QU_cov.join(QU_ss)
VE = VE_cov.join(VE_ss)

del CC_ss, QU_ss, VE_ss #, CC_cov, QU_cov, VE_cov

#%% Creamos matriz de correlación ###
#####################################

#%% Cuadrado #%%%
#################

#%% Concón 

plot = 'cov'
if plot == 'all':
    file_name = 'CorrMat_CC.png'
    title = 'Matriz de Correlación Jerárquica - Concón'
    corr_CC = CC.corr(method='spearman')
elif plot == 'cov':
    file_name = 'CorrMat_CC_cov.png'
    title = 'Matriz de Correlación Jerárquica - Concón COVs'
    corr_CC = CC_cov.corr(method='spearman')

# Definimos el tamaño de la figura y creamos el clustermap
cg_full = sns.clustermap(
    corr_CC, 
    method='ward',            # Método de aglomeración jerárquica
    cmap='seismic',           # Paleta de colores similar a tu referencia
    annot=True,               # Mostrar los valores numéricos
    annot_kws={"size": 6.5},
    fmt=".1f",                # 2 decimales
    vmin=-1, vmax=1,          # Fijar la escala de correlación de -1 a 1
    figsize=(14, 14), 
    dendrogram_ratio=(0.3, 0.3) # Proporción de espacio para el dendrograma
)



# Ocultamos el dendrograma de las columnas (superior)
cg_full.ax_col_dendrogram.set_visible(False)

# 1. EL SECRETO: Volver a encender el eje maestro que Seaborn apagó
cg_full.ax_row_dendrogram.set_axis_on()

# 2. Al encenderlo, aparecerá un recuadro completo. Apagamos los bordes que no sirven:
for spine in ['top', 'right', 'left']:
    cg_full.ax_row_dendrogram.spines[spine].set_visible(False)

# 3. Aseguramos que solo el borde inferior se mantenga visible
cg_full.ax_row_dendrogram.spines['bottom'].set_visible(True)

# 4. Ahora sí, configuramos y mostramos los números en el eje X
cg_full.ax_row_dendrogram.xaxis.set_major_locator(ticker.AutoLocator())
cg_full.ax_row_dendrogram.xaxis.set_major_formatter(ticker.ScalarFormatter())
cg_full.ax_row_dendrogram.tick_params(axis='x', bottom=True, labelbottom=True, labelsize=10,labelrotation=90)
cg_full.ax_row_dendrogram.set_xlabel('Distancia de Enlace \n (Ward)', fontsize=11)


# Posición cbar
heatmap_pos = cg_full.ax_heatmap.get_position()
center_y = heatmap_pos.y0 + (heatmap_pos.height / 2)
cbar_width = 0.02
cbar_height = 0.6
cbar_bottom = center_y - (cbar_height / 2)
cbar_left = heatmap_pos.x1 + 0.14
cg_full.ax_cbar.set_position([cbar_left, cbar_bottom, cbar_width, cbar_height])

# Título
cg_full.fig.suptitle(title, y=0.77)

cg_full.savefig(path_fig+file_name, dpi=300)
plt.show()


#%% Quintero

plot = 'cov'
if plot == 'all':
    file_name = 'CorrMat_QU.png'
    title = 'Matriz de Correlación Jerárquica - Quintero'
    corr_QU = QU.corr(method='spearman')
elif plot == 'cov':
    file_name = 'CorrMat_QU_cov.png'
    title = 'Matriz de Correlación Jerárquica - Quintero COVs'
    corr_QU = QU_cov.corr(method='spearman')

# Definimos el tamaño de la figura y creamos el clustermap
cg_full = sns.clustermap(
    corr_QU, 
    method='ward',            # Método de aglomeración jerárquica
    cmap='seismic',           # Paleta de colores similar a tu referencia
    annot=True,               # Mostrar los valores numéricos
    annot_kws={"size": 6.5},
    fmt=".1f",                # 2 decimales
    vmin=-1, vmax=1,          # Fijar la escala de correlación de -1 a 1
    figsize=(14, 14), 
    dendrogram_ratio=(0.3, 0.3) # Proporción de espacio para el dendrograma
)

# Ocultamos el dendrograma de las columnas (superior)
cg_full.ax_col_dendrogram.set_visible(False)

# 1. EL SECRETO: Volver a encender el eje maestro que Seaborn apagó
cg_full.ax_row_dendrogram.set_axis_on()

# 2. Al encenderlo, aparecerá un recuadro completo. Apagamos los bordes que no sirven:
for spine in ['top', 'right', 'left']:
    cg_full.ax_row_dendrogram.spines[spine].set_visible(False)

# 3. Aseguramos que solo el borde inferior se mantenga visible
cg_full.ax_row_dendrogram.spines['bottom'].set_visible(True)

# 4. Ahora sí, configuramos y mostramos los números en el eje X
cg_full.ax_row_dendrogram.xaxis.set_major_locator(ticker.AutoLocator())
cg_full.ax_row_dendrogram.xaxis.set_major_formatter(ticker.ScalarFormatter())
cg_full.ax_row_dendrogram.tick_params(axis='x', bottom=True, labelbottom=True, labelsize=10,labelrotation=90)
cg_full.ax_row_dendrogram.set_xlabel('Distancia de Enlace \n (Ward)', fontsize=11)


# Posición cbar
heatmap_pos = cg_full.ax_heatmap.get_position()
center_y = heatmap_pos.y0 + (heatmap_pos.height / 2)
cbar_width = 0.02
cbar_height = 0.6
cbar_bottom = center_y - (cbar_height / 2)
cbar_left = heatmap_pos.x1 + 0.14
cg_full.ax_cbar.set_position([cbar_left, cbar_bottom, cbar_width, cbar_height])

# Título
cg_full.fig.suptitle(title, y=0.77)

cg_full.savefig(path_fig+file_name, dpi=300)
plt.show()


#%% Ventanas

plot = 'cov'
if plot == 'all':
    file_name = 'CorrMat_VE.png'
    title = 'Matriz de Correlación Jerárquica - Ventanas'
    corr_VE = VE.corr(method='spearman')
elif plot == 'cov':
    file_name = 'CorrMat_VE_cov.png'
    title = 'Matriz de Correlación Jerárquica - Ventanas COVs'
    corr_VE = VE_cov.corr(method='spearman')

# Definimos el tamaño de la figura y creamos el clustermap
cg_full = sns.clustermap(
    corr_VE, 
    method='ward',            # Método de aglomeración jerárquica
    cmap='seismic',           # Paleta de colores similar a tu referencia
    annot=True,               # Mostrar los valores numéricos
    annot_kws={"size": 6.5},
    fmt=".1f",                # 2 decimales
    vmin=-1, vmax=1,          # Fijar la escala de correlación de -1 a 1
    figsize=(14, 14), 
    dendrogram_ratio=(0.3, 0.3) # Proporción de espacio para el dendrograma
)



# Ocultamos el dendrograma de las columnas (superior)
cg_full.ax_col_dendrogram.set_visible(False)

# 1. EL SECRETO: Volver a encender el eje maestro que Seaborn apagó
cg_full.ax_row_dendrogram.set_axis_on()

# 2. Al encenderlo, aparecerá un recuadro completo. Apagamos los bordes que no sirven:
for spine in ['top', 'right', 'left']:
    cg_full.ax_row_dendrogram.spines[spine].set_visible(False)

# 3. Aseguramos que solo el borde inferior se mantenga visible
cg_full.ax_row_dendrogram.spines['bottom'].set_visible(True)

# 4. Ahora sí, configuramos y mostramos los números en el eje X
cg_full.ax_row_dendrogram.xaxis.set_major_locator(ticker.AutoLocator())
cg_full.ax_row_dendrogram.xaxis.set_major_formatter(ticker.ScalarFormatter())
cg_full.ax_row_dendrogram.tick_params(axis='x', bottom=True, labelbottom=True, labelsize=10,labelrotation=90)
cg_full.ax_row_dendrogram.set_xlabel('Distancia de Enlace \n (Ward)', fontsize=11)


# Posición cbar
heatmap_pos = cg_full.ax_heatmap.get_position()
center_y = heatmap_pos.y0 + (heatmap_pos.height / 2)
cbar_width = 0.02
cbar_height = 0.6
cbar_bottom = center_y - (cbar_height / 2)
cbar_left = heatmap_pos.x1 + 0.14
cg_full.ax_cbar.set_position([cbar_left, cbar_bottom, cbar_width, cbar_height])

# Título
cg_full.fig.suptitle(title, y=0.77)

cg_full.savefig(path_fig+file_name, dpi=300)
plt.show()














#%% Triangular

# a) Calculamos las distancias y el enlace (linkage) manualmente
linkage_matrix = sch.linkage(sch.distance.pdist(corr_CC), method='ward')
dendro = sch.dendrogram(linkage_matrix, no_plot=True)
reordered_idx = dendro['leaves'] # Este es el orden en el que quedarán las variables

# b) Creamos una máscara para el triángulo superior ya reordenado
sorted_mask = np.tril(np.ones_like(corr_CC, dtype=bool))

# c) Revertimos el orden de la máscara para dársela a clustermap en formato original
original_mask = np.empty_like(sorted_mask)
for i, orig_i in enumerate(reordered_idx):
    for j, orig_j in enumerate(reordered_idx):
        original_mask[orig_i, orig_j] = sorted_mask[i, j]

# d) Generamos el gráfico aplicando la máscara
cg_half = sns.clustermap(
    corr_CC, 
    row_linkage=linkage_matrix,
    col_linkage=linkage_matrix,
    mask=original_mask,       # Aplicamos la máscara calculada
    cmap='BrBG',              # Paleta Café-Verde similar a tu primera imagen
    annot=True,
    annot_kws={"size": 5},
    fmt=".1f", 
    vmin=-1, vmax=1, 
    figsize=(12, 12),
    dendrogram_ratio=(0.15, 0.15)
)

# Limpiamos el gráfico ocultando el dendrograma lateral
cg_half.ax_row_dendrogram.set_visible(False)
cg_half.fig.suptitle('Matriz Triangular con Dendrograma - Concón', y=1.03)

plt.show()