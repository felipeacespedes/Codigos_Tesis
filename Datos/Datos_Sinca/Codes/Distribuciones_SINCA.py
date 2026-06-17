# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 09:45:16 2025

@author: felip
"""

# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss
import seaborn as sns
#%% importamos datos

# df HCNM
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_SINCA/'
HCNM = pd.read_csv(path+'HCNM_mod_df.csv') # mod_lod
HCNM['date'] = pd.to_datetime(HCNM['date'])
HCNM = HCNM.set_index('date')

#%% Ajustamos distribuciones 

#%% Centro Quintero ###
#######################
data = HCNM['Centro_Quintero'].dropna()
# botamos 0
mask = data != 0
data = data[mask]

#%% fit 
fit = ss.expon.fit(data)
print(fit)

#%% histograma
# datasort = data.sort_values()
plt.figure(figsize=(5,3))
plt.hist(1/data, density=True, bins=20, zorder=2)
# plt.plot(datasort, ss.expon.pdf(datasort, 
#                                 loc= fit[0],
#                                 scale= fit[1]))
# plt.xlim(-0.05,2.5)
# plt.ylim(0,10)}
plt.grid(zorder=0)
plt.tight_layout()
plt.show()

#%% Box-Cox: encuentra mejor transformación automaticamente
data_transf, lmbda = ss.boxcox(data)

# Plot original and transformed side by side
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(data, kde=True, ax=axs[0], color='skyblue')
axs[0].set_title("Original Data")
axs[0].set_ylim(0,1500)

sns.histplot(data_transf, kde=True, ax=axs[1], color='salmon')
axs[1].set_title(f"Box-Cox Transformed (λ = {lmbda:.2f})")

plt.tight_layout()
plt.show()
#%% Ventanas ###
################
data = HCNM['Ventanas'].dropna()

#%% fit 
fit = ss.expon.fit(data)
print(fit)

#%% histograma
datasort = data.sort_values()
plt.figure(figsize=(5,3))
plt.hist(data, density=True, bins=100, zorder=2)
plt.plot(datasort, ss.expon.pdf(datasort, 
                                  loc= fit[0],
                                  scale= fit[1]))
plt.xlim(-0.05,1)
plt.ylim(0,60)
plt.grid(zorder=0)
plt.tight_layout()
plt.show()


#%% Concón ###
##############
data = HCNM['Concón'].dropna()

#%% fit 
fit = ss.lognorm.fit(data)
print(fit)

#%% histograma
datasort = data.sort_values()
plt.figure(figsize=(5,3))
plt.hist(data, density=True, bins=100, zorder=2)
plt.plot(datasort, ss.lognorm.pdf(datasort, 
                                  fit[0],
                                  loc= fit[1],
                                  scale= fit[2]))
# plt.xscale('log')
plt.xlim(-0.005,3)
plt.ylim(0,3.5)
plt.grid(zorder=0)
plt.tight_layout()
plt.show()

#%% Colmo
data = HCNM['Colmo'].dropna()

#%% fit 
fit = ss.lognorm.fit(data)
print(fit)

#%% histograma
datasort = data.sort_values()
plt.figure(figsize=(5,3))
plt.hist(data, density=True, bins=100, zorder=2)
plt.plot(datasort, ss.lognorm.pdf(datasort, 
                                  fit[0],
                                  loc= fit[1],
                                  scale= fit[2]))
plt.xscale('log')
plt.xlim(-0.005,1)
plt.ylim(0,10)
plt.grid(zorder=0)
plt.tight_layout()
plt.show()

