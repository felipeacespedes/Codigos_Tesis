# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:26:38 2026

@author: felip
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
from matplotlib.colors import BoundaryNorm
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import TruncatedSVD #, PCA
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
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


#%% Juntamos DFs

CC = CC_cov.join(CC_ss)
QU = QU_cov.join(QU_ss)
VE = VE_cov.join(VE_ss)

del CC_cov, QU_cov, VE_cov, CC_ss, QU_ss, VE_ss
#%% Quitamos compuestos no utilizados

drop = []
for col in CC.columns:
    if (col[-2:len(col)] == '_2') or (col in ['Formaldehido', 'Metanol']):
        drop.append(col)

   
CC = CC.drop(columns=drop)
QU = QU.drop(columns=drop)
VE = VE.drop(columns=drop)

###############
#%% K-means ###
###############

cols = ['Benceno_1', 'Tolueno_1', 'Etilbenceno y xilenos', 'Trimetilbenceno',
       'Acetaldehido', 'Butenos', 'DMS', 'Acetonitrilo', 'Propeno', 'Etanol',
       'Acetona', 'AcidoAcetico', 'Furano', 'Isopreno', 'Metacroleina',
       'Butanona', 'Fenol', 'Benzonitrilo', 'Estireno', 'Cresol',
       'Benzofurano', 'Naftaleno', 'Monoterpenos', 'SO2', 'NO', 'NO2', 'CO',
       'O3', 'NOx', 'RadGlob', 'H2S', 'PM10', 'PM25', 'RH', 'Temp', #'DirV',
       'VelV', 'EH2O', 'U', 'V']


site = 'QU'

if site == 'CC':
    df = CC.copy()
    name = 'Concón'
    n_clusters = 6
elif site == 'QU':
    df = QU.copy()
    name = 'Quintero'
    n_clusters = 5
elif site == 'VE':
    df = VE.copy()
    name = 'Ventanas'
    n_clusters = 5

features = df[cols]

#%% 2. Handle NaNs (imputation)
imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(features)

#%% 3. Standardize
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
    
    
plt.figure(figsize=(7,5))

plt.plot(K_range, inertia, "o-")
plt.xlabel("Número de clusters k")
plt.ylabel("Inercia (WCSS)")
# plt.ylim(1500,5500)
# plt.vlines(4,15000,0,colors='r',linestyles='--')
plt.title("Método del codo")
plt.grid(alpha=0.5)


plt.tight_layout()
plt.savefig(path_fig+site+'/'+'Metodo_Codo.png', dpi=300)

#%% 5. Final clustering
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=80, n_init=10000)
clusters = kmeans.fit_predict(X_scaled)
df["Cluster"] = clusters

#%% 6. Visualize PCA space with variable loadings

