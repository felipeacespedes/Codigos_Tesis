# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 10:43:49 2023

@author: felip
"""
#%% Importamos librerías
import Estadisticos_maps as em
import pandas as pd
import matplotlib.pyplot as plt

#%% Creamos listas de variables, estaciones y estadísticos a usar

le = ['Ventanas','Centro_Quintero','Concón','Colmo']

    # ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura' \
    #  ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo']

lv = ['HCNM'] #, 'MP25', 'CO']

lestd = ['50%','99.8%', 'IQR']#['5%','50%','95%','count','mean','std']

#%% Ejecutamos función est_maps() en periodo total
dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Estad/Total/'
em.est_maps(le, lv,lestd,'2019-01-01','2023-12-31',dire)

#%% Ejecutamos función est_maps() en periodo interes
dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Estad/Interes/'
wd, wd_vals, ws_vals = em.est_maps( le, lv, lestd,'2022-08-27','2022-11-23'\
                                   , dire)
# wd, ws = em.est_maps( le, lv, lestd,'2022-08-27','2022-11-23', dire)
 #%% Ejecutamos función est_maps() en 31/08/22
dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Estad/310822/'
em.est_maps( le, lv, lestd,'2022-08-31','2022-08-31', dire)
#%% Ejecutamos función est_maps() en 02/09/22
dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Estad/020922/'
em.est_maps( le, lv, lestd,'2022-09-02','2022-09-02', dire)

#%% Ajustes

# Chequemos porque con 75% se muestran flechas de direferentes largos:
    # - Examinamos los datos por estación
        # Ventanas: 
# Se cree que tiene que ver con la proyección pero por ahora se desconoce
# cómo arreglarnos :( 

# Por ultimo, queremos chequear si las sumas entre u y v dan 1 efectivamente
# Para esto intentamos ver si las sumas particulares de alguna estación 
# (ventanas) entre U y V usando pitagoras, entregan valores 1 lo que si 
# se cumple, pero al momento de calcular alas direcciones promedio, no 
# se obtiene un vector unitario, QUEDA VEER!

#%% Estadísticos de datos modificados

# cargamos df de HCNM modificado
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
HCNM_m = pd.read_pickle(path+'HCNM_mod_df.pkl') 

# ejecutamos fucnión para periodo total
dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Estad/Total/'
em.est_maps_df( 'HCNM', HCNM_m, lestd,'2018-01-01','2023-12-31', dire)

#%% Plotear windroses entre percentiles de HCNM

# cargamos df de HCNM modificado
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
HCNM_m = pd.read_pickle(path+'HCNM_mod_df.pkl')

# ejecutamos fucnión para periodo total
cols = ['Ventanas','Centro_Quintero','Concón','Gaviotas','Colmo']
dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Estad/Total/'
em.windrose_df_entrepercs( 'HCNM', HCNM_m, '2019-01-01','2023-12-31'\
                          , '75%', '95%', dire ,cols)
    
    
#%% 
#######################################################################
#################### Ploteamos con topografía #########################
#######################################################################

#%% Cargamos df de datos modificados
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
# HCNM_m = pd.read_pickle(path+'HCNM_mod_df.pkl')
HCNM_m = pd.read_csv(path+'HCNM_mod_df.csv', index_col='date')
path_topo = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/'
nc = path_topo+'QUINTERO.nc'

#%% ejecutamos fucnión para periodo total
dire = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 1/'
em.est_maps_topo('HCNM', HCNM_m[le], lestd,'2019-01-01','2023-12-31', dire, nc)

#%% 

plt.plot(range(10))
plt.savefig(dire+'test.png')