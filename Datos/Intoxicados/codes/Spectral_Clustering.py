# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 13:54:17 2025

@author: felip
"""

# -*- coding: utf-8 -*-
"""
Modified for Spectral Clustering
"""

#%% Imports

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
import matplotlib.patches as patches 
from matplotlib.colors import BoundaryNorm
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import TruncatedSVD 
# CAMBIO 1: Importamos SpectralClustering
from sklearn.cluster import SpectralClustering
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
import seaborn as sns

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

# Keep only intoxication days (T59 > 0) or handle mask
df = DF_d.copy() # Copia para seguridad
mask = df['Comuna'] == 'Puchuncaví'
df.loc[mask,'T59'] = 0
df.loc[mask,'Comuna'] = float('nan') 
mask = df['T59']>0
print(f"Usamos {len(df.loc[mask])} días con intoxicados de un total "+
      f"de {len(df)} días")

# Variables para clustering:
cols = [
        # 'ies_princ',
        # 'blh_era5',
        # 'ws_dmc',
        'HCNM_CQ',
        # 'HCNM_VE',
        'SO2_CQ',
        # 'SO2_VE',
        'MP25_CQ',
        # 'MP25_VE'
        ]

var_t = 'T59'  
features = df[cols]
target = df[var_t]

# Visualize features distributions (Opcional)
# title='Histogramas de anomalías diarias con datos de 5 a 11 am'
# ax = features.hist(bins=15,figsize=(10,7))
# fig = ax.flatten()[0].figure
# fig.suptitle(title)
# plt.tight_layout()

#%% 2. Handle NaNs (imputation)
imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(features)

# %% 3. Standardize
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X_imputed)

#%% 4. Determine best k (Solo Silhouette, Inertia no aplica igual en Spectral)
sil_scores = []
K_range = range(2, 15)

print("Evaluando número de clusters...")
for k in K_range:
    # CAMBIO 2: Usamos SpectralClustering en el loop
    # affinity='nearest_neighbors' construye un grafo de conectividad (k-NN)
    spectral_eval = SpectralClustering(n_clusters=k, 
                                       affinity='nearest_neighbors',
                                       assign_labels='kmeans',
                                       random_state=50,
                                       n_jobs=-1) 
    labels = spectral_eval.fit_predict(X_scaled)
    sil_scores.append(silhouette_score(X_scaled, labels))

plt.figure(figsize=(6,5)) # Ajustado tamaño ya que solo hay 1 plot
plt.plot(K_range, sil_scores, "o-", color='tab:orange')
plt.xlabel("Número de clusters k")
plt.ylabel("Score de silueta")
plt.title("Método de la silueta (Spectral Clustering)")
plt.grid(alpha=0.5)
plt.tight_layout()
plt.show()

#%% 5. Final clustering
n_clusters = 4 # Define tu n óptimo basado en el gráfico anterior

# CAMBIO 3: Instancia final del modelo
model = SpectralClustering(n_clusters=n_clusters, 
                           affinity='nearest_neighbors',
                           assign_labels='kmeans', # Estrategia para asignar etiquetas post-embedding
                           random_state=80,
                           n_jobs=-1)

clusters = model.fit_predict(X_scaled)
df["Cluster"] = clusters

# Crear DataFrame con estadísticas
resumen_clusters = pd.DataFrame({
    "Total T59": df.groupby("Cluster")["T59"].sum(),
    "Dias cluster": df.groupby("Cluster").size(),
    "Media T59": df.groupby("Cluster")["T59"].mean().round(2),
    "Mediana T59": df.groupby("Cluster")["T59"].median(),
    "Dias T59": df.groupby("Cluster")["T59"].apply(lambda x: (x > 0).sum()) 
})

resumen_clusters["T59 medio"] = (
    resumen_clusters["Total T59"] / resumen_clusters["Dias T59"]).round(2)

print("==================== Resumen de intoxicaciones por cluster ====================")
print(resumen_clusters)

# Guardamos fechas
cluster_dates = {}
for cl in sorted(df["Cluster"].unique()):
    dates = df.loc[df["Cluster"] == cl].index
    cluster_dates[cl] = dates


#%% 6. Visualize PCA space with variable loadings

# 1) Calculamos PCA
pca = TruncatedSVD(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df["PC1"] = X_pca[:,0]
df["PC2"] = X_pca[:,1]

# 2) Loadings
loadings = pca.components_.T  
vars_names = features.columns
scale_factor = 9 

# CAMBIO 4: Calculamos los centroides MANUALMENTE
# SpectralClustering no tiene el atributo cluster_centers_, así que
# calculamos la media de X_scaled para cada grupo asignado.
manual_centroids = []
for i in range(n_clusters):
    # Promedio de las variables escaladas para los días del cluster i
    centroid = X_scaled[clusters == i].mean(axis=0)
    manual_centroids.append(centroid)
manual_centroids = np.array(manual_centroids)

# Proyectamos estos centroides manuales al espacio PCA
centroids_pca = pca.transform(manual_centroids)

# 4) Graficamos
fig, ax = plt.subplots(figsize=(8,7))
levels = list(range(n_clusters+1))
norm = BoundaryNorm(levels, len(levels)-1)

# Puntos
sc = ax.scatter(df["PC1"], df["PC2"], c=df["Cluster"], cmap='tab10',
                 s=25, alpha=0.6, norm=norm, edgecolor='k', linewidth=0.08)

# Centroides (usando los calculados manualmente)
ax.scatter(
    centroids_pca[:, 0], centroids_pca[:, 1],
    c=np.arange(n_clusters), cmap='tab10', norm=norm, s=200, marker='X',
     edgecolor='k', linewidth=1.0, label="Centroides", zorder=2, alpha=0.7)

# Flechas (loadings)
for i, var in enumerate(vars_names):
    d = 0.3 if var == 'MP25_CQ' else 0
    x_vec = loadings[i, 0] * scale_factor
    y_vec = loadings[i, 1] * scale_factor
    ax.arrow(0, 0, x_vec, y_vec, color='k', alpha=0.7, width=0.005,
             head_width=0.08, length_includes_head=True, zorder=3)
    ax.text(x_vec*1.12, y_vec*1.12+d, var, color='k', fontsize=9, fontweight='bold',
            ha='center', va='center', zorder=3)
            
# Ejes y etiquetas
evr = pca.explained_variance_ratio_
ax.set_xlabel(f"PC1 ({evr[0]*100:.1f}%)")
ax.set_ylabel(f"PC2 ({evr[1]*100:.1f}%)")
ax.axhline(0, color='gray', lw=1, alpha=0.5)
ax.axvline(0, color='gray', lw=1, alpha=0.5)
ax.set_title(f"Spectral Clustering en espacio PCA (k={n_clusters})")
ax.grid(alpha=0.4)

# Colorbar
cb = plt.colorbar(sc, ax=ax, pad=0.03, fraction=0.05)
cb.set_label("Cluster", labelpad=8)
current_ticks = cb.get_ticks()
if len(current_ticks) > 1:
    new_ticks = current_ticks + (current_ticks[1] - current_ticks[0]) / 2
    cb.set_ticks(new_ticks[0:n_clusters])
    cb.set_ticklabels(levels[0:n_clusters])

plt.tight_layout()
plt.show()