# 1) Calculamos PCA: usamos TruncatedSVD ya que no centra por media 
pca = TruncatedSVD(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df["PC1"] = X_pca[:,0]
df["PC2"] = X_pca[:,1]

# 2) Obtenemos los "loadings" = pesos de cada variable en cada componente
loadings = pca.components_.T  # shape: (n_variables, n_components)
vars_names = features.columns

# 3) Escala para hacer visibles las flechas en el mismo plano que los puntos
scale_factor = 9  # (ajustamos longitud de los vectores)

# 4) Graficamos
fig, ax = plt.subplots(figsize=(8,7))
levels = list(range(n_clusters+1))
norm = BoundaryNorm(levels, len(levels)-1)

# puntos de cada día coloreados por cluster
sc = ax.scatter(df["PC1"], df["PC2"],c=df["Cluster"], cmap='tab10',
                 s=25, alpha=0.6, norm=norm,edgecolor='k', linewidth=0.08)

# Centroides proyectados al espacio PCA 
centroids_pca = pca.transform(kmeans.cluster_centers_)
ax.scatter(
    centroids_pca[:, 0], centroids_pca[:, 1],
    c=np.arange(n_clusters), cmap='tab10', norm=norm,s=200, marker='X',
     edgecolor='k', linewidth=1.0, label="Centroides",zorder=2, alpha=0.7)


# # flechas para variables (loadings)
# for i, var in enumerate(vars_names):
#     d = 0.3 if var == 'MP25_CQ' else 0
#     x_vec = loadings[i, 0] * scale_factor
#     y_vec = loadings[i, 1] * scale_factor
#     ax.arrow(0, 0, x_vec, y_vec, color='k', alpha=0.7, width=0.005,
#               head_width=0.08, length_includes_head=True,zorder=3)
#     ax.text(x_vec*1.12, y_vec*1.12+d, var, color='k', fontsize=9, fontweight='bold',
#             ha='center', va='center',zorder=3)
            

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
plt.savefig(path_fig+site+'/'+'TruncSVD_2d.png', dpi=300)


#%% 7. Tabla de Componentes Principales (SVD) y Pesos (Loadings)

# Definimos cuántos componentes analizar para la matriz (ej. 5 para mayor cobertura)
n_comp_tabla = 5
svd_tabla = TruncatedSVD(n_components=n_comp_tabla, random_state=42)
svd_tabla.fit(X_scaled)

# 1) Obtener la varianza explicada por cada componente
varianza_explicada = svd_tabla.explained_variance_ratio_ * 100

# 2) Crear nombres de columnas dinámicos con su varianza respectiva
pc_cols = [f"PC{i+1} ({var:.1f}%)" for i, var in enumerate(varianza_explicada)]

# 3) Extraer los pesos y armar el DataFrame
# svd_tabla.components_ tiene dimensiones (n_components, n_features)
df_loadings = pd.DataFrame(
    svd_tabla.components_.T,
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

#%% 8. Cluster profiles

cluster_profiles = pd.DataFrame(X_scaled, columns=features.columns)
cluster_profiles["Cluster"] = clusters
cluster_median = cluster_profiles.groupby("Cluster").median()

vmin = cluster_median.min().min()
vmax = cluster_median.max().max()
if np.abs(vmin)>np.abs(vmax):
    val = np.floor(np.abs(vmin))
else:
    val = np.floor(np.abs(vmax))

plt.figure(figsize=(10,15))
sns.heatmap(cluster_median.T, cmap="coolwarm", annot=True, fmt=".2f",
            annot_kws={"color": "black","fontsize":12}, 
            cbar_kws={'label': 'Desviación (IQR)','fraction':0.05},
            cbar=True, vmin=-val, vmax=val)
plt.title("Perfiles por cluster")
plt.xlabel("Cluster")
plt.ylabel("Variable")
plt.tight_layout(pad=1.3)
plt.savefig(path_fig+site+'/'+'Perfiles.png', dpi=300)

#%% 9. Variable importance per cluster
cluster_median = cluster_profiles.groupby("Cluster").median()
global_median = cluster_profiles.drop(columns="Cluster").median()

for cl in cluster_median.index:
    diffs = cluster_median.loc[cl] - global_median
    diffs_sorted = diffs.abs().sort_values(ascending=False)
    values = diffs[diffs_sorted.index]

    plt.figure(figsize=(15,10))
    values.plot(kind="bar", color=np.where(values > 0, "tab:red", "tab:blue"))
    plt.title(f"Cluster {cl}: Desviación desde mediana global")
    plt.ylabel("Desviación (IQR)")
    plt.xlabel("Variable")
    plt.xticks(rotation=90)#,fontweight='bold')
    plt.grid(alpha=0.5)
    plt.tight_layout()
    plt.savefig(path_fig+site+'/'+'Perfil_cl'+str(cl)+'.png', dpi=300)

#%% 

cluster_median = cluster_profiles.groupby("Cluster").median()
global_median = cluster_profiles.drop(columns="Cluster").median()

for cl in cluster_median.index:
    diffs = cluster_median.loc[cl] - global_median
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
    
