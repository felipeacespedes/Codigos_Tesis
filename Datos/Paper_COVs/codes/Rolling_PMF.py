# -*- coding: utf-8 -*-
"""
Script Consolidado: Rolling PMF para Datos PTR-TOF-MS
"""

#%% [1] IMPORTACIÓN, PREPARACIÓN DE DATOS Y SELECCIÓN DE CAMPAÑA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
from scipy.ndimage import gaussian_filter

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

# --- SELECCIÓN DE CAMPAÑA ---
est = 'QU' # Cambiar a 'CC', 'QU' o 'VE'

if est == 'CC':
    df = CC.iloc[:,0:23].copy()
    df_og = CC.copy()
    sitio = 'Concón'
elif est == 'QU':
    df = QU.iloc[:,0:23].copy()
    df_og = QU.copy()
    sitio = 'Quintero'
elif est == 'VE':
    df = VE.iloc[:,0:23].copy()
    df_og = VE.copy()
    sitio = 'Ventanas'

# Asegurar resolución temporal
df = df.sort_index().resample('30min').mean()
print(f"--- Procesando campaña: {sitio} ---")
print(f"Dimensiones del dataset: {df.shape}")

#%% [2] CÁLCULO DE MDL EMPÍRICO Y MATRIZ DE ERRORES
mdl_dict = {}

for col in df.columns:
    q = df[col].quantile(0.05) # Se ajustó al percentil 5
    background_data = df.loc[df[col] <= q, col]
    std_bg = background_data.std()
    mdl_empirico = (3 * std_bg) 
    mdl_dict[col] = mdl_empirico

mdl_values = pd.Series(mdl_dict)
print("MDL calculados por especie (ppb):")
print(mdl_values.round(3))

error_fraction = 0.05 # Ajustado a 0.05

df_error = pd.DataFrame(index=df.index, columns=df.columns)
for col in df.columns:
    mdl = mdl_values[col]
    median_val = df[col].median()
    missing_mask = df[col].isna()
    below_mdl_mask = (df[col] <= mdl) & (~missing_mask)
    normal_mask = (df[col] > mdl) & (~missing_mask)
    
    df_error.loc[normal_mask, col] = np.sqrt((error_fraction * df.loc[normal_mask, col])**2 + (mdl)**2)
    df_error.loc[below_mdl_mask, col] = (5/6) * mdl
    df_error.loc[missing_mask, col] = 4 * median_val
    
    df.loc[below_mdl_mask, col] = mdl / 2
    df.loc[missing_mask, col] = median_val

df = df.astype(float)
df_error = df_error.astype(float)

#%% [3] EVALUACIÓN DE SEÑAL/RUIDO (S/N) Y CATEGORIZACIÓN EPA
sn_dict = {}
n_samples = len(df)

for col in df.columns:
    diff = df[col] - df_error[col]
    d_ij = np.where(diff > 0, diff / df_error[col], 0)
    sn_dict[col] = np.sum(d_ij) / n_samples

sn_series = pd.Series(sn_dict)

print("--- RELACIÓN SEÑAL/RUIDO (S/N) EPA ---")
print(sn_series.sort_values(ascending=False).round(2))
print("-" * 36)

strong_cols = sn_series[sn_series > 2.0].index.tolist()
weak_cols = sn_series[(sn_series <= 2.0) & (sn_series > 0.2)].index.tolist()
bad_cols = sn_series[sn_series <= 0.2].index.tolist()

print(f"Strong (S/N > 2.0): {len(strong_cols)} especies")
print(f"Weak (0.2 < S/N <= 2.0): {len(weak_cols)} especies")
print(f"Bad (S/N <= 0.2): {len(bad_cols)} especies")

if len(bad_cols) > 0:
    df = df.drop(columns=bad_cols)
    df_error = df_error.drop(columns=bad_cols)
    print(f"[!] Eliminadas {len(bad_cols)} especies 'Bad': {bad_cols}")

