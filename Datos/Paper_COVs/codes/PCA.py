# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 15:46:55 2026

@author: felip
"""
#%%
# Seteamos 3 procesos y cohexistencia de librerías
import os
os.environ["OMP_NUM_THREADS"] = "3"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Silenciamos warning de Intel OpenMP ('libiomp') y LLVM OpenMP ('libomp')
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from sklearn.preprocessing import PowerTransformer, RobustScaler, StandardScaler
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.impute import SimpleImputer
from scipy.stats import rankdata
import seaborn as sns



# path para guardar figuras y datos
path_fig = 'C:/Users/felip/Desktop/U/Tesis/Datos/Paper_COVs/figs/'
path_data = 'C:/Users/felip/Desktop/U/Tesis/Datos/Paper_COVs/data/'

#%% Cargamos datos

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

# reordenamos
order = ['Benceno_1', 'Tolueno_1', 'Etilbenceno y xilenos', 'Trimetilbenceno',
        'Butenos','Propeno_2', 'DMS', 'Isopreno_2', 'Monoterpenos',
        'Acetonitrilo', 'Acetona', 'AcidoAcetico','Metacroleina', 'Butanona', 'Fenol',
        'Etanol', 'Furano', 'Benzonitrilo', 'Estireno',
        'Cresol', 'Benzofurano', 'Naftaleno', 'NO', 'NO2', 'O3',
        'SO2', 'CO', 'PM10', 'PM25',
        'RadGlob', 'Temp', 'EH2O', 'U', 'V']

CC = CC.reindex(columns=order)
QU = QU.reindex(columns=order)
VE = VE.reindex(columns=order)

del CC_ss, QU_ss, VE_ss #, CC_cov, QU_cov, VE_cov
#%% Seleccionamos sitio y tipo de datos a usar
site = 'VE'
use = 'cov+crit' # 'cov' o 'cov+crit' o 'all'
met = ['RadGlob', 'Temp', 'EH2O', 'U', 'V']

if site == 'CC':
    name = 'Concón'
    file_name = 'CC'
    if use == 'cov':
        df = CC_cov.copy()
    elif use == 'cov+crit':
        df = CC.drop(columns=met).copy()
    elif use == 'all':
        df = CC.copy()


elif site == 'QU':
    name = 'Quintero'
    file_name = 'QU'
    if use == 'cov':
        df = QU_cov.copy()
    elif use == 'cov+crit':
        df = QU.drop(columns=met).copy()
    elif use == 'all':
        df = QU.copy()


elif site == 'VE':
    name = 'Ventanas'
    file_name = 'VE'
    if use == 'cov':
        df = VE_cov.copy()
    elif use == 'cov+crit':
        df = VE.drop(columns=met).copy()
    elif use == 'all':
        df = VE.copy()


features = df

#%% 2. Handle NaNs (imputation)
imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(features)

#%% 3. Standardize
# Elige el método: 'spearman' (Opción A), 'yeo-johnson' (Opción B) o 'robust' (Original)
metodo_escala = 'spearman' 

if metodo_escala == 'spearman':
    X_ranked = np.apply_along_axis(rankdata, axis=0, arr=X_imputed)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_ranked)

elif metodo_escala == 'yeo-johnson':
    scaler = PowerTransformer(method='yeo-johnson', standardize=True)
    X_scaled = scaler.fit_transform(X_imputed)

elif metodo_escala == 'robust':
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X_imputed)

#%% 4. Aplicamos SVD

# Definimos cuántos componentes analizar para la matriz (ej. 5 para mayor cobertura)
n_comp_tabla = 5
svd_tabla = PCA(n_components=n_comp_tabla, random_state=42)
# svd_tabla = TruncatedSVD(n_components=n_comp_tabla, random_state=42)
svd_tabla.fit(X_scaled)

# 1) Obtener la varianza explicada por cada componente
varianza_explicada = svd_tabla.explained_variance_ratio_ * 100

# 2) Crear nombres de columnas dinámicos con su varianza respectiva
pc_cols = [f"PC{i+1} ({var:.1f}%)" for i, var in enumerate(varianza_explicada)]

# 3) Extraer los pesos y armar el DataFrame
loadings_corr = svd_tabla.components_.T * np.sqrt(svd_tabla.explained_variance_)
df_loadings = pd.DataFrame(
    loadings_corr,
    index=features.columns,
    columns=pc_cols
)

# 4) Ordenar la tabla por el peso absoluto en PC1 para priorizar los compuestos más influyentes
df_loadings['Magnitud_PC1'] = df_loadings.iloc[:, 0].abs()
df_loadings = df_loadings.sort_values(by='Magnitud_PC1', ascending=False).drop(columns=['Magnitud_PC1'])

print(f"--- Pesos de SVD para {name} ---")
print(f"Varianza total explicada (5 componentes): {varianza_explicada.sum():.1f}%\n")
display(df_loadings.head(15)) # Muestra el top 15 de compuestos en consola

# 5) Exportar tabla a CSV para adjuntar al manuscrito
archivo_salida = path_fig + site + '/' + f'Tabla_Loadings_SVD_{site}.csv'
df_loadings.to_csv(archivo_salida)
print(f"Tabla exportada con éxito a: {archivo_salida}")

#%% 5. Heatmap de Pesos por Componente Principal (SVD)

# Utilizamos el df_loadings generado en la celda anterior.
# Al estar ordenado por PC1, los compuestos que más traccionan la varianza principal quedarán arriba.

# Determinamos el límite simétrico absoluto para centrar el 0 en color neutro
vmin = df_loadings.min().min()
vmax = df_loadings.max().max()
val = np.max([np.abs(vmin), np.abs(vmax)])

plt.figure(figsize=(10, 15))

# Generamos el heatmap (no necesitamos transponer con .T porque df_loadings ya tiene las variables en el índice)
sns.heatmap(df_loadings, cmap="coolwarm", annot=True, fmt=".2f",
            annot_kws={"color": "black", "fontsize": 11}, 
            cbar_kws={'label': 'Peso (Loading)', 'fraction': 0.05},
            cbar=True, vmin=-val, vmax=val)

plt.title(f"Pesos de las Componentes Principales - {name} - {metodo_escala}", fontsize=14, pad=15)
plt.xlabel("Componente Principal", fontsize=12)
plt.ylabel("Variable", fontsize=12)

# Ajustamos los márgenes y guardamos
plt.tight_layout(pad=1.3)
plt.savefig(path_fig + '/Heatmap_PCA_' + file_name +'_'+ use +'_'+ metodo_escala + '.png', dpi=300)
plt.show()

#%% 6. Barplots de Pesos por Componente Principal (SVD) - Estilo Pandas

# Configuración de la figura
fig, axes = plt.subplots(nrows=n_comp_tabla, ncols=1, figsize=(12, 10), sharex=True)
fig.subplots_adjust(hspace=0.1) # Espaciado mínimo entre plots

for i, col in enumerate(df_loadings.columns):
    ax = axes[i]
    valores = df_loadings[col]
    
    # Asignación de colores: basándonos en tu snippet (tab:red para positivo, tab:blue para negativo)
    colores = np.where(valores > 0, "tab:red", "tab:blue")
    
    # Ploteo directo con pandas para emular el estilo de "image_2fa546.png"
    valores.plot(kind="bar", color=colores, ax=ax, width=0.6)
    
    # Formateo del eje Y y línea central
    ax.set_ylim(-1, 1)
    ax.axhline(0, color='black', linewidth=1)
    ax.set_ylabel(col, fontsize=11, fontweight='bold')
    
    # Grilla estilo seaborn/pandas (suave)
    ax.grid(True, which='both', linestyle='-', alpha=0.5)
    
    # Configuración de ticks: mantenemos los "palitos" (bottom=True) pero ocultamos los textos
    if i < n_comp_tabla - 1:
        ax.tick_params(axis='x', which='both', bottom=True, labelbottom=False)
    else:
        ax.tick_params(axis='x', which='both', bottom=True, labelbottom=True)

# Rotación y estilo de los labels en el eje X (solo afecta al último subplot por sharex=True)
plt.xticks(rotation=90, fontweight='bold', fontsize=11)
axes[-1].set_xlabel("Variable", fontsize=12, fontweight='bold', labelpad=10)

plt.suptitle(f"Pesos de las Componentes Principales (SVD) - {name} - {metodo_escala}", fontsize=14, fontweight='bold', y=0.91)

# Ajuste fino de layout para evitar que los labels a 90 grados queden cortados
plt.tight_layout(rect=[0, 0, 1, 0.92]) 
plt.savefig(path_fig + '/Barplots_PCA' + file_name +'_'+ use +'_'+ metodo_escala + '.png', dpi=300)
plt.show()

