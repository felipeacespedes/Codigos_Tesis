# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 12:20:38 2024

Inspeccionar posible correlación entre CO y HCNM
"""
# Importamos librerias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
#%% COV total cómo número de carbonos

# Número de atomos de carbono por compuesto
NC_COV = [1, 1, 2, 3, 2, 2, 4, 3, 2, 2, 4, 5, 4, 
          4, 6, 7, 6, 7, 8, 8, 7, 8, 9, 10, 10]

# Aplicamos factores a COVs y sumamos
COV['COV_tot'] = COV.mul(NC_COV,axis='columns').sum(axis='columns')

# Creamos DF para guardar datos horarios de campaña de invierno 2022
HCC_df = pd.DataFrame( columns=['HCNM','CO','COV_tot'], index=COV.index)
HCC_df['COV_tot'] = COV['COV_tot']

del NC_COV
#%% Cargamos datos SINCA

# HCNM
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_SINCA/'
HCNM = pd.read_csv(path+'HCNM_mod_lod_df.csv') # mod_lod
HCNM['date'] = pd.to_datetime(HCNM['date'])
HCNM = HCNM.set_index('date')
HCNM = HCNM.loc[:,'Centro_Quintero']*1000 # queda en ppb
# Creamos Dataframe para guardar datos 1823 de HCNM y CO
HC_df = pd.DataFrame(columns=['HCNM','CO'],index=HCNM.index)
HC_df['HCNM'] = HCNM.values
# Cortamos para datos de campaña de invierno 2022
HCC_df['HCNM'] = HCNM[Ti:Tf]

#%% CO (sin corregir)
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
CO = pd.read_csv(path+'CO-CQ_2018-2023.csv', delimiter=';', decimal=',',
                 skiprows=23, skipfooter=24)
CO = CO.iloc[:,4]; CO = CO.rename('Centro_Quintero')
CO = CO.astype('float64'); CO = CO*1000 # ppb
CO.index = pd.date_range('2018-01-01 00:00:00', '2023-12-31 23:00:00',freq='H')
# Asignamos a Dataframe de datos 1823 de HCNM y CO
HC_df['CO'] = CO.values
# Cortamos para datos de campaña de invierno 2022
HCC_df['CO'] = CO[Ti:Tf]

del path, Ti, Tf

#%% Calculamos correlaciones entre series

# Correlación entre HCNM y CO
corr_HC = HC_df.corr( method='pearson')

# Correlación entre COV_tot y CO
corr_HCC = HCC_df.corr( method='pearson')

#%% Path de guardado

path = 'C:/Users/felip/Desktop/Avances/11/CO/'

#%% Ploteamos series de tiempo de campaña de invierno

HCC_df.plot(subplots=True, layout=(3,1),figsize=(7,7), grid=True, 
            legend=True)
plt.suptitle('Series de tiempo, Campaña Invierno 2022')
plt.tight_layout()
plt.savefig(path+'Campaña Invierno/'+'Series de Tiempo.png',dpi=300)

#%% Ploteamos scatter plots con regresion lineal de campaña invierno

fig, axs = plt.subplots(1,3, figsize=(15,5.5))

# ax0
corr = corr_HCC.loc['CO','HCNM']
sns.regplot( ax = axs[0], data=HCC_df,  x = 'CO', y = 'HCNM', color = 'mediumblue',
            line_kws=dict(label=fr'$\rho$ = {corr: .2f}'))
axs[0].set_xlabel('CO [ppb]')
axs[0].set_ylabel('HCNM [ppb]')
axs[0].set_title('CO vs HCNM')
axs[0].grid(zorder=-1)
axs[0].legend()

# ax1
corr = corr_HCC.loc['CO','COV_tot']
sns.regplot( ax = axs[1], data=HCC_df, x = 'CO',y = 'COV_tot',color = 'darkorange',
            line_kws=dict(label=fr'$\rho$ = {corr: .2f}'))
axs[1].set_xlabel('CO [ppb]')
axs[1].set_ylabel('COVs Totales [ppbC]')
axs[1].set_title('CO vs COVs Totales')
axs[1].grid(zorder=-1)
axs[1].legend()

# ax2
corr = corr_HCC.loc['HCNM','COV_tot']
sns.regplot( ax = axs[2], data=HCC_df, x = 'HCNM',y = 'COV_tot',color = 'purple',
            line_kws=dict(label=fr'$\rho$ = {corr: .2f}'))
axs[2].set_xlabel('HCNM [ppb]')
axs[2].set_ylabel('COVs Totales [ppbC]')
axs[2].set_title('HCNM vs COVs Totales')
axs[2].grid(zorder=-1)
axs[2].legend()

fig.suptitle('Scatter y Regresión Lineal, Campaña Invierno 2022', 
              fontsize=13)
fig.tight_layout()
plt.savefig(path+'Campaña Invierno/'+'Scatter y Regresion.png',dpi=300)

del corr, axs, fig
#%% Ploteamos series de tiempo de campaña de invierno

HC_df.plot(subplots=True, layout=(2,1),figsize=(7,4), grid=True, 
            legend=True)
plt.suptitle('Series de tiempo 2018-2023')
plt.tight_layout()
plt.savefig(path+'2018-2023/'+'Series de Tiempo.png',dpi=300)

#%% Scatter plot serie 2018-2023

fig, ax = plt.subplots(figsize=(6,6))

# ax0
corr = corr_HC.loc['CO','HCNM']
sns.regplot( ax = ax, data=HC_df,  x = 'CO', y = 'HCNM', color = 'mediumblue',
            line_kws=dict(label=fr'$\rho$ = {corr: .2f}'))
ax.set_xlabel('CO [ppb]')
ax.set_ylabel('HCNM [ppb]')
ax.set_title('CO vs HCNM')
ax.set_xlim((0,2500))
ax.set_ylim((0,2500))
# ax.set_yscale('log')
ax.grid(zorder=-1)
ax.legend()

fig.suptitle('Scatter y Regresión Lineal, Serie 2018-2023', 
              fontsize=13)
fig.tight_layout()
plt.savefig(path+'2018-2023/'+'Scatter y Regresion.png',dpi=300)

del corr, ax, fig
#%% 