if len(weak_cols) > 0:
    df_error[weak_cols] = df_error[weak_cols] * 3
    print(f"[!] Triplicado el error de {len(weak_cols)} especies 'Weak': {weak_cols}")

X_weighted = df / df_error
X_weighted = X_weighted.fillna(0)

#%% [4] EVALUACIÓN DEL NÚMERO DE FACTORES (Q/Qexp)
rango_factores = range(2, 9)
q_true_list, q_exp_list, ratio_list = [], [], []
n_samples_w, n_features_w = X_weighted.shape

for p in rango_factores:
    nmf = NMF(n_components=p, init='nndsvd', max_iter=2000, random_state=42)
    W_w = nmf.fit_transform(X_weighted)
    H_w = nmf.components_
    
    X_reconstructed = np.dot(W_w, H_w)
    residuals = X_weighted.values - X_reconstructed
    q_true = np.sum(residuals**2)
    q_exp = (n_samples_w * n_features_w) - p * (n_samples_w + n_features_w)
    ratio = q_true / q_exp
    
    q_true_list.append(q_true)
    q_exp_list.append(q_exp)
    ratio_list.append(ratio)
    
    print(f"Factores: {p} | Q_true: {q_true:.0f} | Q_exp: {q_exp} | Ratio: {ratio:.2f}")

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

#%% [5] CÁLCULO DE PMF BASE (ANCLAJE)
n_components = 5 # <--- Ajustado a 5 según el ratio Q/Qexp

nmf_base = NMF(n_components=n_components, init='nndsvd', max_iter=10000, random_state=42)
nmf_base.fit(X_weighted)
H_base_weighted = nmf_base.components_

H_base = H_base_weighted * df_error.mean().values.reshape(1, -1)
for i in range(n_components):
    if H_base[i, :].sum() > 0:
        H_base[i, :] = H_base[i, :] / H_base[i, :].sum()

#%% [6] EJECUCIÓN DE ROLLING PMF Y ALINEACIÓN
window_days = 7
shift_days = 1

start_date = X_weighted.index.min()
end_date = X_weighted.index.max()

W_sum = pd.DataFrame(0.0, index=X_weighted.index, columns=[f'Factor {i+1}' for i in range(n_components)])
W_count = pd.DataFrame(0.0, index=X_weighted.index, columns=[f'Factor {i+1}' for i in range(n_components)])
H_history = [] 

current_start = start_date
print("Iniciando iteraciones de Rolling PMF...")

while current_start + pd.Timedelta(days=window_days) <= end_date:
    current_end = current_start + pd.Timedelta(days=window_days)
    
    X_win = X_weighted.loc[current_start:current_end]
    df_error_win = df_error.loc[current_start:current_end]
    
    if len(X_win.dropna(how='all')) < 100: 
        current_start += pd.Timedelta(days=shift_days)
        continue
        
    nmf_win = NMF(n_components=n_components, init='nndsvda', max_iter=10000, tol=1e-4)
    W_w = nmf_win.fit_transform(X_win)
    H_w = nmf_win.components_
    
    W_un = W_w
    H_un = H_w * df_error_win.mean().values.reshape(1, -1)
    
    for i in range(n_components):
        f_sum = H_un[i, :].sum()
        if f_sum > 0:
            H_un[i, :] = H_un[i, :] / f_sum
            W_un[:, i] = W_un[:, i] * f_sum
            
    aligned_H = np.zeros_like(H_un)
    aligned_W = np.zeros_like(W_un)
    available_indices = list(range(n_components))
    
    for base_idx in range(n_components):
        best_corr = -1
        best_win_idx = -1
        for win_idx in available_indices:
            corr = np.corrcoef(H_base[base_idx], H_un[win_idx])[0, 1]
            if corr > best_corr:
                best_corr = corr
                best_win_idx = win_idx
                
        aligned_H[base_idx] = H_un[best_win_idx]
        aligned_W[:, base_idx] = W_un[:, best_win_idx]
        available_indices.remove(best_win_idx)
        
    win_dates = X_win.index
    W_df_aligned = pd.DataFrame(aligned_W, index=win_dates, columns=W_sum.columns)
    
    W_sum.loc[win_dates] += W_df_aligned
    W_count.loc[win_dates] += 1
    H_history.append(aligned_H)
    
    current_start += pd.Timedelta(days=shift_days)

