# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 22:30:30 2023

@author: felip
"""

import numpy as np
import pandas as pd
from Vis_fun import Vis

#### Visualizador de serie de tiempo ####

#%% Importamos csv

HCNM = pd.read_csv('C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca'\
                   '/Estaciones/Los_Maitenes/CO.csv'
                 , delimiter=";"
                 , dtype={'a': str, 'b': str, 'c': float} 
                 , skiprows=23
                 , skipfooter=24
                 , usecols=(0,1,4)     
                 , decimal=","
                 , names=['Fecha','Hora','HCNM']
                 , header=0
                 )

    
HCNM.head()



Fecha = HCNM.Fecha
Hora = HCNM.Hora
#%% Creamos matriz de fechas originales de variables

tr1 = str(HCNM.Fecha[0]); tr1='0'+tr1 if len(tr1)==5 else tr1
tr2 = str(HCNM.Fecha[len(HCNM.Fecha)-1])
h1 = '0'+str(HCNM.Hora[0])+':00:00'
h2 = str(HCNM.Hora[len(HCNM.Hora)-1])[0:2]+':00:00'

t1 = '20'+tr1[0:2]+'-'+tr1[2:4]+'-'+tr1[4:6]+' '+h1
t2 = '20'+tr2[0:2]+'-'+tr2[2:4]+'-'+tr2[4:6]+' '+h2

T = pd.date_range(start=t1, end=t2, freq='H')

HCNM['T'] = T

#%% Quitamos índices de días 29/02 

# HCNM = HCNM[(T.month != 2) & (T.day != 29)]

# T = T[(T.month != 2) & (T.day != 29)]

#%% Obtenemos índices de fechas de interés y recortamos series

i1 = T.get_loc('2018-01-01 00:00:00')
i2 = T.get_loc('2023-07-31 23:00:00')

# Cortamos series de tiempo
HCNM = HCNM[i1:i2+1]
T = T[i1:i2+1]



aux = pd.date_range('2018-01-01 00:00:00','2019-12-31 23:00:00',freq='H')
orig = pd.date_range('2018-02-01 00:00:00','2019-11-30 23:00:00',freq='H')
Voe = np.ones(len(orig))

dif = np.in1d(aux,orig)

Vfe = np.tile(np.nan,len(dif))
Vfe[dif] = Voe 


Vis('Centro_Quintero','HCNM','ppm','2018-01-01','2023-07-31','PorAño')

#%% Series Completas



#%% Ciclo diario

#%% Ciclo estacional

#%% Estadísticos 

#%%