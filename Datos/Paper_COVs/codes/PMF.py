# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 11:38:29 2026

@author: felip
"""

#%% Importamos librerías, datos y definimos paths
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
import seaborn as sns


# path para guardar figuras y datos
path_fig = 'C:/Users/felip/Desktop/U/Tesis/Datos/Paper_COVs/figs/'
path_data = 'C:/Users/felip/Desktop/U/Tesis/Datos/Paper_COVs/data/'

# Datos COVs
CC_cov = pd.read_csv(path_data+'Serie_Concon_mean_30min.csv', index_col=0,
                     parse_dates=True).rename_axis('date')
QU_cov = pd.read_csv(path_data+'Serie_Quintero_mean_30min.csv', index_col=0, 
                     parse_dates=True).rename_axis('date')
VE_cov = pd.read_csv(path_data+'Serie_Ventanas_mean_30min.csv', index_col=0, 
                     parse_dates=True).rename_axis('date')

# Datos Contaminantes Criterio y Meteo Supersitios
new_ord = ['NO', 'NO2', 'O3', 'NOx', 'CO', 'PM10', 'PM25', 'SO2', 'H2S',
           'RadGlob', 'RH', 'Temp', 'DirV', 'VelV', 'EH2O', 'U', 'V']
CC_ss = pd.read_csv(path_data+'Serie_SS_Concon_mean_30min.csv', index_col=0, 
                    parse_dates=True).rename_axis('date').reindex(columns=new_ord)
QU_ss = pd.read_csv(path_data+'Serie_SS_Quintero_mean_30min.csv', index_col=0, 
                    parse_dates=True).rename_axis('date').reindex(columns=new_ord)
VE_ss = pd.read_csv(path_data+'Serie_SS_Ventanas_mean_30min.csv', index_col=0, 
                    parse_dates=True).rename_axis('date').reindex(columns=new_ord)

# Juntamos DFs
CC = CC_cov.join(CC_ss)
QU = QU_cov.join(QU_ss)
VE = VE_cov.join(VE_ss)


# Quitamos variables repetidas 
drop = []
for col in CC.columns:
    if (col[-2:len(col)] == '_2') or (col in ['Formaldehido', 'Metanol']):
        drop.append(col)

CC = CC.drop(columns=drop)
QU = QU.drop(columns=drop)
VE = VE.drop(columns=drop)

del CC_cov, QU_cov, VE_cov, CC_ss, QU_ss, VE_ss, new_ord, drop, col
#%% [1] CONFIGURACIÓN Y SELECCIÓN DE CAMPAÑA

# Definimos estación
est = 'CC'

if est == 'CC':
    df = CC.iloc[:,0:23].copy()
    sitio = 'Concón'

elif est == 'QU':
    df = QU.iloc[:,0:23].copy()
    sitio = 'Quintero'

elif est == 'VE':
    df = VE.iloc[:,0:23].copy()
    sitio = 'Ventanas'


# Asegurar resolución de 30 minutos por si hay datos faltantes en la serie temporal
df = df.sort_index().resample('30min').mean()

print(f"--- Procesando campaña: {sitio} ---")
print(f"Dimensiones del dataset: {df.shape}")

#%% [2] PARÁMETROS INSTRUMENTALES (PTR-TOF-MS)
# Límite de Detección del Método (MDL) para los 29 compuestos.
# Reemplaza 0.05 con un diccionario o Serie si tienes MDLs específicos por compuesto.
# mdl_values = pd.Series(0.01, index=df.columns) 

# # Fracción de error analítico (Usualmente entre 10% y 20% para PTR-TOF-MS)
# error_fraction = 0.10

#%% [2] CÁLCULO DE MDL EMPÍRICO (ECUACIÓN 3) Y PARÁMETROS
# Se estima el MDL para cada compuesto basándose en el ruido de fondo (background)
# de sus mediciones más bajas, asumiendo que los valores base representan ruido instrumental.

mdl_dict = {}

for col in df.columns:
    # 1. Calcular el valor correspondiente al percentil 2
    q = df[col].quantile(0.02)
    
    # 2. Filtrar los datos que están por debajo de este percentil (el "ruido de fondo")
    background_data = df.loc[df[col] <= q, col]
    
    # 3. Calcular el MDL como 3 veces la desviación estándar de este fondo
    # Se agrega un factor de seguridad (ej. + 0.005) por si la std es 0 debido a datos estáticos
    std_bg = background_data.std()
    mdl_empirico = (3 * std_bg) #+ 0.005 
    
    mdl_dict[col] = mdl_empirico

# Convertir el diccionario en la Serie que alimenta la matriz de errores
mdl_values = pd.Series(mdl_dict)

# Puedes imprimir los resultados para revisarlos antes de correr el PMF
print("MDL calculados por especie (ppb):")
print(mdl_values.round(3))

# Fracción de error analítico sugerida para PTR-TOF-MS procesado
error_fraction = 0.05

#%% [3] CÁLCULO DE LA MATRIZ DE ERRORES (Guidelines EPA PMF)
# Se crea la matriz de errores y se corrigen las concentraciones en 'df'

df_error = pd.DataFrame(index=df.index, columns=df.columns)

for col in df.columns:
    mdl = mdl_values[col]
    
    # Regla 1: Valores faltantes (NaN) -> Conc = Mediana, Error = 4 * Mediana
    median_val = df[col].median()
    missing_mask = df[col].isna()
    
    # Regla 2: Valores por debajo del MDL (o negativos) -> Conc = MDL / 2, Error = (5/6) * MDL
    below_mdl_mask = (df[col] <= mdl) & (~missing_mask)
    
    # Regla 3: Valores normales (> MDL) -> Error = sqrt((Error_Fraction * Conc)^2 + MDL^2)
    normal_mask = (df[col] > mdl) & (~missing_mask)
    
    # 1. Asignar errores
    df_error.loc[normal_mask, col] = np.sqrt((error_fraction * df.loc[normal_mask, col])**2 + (mdl)**2)
    df_error.loc[below_mdl_mask, col] = (5/6) * mdl
    df_error.loc[missing_mask, col] = 4 * median_val
    
    # 2. Reemplazar concentraciones en el dataframe principal
    df.loc[below_mdl_mask, col] = mdl / 2
    df.loc[missing_mask, col] = median_val

# Convertir todo a float explícitamente para evitar problemas con sklearn
df = df.astype(float)
df_error = df_error.astype(float)

print(f"Matriz de errores calculada y datos por debajo del MDL reemplazados para {sitio}.")

#%% [3.5] EVALUACIÓN DE SEÑAL/RUIDO (S/N) Y CATEGORIZACIÓN EPA
# Esta celda clasifica los COVs en Strong, Weak o Bad, purificando la matriz
# antes de calcular X_weighted y evaluar Q/Qexp.

sn_dict = {}
n_samples = len(df)

for col in df.columns:
    # Diferencia entre la concentración (X) y la incertidumbre (U)
    diff = df[col] - df_error[col]
    
    # Aplicar la regla de la EPA: si X > U, calcular ratio, sino 0
    d_ij = np.where(diff > 0, diff / df_error[col], 0)
    
    # El S/N de la especie es el promedio de d_ij en toda la campaña
    sn_dict[col] = np.sum(d_ij) / n_samples

sn_series = pd.Series(sn_dict)

print("--- RELACIÓN SEÑAL/RUIDO (S/N) EPA ---")
print(sn_series.sort_values(ascending=False).round(2))
print("-" * 36)

# Categorización según los umbrales oficiales de EPA PMF 5.0
strong_cols = sn_series[sn_series > 2.0].index.tolist()
weak_cols = sn_series[(sn_series <= 2.0) & (sn_series > 0.2)].index.tolist()
bad_cols = sn_series[sn_series <= 0.2].index.tolist()

print(f"Resumen de categorización para {sitio}:")
print(f"Strong (S/N > 2.0): {len(strong_cols)} especies")
print(f"Weak (0.2 < S/N <= 2.0): {len(weak_cols)} especies")
print(f"Bad (S/N <= 0.2): {len(bad_cols)} especies")

# === APLICACIÓN DE REGLAS EPA ===

# 1. Especies "Bad": Se eliminan por completo (son casi puro ruido)
if len(bad_cols) > 0:
    df = df.drop(columns=bad_cols)
    df_error = df_error.drop(columns=bad_cols)
    print(f"\n[!] Eliminadas {len(bad_cols)} especies 'Bad': {bad_cols}")

# 2. Especies "Weak": Se triplica su incertidumbre para reducir su peso al minimizar Q
if len(weak_cols) > 0:
    df_error[weak_cols] = df_error[weak_cols] * 3
    print(f"[!] Triplicado el error de {len(weak_cols)} especies 'Weak': {weak_cols}")

# 3. Recalcular la matriz ponderada (X_weighted) ya purificada
X_weighted = df / df_error
X_weighted = X_weighted.fillna(0)

print("\nMatriz purificada y lista para evaluar Q/Qexp.")

#%% EXPORTACIÓN PARA EPA PMF 5.0 (RECOMENDADO PARA LA TESIS)
# Se exportan con el nombre del sitio para no chancar los archivos al correr los 3 DFs.

archivo_datos = f'PMF_Data_{sitio}.csv'
archivo_errores = f'PMF_Error_{sitio}.csv'

df.to_csv(path_data+archivo_datos)
df_error.to_csv(path_data+archivo_errores)

print(f"Archivos listos para EPA PMF: {archivo_datos} y {archivo_errores}")

#%% [4] EVALUACIÓN DEL NÚMERO DE FACTORES (Q/Qexp)

# Ponderación por incertidumbre (Data / Error)
X_weighted = df / df_error
X_weighted = X_weighted.fillna(0) # Por seguridad

# Definir rango de factores a evaluar
rango_factores = range(2, 9)

# Variables para almacenar resultados
q_true_list = []
q_exp_list = []
ratio_list = []

n_samples, n_features = X_weighted.shape

for p in rango_factores:
    # Correr NMF ponderado
    nmf = NMF(n_components=p, init='nndsvd', max_iter=2000, random_state=42)
    W_w = nmf.fit_transform(X_weighted)
    H_w = nmf.components_
    
    # Reconstruir la matriz (con la ponderación del error incluida)
    X_reconstructed = np.dot(W_w, H_w)
    
    # Q_true es la norma de Frobenius al cuadrado de (Datos Reales - Datos Reconstruidos)
    # Ya que X_weighted está dividida por el error, esto equivale al Q_true de PMF
    residuals = X_weighted.values - X_reconstructed
    q_true = np.sum(residuals**2)
    
    # Q_expected
    q_exp = (n_samples * n_features) - p * (n_samples + n_features)
    
    ratio = q_true / q_exp
    
    q_true_list.append(q_true)
    q_exp_list.append(q_exp)
    ratio_list.append(ratio)
    
    print(f"Factores: {p} | Q_true: {q_true:.0f} | Q_exp: {q_exp} | Ratio: {ratio:.2f}")

# Graficar el Ratio Q/Qexp
plt.figure(figsize=(8, 5))
plt.plot(rango_factores, ratio_list, marker='o', linestyle='-', color='indigo', lw=2)
plt.axhline(y=1.0, color='red', linestyle='--', label='Ideal Ratio (1.0)')

plt.title('Evaluación del número de factores: Ratio Q / Q_expected')
plt.xlabel('Número de Factores (p)')
plt.ylabel('Q_true / Q_expected')
plt.grid(True, alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# Nota: El "codo" de la curva o el punto donde se estabiliza cerca de 1.0 
# es matemáticamente el número óptimo inicial.

#%% [5] APLICACIÓN DE PMF VÍA SCIPY/SKLEARN (APROXIMACIÓN PYTHON)

# Definir número de factores a extraer (ajústalo según la varianza explicada que busques)
n_components = 5 

nmf_model = NMF(n_components=n_components, init='nndsvd', max_iter=5000, random_state=42)
W_weighted = nmf_model.fit_transform(X_weighted)
H_weighted = nmf_model.components_

# Deshacer la ponderación
W = W_weighted # Contribuciones temporales (Time Series)
H = H_weighted * df_error.mean().values.reshape(1, -1) # Perfiles químicos (Source Profiles)

# Normalizar H para que sume 1 (o 100%) por factor y ajustar W
for i in range(n_components):
    factor_sum = H[i, :].sum()
    if factor_sum > 0:
        H[i, :] = H[i, :] / factor_sum
        W[:, i] = W[:, i] * factor_sum

df_H = pd.DataFrame(H, columns=df.columns, index=[f'Factor {i+1}' for i in range(n_components)])
df_W = pd.DataFrame(W, index=df.index, columns=[f'Factor {i+1}' for i in range(n_components)])

#%% [6] VISUALIZACIÓN DE RESULTADOS PARA EL SITIO SELECCIONADO

# 6.1 Gráfico de Perfiles (Fingerprints)
fig, axes = plt.subplots(n_components, 1, figsize=(12, 2 * n_components), sharex=True)
fig.subplots_adjust(hspace=0.4)
fig.suptitle(f'Perfiles de Fuentes PMF - {sitio}', fontsize=14, y=0.92)

for i in range(n_components):
    ax = axes[i]
    factor_profile = df_H.iloc[i]
    ax.bar(factor_profile.index, factor_profile.values, color='steelblue')
    ax.set_title(f'Factor {i+1}')
    ax.set_ylabel('Fracción Másica')
    ax.tick_params(axis='x', rotation=90)

plt.show()

# 6.2 Gráfico de Series Temporales (Time Series de los factores)
fig, axes = plt.subplots(n_components, 1, figsize=(14, 2 * n_components), sharex=True)
fig.subplots_adjust(hspace=0.4)
fig.suptitle(f'Contribución Temporal de las Fuentes - {sitio}', fontsize=14, y=0.92)

for i in range(n_components):
    ax = axes[i]
    ax.plot(df_W.index, df_W[f'Factor {i+1}'], color='darkorange')
    ax.set_title(f'Factor {i+1}')
    ax.set_ylabel('ppb')

plt.show()

#%% [7] VISUALIZACIÓN: CICLOS DIARIOS (DIURNAL PROFILES)

# Extraer la hora del índice temporal
df_W_hourly = df_W.copy()
df_W_hourly['Hora'] = df_W_hourly.index.hour

# Agrupar por hora calculando la media y el intervalo de confianza (desviación estándar)
hourly_mean = df_W_hourly.groupby('Hora').mean()
hourly_std = df_W_hourly.groupby('Hora').std()

fig, axes = plt.subplots(n_components, 1, figsize=(10, 2.5 * n_components), sharex=True)
fig.subplots_adjust(hspace=0.3)
fig.suptitle(f'Ciclo Diario de las Fuentes - {sitio}', fontsize=14, y=0.92)

for i in range(n_components):
    ax = axes[i]
    factor_name = f'Factor {i+1}'
    
    # Graficar la media
    ax.plot(hourly_mean.index, hourly_mean[factor_name], color='crimson', lw=2)
    # Sombrear la desviación estándar (variabilidad)
    ax.fill_between(hourly_mean.index, 
                    hourly_mean[factor_name] - hourly_std[factor_name], 
                    hourly_mean[factor_name] + hourly_std[factor_name], 
                    color='crimson', alpha=0.2)
    
    ax.set_title(factor_name)
    ax.set_ylabel('ppb')
    ax.set_xticks(range(0, 24, 2))
    ax.grid(True, linestyle='--', alpha=0.5)

ax.set_xlabel('Hora del día (Local)')
plt.show()

#%% [8] VISUALIZACIÓN: ÁREAS APILADAS (STACKED AREA CHART)
# Ideal para ver qué factor domina la contaminación total en el tiempo

fig, ax = plt.subplots(figsize=(14, 6))

# colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'] # Ajustar según n_components
ax.stackplot(df_W.index, df_W.T, labels=df_W.columns, alpha=0.8)

ax.set_title(f'Contribución Absoluta Apilada de COVs - {sitio}')
ax.set_ylabel('Concentración Total (ppb)')
ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
ax.margins(x=0)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# %%