print("Rolling PMF completado.")
W_rolling_final = W_sum.divide(W_count.replace(0, np.nan)).fillna(0)

#%% [7] VISUALIZACIÓN DINÁMICA (PERFILES Y SERIES GLOBALES)
fig, axes = plt.subplots(n_components, 1, figsize=(14, 2 * n_components), sharex=True)
fig.subplots_adjust(hspace=0.4)
fig.suptitle(f'Rolling PMF: Contribución Temporal (W) - {sitio}', fontsize=14, y=0.92)

for i in range(n_components):
    ax = axes[i]
    ax.plot(W_rolling_final.index, W_rolling_final[f'Factor {i+1}'], color='teal')
    ax.set_title(f'Factor {i+1}')
    ax.set_ylabel('ppb')

plt.show()

H_3D = np.array(H_history) 
fig, axes = plt.subplots(n_components, 1, figsize=(14, 3 * n_components), sharex=True)
fig.subplots_adjust(hspace=0.4)
fig.suptitle(f'Rolling PMF: Mutación Dinámica de Perfiles (H) - {sitio}', fontsize=14, y=0.92)

for i in range(n_components):
    ax = axes[i]
    factor_data = H_3D[:, i, :] 
    ax.boxplot(factor_data, patch_artist=True, boxprops=dict(facecolor='lightblue', color='blue'),
               medianprops=dict(color='red'), showfliers=False)
    ax.set_title(f'Evolución del Perfil Químico - Factor {i+1}')
    ax.set_ylabel('Fracción Másica')
    ax.set_xticks(range(1, len(df.columns) + 1))
    ax.set_xticklabels(df.columns, rotation=90)

plt.show()

#%% [8] VISUALIZACIÓN: CICLOS DIARIOS (DIURNAL PROFILES)
# Corrección: Modificado df_W por W_rolling_final
df_W_hourly = W_rolling_final.copy()
df_W_hourly['Hora'] = df_W_hourly.index.hour

hourly_mean = df_W_hourly.groupby('Hora').mean()
hourly_std = df_W_hourly.groupby('Hora').std()

fig, axes = plt.subplots(n_components, 1, figsize=(10, 2.5 * n_components), sharex=True)
fig.subplots_adjust(hspace=0.3)
fig.suptitle(f'Ciclo Diario de las Fuentes - {sitio}', fontsize=14, y=0.92)

for i in range(n_components):
    ax = axes[i]
    factor_name = f'Factor {i+1}'
    
    ax.plot(hourly_mean.index, hourly_mean[factor_name], color='crimson', lw=2)
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

#%% [9] VISUALIZACIÓN: ÁREAS APILADAS (STACKED AREA CHART)
# Corrección: Modificado df_W por W_rolling_final
fig, ax = plt.subplots(figsize=(14, 6))

ax.stackplot(W_rolling_final.index, W_rolling_final.T, labels=W_rolling_final.columns, alpha=0.8)

ax.set_title(f'Contribución Absoluta Apilada de COVs - {sitio}')
ax.set_ylabel('Concentración Total (ppb)')
ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
ax.margins(x=0)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#%% [10] INTEGRACIÓN CON METEOROLOGÍA
data_polar = W_rolling_final.copy()
data_polar['VelV'] = df_og['VelV']
data_polar['DirV'] = df_og['DirV']

data_polar = data_polar.dropna(subset=['VelV', 'DirV'])

