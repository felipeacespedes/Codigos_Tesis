# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:19:58 2024

@author: felip

Código para ejecutar función Ser_Corr() del modulo corregir_series_fun.py
con el fin de aplicar una corrección de valor medio a series SINCA.
"""

#%% Librerías

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from corregir_series_fun import Corr_Ser
from import_var import import_var, import_var_pf
from Vis_fun import Vis_Est
plt.style.use('bmh')

#%% Creamos pandas DataFrame para plotear e indexar

# Fechas inicial y final
Fi = '2018-01-01'
Ff = '2023-12-31'

# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

# Primero creamos df de HCNM con estaciones de interés
le = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura' \
     ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo']
    
le.append('T')
HCNM = pd.DataFrame(columns=le)
HCNM['T'] = T
HCNM = HCNM.set_index('T')
le.remove('T')
for e in le:
    HCNM[e] = import_var(e,'Cont','HCNM',Fi,Ff)
    
# Aparte creamos un DF con los datos finales modificados
le.append('T')
HCNM_m = pd.DataFrame(columns=le)
HCNM_m['T'] = T
HCNM_m = HCNM_m.set_index('T')
le.remove('T')

#%% Creamos DF para datos de velocidad y dirección de viento

# Fechas inicial y final
Fi = '2018-01-01'
Ff = '2023-12-31'

# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

# Primero creamos df de HCNM con estaciones de interés
le = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura' \
     ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo']
    
le.append('T')
WS = pd.DataFrame(columns=le)
WD = pd.DataFrame(columns=le)
WS['date'] = T
WD['date'] = T
WS = WD.set_index('date')
WD = WD.set_index('date')

le.remove('T')

for e in le:
    WS[e] = import_var(e,'Meteo','Vel',Fi,Ff)
    WD[e] = import_var(e,'Meteo','Dir',Fi,Ff)


#%% Ploteo de varias estaciones

# Plotemamos las 9 estaciones:
Fi='2018-01-01'
Hi='00'
Ff='2023-01-01'
Hf='00'
y_min = 0
y_max = 360
Vis_Est(WD,'wd','°',Fi,Hi,Ff,Hf,y_min,y_max)
y_min = 0
y_max = 10
Vis_Est(WS,'ws','m/s',Fi,Hi,Ff,Hf,y_min,y_max)



#%% Corregimos HCNM para estaciones solicitadas ###

#%% Centro_Quintero ###

# Serie Original
CQ_or = HCNM['Centro_Quintero']
i = T.get_loc('2022-06-01 00:00:00')
f = T.get_loc('2022-12-31 23:00:00')
y_min = 0
y_max = 0.5
fig = plt.figure(figsize=(20,10))
plt.plot(T[i:f],CQ_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% Hacemos nan periodos:

# [2018-01-01 00:00 - 2018-10-16 16:00]
CQ = Corr_Ser(T,CQ_or,'2018-01-01','00','2018-10-16','16','nan',0)

# [2019-03-01 15:00 - 2019-03-08 12:00]
CQ = Corr_Ser(T,CQ,'2019-03-01','15','2019-03-08','12','nan',0)

# [2021-11-19 12:00 - 2022-01-05 12:00]
CQ = Corr_Ser(T,CQ,'2021-11-19','12','2022-01-05','12','nan',0)

# [2022-08-11 15:00 - 2022-09-09 16:00]
# CQ = Corr_Ser(T,CQ,'2022-08-11','15','2022-09-09','16','nan',0)

# [2022-12-28 18:00 - 2023-01-04 18:00]
CQ = Corr_Ser(T,CQ,'2022-12-28','18','2023-01-04','18','nan',0)


#%%
# Fechas
date = '2023-07-01'
days = 30
i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')+datetime.timedelta(days=days))
y_min = 0
y_max = 0.5
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CQ_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CQ[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99]) 
plt.show()

# Agregamos serie a df modificado
HCNM_m['Centro_Quintero'] = CQ


#%% Colmo ###

# Serie Original
CO_or = HCNM['Colmo']
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(15,5))
plt.plot(T[i:f],CO_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% Hacemos Nan periodos:

# [2018-01-09 12:00 - 2018-01-30 12:00]
CO = Corr_Ser(T,CO_or,'2018-01-09','12','2018-01-30','12','nan',0)

# [2018-06-09 00:00 - 2018-06-12 18:00]
CO = Corr_Ser(T,CO,'2018-06-09','00','2018-06-12','18','nan',0)

# [2018-06-19 00:00 - 2018-06-24 00:00]
CO = Corr_Ser(T,CO,'2018-06-18','00','2018-07-07','12','nan',0)

# [2018-09-21 00:00 - 2018-11-06 00:00]
CO = Corr_Ser(T,CO,'2018-09-21','00','2018-11-06','00','nan',0)

# [2018-11-27 00:00 - 2018-12-05 00:00]
CO = Corr_Ser(T,CO,'2018-11-27','00','2018-12-05','00','nan',0)

# [2019-02-26 12:00 - 2019-03-14 00:00]
CO = Corr_Ser(T,CO,'2019-02-26','12','2019-03-14','00','nan',0)

# [2019-05-13 12:00 - 2019-05-17 00:00]
CO = Corr_Ser(T,CO,'2019-05-13','12','2019-05-17','00','nan',0)

# [2019-06-09 00:00 - 2019-06-29 00:00] HAcer
CO = Corr_Ser(T,CO,'2019-06-09','00','2019-06-29','00','nan',0)

# [2019-07-29 00:00 - 2019-11-15 00:00]
CO = Corr_Ser(T,CO,'2019-07-29','10','2019-11-15','00','nan',0)

# [2020-01-27 12:00 - 2020-01-31 00:00]
CO = Corr_Ser(T,CO,'2020-01-27','12','2020-01-31','00','nan',0)

# [2020-09-22 00:00 - 2021-06-19 10:00]
CO = Corr_Ser(T,CO,'2020-09-07','12','2021-06-19','10','nan',0)

# [2021-11-14 00:00 - 2021-12-04 00:00]
CO = Corr_Ser(T,CO,'2021-11-14','00','2021-12-04','00','nan',0)

# [2021-12-21 00:00 - 2022-01-18 00:00]
CO = Corr_Ser(T,CO,'2021-12-21','00','2022-01-18','00','nan',0)

# [2022-01-31 00:00 - 2022-03-01 00:00]
CO = Corr_Ser(T,CO,'2022-01-31','00','2022-03-01','00','nan',0)

# [2022-05-07 00:00 - 2022-05-17 00:00]
CO = Corr_Ser(T,CO,'2022-05-07','00','2022-05-17','00','nan',0)

# [2022-07-25 00:00 - 2022-09-08 00:00]
CO = Corr_Ser(T,CO,'2022-07-25','00','2022-09-08','00','nan',0)

# [2022-10-21 00:00 - 2022-11-03 00:00]
CO = Corr_Ser(T,CO,'2022-10-21','00','2022-11-03','00','nan',0)

# [2023-03-14 00:00 - 2023-03-24 00:00]
CO = Corr_Ser(T,CO,'2023-03-14','00','2023-03-24','00','nan',0)

# [2018-03-13 00:00 - 2018-03-21 00:00]
CO = Corr_Ser(T,CO,'2018-03-13','00','2018-03-21','00','nan',0)

#%%

# for m in np.arange(6,13,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2021-'+mes+'-01'
date = '2022-01-01'
days = 363*2
i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')
              +datetime.timedelta(days=days))
y_min = 0
y_max = 0.5
LOD = 0.05
alpha = 0.5
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CO_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
ax1.hlines(LOD,T[i],T[f],'r','--',alpha=alpha)
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CO[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
ax2.hlines(LOD,T[i],T[f],'r','--',alpha=alpha)
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%%
# Agregamos serie a df modificado
HCNM_m['Colmo'] = CO

#%% Concón ###

# Serie Original
CC_or = HCNM['Concón']
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2018-12-31 23:00:00')
y_min = 0
y_max = 3
fig = plt.figure(figsize=(15,5))
plt.plot(T[i:f],CC_or[i:f])
plt.hlines(0.05,T[i],T[f],'r','--',alpha=0.5)
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% Hacemos Nan periodos:

# [2018-01-01 - 2018-09-04]
CC = Corr_Ser(T,CC_or,'2018-01-01','00','2018-09-04','00','nan',0)

# [2018-11-25 - 2018-12-25]
CC = Corr_Ser(T,CC,'2018-11-25','00','2018-12-25','00','nan',0)

# [2019-01-08 - 2019-01-10]
CC = Corr_Ser(T,CC,'2019-01-08','00','2019-01-10','00','nan',0)

# [2019-02-04 - 2019-02-06]
CC = Corr_Ser(T,CC,'2019-02-04','00','2019-02-06','00','nan',0)

# [2019-03-09 - 2019-04-13]
CC = Corr_Ser(T,CC,'2019-03-09','00','2019-04-13','00','nan',0)

# [2019-08-08 - 2020-08-15]
CC = Corr_Ser(T,CC,'2019-08-08','00','2020-08-15','00','nan',0)

# [2021-11-10 - 2021-12-16]
CC = Corr_Ser(T,CC,'2021-11-10','00','2021-12-16','00','nan',0)

# [2020-09-06 - 2020-09-16]
CC = Corr_Ser(T,CC,'2020-09-06','00','2020-09-16','00','nan',0)


#%%

# Fecha
# Plotear 12 meses de un año
# for m in np.arange(1,13,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2021-'+mes+'-01'
#     days = 30
# Plotear 6 años disponibles
# for a in np.arange(18,24,1):
#     date = '20'+str(a)+'-01-01'
#     days = 364
    
#Plotear fecha de interes
date = '2018-01-01'
days = 364*6

i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')
              +datetime.timedelta(days=days))
y_min = 0
y_max = 4
LOD = 0.05
alpha = 0.5
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CC_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
ax1.hlines(LOD,T[i],T[f],'r','--',alpha=alpha)
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CC[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
ax2.hlines(LOD,T[i],T[f],'r','--',alpha=alpha)
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

# Agregamos serie a df modificado
HCNM_m['Concón'] = CC


#%% Las Gaviotas ###

# En figura total se muestra que se debe tomar desde aprox abril de 2021,
# pero además se observa una anomalía a principios del 2023.

# Serie Original
GA_or = HCNM['Gaviotas']
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(15,5))
plt.plot(T[i:f],GA_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])


#%% Hacemos Nan periodos:

# [2018-01-01 - 2020-04-01]
GA = Corr_Ser(T,GA_or,'2018-01-01','00','2020-04-01','00','nan',0)

# [2020-06-24 - 2020-12-04]
GA = Corr_Ser( T, GA,'2020-06-24','00','2020-12-04','00','nan',0)

# [2021-02-22 - 2021-04-06]
GA = Corr_Ser( T, GA,'2021-02-22','00','2021-04-21','00','nan',0)

# [2021-05-16 - 2021-05-20]
GA = Corr_Ser( T, GA,'2021-05-16','00','2021-05-20','00','nan',0)

# [2022-11-05 - 2023-01-19]
GA = Corr_Ser( T, GA,'2022-11-05','00','2023-01-19','00','nan',0)

# [2023-11-07 - 2023-11-30]
GA = Corr_Ser( T, GA,'2023-11-07','00','2023-11-30','00','nan',0)


#%%

# Fechas
# Plotear 12 meses de un año
# for m in np.arange(1,13,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2023-'+mes+'-01'
#     days = 30
    
# Plotear 6 años disponibles
# for a in np.arange(18,24,1):
#     date = '20'+str(a)+'-01-01'
#     days = 364
    
#Plotear fecha de interes
date = '2018-01-01'
days = 364*6

i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')
              +datetime.timedelta(days=days))
y_min = 0
y_max = 4
LOD = 0.05
alpha = 0.5
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],GA_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
ax1.hlines(LOD,T[i],T[f],'r','--',alpha=alpha)
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],GA[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
ax2.hlines(LOD,T[i],T[f],'r','--',alpha=alpha)
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Agregamos serie a df modificado
HCNM_m['Gaviotas'] = GA

#%% Junta de Vecinos ###

### NO USAR!! ###
HCNM_m['Junta_Vecinos'] = Corr_Ser(T,HCNM['Junta_Vecinos'],'2018-01-01','00','2023-12-31','23'\
                  ,'nan',0)

JV_or = HCNM['Junta_Vecinos']    

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(25,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],JV_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],HCNM_m['Junta_Vecinos'][i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% Loncura ###

### NO USAR!! ###
HCNM_m['Loncura'] = Corr_Ser(T,HCNM['Loncura'],'2018-01-01','00','2023-12-31'\
                             ,'23','nan',0)
    
LO_or = HCNM['Loncura']    

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(25,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],LO_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],HCNM_m['Loncura'][i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Los Maitenes ###

### NO USAR!! ###
HCNM_m['Los_Maitenes'] = Corr_Ser(T,HCNM['Los_Maitenes'],'2018-01-01','00'\
                                  ,'2023-12-31','23','nan',0)

LM_or = HCNM['Los_Maitenes']

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(25,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],LM_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],HCNM_m['Los_Maitenes'][i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()



#%% Sur ###

### NO USAR!! ###
HCNM_m['Sur'] = Corr_Ser(T,HCNM['Sur'],'2018-01-01','00','2023-12-31','23'\
                  ,'nan',0)

SU_or = HCNM['Sur']
 
# Ploteamos para ver diferencia
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 2.5
fig = plt.figure(figsize=(18,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],SU_or[i:f])
ax1.set_xlim(T[i],T[f])
ax1.set_ylim(y_min,y_max)
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],HCNM_m['Sur'][i:f])
ax2.set_xlim(T[i],T[f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% Ventanas ###

# tomamos a partir de 2018-10-26 00:00

# Serie Original
VE_or = HCNM['Ventanas']
i = T.get_loc('2018-10-01 00:00:00')
f = T.get_loc('2018-12-31 23:00:00')
y_min = 0
y_max = 0.2
fig = plt.figure(figsize=(15,5))
plt.plot(T[i:f],VE_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% Hacemos Nan periodo:
    
# [2018-01-01 00:00, 2018-10-25 23:00]
VE = Corr_Ser(T,VE_or,'2018-01-01','00','2018-10-25','23','nan',0)

# [2023-07-06 00:00, 2023-07-23 00:00]
VE = Corr_Ser(T,VE,'2023-07-06','00','2023-07-23','00','nan',0)

# [2023-12-18 07:00, 2023-12-18 09:00]
VE = Corr_Ser(T,VE,'2023-12-18','07','2023-12-18','09','nan',0)

#%%

# Fechas
# Plotear 12 meses de un año
# for m in np.arange(1,13,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2023-'+mes+'-01'
#     days = 30
    
# Plotear 6 años disponibles
# for a in np.arange(18,24,1):
#     date = '20'+str(a)+'-01-01'
#     days = 364
    
#Plotear fecha de interes
date = '2023-12-01'
days = 30

i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')
              +datetime.timedelta(days=days))
y_min = 0
y_max = 0.5
LOD = 0.05
alpha = 0.5
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],VE_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],VE[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Agregamos serie a df modificado
HCNM_m['Ventanas'] = VE


#%% Seteamos todo los datos menores al LOD como el LOD

# path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
# HCNM_m = pd.read_pickle(path+'HCNM_mod_df.pkl')

# LOD
cols = ['Ventanas','Centro_Quintero','Concón','Gaviotas','Colmo']
LOD = 0.05
HCNM_m_lod = HCNM_m.copy()
HCNM_m_lod[cols] = HCNM_m_lod[cols].applymap(lambda x: LOD if x <= LOD else x)

# Serie Original
HCNM.hist(column=cols,figsize=(6,6),bins=50,range=(0,0.5),sharey=True)    
plt.suptitle('Series sin procesar')
plt.tight_layout()    
# Serie modificada por inspección
HCNM_m.hist(column=cols,figsize=(6,6),bins=50,range=(0,0.5),sharey=True)
plt.suptitle('Series modificadas por inspección')
plt.tight_layout()
# Serie modificada y aplicando LOD
HCNM_m_lod.hist(column=cols,figsize=(6,6),bins=50,range=(0,0.5),sharey=True)
plt.suptitle('Series modificadas y aplicando LOD = '+str(LOD))
plt.tight_layout()

#%% Creamos Tabla de Estadísticos de interés para series modificadas

# Asignamos 
HCNM_estd = HCNM.apply(lambda x: x.describe([.05,.5,.95]))
# HCNM_estd = HCNM_estd.drop(['freq','top','unique'],axis='index')
index = list(HCNM_estd.index); a, b = index[1], index[0]
index[0], index[1] = a, b
HCNM_estd = HCNM_estd.reindex(index)

HCNM_m_estd = HCNM_m.apply(lambda x: x.describe([.05,.5,.95]))
# HCNM_m_estd = HCNM_m_estd.drop(['freq','top','unique'],axis='index')
index = list(HCNM_m_estd.index); a, b = index[1], index[0]
index[0], index[1] = a, b
HCNM_m_estd = HCNM_m_estd.reindex(index)

HCNM_m_lod_estd = HCNM_m_lod.apply(lambda x: x.describe([.05,.5,.95]))
# HCNM_m_estd = HCNM_m_estd.drop(['freq','top','unique'],axis='index')
index = list(HCNM_m_lod_estd.index); a, b = index[1], index[0]
index[0], index[1] = a, b
HCNM_m_lod_estd = HCNM_m_lod_estd.reindex(index)

# Exportamos a excell a carpeta de figuras
path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Estad/Total/'

HCNM_estd.to_excel(path+'HCNM_orig_estd.xlsx')
HCNM_m_estd.to_excel(path+'HCNM_mod_estd.xlsx')
HCNM_m_lod_estd.to_excel(path+'HCNM_mod_lod_estd.xlsx')

#%% Guardamos df original, modificado y tabla de estadísticos
# como pkl en carpeta de datos sinca, además de el excell
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
HCNM.to_pickle(path+'HCNM_orig_df.pkl')
HCNM.to_csv(path+'HCNM_orig_df.txt')
HCNM_m.to_pickle(path+'HCNM_mod_df.pkl')
HCNM_m.to_csv(path+'HCNM_mod_df.txt')
HCNM_m_lod.to_pickle(path+'HCNM_mod_lod_df.pkl')
HCNM_m_lod.to_csv(path+'HCNM_mod_lod_df.txt')
HCNM_estd.to_pickle(path+'HCNM_orig_estd_df.pkl')
HCNM_estd.to_excel(path+'HCNM_orig_estd.xlsx')
HCNM_m_estd.to_pickle(path+'HCNM_mod_estd_df.pkl')
HCNM_m_estd.to_excel(path+'HCNM_mod_estd.xlsx')
HCNM_m_lod_estd.to_pickle(path+'HCNM_mod_lod_estd_df.pkl')
HCNM_m_lod_estd.to_excel(path+'HCNM_mod_lod_estd.xlsx')

    
#%% Modificamos pkl a text para leer en R

# Creamos ruta de acceso y guardado
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'

# Leemos archivos pkl
# HCNM = pd.read_pickle(path+'HCNM_orig_df.pkl')
# HCNM_m = pd.read_pickle(path+'HCNM_mod_df.pkl')
# HCNM_m_lod = pd.read_pickle(path+'HCNM_mod_lod_df.pkl')

HCNM.index.names = ['date']
HCNM_m.index.names = ['date']
HCNM_m_lod.index.names = ['date']

# Guardamos como .csv
HCNM.to_csv(path+'HCNM_orig_df.csv')
HCNM_m.to_csv(path+'HCNM_mod_df.csv')
HCNM_m_lod.to_csv(path+'HCNM_mod_lod_df.csv')


#%% Creamos 1 DF por estación

# Estaciones con datos a utilizar:
le = ['Ventanas','Centro_Quintero','Concón','Colmo']

lea = ['VE','CQ','CC','CO']

# Creamos ruta de acceso y guardado
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'

# creamos DFs

#%% Vientos

WD[le].to_csv(path+'WD_df.csv')
WS[le].to_csv(path+'WS_df.csv')

#%% HCNM
ei = 0
for e in le:
    print(e)
    print(lea[ei])
    globals()[f'{lea[ei]}_df'] = pd.DataFrame({'date':T,'HCNM':HCNM_m[e]\
                                               ,'ws':WS[e], 'wd': WD[e]})
    globals()[f'{lea[ei]}_df'] = eval(f'{lea[ei]}_df').set_index('date')
    eval(f'{lea[ei]}_df').to_csv(path+lea[ei]+'_df.csv')
    ei = ei + 1

    




# hay que ver cómo asignar de manera correcta los valores de viento y HCNM a 
# cada data frame, para etso se debe comparar cada df de estacion por los 
# dfs de HCNM, WD y WS


#%%
########################################################
#%% Incluímos datos de 2024 a estaciones de interés  ###
########################################################

#%% Primero abordamos datos originales ###

## Importamos datos de serie originales y modificados
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'

# Datos Originales
HCNM_og = pd.read_csv(path+'HCNM_orig_df.csv')
HCNM_og['date'] = pd.to_datetime(HCNM_og['date'])
HCNM_og = HCNM_og.set_index('date')


## Importamos datos de de HCNM 2024, ***(queda pendiente Ws y Wd)***

# Creamos df con fechas de interés para rellenar
Fi = '2024-01-01 00:00:00'
Ff = '2024-08-30 00:00:00'
date = pd.date_range(Fi,Ff,freq='H')
cols = HCNM_og.columns
HCNM_24o = pd.DataFrame(index=date,columns=cols)

# Iteramos sobre estaciones de original
le = ['VE','LM','CQ','LO','SU','JV','CC','GA','CO']
ci = 0
for e in le:
    HCNM_24o[cols[ci]] = import_var_pf('Cont',path+'Datos_2024/Cont/'+e\
                                      +'_2024.csv', Fi, Ff)
    ci = ci+1

# Agregamos datos de 2024 a la cola
HCNM_og24 = pd.concat([HCNM_og,HCNM_24o], axis=0)

# Guardamos nuevamente los datos


#%% Segundo, inspeccionamos y aplicamos LOD a datos 2024

# La idea es inspeccionar cada una de las 5 estaciones haciendo Nan los
# los periodos con no tengan una variabilidad natural o que muestren un 
# cambio abrupto de nivel base. Luego, se quiere aplicar cota de LOD para 
# quitar datos que estén bajo el límite de detección del instrumento.

# Definimos lista de 5 estaciones a usar de red SINCA
les = ['Ventanas','Centro_Quintero','Concón','Gaviotas','Colmo']

# Datos Modificados (corrección por inspección y LOD)
HCNM_ml = pd.read_csv(path+'HCNM_mod_lod_df.csv')
HCNM_ml['date'] = pd.to_datetime(HCNM_ml['date'])
HCNM_ml = HCNM_ml.set_index('date')

# Creamos df vacío con estructura de HCNM_og24 y lo rellenamos
HCNM_ml24 = pd.DataFrame().reindex_like(HCNM_og24)
HCNM_ml24.loc['2018-01-01 00:00:00':'2023-12-31 23:00:00',:] = HCNM_ml

#%% Inspección 2024

# Fechas inicial y final

# Para HCNM_ml
# Fi = '2018-01-01 00:00:00'
# Ff = '2023-12-31 23:00:00'

# Para HCNM_og24
Fi = '2018-01-01 00:00:00'
Ff = '2024-08-30 00:00:00'


# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi,Ff,freq='H')

#%% Ventanas ###
################

# Serie Original
VE_og = HCNM_og24['Ventanas'].copy()
i = T.get_loc('2024-01-01 00:00:00')
f = T.get_loc('2024-08-30 00:00:00')
y_min = 0
y_max = 0.5
LOD = 0.05
fig = plt.figure(figsize=(20,7))
plt.plot(T[i:f],VE_og[i:f])
plt.hlines(LOD,T[i],T[f], color='r',linestyles='dashed', label='LOD'\
           , alpha=0.5)
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Ventanas, LOD='+str(LOD))
plt.legend()
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% modificamos

# [2023-12-20 - 2024-01-04]
VE = Corr_Ser(T,VE_og,'2023-12-20','12','2024-01-04','00','nan',0)

# [2024-03-02 - 2024-03-06] inicio marzo
VE = Corr_Ser(T,VE,'2024-03-02','00','2024-03-06','00','nan',0)

# [2024-03-27 - 2024-04-25] abril
VE = Corr_Ser(T,VE,'2024-03-27','12','2024-04-25','00','nan',0)

# [2024-07-30 - 2024-08-23] junio-agosto
VE = Corr_Ser(T,VE,'2024-07-30','00','2024-08-03','00','nan',0)

# [2024-08-08 - 2024-08-23] agosto
VE = Corr_Ser(T,VE,'2024-08-08','00','2024-08-23','00','nan',0)


#%% Revisamos serie

# Fechas
# Plotear 12 meses de un año
# for m in np.arange(1,9,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2024-'+mes+'-01'
#     days = 29
    
# Plotear fecha de interes
date = '2024-01-01'
days = 30*8

i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')
              +datetime.timedelta(days=days))
y_min = 0
y_max = 1
LOD = 0.05
alpha = 0.5
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],VE_og[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
ax1.hlines(LOD,T[i],T[f],'r','--',alpha=alpha)
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],VE[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
ax2.hlines(LOD,T[i],T[f],'r','--',alpha=alpha)
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% Aplicar LOD a serie y agregar a df 

# Aplicar LOD
LOD = 0.05
VE[VE <= LOD] = LOD

# Agregar df
HCNM_ml24.loc['2024-01-01 00:00:00':'2024-08-30 00:00:00','Ventanas'] = VE

#%% Centro Quintero ###
#######################

# Serie Original
CQ_og = HCNM_og24['Centro_Quintero'].copy()

# Plotear meses de un año
for m in np.arange(1,9,1):
    # Fechas    
    mes = '0'+str(m) if m<10 else str(m)
    date = '2024-'+mes+'-01'
    days = 29
    
# Plotear periodo desde 
# date = '2024-01-01'
# days = 30*8

    i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
    f = T.get_loc(pd.to_datetime(date+' 00:00:00')
                  +datetime.timedelta(days=days))
    
    # Fechas especificas
    # i = T.get_loc('2023-06-01 00:00:00')
    # f = T.get_loc('2024-08-30 00:00:00')
    y_min = 0
    y_max = 2
    LOD = 0.05
    fig = plt.figure(figsize=(20,9))
    plt.plot(T[i:f],CQ_og[i:f])
    plt.hlines(LOD,T[i],T[f], color='r',linestyles='dashed', label='LOD'\
               , alpha=0.5)
    plt.ylim(y_min,y_max)
    plt.xticks(rotation=20)
    plt.title('Centro Quintero, LOD='+str(LOD))
    plt.legend()
    fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% modificamos

# Por ahora, mentenemos original

CQ = CQ_og

# [2023-12-20 - 2024-01-04]
# CQ = Corr_Ser(T,CQ_og,'2023-12-20','12','2024-01-04','00','nan',0)


#%% Revisamos serie

# Fechas
# Plotear 12 meses de un año
# for m in np.arange(1,9,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2024-'+mes+'-01'
#     days = 29
    
# Plotear fecha de interes
date = '2024-01-01'
days = 30*8

i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')
              +datetime.timedelta(days=days))
y_min = 0
y_max = 1
LOD = 0.05
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CQ_og[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
ax1.hlines(LOD,T[i],T[f],'r','--',alpha=0.5)
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CQ[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
ax2.hlines(LOD,T[i],T[f],'r','--',alpha=0.5)
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% Aplicar LOD a serie y agregar a df 

# Aplicar LOD
LOD = 0.05
CQ[CQ <= LOD] = LOD

# Agregar df
HCNM_ml24.loc['2024-01-01 00:00:00':'2024-08-30 00:00:00'
              ,'Centro_Quintero'] = CQ

#%% Concón ###
##############

# Serie Original
CC_og = HCNM_og24['Concón'].copy()

# Plotear meses de un año
for m in np.arange(1,9,1):
    # Fechas    
    mes = '0'+str(m) if m<10 else str(m)
    date = '2024-'+mes+'-01'
    days = 29
    
# Plotear periodo desde 
# date = '2024-01-01'
# days = 30*8

    i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
    f = T.get_loc(pd.to_datetime(date+' 00:00:00')
                  +datetime.timedelta(days=days))
    
    # Fechas especificas
    # i = T.get_loc('2023-06-01 00:00:00')
    # f = T.get_loc('2024-08-30 00:00:00')
    y_min = 0
    y_max = 2
    LOD = 0.05
    fig = plt.figure(figsize=(20,9))
    plt.plot(T[i:f],CC_og[i:f])
    plt.hlines(LOD,T[i],T[f], color='r',linestyles='dashed', label='LOD'\
               , alpha=0.5)
    plt.ylim(y_min,y_max)
    plt.xticks(rotation=20)
    plt.title('Concón, LOD='+str(LOD))
    plt.legend()
    fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% modificamos

# [2024-01-12 - 2024-01-12]
CC = Corr_Ser(T,CC_og,'2024-01-11','12','2024-01-13','04','nan',0)

# [2024-01-16 - 2024-08-30]
CC = Corr_Ser(T,CC,'2024-01-16','12','2024-08-30','23','nan',0)


#%% Revisamos serie

# Fechas
# Plotear 12 meses de un año
# for m in np.arange(1,9,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2024-'+mes+'-01'
#     days = 29
    
# Plotear fecha de interes
date = '2024-01-01'
days = 30

i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')
              +datetime.timedelta(days=days))
y_min = 0
y_max = 1
LOD = 0.05
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CC_og[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
ax1.hlines(LOD,T[i],T[f],'r','--',alpha=0.5)
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CC[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
ax2.hlines(LOD,T[i],T[f],'r','--',alpha=0.5)
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% Aplicar LOD a serie y agregar a df 

# Aplicar LOD
LOD = 0.05
CC[CC <= LOD] = LOD

# Agregar df
HCNM_ml24.loc['2024-01-01 00:00:00':'2024-08-30 00:00:00'
              ,'Concón'] = CC

#%% Gaviotas ###
################

# Serie Original
GA_og = HCNM_og24['Gaviotas'].copy()

# Plotear meses de un año
# for m in np.arange(1,9,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2024-'+mes+'-01'
#     days = 29
    
# Plotear periodo desde 
# date = '2024-01-01'
# days = 30*8

# i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
# f = T.get_loc(pd.to_datetime(date+' 00:00:00')
#               +datetime.timedelta(days=days))

# Fechas especificas
i = T.get_loc('2024-03-01 00:00:00')
f = T.get_loc('2024-04-30 00:00:00')
y_min = 0
y_max = 2
LOD = 0.05
fig = plt.figure(figsize=(20,9))
plt.plot(T[i:f],GA_og[i:f])
plt.hlines(LOD,T[i],T[f], color='r',linestyles='dashed', label='LOD'\
           , alpha=0.5)
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Gaviotas, LOD='+str(LOD))
plt.legend()
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% modificamos

# [2024-03-22 - 2024-04-03]
GA = Corr_Ser(T,GA_og,'2024-03-22','06','2024-04-03','00','nan',0)


#%% Revisamos serie

# Fechas
# Plotear 12 meses de un año
# for m in np.arange(1,9,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2024-'+mes+'-01'
#     days = 29
    
# Plotear fecha de interes
date = '2024-01-01'
days = 30*8

i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')
              +datetime.timedelta(days=days))
y_min = 0
y_max = 1
LOD = 0.05
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],GA_og[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
ax1.hlines(LOD,T[i],T[f],'r','--',alpha=0.5)
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],GA[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
ax2.hlines(LOD,T[i],T[f],'r','--',alpha=0.5)
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% Aplicar LOD a serie y agregar a df 

# Aplicar LOD
LOD = 0.05
GA[GA <= LOD] = LOD

# Agregar df
HCNM_ml24.loc['2024-01-01 00:00:00':'2024-08-30 00:00:00'
              ,'Gaviotas'] = GA

#%% Colmo ###
#############

# Serie Original
CO_og = HCNM_og24['Colmo'].copy()

# Plotear meses de un año
# for m in np.arange(1,9,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2024-'+mes+'-01'
#     days = 29
    
# Plotear periodo desde 
# date = '2024-01-01'
# days = 30*8

# i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
# f = T.get_loc(pd.to_datetime(date+' 00:00:00')
#               +datetime.timedelta(days=days))

# Fechas especificas
i = T.get_loc('2024-04-20 00:00:00')
f = T.get_loc('2024-04-30 00:00:00')
y_min = 0
y_max = 0.75
LOD = 0.05
fig = plt.figure(figsize=(20,9))
plt.plot(T[i:f],CO_og[i:f])
plt.hlines(LOD,T[i],T[f], color='r',linestyles='dashed', label='LOD'\
           , alpha=0.5)
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Colmo, LOD='+str(LOD))
plt.legend()
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% modificamos

# Este periodo se ve con variabilidad extraña, pero por ahora se dejará
# [2024-01-16 - 2024-04-24]
# CO = Corr_Ser(T,CO_og,'2024-01-16','00','2024-04-24','00','nan',0)
CO = CO_og

#%% Revisamos serie

# Fechas
# Plotear 12 meses de un año
# for m in np.arange(1,9,1):
#     # Fechas    
#     mes = '0'+str(m) if m<10 else str(m)
#     date = '2024-'+mes+'-01'
#     days = 29
    
# Plotear fecha de interes
date = '2024-01-01'
days = 30*8

i = T.get_loc(pd.to_datetime(date+' 00:00:00'))
f = T.get_loc(pd.to_datetime(date+' 00:00:00')
              +datetime.timedelta(days=days))
y_min = 0
y_max = 1
LOD = 0.05
fig = plt.figure(figsize=(20,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CO_og[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
ax1.hlines(LOD,T[i],T[f],'r','--',alpha=0.5)
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CO[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
ax2.hlines(LOD,T[i],T[f],'r','--',alpha=0.5)
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% Aplicar LOD a serie y agregar a df 

# Aplicar LOD
LOD = 0.05
CO[CO <= LOD] = LOD

# AgreCOr df
HCNM_ml24.loc['2024-01-01 00:00:00':'2024-08-30 00:00:00'
              ,'Colmo'] = CO

#%% Ploteamos expoloratoriamente
#%% Todas las estaciones
date_1 = pd.to_datetime('2023-06-01 00:00:00')
date_2 = pd.to_datetime('2024-08-30 23:00:00')
HCNM_ml.loc[date_1:date_2,cols]\
    .plot(subplots=True, layout=(9,1), ylabel='[ppm]'\
    , grid=True, figsize=(10,15), ylim=(0,4))
plt.suptitle('2024')
plt.tight_layout()

#%% 1 estación
date_1 = pd.to_datetime('2023-06-01 00:00:00')
date_2 = pd.to_datetime('2023-12-31 23:00:00')
HCNM_ml.loc[date_1:date_2,'Gaviotas']\
    .plot(ylabel='[ppm]', grid=True, figsize=(10,5), ylim=(0,1.5))
plt.suptitle('2024')
plt.tight_layout()

#%% Guardamos DF de datos 2018-2023+2024

# Definimos path
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'

# Cambiamos le nombre de index a date (para R) antes de guardar
HCNM_og24.index.names = ['date']
HCNM_ml24.index.names = ['date']

# Guardamos datos originales, ahora incluyendo 2024 
HCNM_og24.to_pickle(path+'HCNM_orig_+24_df.pkl')
HCNM_og24.to_csv(path+'HCNM_orig_+24_df.txt')
HCNM_og24.to_csv(path+'HCNM_orig_+24_df.csv')

# Guardamos datos modificados y con LOD, ahora incluyendo 2024 
HCNM_ml24.to_pickle(path+'HCNM_mod_lod_+24_df.pkl')
HCNM_ml24.to_csv(path+'HCNM_mod_lod_+24_df.txt')
HCNM_ml24.to_csv(path+'HCNM_mod_lod_+24_df.csv')







