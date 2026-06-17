# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:27:02 2024

@author: felip

Código para identificar los peaks de HCNM en Estación Centro_quintero que 
sobrepasen el percentil 95 (permisivo, pero lo pidió Rodrigo) e identificar
COVs que se miden en PTR.
"""
# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
from Plot_covs_functs import Plot_COV, Plot_MET
from Ternario_functs import COV_Ternary_tod, COV_Ternary_wd

#%% Importamos datos
#%% COVs PTR-MS-TOF
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
file = 'datos_inv/inv_data_5min.csv' #1min
COV = pd.read_csv(path+file,delimiter=';')
COV['date'] = pd.to_datetime(COV['date'],format='%d/%m/%Y %H:%M:%S')
COV['date'] = pd.to_datetime(COV['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV = COV.set_index('date')
COV_m = COV.copy() # copiamos 1 minuto
COV = COV.resample('H').mean()
# Guardamos hora inicial y final de COV para cortar HCNM
Ti = COV.index[0]; Tf = COV.index[-1]
del path, file
#%% HCNM Centro_Quintero
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_SINCA/'
HCNM = pd.read_csv(path+'HCNM_mod_lod_df.csv') # mod_lod
HCNM['date'] = pd.to_datetime(HCNM['date'])
HCNM = HCNM.set_index('date')
std_3 = HCNM['Centro_Quintero'].quantile(0.998)*1000 # perc998 en ppb
perc_99 = HCNM['Centro_Quintero'].quantile(0.99)*1000 # perc99 en ppb
perc_95 = HCNM['Centro_Quintero'].quantile(0.95)*1000 # perc95 en ppb 
HCNM = HCNM.loc[Ti:Tf,'Centro_Quintero']*1000 # queda en ppb
del path, Ti, Tf
#%% Pedimos a HCNM fechas que sean >= a su perc 95

# Guardamos fechas en que datos sobrepasan percentil 95 (boolean)
k_p95 = HCNM >= perc_95

#%% Creamos listas de peaks

# Creamos listas para rellenar con instantes iniciales y finales
Pi = []
Pf = []
# Iteramos por valores Booleanos para encontrar ki y kf de cada peak +-2h
for ki in range(len(k_p95)):
    # Definimos n cómo el número de valores hacia atras/adelante a partir
    # de ki, que se pide que no sobrepasen el p95. Además es desde donde
    # se define y ploteará el episodio para ver cualquier aumento de rms
    # previo/posterior a que se sobrepasará el p95.
    n = 6
    # Guardar comienzo: Se pide que los n valores anteriores
    # no sean False para guardar cómo comienzo de episodio
    if k_p95[ki] == True and k_p95[ki-n:ki].sum()==0:
        # guardamos hora -4
        Pi.append(k_p95.index[ki-n])
    # Guardamos final
    if k_p95[ki] == True and k_p95[ki+1:ki+(n+1)].sum()==0:
        # guardamos hora +4
        Pf.append(k_p95.index[ki+n])
    else:
        continue
del ki, n
#%% Ploteamos momentos en serie HCNM

path = 'C:/Users/felip/Desktop/Avances/11/Peaks perc95/HCNM/'

# Iteramos por peaks
for p in range(len(Pi)):
    # Definmos momentos inicial y final
    date_1 = pd.to_datetime(Pi[p])
    date_2 = pd.to_datetime(Pf[p])
    # Ploteamos
    plt.figure()
    ax = HCNM.loc[date_1:date_2].plot(grid=True, figsize=(14,7),ylim=(-0.1,3000))
    plt.hlines(std_3,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
               .format(std_3), linestyle='dashed', color='m')
    plt.hlines(perc_99,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
               .format(perc_99), linestyle='dashed', color='g')
    plt.hlines(perc_95,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
               .format(perc_95), linestyle='dashed', color='c')
    plt.suptitle('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
              +date_2.strftime('%Y-%m-%d, %H:%M.'))
    plt.ylabel('ppb')
    plt.legend()
    plt.tight_layout()
    plt.savefig(path+'CQ_'+date_1.strftime('%Y-%m-%d %H')+'.png', dpi=300)

del path, p, date_1, date_2, ax
#%% Ploteamos momentos en PTR

path= 'C:/Users/felip/Desktop/Avances/11/Peaks perc95/COV/'

# Iteramos por peaks
for p in range(len(Pi)):

    ### Frecuencia Minutaria
    ## 1 plot
    # # 50 ppb
    # Plot_COV(COV_m, Pi[p], Pf[p], 50, '1plot', 'Minutaria', path)
    # # 200 pbb
    # Plot_COV(COV_m, Pi[p], Pf[p], 200, '1plot', 'Minutaria', path)

    ## 25 plot
    # # 50 ppb
    # Plot_COV(COV_m, Pi[p], Pf[p], 50, '25plot', 'Minutaria', path)
    # # 200 pbb
    # Plot_COV(COV_m, Pi[p], Pf[p], 200, '25plot', 'Minutaria', path)

    ### Frecuencia Horaria
    ## 1 plot
    # # 10 ppb
    Plot_COV(COV, Pi[p], Pf[p], 10, '1plot', 'Horaria', path)
    # # 50 pbb
    # Plot_COV(COV, Pi[p], Pf[p], 50, '1plot', 'Horaria', path)

    ## 25 plot
    # 10 ppb
    Plot_COV(COV, Pi[p], Pf[p], 10, '25plot', 'Horaria', path)
    # 50 pbb
    # Plot_COV(COV, Pi[p], Pf[p], 50, '25plot', 'Horaria', path)

#%% Ploteamos variables meteo para datos 5min

path= 'C:/Users/felip/Desktop/Avances/11/Peaks perc95/MET/'

# Iteramos por peaks
for p in range(len(Pi)):
    
    # Ploteamos con función Plot_MET()
    Plot_MET(COV_m,Pi[p],Pf[p],path)
    
#%% Ploteamos diagramas ternarios

path= 'C:/Users/felip/Desktop/Avances/11/Peaks perc95/Ternario/'

### TOD y Wd ###
for i in range(len(Pi)):
    COV_Ternary_tod(COV_m, Pi[i], Pf[i], '5min', path+'TOD/', str(i)+'_tod')
    COV_Ternary_wd(COV_m, Pi[i], Pf[i], path+'Wd/', str(i)+'_wd')

