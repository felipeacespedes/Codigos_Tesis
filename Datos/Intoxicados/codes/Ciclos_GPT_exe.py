# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 11:39:45 2025

@author: felip
"""
#%% Importamos librerías
import os
#%cd C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/codes
import pandas as pd
import Ciclos_GPT as cg
import Ciclos_Viento_GPT as cvg
import Ciclos_Viento_GPT_mod as cvgm
import CVGM_GeminiRev as cvgm_gr

#%% Importamos DF_h y DF_d

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
DF_h = pd.read_csv(path+'DF_h.csv',index_col='date',parse_dates=True)

# Definimos dfs viento 
WD = DF_h[['wd_VE','wd_princ','wd_dmc','wd_CQ']]#,'wd_quint']]
WS = DF_h[['ws_VE','ws_princ','ws_dmc','ws_CQ']]#,'ws_quint']]
WD = WD.rename(columns={'wd_VE':'Ventanas','wd_princ':'Principal',
                        'wd_dmc':'DMC','wd_CQ':'Centro_Quintero'})#,'wd_quint':'Quintero'})
WS = WS.rename(columns={'ws_VE':'Ventanas','ws_princ':'Principal',
                        'ws_dmc':'DMC','ws_CQ':'Centro_Quintero'})#,'ws_quint':'Quintero'})

#%% Antiguo

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
WD = pd.read_csv(path+'WD_df.csv',index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])
WS = pd.read_csv(path+'WS_df.csv',index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])
HCNM = pd.read_csv(path+'HCNM_mod_df.csv',index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])

# Cortamos DFs a periodo 2019-2023
d1 = pd.to_datetime('2019-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
WD = WD.loc[d1:d2]
WS = WS.loc[d1:d2]
HCNM = HCNM.loc[d1:d2]

#%% Ejecutamos ###

#%% Ploteamos HCNM

cg.plot_all_cycles(HCNM)

#%% Ploteamos todos los ciclos contaminantes
cols = [
        
        # 'HCNM_CQ','SO2_CQ','NO_CQ','NO2_CQ','O3_CQ','CO_CQ',
        # 'MP25_CQ','MP10_CQ',
    
        # 'HCNM_VE','SO2_VE','NO_VE','NO2_VE','O3_VE',
        # 'MP25_VE','MP10_VE',
        
        'HCNM_CC','SO2_CC',
        'MP25_CC','MP10_CC'

        ]
cg.plot_all_cycles(DF_h[cols],name='CC')

#%% Ploteamos ciclo de variables meteo

# Interpolar horario para blh

data = DF_h.copy()
data['blh_era5'] = data['blh_era5'].interpolate()

#%%
cols = [
        'blh_era5','ies_princ','t_dmc',
        'hr_dmc','slp_dmc','r_dmc',
        ]
cg.plot_DA_cycles(data[cols])

#%% Validación ERA5-DMC


# Interpolar horario para era5
data = DF_h.copy()
data[['p_era5','t_era5','hr_era5']] = data[['p_era5','t_era5','hr_era5']].interpolate()


#%% Ploteamos

# ERA5
cols = ['p_era5','t_era5','hr_era5']
cg.plot_DA_cycles(data[cols])
# DMC
cols = ['p_dmc','t_dmc','hr_dmc']
cg.plot_DA_cycles(data[cols])

#%% Ploteamos ciclos de viento

# Diario
cvg.plot_wind_direction_and_speed(WD, WS, cycle='daily')
# Anual
cvg.plot_wind_direction_and_speed(WD, WS, cycle='yearly')

#%% Ploteamos ciclos de viento con U y V

# Diario
cvgm.plot_wd_ws_u_v(WD, WS, cycle='daily')
# Anual
cvgm.plot_wd_ws_u_v(WD, WS, cycle='yearly')

#%% Ploteamos ciclos de viento con U y V por estación del año
seasonal_save_dir = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Wind_Season'
cvgm.plot_wd_ws_u_v_seasonal(WD, WS, save_dir=seasonal_save_dir, show=True)

#%% Ploteamos ciclos de viento con U y V por mes
monthly_save_dir = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Wind_Month'
cvgm.plot_wd_ws_u_v_monthly(WD, WS, save_dir=monthly_save_dir, show=True)

#%%#########################################################
############################################################
############ Ciclo diario por mes en Heatmap! ##############
############################################################

# Defininmos variables
df = HCNM.copy()
vars_a_graficar = ['Ventanas','Centro_Quintero','Concón','Colmo']
labels_derecha = ['HCNM']
grupos_colores = [0, 1, 2, 3]  # 0 para Var1, 1 para Var2...
titulos = ['Ventanas','Centro_Quintero','Concón','Colmo']
unidades = ['HCNM [$ppm$]','HCNM [$ppm$]','HCNM [$ppm$]','HCNM [$ppm$]'] 

# Llamamos a función
fig = cg.plot_seasonal_daily_cycle(
    df, 
    variables=vars_a_graficar, 
    right_labels=labels_derecha,
    cbar_groups=grupos_colores, 
    agg_func='mean', # Puedes cambiar esto por cg.iqr o lambda x: cg.perc(x, 90)
    grid_shape=(1, 4),
    station_names=titulos,
    unit_labels=unidades
)