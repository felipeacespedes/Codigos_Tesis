# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 17:53:20 2024

@author: felip
"""
# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
#%% Importamos datos
#%% COVs PTR-MS-TOF
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
file = 'datos_inv/inv_data_1min.csv' #5min
COV = pd.read_csv(path+file,delimiter=';')
COV['date'] = pd.to_datetime(COV['date'],format='%d/%m/%Y %H:%M:%S')
COV['date'] = pd.to_datetime(COV['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV = COV.set_index('date')
COV = COV.resample('H').mean()
# Guardamos hora inicial y final de COV para cortar HCNM
Ti = COV.index[0]; Tf = COV.index[-1]
del path, file
#%% HCNM Centro_Quintero
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_SINCA/'
HCNM = pd.read_csv(path+'HCNM_mod_lod_df.csv') # mod_lod
HCNM['date'] = pd.to_datetime(HCNM['date'])
HCNM = HCNM.set_index('date')
HCNM = HCNM.loc[Ti:Tf,'Centro_Quintero']*1000 # queda en ppb
del path, Ti, Tf
#%% Lista de factores de conversión a fracción de carbono para COVs y HCNM
# # Fracción de carbono de COVs en orden de columnas de DF COV:
# FC_COV = [0.4, 0.375, 0.585, 0.856, 0.545, 0.521, 0.856, 0.62, 0.4, 0.387, 
#           0.706, 0.882, 0.685, 0.666, 0.923, 0.912, 0.766, 0.815, 0.923, 
#           0.905, 0.777, 0.813, 0.899, 0.937, 0.882]
# # Fracción de carbono de propano para HCNM
# FC_HCNM = 0.8181
#%% Lista de factores de conversión a numero de carbono para COVs y HCNM

# Número de atomos de carbono por compuesto
NC_COV = [1, 1, 2, 3, 2, 2, 4, 3, 2, 2, 4, 5, 4, 
          4, 6, 7, 6, 7, 8, 8, 7, 8, 9, 10, 10]

# Número de atomos de carbono propano
NC_HCNM = 3

#%% Aplicamos factores y sumamos cómo COVs Totales

#COV
COV_tot = COV.mul(NC_COV,axis='columns')
COV_tot['Total'] = COV_tot.sum(axis='columns')
# Ploteamos COVs Totales
COV_tot['Total'].plot(grid=True, figsize=(10,5),ylabel='[ppb fc]')
# plt.title('COVs Totales según fracción de masa molar de carbono')
plt.tight_layout()

#HCNM
HCNM = HCNM
# Ploteamos parte de Carbono de HCNM 
HCNM.plot(grid=True, figsize=(10,5),ylabel='[ppb]')
plt.title('HCNM Centro Quintero, periodo campaña invierno 2022')
plt.tight_layout()

del COV
#%% Creamos DF con datos COVs Totales y HCNM

# Creamos DF y columnas
DATA_CA = pd.DataFrame(index=COV_tot.index,columns=['COV','HCNM'])
DATA_CA['COV'] = COV_tot['Total']
DATA_CA['HCNM'] = HCNM


# Ploteamos ambas columnas
DATA_CA.plot(subplots=True,layout=(2,1),figsize=(15,8),
             ylabel='[ppbc]',grid=True)
plt.suptitle('COVs Totales y HCNM, ambos en razón de mezcla según n° '+
             'carbonos molecular')
plt.legend()
plt.tight_layout()

#%% 