#%% [11] ANÁLISIS ESPACIAL DE FUENTES (CBPF & NWR PARA TODOS LOS FACTORES)
wd_bins = np.arange(0, 361, 22.5) 
ws_bins = np.arange(0, int(data_polar['VelV'].max()) + 2, 1) 
theta, r = np.meshgrid(np.radians(wd_bins), ws_bins)
percentil_critico = 90

grid_res = 100
max_ws = data_polar['VelV'].max()
xi = np.linspace(-max_ws, max_ws, grid_res)
yi = np.linspace(-max_ws, max_ws, grid_res)
X, Y = np.meshgrid(xi, yi)
sigma = 3.0 

R_grid = np.sqrt(X**2 + Y**2)
Theta_grid = np.arctan2(-X, -Y)
Theta_grid[Theta_grid < 0] += 2 * np.pi

u_wind = (-data_polar['VelV'] * np.sin(np.radians(data_polar['DirV']))).values
v_wind = (-data_polar['VelV'] * np.cos(np.radians(data_polar['DirV']))).values
idx_x = np.digitize(u_wind, xi) - 1
idx_y = np.digitize(v_wind, yi) - 1

n_total, _, _ = np.histogram2d(data_polar['DirV'], data_polar['VelV'], bins=[wd_bins, ws_bins])

for factor_idx in range(n_components):
    factor_target = f'Factor {factor_idx + 1}'
    print(f"Procesando análisis espacial para: {factor_target}...")
    
    # === CÁLCULO CBPF ===
    umbral_x = np.percentile(data_polar[factor_target].dropna(), percentil_critico)
    mask_exceso = data_polar[factor_target] > umbral_x
    m_exceso, _, _ = np.histogram2d(data_polar.loc[mask_exceso, 'DirV'], 
                                    data_polar.loc[mask_exceso, 'VelV'], 
                                    bins=[wd_bins, ws_bins])
    
    with np.errstate(divide='ignore', invalid='ignore'):
        cbpf_matrix = np.divide(m_exceso, n_total)
        cbpf_matrix[n_total < 2] = np.nan
        
    # === CÁLCULO NWR ===
    C_matrix = np.zeros((grid_res, grid_res))
    W_matrix = np.zeros((grid_res, grid_res))
    
    factor_array = data_polar[factor_target].values
    
    for i in range(len(data_polar)):
        if 0 <= idx_x[i] < grid_res and 0 <= idx_y[i] < grid_res:
            if not np.isnan(factor_array[i]): 
                C_matrix[idx_y[i], idx_x[i]] += factor_array[i]
                W_matrix[idx_y[i], idx_x[i]] += 1
                
    with np.errstate(divide='ignore', invalid='ignore'):
        Raw_Field = np.divide(C_matrix, W_matrix)
        Raw_Field[W_matrix == 0] = 0
        
    NWR_Smoothed = gaussian_filter(Raw_Field, sigma=sigma)
    NWR_Smoothed[R_grid > max_ws] = np.nan

    # === VISUALIZACIÓN ===
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), subplot_kw=dict(projection='polar'))
    
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction(-1)
    c1 = ax1.pcolormesh(theta, r, cbpf_matrix.T, cmap='YlOrRd', shading='auto')
    ax1.set_title(f'CBPF - Probabilidad > P{percentil_critico}', pad=15)
    plt.colorbar(c1, ax=ax1, label='Probabilidad (0-1)', pad=0.1, shrink=0.7)
    
    ax2.set_theta_zero_location('N')
    ax2.set_theta_direction(-1)
    contour = ax2.contourf(Theta_grid, R_grid, NWR_Smoothed, levels=20, cmap='inferno')
    ax2.set_title(f'NWR - Concentración Espacial', pad=15)
    plt.colorbar(contour, ax=ax2, label='Concentración Suavizada (ppb)', pad=0.1, shrink=0.7)
    
    plt.suptitle(f'Rosa de Contaminación Bivariada - {factor_target}', fontsize=16)
    plt.tight_layout()
    plt.show()