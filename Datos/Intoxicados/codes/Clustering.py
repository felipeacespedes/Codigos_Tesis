# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 19:50:09 2025

@author: felip
"""

#%% Imports
import os
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches 
from matplotlib.colors import BoundaryNorm
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
import seaborn as sns
import math

# ACE_functs
import ACE_functs as ace


# path para guardar figuras
path_fig = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 2/Clusters/'

#%% 1. Load and restrict to intoxication days
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
DF_d = pd.read_csv(path+'DF_dhma_ContMean.csv', index_col='date', parse_dates=True)
d1 = pd.to_datetime('2022-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
DF_d = DF_d.loc[d1:d2]
DF_d['fcpmr_CQ'] = DF_d['MP25_CQ']/DF_d['MP10_CQ'] 

# Keep only intoxication days (T59 > 0)
# df = DF_d[DF_d["T59"] > 0].copy()
df = DF_d
mask = df['Comuna'] == 'Puchuncaví'
df.loc[mask,'T59'] = 0
df.loc[mask,'Comuna'] = float('nan') 
mask = df['T59']>0
print(f"Usamos {len(df.loc[mask])} días con intoxicados de un total "+
      f"de {len(df)} días")


# Feature set
# cols = [
#         'ies_princ',
#         'blh_era5',
#         # 't_dmc',
#         'hr_dmc',
#         # 'r_dmc',
#         # 'slp_dmc',
#         # 'slp_dmc_diff',

#         'ws_dmc',
#         'u_princ',
#         'v_CC',
    
#         'HCNM_CQ',
#         # 'CO_CQ',
#         'SO2_CQ',
#         'NO2_CQ',
#         # 'NO_CQ',
#         # 'NOx_CQ',
#         'O3_CQ',
#         'MP25_CQ',
#         'MP10_CQ',

#         ]

# 4 Clusters:
cols = [
        'ies_princ',
        'blh_era5',
        'ws_dmc',

    
        'HCNM_CQ',
        'SO2_CQ',
        'MP25_CQ'
        
        ]

# 5 cluster: HCNM, SO2, O3-WN, Baja Cost. y  Baja Variabilidad
# cols = [
#         'ies_princ',
#         'blh_era5',
#         # 'hr_dmc',
        
#         # 'r_dmc',
#         't_dmc',

#         'ws_dmc',
#         'u_princ',
#         'v_CC',
    
#         'HCNM_CQ',
#         'SO2_CQ',
#         'NO_CQ',
#         'NO2_CQ',
#         # 'O3_CQ',
#         'MP25_CQ',
#         'MP10_CQ',
        
#         # 'CO_CQ'
    
#         ]

var_t = 'T59'  # target variable (can change to T59 if needed)
features = df[cols]
target = df[var_t]

# Visualize features distributions
title='Histogramas de anomalías diarias con datos de 5 a 11 am'
ax = features.hist(bins=15,figsize=(10,7))
fig = ax.flatten()[0].figure
fig.suptitle(title)
plt.tight_layout()
# plt.savefig(path_fig+'Hist_features.png', dpi=300)

#%% 2. Handle NaNs (imputation)
imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(features)

# %% 3. Standardize
# scaler = StandardScaler()
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X_imputed)

#%% 4. Determine best k (elbow + silhouette)
inertia = []
sil_scores = []
K_range = range(2, 15)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=50, n_init=100)
    labels = kmeans.fit_predict(X_scaled)
    inertia.append(kmeans.inertia_)
    sil_scores.append(silhouette_score(X_scaled, labels))

plt.figure(figsize=(11,5))

plt.subplot(1,2,1)
plt.plot(K_range, inertia, "o-")
plt.xlabel("Número de clusters k")
plt.ylabel("Inercia (WCSS)")
plt.ylim(1000,6000)
plt.vlines(4,15000,0,colors='r',linestyles='--')
plt.title("Método del codo")
plt.grid(alpha=0.5)

plt.subplot(1,2,2)
plt.plot(K_range, sil_scores, "o-")
plt.xlabel("Número de clusters k")
plt.ylabel("Score de silueta")
plt.title("Método de la silueta")
plt.grid(alpha=0.5)

plt.tight_layout()
# plt.savefig(path_fig+'Metodos_Codo-Silueta.png', dpi=300)

#%% 5. Final clustering
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=80, n_init=10000)
clusters = kmeans.fit_predict(X_scaled)
df["Cluster"] = clusters

# Crear DataFrame con estadísticas
resumen_clusters = pd.DataFrame({
    "Total T59": df.groupby("Cluster")["T59"].sum(),
    "Dias cluster": df.groupby("Cluster").size(),
    "Media T59": df.groupby("Cluster")["T59"].mean().round(2),
    "Mediana T59": df.groupby("Cluster")["T59"].median(),
    "Dias T59": df.groupby("Cluster")["T59"].apply(lambda x: (x > 0).sum()),
    
})

# Añadir número medio de intoxicados por evento
resumen_clusters["T59 medio"] = (
    resumen_clusters["Total T59"] / resumen_clusters["Dias T59"]).round(2)

# Guardamos
# resumen_clusters.to_csv(path+'resumen_clusters.csv')

print("==================== Resumen de intoxicaciones por cluster ====================")
print(resumen_clusters)

# Guardamos fechas
cluster_dates = {}
for cl in sorted(df["Cluster"].unique()):
    dates = df.loc[df["Cluster"] == cl].index
    cluster_dates[cl] = dates
    
# PCA
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_scaled)
df["PC1"] = X_pca[:,0]
df["PC2"] = X_pca[:,1]
df["PC3"] = X_pca[:,2]


#%% 6. Visualize PCA space

# Explained variance for nicer axis labels
evr = pca.explained_variance_ratio_
pc1_lbl = f"PC1 ({evr[0]*100:.1f}%)"
pc2_lbl = f"PC2 ({evr[1]*100:.1f}%)"
pc3_lbl = f"PC3 ({evr[2]*100:.1f}%)"

levels = list(range(n_clusters+1))
norm = BoundaryNorm(levels, len(levels)-1)
plt.figure(figsize=(9,7))
sc1 = plt.scatter(df["PC1"], df["PC2"],s=20,c=df["Cluster"], cmap='tab10',
                  alpha=0.7,norm=norm)
cb1 = plt.colorbar(sc1, label="Cluster",fraction=0.05)
current_ticks = cb1.get_ticks()
new_ticks = current_ticks + (current_ticks[1] - current_ticks[0]) / 2
cb1.set_ticks(new_ticks[0:n_clusters])
cb1.set_ticklabels(levels[0:n_clusters])

plt.xlabel(pc1_lbl)
plt.ylabel(pc2_lbl)
plt.grid(alpha=0.5)
plt.title(f"Clustering de días en espacio PCA (k={n_clusters})")
plt.tight_layout()
# plt.savefig(path_fig+'PCA_2d.png', dpi=300)


#%% 7. Visualize PCA space in 3D

# Project cluster centroids into PCA space
centroids_pca = pca.transform(kmeans.cluster_centers_)

fig = plt.figure(figsize=(9,7))
ax = fig.add_subplot(111, projection='3d')

# Choose a categorical colormap with enough distinct colors
cmap = 'tab10'
levels = list(range(n_clusters+1))
norm = BoundaryNorm(levels, len(levels)-1)

sc = ax.scatter(
    df["PC1"], df["PC2"], df["PC3"],norm=norm,
    c=df["Cluster"], cmap=cmap, s=20, alpha=0.5, depthshade=True
)

# Overlay centroids
ax.scatter(
    centroids_pca[:, 0], centroids_pca[:, 1], centroids_pca[:, 2],
    c=np.arange(n_clusters), cmap=cmap, s=140, marker='X', edgecolor='k', linewidth=1.0,
    label="Centroides",norm=norm,
)

# Pretty axes
ax.set_xlabel(pc1_lbl)
ax.set_ylabel(pc2_lbl)
ax.set_zlabel(pc3_lbl)
ax.view_init(elev=30, azim=50)  

# Colorbar labeled with cluster IDs
cbar = plt.colorbar(sc, ax=ax, pad=0.02, shrink=0.8)
current_ticks = cbar.get_ticks()
new_ticks = current_ticks + (current_ticks[1] - current_ticks[0]) / 2
cbar.set_ticks(new_ticks[0:n_clusters])
cbar.set_ticklabels(levels[0:n_clusters])

# Optional: add a small legend entry for centroids
ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98))

plt.title(f"Clustering de días en espacio PCA (k={n_clusters})")
plt.tight_layout()
plt.show()



#%% 6bis. Visualize PCA space with variable loadings (biplot estilo químico)

# from matplotlib.patches import FancyArrowPatch

# 1) Reusamos el PCA ya calculado
# (si no lo tienes en memoria, asegúrate de haber corrido el bloque anterior)
# pca, X_scaled, df, features, n_clusters deben existir

# 2) Obtenemos los "loadings" = pesos de cada variable en cada componente
loadings = pca.components_.T  # shape: (n_variables, n_components)
vars_names = features.columns

# 3) Escala para hacer visibles las flechas en el mismo plano que los puntos
#    (ajustamos longitud de los vectores)
scale_factor = 9  # puedes ajustar este número según dispersión de puntos

# 4) Graficamos
fig, ax = plt.subplots(figsize=(6,5))
levels = list(range(n_clusters+1))
norm = BoundaryNorm(levels, len(levels)-1)

# puntos de cada día coloreados por cluster
sc = ax.scatter(df["PC1"], df["PC2"],c=df["Cluster"], cmap='tab10',
                 s=25, alpha=0.6, norm=norm,edgecolor='k', linewidth=0.08)

# Centroides proyectados al espacio PCA (opcional, como en tu 3D previo)
centroids_pca = pca.transform(kmeans.cluster_centers_)
ax.scatter(
    centroids_pca[:, 0], centroids_pca[:, 1],
    c=np.arange(n_clusters), cmap='tab10', norm=norm,s=200, marker='X',
     edgecolor='k', linewidth=1.0, label="Centroides",zorder=2, alpha=0.7)


# flechas para variables (loadings)
for i, var in enumerate(vars_names):
    d = 0.3 if var == 'MP25_CQ' else 0
    x_vec = loadings[i, 0] * scale_factor
    y_vec = loadings[i, 1] * scale_factor
    ax.arrow(0, 0, x_vec, y_vec, color='k', alpha=0.7, width=0.005,
              head_width=0.08, length_includes_head=True,zorder=3)
    ax.text(x_vec*1.12, y_vec*1.12+d, var, color='k', fontsize=9, fontweight='bold',
            ha='center', va='center',zorder=3)

# ejes y etiquetas
evr = pca.explained_variance_ratio_
ax.set_xlabel(f"PC1 ({evr[0]*100:.1f}%)")
ax.set_ylabel(f"PC2 ({evr[1]*100:.1f}%)")
ax.axhline(0, color='gray', lw=1,alpha=0.5)
ax.axvline(0, color='gray', lw=1,alpha=0.5)
ax.set_title(f"Clustering de días en espacio PCA (k={n_clusters})")
ax.grid(alpha=0.4)

# colorbar de clusters
cb = plt.colorbar(sc, ax=ax, pad=0.03, fraction=0.05)
cb.set_label("Cluster",labelpad=8)
current_ticks = cb.get_ticks()
new_ticks = current_ticks + (current_ticks[1] - current_ticks[0]) / 2
cb.set_ticks(new_ticks[0:n_clusters])
cb.set_ticklabels(levels[0:n_clusters])

plt.tight_layout()
# plt.savefig(path_fig+'PCA_2d.png', dpi=300)
# plt.savefig(path_fig[:31]+'Simposio_CR2/figs/PCA_2d.png', dpi=300)


#%% 7bis. Biplot PCA 3D con vectores de variables (loadings)

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# Asegúrate de haber corrido antes el PCA de 3 componentes y tener PC1/PC2/PC3 en df
# pca, df["PC1"], df["PC2"], df["PC3"], kmeans, n_clusters, features deben existir

# Loadings: pesos de cada variable en cada componente (PC1, PC2, PC3)
loadings_3d = pca.components_.T[:, :3]        # shape: (n_vars, 3)
vars_names  = features.columns

# Escala para las flechas: la ajustamos a la nube de puntos para que se vean bien
# (puedes cambiar el percentil o el factor si quieres flechas más largas/cortas)
pc_points = df[["PC1", "PC2", "PC3"]].values
cloud_scale = np.percentile(np.linalg.norm(pc_points, axis=1), 85)
scale_factor = 4 * cloud_scale

# Centroides proyectados al espacio PCA (opcional, como en tu 3D previo)
centroids_pca = pca.transform(kmeans.cluster_centers_)

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

# Colores por cluster
cmap = 'tab10'
levels = list(range(n_clusters+1))
norm = BoundaryNorm(levels, len(levels)-1)

# Dispersión de puntos
sc = ax.scatter(
    df["PC1"], df["PC2"], df["PC3"],
    c=df["Cluster"], cmap=cmap, norm=norm,
    s=10, alpha=0.35, depthshade=True,
    #edgecolor='k', linewidth=0.08,
)

# Centroides
ax.scatter(
    centroids_pca[:, 0], centroids_pca[:, 1], centroids_pca[:, 2],
    c=np.arange(n_clusters), cmap=cmap, norm=norm,
    s=350, marker='X', edgecolor='k', linewidth=1.5, 
    label="Centroides", alpha=1
)

# Vectores de variables (flechas rojas) desde el origen
for i, var in enumerate(vars_names):
    vx, vy, vz = (loadings_3d[i, :] * scale_factor)
    d = 0.3 if var == 'MP25_CQ' else 0
    ax.quiver(0, 0, 0, vx, vy, vz,arrow_length_ratio=0.08,
               color='k', linewidth=1.4, alpha=0.85,zorder=2)
    # etiqueta un poco más allá de la punta
    ax.text(vx*1.08, vy*1.08, (vz*1.08)+d, var, color='k', ha='center',
            va='center',fontsize=10, fontweight='bold')

# Etiquetas de ejes con varianza explicada
evr = pca.explained_variance_ratio_
ax.set_xlabel(f"PC1 ({evr[0]*100:.1f}%)")
ax.set_ylabel(f"PC2 ({evr[1]*100:.1f}%)")
ax.set_zlabel(f"PC3 ({evr[2]*100:.1f}%)")

# Vista y estética
ax.view_init(elev=50, azim=220)   # ajusta si quieres otro ángulo
ax.grid(True, alpha=0.3)

# Colorbar de clusters con ticks centrados como en tus bloques
cbar = plt.colorbar(sc, ax=ax, pad=0.05, shrink=0.8, fraction=0.1)
current_ticks = cbar.get_ticks()
if len(current_ticks) >= 2:
    new_ticks = current_ticks + (current_ticks[1] - current_ticks[0]) / 2
    cbar.set_ticks(new_ticks[0:n_clusters])
    cbar.set_ticklabels(levels[0:n_clusters])
else:
    cbar.set_ticks(range(n_clusters))
    cbar.set_ticklabels(levels[0:n_clusters])
cbar.set_label("Cluster")

# Leyenda para centroides
ax.legend(loc="upper left", bbox_to_anchor=(-0.08, 0.98),prop={'size': 16})

plt.title(f"Clustering de días en espacio PCA (k={n_clusters})")
plt.tight_layout()
# plt.savefig(path_fig+'PCA_3d.png', dpi=300)



#%% 8. Cluster profiles
cluster_profiles = pd.DataFrame(X_scaled, columns=features.columns)
cluster_profiles["Cluster"] = clusters
cluster_mean = cluster_profiles.groupby("Cluster").mean()

vmin = cluster_mean.min().min()
vmax = cluster_mean.max().max()
if np.abs(vmin)>np.abs(vmax):
    val = np.abs(vmin)
else:
    val = np.abs(vmax)

plt.figure(figsize=(10,8))
sns.heatmap(cluster_mean.T, cmap="coolwarm", annot=True, fmt=".2f",
            annot_kws={"color": "black","fontsize":12}, 
            cbar_kws={'label': 'Desviación (IQR)','fraction':0.05},
            cbar=True, vmin=-val, vmax=val)
plt.title("Perfiles por cluster")
plt.xlabel("Cluster")
plt.ylabel("Variable")
plt.tight_layout(pad=1.3)
plt.savefig(path_fig+'Perfiles.png', dpi=300)


#%% 9. Variable importance per cluster
cluster_mean = cluster_profiles.groupby("Cluster").mean()
global_mean = cluster_profiles.drop(columns="Cluster").mean()

for cl in cluster_mean.index:
    diffs = cluster_mean.loc[cl] - global_mean
    diffs_sorted = diffs.abs().sort_values(ascending=False)
    values = diffs[diffs_sorted.index]

    plt.figure(figsize=(10,6))
    values.plot(kind="bar", color=np.where(values > 0, "tab:red", "tab:blue"))
    plt.title(f"Cluster {cl}: Desviación desde mediana global")
    plt.ylabel("Desviación (IQR)")
    plt.xlabel("Variable")
    plt.xticks(rotation=45,fontweight='bold')
    plt.grid(alpha=0.5)
    plt.tight_layout()
    
    
##############################################    
##############################################
#%%# 10-11. Analisis Centrado en Eventos  ####

# Definimos variables
cols = [
        'HCNM_CQ','NO_CQ','NO2_CQ','O3_CQ',
        'SO2_CQ','MP25_CQ','MP10_CQ','CO_CQ',
        
        'ies_princ','blh_era5','hr_dmc','r_dmc',
        'ws_dmc','u_dmc','v_dmc','slp_dmc',
        'slp_dmc_diff','u_princ','v_CC','t_dmc',
        ]


# Opción de usar DF de datos diarios para valores diarios
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
DF = pd.read_csv(path+'DF_d.csv', index_col='date', parse_dates=True)
d1 = pd.to_datetime('2022-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
DF = DF.loc[d1:d2]
# DF = df.copy()

# Importamos DF datos horarios para ciclos diarios
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
DF_h = pd.read_csv(path+'DF_h.csv', index_col='date', parse_dates=True)
d1 = pd.to_datetime('2022-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
DF_h = DF_h.loc[d1:d2]

##################################################################################
#%% 10: ACE ±5 días valores diarios originales o anomalía, opción std. robusto ###

## Opción para Estandarizar Robusto (usado al separar clusters) ##
std_R = False

# En caso de querer variables con estandarizado robusto (las que crean clusters)
if std_R == True:
    
    # 1) Copia y estandarización robusta
    DF_d_std = DF.copy()

    # Solo transformamos las columnas de interés (cols)
    _features = DF_d_std[cols].copy()

    # Imputación por mediana (si alguna columna es TODO NaN, su mediana es NaN; 
    # rellenamos remanentes con 0 como fallback)
    _features = _features.apply(lambda s: s.fillna(s.median()))
    _features = _features.fillna(0)  # fallback por si quedan NaNs (e.g., columnas completamente vacías)

    # Estandarizador robusto
    _scaler = RobustScaler(quantile_range=(25.0, 75.0))
    _features_scaled = _scaler.fit_transform(_features)

    # Volvemos a DataFrame con mismos índices/columnas
    DF_d_std.loc[:, cols] = pd.DataFrame(_features_scaled,
                                         index=_features.index, 
                                         columns=_features.columns)
    
    # Adjudicamos DF_d_std a DF_bis
    DF_bis = DF_d_std
else:
    DF_bis = DF.copy()
    

# Ploteamos
for cl in range(n_clusters):
    # Días del cluster (todos) y días del cluster con evento (T59>0)
    dates_cl = df.loc[df["Cluster"] == cl].index
    dates_cl_evento = df.loc[(df["Cluster"] == cl) & (df["T59"] > 0)].index

    window = 5
    lags = range(-window, window+1)

    fig, axes = plt.subplots(4, 5, figsize=(15,8), sharex=True)
    axes = axes.flatten(order='F')

    for i, var in enumerate(DF_bis[cols].columns.values):
        if var == 'slp_dmc_diff':
            axes[i].axis('off')
            continue
        # --- ventanas centradas en todos los días del cluster ---
        data_windows_all = []
        for d in dates_cl:
            win = DF_bis.loc[d - pd.Timedelta(days=window): d + pd.Timedelta(days=window), var]
            if len(win) == 2*window+1:
                data_windows_all.append(win.values)

        # --- ventanas centradas solo en días con evento ---
        data_windows_evt = []
        for d in dates_cl_evento:
            win = DF_bis.loc[d - pd.Timedelta(days=window): d + pd.Timedelta(days=window), var]
            if len(win) == 2*window+1:
                data_windows_evt.append(win.values)

        if not data_windows_all:
            continue

        arr_all = np.array(data_windows_all)
        mean_all   = np.nanmean(arr_all, axis=0)
        median_all = np.nanmedian(arr_all, axis=0)
        p25_all    = np.nanpercentile(arr_all, 25, axis=0)
        p75_all    = np.nanpercentile(arr_all, 75, axis=0)

        ax = axes[i]

        # --- TODOS LOS DÍAS del cluster (alpha=0.5) ---
        ax.plot(lags, mean_all, "--",   label="Media cluster",   color="tab:blue", alpha=0.4,linewidth=0.8)
        ax.plot(lags, median_all, label="Mediana cluster", color="tab:blue", alpha=0.6,linewidth=1.2)
        ax.fill_between(lags, p25_all, p75_all, color="tab:blue", alpha=0.08, label="P25–P75 cluster")

        # --- SOLO EVENTOS (T59>0): línea destacada con la mediana ---
        if data_windows_evt:
            arr_evt = np.array(data_windows_evt)
            mean_evt = np.nanmean(arr_evt, axis=0)
            median_evt = np.nanmedian(arr_evt, axis=0)
            p25_evt    = np.nanpercentile(arr_evt, 25, axis=0)
            p75_evt    = np.nanpercentile(arr_evt, 75, axis=0)
            ax.plot(lags, mean_evt, "--", label="Media eventos", color="tab:orange", linewidth=1.2, alpha=0.8)
            ax.plot(lags, median_evt, label="Mediana eventos", color="tab:orange", linewidth=1.8,alpha=0.95)
            ax.fill_between(lags, p25_evt, p75_evt, color="tab:orange", alpha=0.15, label="P25–P75 eventos")


        ax.axvline(0, color="k", linestyle=":", alpha=0.7)
        ax.set_ylabel(var, fontweight="bold", fontsize=12)
        ax.grid(alpha=0.2)

        # Solo añadimos la leyenda una vez
        if i == 0:
            # Leyenda afuera, parte superior derecha
            fig.legend(
                loc="upper left",
                # bbox_to_anchor=(0.87, 0.9),
                bbox_to_anchor=(0.85, 0.93),
                borderaxespad=0.,
                frameon=False
            )
            
    # 1. Definimos las POSICIONES para TODAS las marcas y líneas de grid.
    ticks_posiciones = range(-window, window + 1) # -> [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    
    # 2. Creamos las ETIQUETAS: el número si es par, o un texto vacío si es impar.
    ticks_etiquetas = [str(n) if n % 5 == 0 else '' for n in ticks_posiciones]
    # -> ['', '-4', '', '-2', '', '0', '', '2', '', '4', '']
    
    # 3. Aplicamos ambas configuraciones a todos los ejes.
    for ax in axes:
        if ax.get_visible():
            # Primero le decimos dónde poner TODAS las marcas.
            ax.set_xticks(ticks_posiciones)
            # Luego le decimos qué ETIQUETA poner en cada una de esas marcas.
            ax.set_xticklabels(ticks_etiquetas)
            
    if std_R == True:
        fig.suptitle(f"±{window} días - Cluster {cl} (robusto estandarizado)", fontsize=16, y=0.986)
    else:
        fig.suptitle(f"±{window} días - Cluster {cl}", fontsize=16, y=0.986)
    
    plt.tight_layout()#rect=[0, 0, 0.85, 1])  # dejar espacio a la derecha para la leyenda
            

    # Because you used flatten(order='F'), the indices of the axes are:
    # HCNM_CQ: 0, SO2_CQ: 4, MP25_CQ: 5, ies_princ: 8, blh_era5: 9, ws_dmc: 12
    
    # Get the bounding boxes of the key subplots in figure coordinates (from 0 to 1)
    bbox0 = axes[0].get_position()
    bbox4 = axes[4].get_position()
    bbox5 = axes[5].get_position()
    bbox9 = axes[9].get_position()
    bbox12 = axes[12].get_position()
    
    # Define the vertices of the polygon that will enclose the subplots
    
    vertices = [
        (bbox0.x0-0.049, bbox0.y1+0.015),     # Top-left of HCNM_CQ
        (bbox12.x1+0.01, bbox12.y1+0.015),    # Top-right of ws_dmc
        (bbox12.x1+0.01, bbox12.y0-0.015),    # Bottom-right of ws_dmc
        (bbox9.x1+0.01 , bbox9.y1+0.0132),    # Top-right of blh_era5
        (bbox9.x1+0.01 , bbox9.y0-0.015),     # Bottom-right of blh_era5
        (bbox5.x0-0.04 , bbox5.y0-0.015),     # Bottom-left of MP25_CQ
        (bbox5.x0-0.04 , bbox5.y1+0.0132),    # Top-left of MP25_CQ
        (bbox0.x0-0.049, bbox0.y0-0.015),     # Bottom-left of HCNM_CQ
    ]
    
    # Create the polygon patch
    highlighter = patches.Polygon(
        vertices,
        edgecolor='grey',
        facecolor='none', # No fill
        linestyle='--',
        linewidth=2,
        alpha=0.5,
        closed=True,
        transform=fig.transFigure, # Use figure coordinates
        clip_on=False # Allow drawing outside of axes area
    )
    
    # Add the patch to the figure
    fig.add_artist(highlighter)
    
    # Guardamos
    fig.savefig(path_fig+f'ACE/ValorDiario/VD_Cl{cl}.png', dpi=300)

    
################################################################
#%% 11.1: Ciclos de 72h (n-1, n, n+1) a partir de DF horario ###

# Plot por cluster
for cl in range(n_clusters):
    dates_cl = df.loc[df["Cluster"]==cl].index
    dates_evt = df.loc[(df["Cluster"]==cl) & (df["T59"]>0)].index
    
    fig, axes = plt.subplots(4,5,figsize=(15,8), sharex=True)
    axes = axes.flatten(order='F')
    x = np.arange(72)  # horas: 0..71
    
    for i,var in enumerate(cols):
        if var == 'slp_dmc_diff':
            axes[i].axis('off')
            continue
        ax = axes[i]
        stats_all = ace.aggregate_72h(DF_h, dates_cl, var)
        stats_evt = ace.aggregate_72h(DF_h, dates_evt, var) if len(dates_evt)>0 else None
        
        if stats_all:
            ax.plot(x, stats_all['mean'], "--", color="tab:blue", alpha=0.4, lw=0.8, label="Media cluster")
            ax.plot(x, stats_all['median'], color="tab:blue", alpha=0.6, lw=1.2, label="Mediana cluster")
            ax.fill_between(x, stats_all['p25'], stats_all['p75'], color="tab:blue", alpha=0.08,label="P25–P75 cluster")
        if stats_evt:
            ax.plot(x, stats_evt['mean'], "--", color="tab:orange", alpha=0.8, lw=1.2, label="Media eventos")
            ax.plot(x, stats_evt['median'], color="tab:orange", alpha=0.95, lw=1.8, label="Mediana eventos")
            ax.fill_between(x, stats_evt['p25'], stats_evt['p75'], color="tab:orange", alpha=0.15,label="P25–P75 eventos")
        
        # Líneas divisorias entre días (24h,48h)
        ax.axvline(24, color="k", ls=":", alpha=0.6)
        ax.axvline(48, color="k", ls=":", alpha=0.6)
        ax.set_xlim(0,71)
        ax.set_xticks([0,12,24,36,48,60,71])
        ax.set_xticklabels([-24,-12,0,12,24,36,47])
        ax.set_ylabel(var, fontweight="bold", fontsize=12)
        ax.grid(alpha=0.2)
        
        if i==0:
            fig.legend(loc="upper left", bbox_to_anchor=(0.85,0.93), 
                       frameon=False,borderaxespad=0.)
    
    fig.suptitle(f"Ciclo diario [n-1 , n , n+1] — Cluster {cl}", fontsize=16, y=0.986)
    plt.tight_layout(w_pad=0.4)#rect=[0,0,0.91,1])
            
    # =========================================================================
    # START: NEW CODE TO DRAW THE HIGHLIGHTING SHAPE
    # =========================================================================
    # Because you used flatten(order='F'), the indices of the axes are:
    # HCNM_CQ: 0, SO2_CQ: 4, MP25_CQ: 5, ies_princ: 8, blh_era5: 9, ws_dmc: 12
    
    # Get the bounding boxes of the key subplots in figure coordinates (from 0 to 1)
    bbox0 = axes[0].get_position()
    bbox4 = axes[4].get_position()
    bbox5 = axes[5].get_position()
    bbox9 = axes[9].get_position()
    bbox12 = axes[12].get_position()
    
    # Define the vertices of the polygon that will enclose the subplots
    
    vertices = [
        (bbox0.x0-0.045, bbox0.y1+0.015),     # Top-left of HCNM_CQ
        (bbox12.x1+0.01, bbox12.y1+0.015),    # Top-right of ws_dmc
        (bbox12.x1+0.01, bbox12.y0-0.015),    # Bottom-right of ws_dmc
        (bbox9.x1+0.01 , bbox9.y1+0.0133),    # Top-right of blh_era5
        (bbox9.x1+0.01 , bbox9.y0-0.015),     # Bottom-right of blh_era5
        (bbox5.x0-0.04 , bbox5.y0-0.015),     # Bottom-left of MP25_CQ
        (bbox5.x0-0.04 , bbox5.y1+0.0133),    # Top-left of MP25_CQ
        (bbox0.x0-0.045, bbox0.y0-0.015),     # Bottom-left of HCNM_CQ
    ]
    
    # Create the polygon patch
    highlighter = patches.Polygon(
        vertices,
        edgecolor='grey',
        facecolor='none', # No fill
        linestyle='--',
        linewidth=2,
        alpha=0.5,
        closed=True,
        transform=fig.transFigure, # Use figure coordinates
        clip_on=False # Allow drawing outside of axes area
    )
    
    # Add the patch to the figure
    fig.add_artist(highlighter)
    
    # Guardamos
    fig.savefig(path_fig+f'ACE/CicloDiario/CD_Cl{cl}.png', dpi=300)
    
    
######################################
######################################
#%%##### Figuras Simposio CR2 ########
######################################


# Definimos variables
cols = [
        'HCNM_CQ','MP25_CQ',
        'ies_princ','ws_dmc',
        # 'slp_dmc',
        ]


# Opción de usar DF de datos diarios para valores diarios
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
DF = pd.read_csv(path+'DF_d.csv', index_col='date', parse_dates=True)
d1 = pd.to_datetime('2022-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
DF = DF.loc[d1:d2]
# DF = df.copy()

# Importamos DF datos horarios para ciclos diarios
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
DF_h = pd.read_csv(path+'DF_h.csv', index_col='date', parse_dates=True)
d1 = pd.to_datetime('2022-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
DF_h = DF_h.loc[d1:d2]
    
#####################################    
#%% 10: datos anomalía/originales ###

DF_bis = DF.copy()    

# Ploteamos
for cl in range(n_clusters):
    # Días del cluster (todos) y días del cluster con evento (T59>0)
    dates_cl = df.loc[df["Cluster"] == cl].index
    dates_cl_evento = df.loc[(df["Cluster"] == cl) & (df["T59"] > 0)].index

    window = 5
    lags = range(-window, window+1)

    fig, axes = plt.subplots(4, 1, figsize=(5,7), sharex=True)
    axes = axes.flatten(order='F')

    for i, var in enumerate(DF_bis[cols].columns.values):

        # --- ventanas centradas en todos los días del cluster ---
        data_windows_all = []
        for d in dates_cl:
            win = DF_bis.loc[d - pd.Timedelta(days=window): d + pd.Timedelta(days=window), var]
            if len(win) == 2*window+1:
                data_windows_all.append(win.values)

        # --- ventanas centradas solo en días con evento ---
        data_windows_evt = []
        for d in dates_cl_evento:
            win = DF_bis.loc[d - pd.Timedelta(days=window): d + pd.Timedelta(days=window), var]
            if len(win) == 2*window+1:
                data_windows_evt.append(win.values)

        if not data_windows_all:
            continue

        arr_all = np.array(data_windows_all)
        mean_all   = np.nanmean(arr_all, axis=0)
        median_all = np.nanmedian(arr_all, axis=0)
        p25_all    = np.nanpercentile(arr_all, 25, axis=0)
        p75_all    = np.nanpercentile(arr_all, 75, axis=0)

        ax = axes[i]

        # --- TODOS LOS DÍAS del cluster (alpha=0.5) ---
        ax.plot(lags, mean_all, "--",   label="Media cluster",   color="tab:blue", alpha=0.4,linewidth=0.8)
        ax.plot(lags, median_all, label="Mediana cluster", color="tab:blue", alpha=0.6,linewidth=1.2)
        ax.fill_between(lags, p25_all, p75_all, color="tab:blue", alpha=0.08, label="P25–P75 cluster")
        ## Percentil 95
        # if var in ['HCNM_CQ','MP25_CQ']:
        #     p95_all    = np.nanpercentile(arr_all, 95, axis=0)
        #     ax.plot(lags, p95_all, ":",   label="P95 cluster",   color="tab:blue", alpha=0.4,linewidth=0.8)

        # --- SOLO EVENTOS (T59>0): línea destacada con la mediana ---
        if data_windows_evt:
            arr_evt = np.array(data_windows_evt)
            mean_evt = np.nanmean(arr_evt, axis=0)
            median_evt = np.nanmedian(arr_evt, axis=0)
            p25_evt    = np.nanpercentile(arr_evt, 25, axis=0)
            p75_evt    = np.nanpercentile(arr_evt, 75, axis=0)
            
            ax.plot(lags, mean_evt, "--", label="Media eventos", color="tab:orange", linewidth=1.2, alpha=0.8)
            ax.plot(lags, median_evt, label="Mediana eventos", color="tab:orange", linewidth=1.8,alpha=0.95)
            ax.fill_between(lags, p25_evt, p75_evt, color="tab:orange", alpha=0.15, label="P25–P75 eventos")
            ## Percentil 95
            # if var in ['HCNM_CQ','MP25_CQ']:
            #     p95_evt = np.nanpercentile(arr_evt, 95, axis=0)
            #     ax.plot(lags, p95_evt, ":", label="P95 eventos", color="tab:orange", linewidth=1.2, alpha=0.8)


        ax.axvline(0, color="k", linestyle=":", alpha=0.7)
        ax.set_ylabel(var, fontweight="bold", fontsize=12)
        ax.grid(alpha=0.2)
            
    # 1. Definimos las POSICIONES para TODAS las marcas y líneas de grid.
    ticks_posiciones = range(-window, window + 1) # -> [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    
    # 2. Creamos las ETIQUETAS: el número si es par, o un texto vacío si es impar.
    ticks_etiquetas = [str(n) if n % 5 == 0 else '' for n in ticks_posiciones]
    # -> ['', '-4', '', '-2', '', '0', '', '2', '', '4', '']
    
    # 3. Aplicamos ambas configuraciones a todos los ejes.
    for ax in axes:
        if ax.get_visible():
            # Primero le decimos dónde poner TODAS las marcas.
            ax.set_xticks(ticks_posiciones)
            # Luego le decimos qué ETIQUETA poner en cada una de esas marcas.
            ax.set_xticklabels(ticks_etiquetas)
            

    fig.suptitle(f"±{window} días - Cluster {cl}", fontsize=12, y=0.975)
    plt.tight_layout()
    
    # Guardamos
    if cl == 3:
        fig.savefig(path_fig[:31]+f'Simposio_CR2/figs/VD_Cl{cl}.png', dpi=300)

################################################################    
#%% 11.1: Ciclos de 72h (n-1, n, n+1) a partir de DF horario ###

# Plot por cluster
for cl in range(n_clusters):
    dates_cl = df.loc[df["Cluster"]==cl].index
    dates_evt = df.loc[(df["Cluster"]==cl) & (df["T59"]>0)].index
    
    fig, axes = plt.subplots(4,1,figsize=(5,8), sharex=True)
    axes = axes.flatten(order='F')
    x = np.arange(72)  # horas: 0..71
    
    for i,var in enumerate(cols):

        ax = axes[i]
        stats_all = ace.aggregate_72h_p95(DF_h, dates_cl, var)
        stats_evt = ace.aggregate_72h_p95(DF_h, dates_evt, var) if len(dates_evt)>0 else None
        
        if stats_all:
            ax.plot(x, stats_all['mean'], "--", color="tab:blue", alpha=0.4, lw=0.8, label="Media cluster")
            ax.plot(x, stats_all['median'], color="tab:blue", alpha=0.6, lw=1.2, label="Mediana cluster")
            ax.fill_between(x, stats_all['p25'], stats_all['p75'], color="tab:blue", alpha=0.08,label="P25–P75 cluster")
            ## Percentil 95
            # if var in ['HCNM_CQ','MP25_CQ']:
            #     ax.plot(x, stats_all['p95'], ":", color="tab:blue", alpha=0.4, lw=0.8, label="P95 cluster")
        if stats_evt:
            ax.plot(x, stats_evt['mean'], "--", color="tab:orange", alpha=0.8, lw=1.2, label="Media eventos")
            ax.plot(x, stats_evt['median'], color="tab:orange", alpha=0.95, lw=1.8, label="Mediana eventos")
            ax.fill_between(x, stats_evt['p25'], stats_evt['p75'], color="tab:orange", alpha=0.15,label="P25–P75 eventos")
            ## Percentil 95
            # if var in ['HCNM_CQ','MP25_CQ']:
            #     ax.plot(x, stats_evt['p95'], ":", color="tab:orange", alpha=0.8, lw=1.2, label="P95 eventos")

        
        # Líneas divisorias entre días (24h,48h)
        ax.axvline(24, color="k", ls=":", alpha=0.6)
        ax.axvline(48, color="k", ls=":", alpha=0.6)
        ax.set_xlim(0,71)
        ax.set_xticks([0,12,24,36,48,60,71])
        ax.set_xticklabels([-24,-12,0,12,24,36,47])
        ax.set_ylabel(var, fontweight="bold", fontsize=12)
        ax.grid(alpha=0.2)
    
    fig.suptitle(f"Ciclo diario [n-1 , n , n+1] — Cluster {cl}", fontsize=11, y=0.974)
    plt.tight_layout(w_pad=0.4)#,rect=[0,0,0.87,1])
    
    # Guardamos
    if cl == 3:
        fig.savefig(path_fig[:31]+f'Simposio_CR2/figs/CD_Cl{cl}.png', dpi=300)
        
        
        
        
#################################################################
#%% 11.2: Ciclo horario SOLO PARA DÍA N a partir de DF horario ###

# Ploteo por cluster
for cl in range(n_clusters):
    dates_cl = df.loc[df["Cluster"] == cl].index
    dates_evt = df.loc[(df["Cluster"] == cl) & (df["T59"] > 0)].index
    
    fig, axes = plt.subplots(4, 4, figsize=(15,8), sharex=True)
    axes = axes.flatten()
    hours = np.arange(24)
    
    for i,var in enumerate(cols):
        ax = axes[i]
        stats_all = ace.aggregate_24h(DF_h, dates_cl, var)
        stats_evt = ace.aggregate_24h(DF_h, dates_evt, var) if len(dates_evt) > 0 else None
        
        if stats_all:
            ax.plot(hours, stats_all['mean'], "--", color="tab:blue", alpha=0.4, lw=0.8, label="Media (todos)")
            ax.plot(hours, stats_all['median'], color="tab:blue", alpha=0.6, lw=1.2, label="Mediana (todos)")
            ax.fill_between(hours, stats_all['p25'], stats_all['p75'], color="tab:blue", alpha=0.08)
        if stats_evt:
            ax.plot(hours, stats_evt['mean'], "--", color="tab:orange", alpha=0.8, lw=1.2, label="Media (eventos)")
            ax.plot(hours, stats_evt['median'], color="tab:orange", alpha=0.95, lw=1.8, label="Mediana (eventos)")
            ax.fill_between(hours, stats_evt['p25'], stats_evt['p75'], color="tab:orange", alpha=0.15)
        
        ax.set_xlim(0,23)
        ax.set_xticks([0,6,12,18,23])
        ax.set_xticklabels([-24,-12,0,12,24,36,47])
        ax.set_ylabel(var, fontweight="bold", fontsize=11)
        ax.grid(alpha=0.5)
        
        if i == 0:
            fig.legend(loc="upper left", bbox_to_anchor=(0.87,0.92), frameon=False)
    
    fig.suptitle(f"Ciclo diario [N] — Cluster {cl}", fontsize=16, y=0.986)
    plt.tight_layout(rect=[0,0,0.85,1])
    plt.show()



#%% 12. Export cluster dates for composites
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/Clusters/2022-2023_5C_Cluster0BajaCost/'
for cl in range(n_clusters):
    dates_cl = df.loc[df["Cluster"] == cl].index
    # Force all datetimes to 12:00:00 UTC
    dates_cl = dates_cl.normalize() + pd.Timedelta(hours=12)
    # ### CSV ###
    # dates_str = dates_cl.strftime("%Y-%m-%d %H:%M:%S")
    # path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
    # dates_str.to_series().to_csv(path+f'cluster_{cl}.csv', index=False, header=False)
      
    
    ### TXT ###
    # Format as YYYYMMDD strings
    dates_str = dates_cl.strftime("%Y%m%d").tolist()
    outfile = path+f'cluster_{cl}.txt'
    with open(outfile, "w") as f:
        f.write(f"{len(dates_str)}\n")
        for d in dates_str:
            f.write(d + "\n")
    print(f"File saved: {outfile}")

#%% 13. Histogramas de intoxicados en días totales por cluster

# Graficar histogramas de la distribución de intoxicados (T59) en cada cluster
n_clusters = df["Cluster"].nunique()
fig, axes = plt.subplots(math.ceil(n_clusters/2), 2, figsize=(12, 8), sharex=True, sharey=True)

axes = axes.flatten()

for cl in sorted(df["Cluster"].unique()):
    datos_cl = df.loc[df["Cluster"] == cl, "T59"]
    ax = axes[cl]
    ax.hist(datos_cl, bins=10, color="tab:blue", alpha=0.7, edgecolor="black")
    ax.set_title(f"Cluster {cl} - Histograma T59")
    ax.set_xlabel("Nº de intoxicados por evento")
    ax.set_ylabel("Frecuencia")
    ax.grid(alpha=0.4)

plt.tight_layout()
plt.show()

#%% 14. Histogramas de intoxicados en días con evento por cluster

# Graficar histogramas de la distribución de intoxicados (T59) en cada cluster,
# pero considerando solo los días con intoxicados (T59 > 0)
n_clusters = df["Cluster"].nunique()
fig, axes = plt.subplots(n_clusters,1, figsize=(5, 8), sharex=True, sharey=True)

axes = axes.flatten()

for i, cl in enumerate(sorted(df["Cluster"].unique())):
    # Filtrar solo días con eventos de intoxicación
    datos_cl = df.loc[(df["Cluster"] == cl) & (df["T59"] > 0), "T59"]

    ax = axes[i]
    ax.hist(datos_cl, bins=15, color="tab:blue", alpha=0.7, edgecolor="black")
    ax.set_ylabel(f"Cluster {cl}",fontweight='bold')
    if i == n_clusters-1:
        ax.set_xlabel("Nº de intoxicados por evento")
    ax.grid(alpha=0.4)

# Eliminar ejes vacíos si el número de clusters es impar
for j in range(i+1, len(axes)):
    fig.delaxes(axes[j])
fig.suptitle('Histograma T59 (eventos)')
plt.tight_layout()
plt.show()


#%% 14. Visualize var_t time series
var_t = 'T59'
fig, ax = plt.subplots(figsize=(12,6))
ax.bar(df.index, df[var_t], color='blue', alpha=0.4, label=var_t)
for cluster_id in range(n_clusters):#df["Cluster"].unique():
    cluster_days = df[df["Cluster"] == cluster_id].index
    ax.scatter(cluster_days, df.loc[cluster_days, var_t],
               label=f"Cluster {cluster_id}", s=40)
ax.set_title(f"{var_t} v/s clusters")
ax.set_ylabel(var_t)
ax.set_xlabel("Date")
ax.grid(alpha=0.4)
d1 = pd.to_datetime('2022-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
# d1 = pd.to_datetime('2022-08-27 00:00:00')
# d2 = pd.to_datetime('2022-11-03 23:00:00')
# d1 = pd.to_datetime('2023-05-01 00:00:00')
# d2 = pd.to_datetime('2023-07-01 23:00:00')
ax.set_xlim(d1,d2)
ax.legend()
plt.tight_layout()
plt.show()



#%% 15. Serie temporal de intoxicados con distinción por comuna

var_t = "T59"

# Definir colores por comuna
colores_comuna = {
    "Quintero": "tab:blue",
    "Puchuncaví": "tab:green",
    "Quintero y Puchuncaví": "tab:orange"
}

fig, ax = plt.subplots(figsize=(12,6))

# Graficar barras coloreadas por comuna
for comuna, color in colores_comuna.items():
    subset = df[df["Comuna"] == comuna]
    ax.bar(subset.index, subset[var_t], 
           color=color, alpha=0.6, label=comuna)

# Superponer clusters con scatter
for cluster_id in range(n_clusters):
    cluster_days = df[df["Cluster"] == cluster_id].index
    ax.scatter(cluster_days, df.loc[cluster_days, var_t],
               label=f"Cluster {cluster_id}", s=50, edgecolor="black")

ax.set_title(f"{var_t} v/s clusters con distinción por comuna")
ax.set_ylabel("Número de intoxicados")
ax.set_xlabel("Fecha")
ax.grid(alpha=0.4)
# d1 = pd.to_datetime('2022-01-01 00:00:00')
# d2 = pd.to_datetime('2023-12-31 23:00:00')
# d1 = pd.to_datetime('2022-06-01 00:00:00')
# d2 = pd.to_datetime('2022-08-01 23:00:00')
d1 = pd.to_datetime('2023-03-01 00:00:00')
d2 = pd.to_datetime('2023-10-01 23:00:00')
ax.set_xlim(d1,d2)
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")  # leyenda afuera para mejor lectura
plt.tight_layout()
plt.show()

#%% 16. Time series visualization
d1 = pd.to_datetime('2023-05-29 00:00:00')
d2 = pd.to_datetime('2023-06-06 23:00:00')
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
T59 = pd.read_csv(path+'serie_T59full.csv', index_col='date',
                  parse_dates=True)
T59 = T59.loc[d1:d2,['T59','Comuna']]
# Fechas
# d1 = pd.to_datetime('2022-06-01 00:00:00')
# d2 = pd.to_datetime('2022-07-01 23:00:00')
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
data = pd.read_csv(path+'DF_h.csv', index_col='date', parse_dates=True)

# data['slp_dmc_diff'] = data['slp_dmc'].diff() 
# data['slp_dmc_rm'] = data['slp_dmc'].rolling(window=13,center=True).mean()
# data['slp_dmc_rmdiff'] = data['slp_dmc_rm'].diff()
data['T59'] = T59['T59'].asfreq('h')
# mask = data['T59']<10
# data.loc[mask,'T59'] = 0
# data.loc[mask,'Comuna'] = float('nan')
# Variables
variables = [
    
            'HCNM_CC','SO2_CC',
            'MP25_CC','MP10_CC',
            
            'HCNM_CQ','SO2_CQ',
            'MP25_CQ','MP10_CQ',
            'NO_CQ','NO2_CQ','O3_CQ',
            'CO_CQ',
            
            
            'HCNM_VE','SO2_VE',
            'MP25_VE','MP10_VE',
            'NO_VE','NO2_VE','O3_VE',
            

    
            # 'blh_era5','ies_princ',
            # 't_dmc','hr_dmc','slp_dmc',#'slp_dmc_diff',
            # 'r_dmc','ws_dmc',
            # 'ws_VE','ws_princ','ws_dmc','ws_CQ','ws40_princ',

            # 'blh_era5','ies_princ','r_dmc','t_dmc','slp_dmc','slp_dmc_diff','slp_dmc_rm','slp_dmc_rmdiff'
            # 'u_princ','v_princ','slp_dmc','slp_dmc_diff',
            # 'u_VE','v_VE',
            # 'u_princ','v_princ',
            # 'u_dmc','v_dmc',
            # 'u_CQ','v_CQ',
            
            # 'T59',

            ]

# Ploteamos Horizontal
# n_var = len(variables)
# c_plot = math.ceil(n_var/5)
# axs = data.loc[d1:d2,variables].plot(subplots=True, layout=(5,1*c_plot),
#                                     grid=True, figsize=(6*c_plot,10), 
#                                     marker='.', lw=1,ms=3, sharex=True)

# Ploteamos Vertical
axs = data.loc[d1:d2,variables].plot(subplots=True,
                                    grid=True, figsize=(10.5,20), 
                                    marker='.', lw=1,ms=3, sharex=True)

# d129 = pd.to_datetime('2022-09-12 00:00:00')
# d410 = pd.to_datetime('2022-10-04 00:00:00')
# d710 = pd.to_datetime('2022-10-07 00:00:00')
# for ax in axs.flat: 
#     ax.axvline(d129, color='r', linestyle='--', alpha=0.5)
#     ax.axvline(d410, color='r', linestyle='--', alpha=0.5)
#     ax.axvline(d710, color='r', linestyle='--', alpha=0.5)

plt.tight_layout()

