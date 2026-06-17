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
from corregir_series_fun import Corr_Ser
from import_var import import_var
from Vis_fun import Vis_Est
plt.style.use('bmh')

#%% Creamos pandas DataFrame para plotear e indexar

# Fechas inicial y final
Fi = '2018-01-01'
Ff = '2023-12-31'

# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

# Primero creamos df de HCNM con estaciones de interés
# le = [ 'Centro_Quintero', 'Colmo', 'Concón','Gaviotas', 'Junta_Vecinos'\
#       , 'Loncura', 'Los_Maitenes', 'Sur', 'Ventanas']
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


#%% Ploteo de varias estaciones

# Plotemamos las 9 estaciones:
Fi='2021-11-05'
Hi='00'
Ff='2021-11-17'
Hf='00'
y_min = 0
y_max = 2.0
Vis_Est(HCNM,'HCNM','ppm',Fi,Hi,Ff,Hf,y_min,y_max)

#%% Corregimos HCNM para estaciones solicitadas


#%% Centro_Quintero #%%

# Serie Original
CQ_or = HCNM['Centro_Quintero']
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 3.0
fig = plt.figure(figsize=(20,10))
plt.plot(T[i:f],CQ_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% 1: Corregimos periodo [01/09/18 00:00 - 16/10/18 16:00]

# Dividimos en 2 periodos

# 1ro: [01/01/18 00:00 - 31/08/18 23:00]
CQ_11 = Corr_Ser(T,CQ_or,'2018-01-01','00','2018-08-31','23', 'nan', 0)
# 2do: [01/09/18 00:00 - 14/09/18 09:00]
CQ_12 = Corr_Ser(T,CQ_11,'2018-09-01','00','2018-09-14','09', 'sum', -0.235)
# 3ro: [14/09/18 12:00 - 16/10/18 16:00]
CQ_13 = Corr_Ser(T,CQ_12,'2018-09-14','12','2018-10-16','16', 'sum', -0.253)

# Ploteamos para ver diferencia
i = T.get_loc('2018-08-15 00:00:00')
f = T.get_loc('2018-11-15 00:00:00')
y_min = 0
y_max = 3.0
fig = plt.figure(figsize=(10,6))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CQ_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CQ_13[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% 2: Corregimos [01/03/19 15:00 - 08/03/19 10:00]

CQ_2 = Corr_Ser(T,CQ_13,'2019-03-01','15','2019-03-08','10', 'sum', -0.055)

# Ploteamos para ver diferencia
i = T.get_loc('2019-02-15 00:00:00')
f = T.get_loc('2019-03-25 00:00:00')
y_min = 0
y_max = 0.2
fig = plt.figure(figsize=(10,6))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CQ_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CQ_2[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% 3: Corregimos [25/10/19 13:00 - 30/10/19 13:00]

CQ_3 = Corr_Ser(T,CQ_2,'2019-10-25','13','2019-10-30','13', 'nan', 0)

# Ploteamos para ver diferencia
i = T.get_loc('2019-10-20 00:00:00')
f = T.get_loc('2019-11-05 00:00:00')
y_min = 0
y_max = 0.2
fig = plt.figure(figsize=(10,6))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CQ_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CQ_3[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% 4: Corregimos [2021-09-10 12:00, 2021-09-16 10:00] y 
###    [19/11/21 18:00 - 04/01/22 18:00]


# 1ro: [2021-09-10 12:00, 2021-09-16 10:00]
CQ_41 = Corr_Ser(T,CQ_3,'2021-09-10','12','2021-09-16','10','nan',0.02)

# 2do: [19/11/21 18:00 - 09/12/21 12:00], sum
CQ_42 = Corr_Ser(T,CQ_41,'2021-11-19','12','2021-12-09','12', 'nan', 0.02)
# 3ro: [09/12/21 12:00 - 04/01/22 18:00], sum
CQ_43 = Corr_Ser(T,CQ_42,'2021-12-09','12','2022-01-04','18', 'nan', 0.03)

### Ejemplo a conversar con Rodrigo: Se observa que la variabilidad tiene 
### un cambio significativo en el tramo [09/12/21 12:00 - 04/01/22 18:00],
### es por esto que se estima relevante evaluar si solo aplicar cambios
### aplicando suma de una valor a periodo o tambien se debe aplicar un
### factor a estos datos con el fin de agrandar o disminuir variabilidad.

# # 2do: [09/12/21 12:00 - 04/01/22 18:00], sum
# CQ_42 = Corr_Ser(T,CQ_41,'2021-12-09','12','2022-01-04','18', 'sum', 0.03)
# # 3ro:[09/12/21 12:00 - 04/01/22 18:00], mult
# CQ_43 = Corr_Ser(T,CQ_42,'2021-12-09','12','2022-01-04','18', 'mult', 1.3)
 

# Ploteamos para ver diferencia
i = T.get_loc('2021-09-01 00:00:00')
f = T.get_loc('2022-04-01 00:00:00')
y_min = 0
y_max = 1.5
fig = plt.figure(figsize=(15,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CQ_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CQ_43[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% 5: Corregimos [12/08/22 14:00 - 12/09/22 12:00]

# 1ro: [12/08/22 14:00 - 19/08/22 10:00], sum
CQ_51 = Corr_Ser(T,CQ_43,'2022-08-12','14','2022-08-19','10', 'nan', 0.015)
# 2do: [19/08/22 12:00 - 04/09/22 00:00], sum
CQ_52 = Corr_Ser(T,CQ_51,'2022-08-19','12','2022-09-04','00', 'nan', -0.025)
# 3ro: [04/09/22 00:00 - 12/09/22 12:00], nan
CQ_53 = Corr_Ser(T,CQ_52,'2022-09-04','00','2022-09-12','12', 'nan', 0)

# Ploteamos para ver diferencia
i = T.get_loc('2022-08-01 00:00:00')
f = T.get_loc('2022-10-01 00:00:00')
y_min = 0
y_max = 0.5
fig = plt.figure(figsize=(15,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CQ_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CQ_53[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% 6: Corregimos [28/12/22 22:00 - 04/01/23 17:00]

# [28/12/22 22:00 - 04/01/23 17:00], sum
CQ_6 = Corr_Ser(T,CQ_53,'2022-12-28','22','2023-01-04','17','sum',-0.045)

# Ploteamos para ver diferencia
i = T.get_loc('2022-12-20 00:00:00')
f = T.get_loc('2023-01-10 00:00:00')
y_min = 0
y_max = 0.1
fig = plt.figure(figsize=(15,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CQ_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CQ_6[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Ploteamos resultado final para Centro_Quintero

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(25,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CQ_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CQ_6[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

# Agregamos serie a df modificado
HCNM_m['Centro_Quintero'] = CQ_6


#%% Colmo #%%

# Se debe arreglar el GAP del 2021

# Ver 2 periodos sospechosos:
    # - fin 2018: Desechamos datos previos a 2018-09-01 00:00 y corregimos
    #             datos entre 2018-09-01 00:00 y 2018-10-16 17:00
    # - fin 2019: Corregimos datos entre 

# Serie Original
CO_or = HCNM['Colmo']
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2020-03-01 00:00:00')
y_min = 0
y_max = 0.4
fig = plt.figure(figsize=(15,5))
plt.plot(T[i:f],CO_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% 1: Desechamos datos previos a [2018-09-01 00:00] y corregimos
###    datos entre [2018-09-01 00:00, 2018-10-16 17:00]

# 1ro: Hacemos Nan datos previos a [2018-09-01 00:00]
CO_11 = Corr_Ser(T,CO_or,'2018-01-01','00','2018-08-31','00','nan',0)

# 2do: Corregimos datos entre [2018-09-01 00:00, 2018-09-21 14:00]
CO_12 = Corr_Ser(T,CO_11,'2018-09-11','10','2018-09-21','14','sum',-0.04)


# Ploteamos para ver diferencia
# i = T.get_loc('2018-01-01 00:00:00')
# f = T.get_loc('2018-12-31 00:00:00')
i = T.get_loc('2018-09-01 00:00:00')
f = T.get_loc('2019-06-18 00:00:00')
y_min = 0
y_max = 0.4
fig = plt.figure(figsize=(22,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CO_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CO_12[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% 2: Corregimos datos entre [28/09/20, 18:00 - 19/06/21, 00:00] 

CO_2 = Corr_Ser(T,CO_12,'2020-09-28','18','2021-06-19','00','nan',0)
HCNM_m['Colmo'] = CO_2

# Ploteamos para ver diferencia
i = T.get_loc('2020-09-20 00:00:00')
f = T.get_loc('2021-08-01 00:00:00')
y_min = 0
y_max = 0.5
fig = plt.figure(figsize=(15,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CO_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CO_2[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Ploteamos resultado final para Colmo

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 1.5
# i = T.get_loc('2020-09-20 00:00:00')
# f = T.get_loc('2021-07-01 00:00:00')
# y_min = 0
# y_max = 0.4
fig = plt.figure(figsize=(25,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CO_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CO_2[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

# Agregamos serie a df modificado
HCNM_m['Colmo'] = CO_2

#%% Concón #%%

# Tomar desde 2021 y sacando apróximadamente Nov-Dic de 2021.

# Hay 2 tramos de interés:
    # 1.- [2021-11-10, 17:00 - 2021-11-11, 15:00]
    # 2.- [2021-11-10, 17:00 - 2021-12-15, 17:00]

# Considerar rutas:
    # - aplicar a 1 ('mult',2.25) y a 2 ('sum',0.4)
    # - aplicar a 1 ('sum',0.05)  y a 2 ('mult',6)
    # - aplicar una combinación de sum y mult a 1 y 2

# Esta última nos lleva a pensar cómo deberían escalarse los periodos 
# de las series en que los datos cambian de nivel base.

# *** Estudiar variabilidad típica de valores pertenecientes a un sector 
#     acotado de quantiles  (o sea, evitando grandes peaks e inusuales bajos 
#     valores) y de periodos con alta confiabilidad de datos, con tal de 
#     poder estimar periodos en los que ha habido un corrimiento de valores
#     o un cambio en la variabilidad de los datos.

# *** Estudiar índices de confiabilidad de datos en series de tiempo 

# AL final se ajustará periodo entre 2019/16 a 2020/06 aprox, revisar 
# figura total

# Serie Original
CC_or = HCNM['Concón']
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 00:00:00')
y_min = 0
y_max = 1.0
fig = plt.figure(figsize=(15,5))
plt.plot(T[i:f],CC_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% 1: Eliminamos datos entre [2018-01-01 00:00, 2018-10-01 00:00]

CC_1  = Corr_Ser(T,CC_or,'2018-01-01','00','2018-10-01','00','nan',0)

# Ploteamos para ver diferencia
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2020-10-01 00:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(15,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CC_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CC_1[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% 2: [2019-06, 2020-06]

CC_21 = Corr_Ser(T,CC_1,'2019-08-08','12','2020-08-14','12','sum',0.4)
CC_22 = Corr_Ser(T,CC_21,'2019-08-08','12','2019-08-31','00','nan',0)
CC_23 = Corr_Ser(T,CC_22,'2020-07-30','12','2020-08-18','00','nan',0)

# Ploteamos para ver diferencia
i = T.get_loc('2019-06-01 00:00:00')
f = T.get_loc('2020-10-01 00:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(15,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CC_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CC_23[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% 3: Elevar [2021-11-10, 17:00 - 2021-11-11, 15:00]
###    y luego elevar [2021-11-10, 17:00 - 2021-12-15, 17:00]

# Elevamos tramo pequeño [2021-11-10, 17:00 - 2021-11-11, 15:00]
# CC_3 = Corr_Ser(T,CC_or,'2021-11-10','17','2021-11-11','15','mult',2.25)
CC_31 = Corr_Ser(T,CC_23,'2021-11-10','17','2021-11-11','15','sum',0.05)

# Elevamos tramo completo [2021-11-10, 17:00 - 2021-12-15, 17:00]
# CC_3 = Corr_Ser(T,CC_2,'2021-11-10','17','2021-12-15','17','mult',6)
CC_32 = Corr_Ser(T,CC_31,'2021-11-10','17','2021-12-15','17','sum',0.4)

# Ploteamos para ver diferencia
i = T.get_loc('2021-11-05 00:00:00')
f = T.get_loc('2021-11-17 00:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(15,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CC_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CC_32[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Ploteamos resultado final para Concón

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 1.5
fig = plt.figure(figsize=(25,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],CC_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],CC_32[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

# Agregamos serie a df modificado
HCNM_m['Concón'] = CC_22


#%% Las Gaviotas #%%

# En figura total se muestra que se debe tomar desde aprox abril de 2021,
# pero además se observa una anomalía a principios del 2023.

# Serie Original
GA_or = HCNM['Gaviotas']
i = T.get_loc('2021-03-01 00:00:00')
f = T.get_loc('2021-07-01 00:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(15,5))
plt.plot(T[i:f],GA_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])


#%% 1: Tomar desde 06/21.

GA_1 = Corr_Ser(T,GA_or,'2018-01-01','00','2021-05-31','23','nan',0)

# Ploteamos para ver diferencia
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2022-01-01 00:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(15,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],GA_or[i:f])
ax1.set_xlim(T[i],T[f])
ax1.set_ylim(y_min,y_max)
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],GA_1[i:f])
ax2.set_xlim(T[i],T[f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()


#%% 2: Corregir principios de 2023.

# Debemos hacer Nan el tramo [2023-01-03 10:00, 2023-01-04 12:00]
GA_21 = Corr_Ser(T,GA_1,'2023-01-03','06','2023-01-04','12','nan',0)

# Luego ajustamos tramo [2023-01-04 12:00, 2023-01-18 11:00]
GA_22 = Corr_Ser(T,GA_21,'2023-01-04','12','2023-01-18','10','sum',-0.19)

# Ploteamos para ver diferencia
i = T.get_loc('2022-12-01 00:00:00')
f = T.get_loc('2023-03-01 00:00:00')
y_min = 0
y_max = 1.0
fig = plt.figure(figsize=(15,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],GA_or[i:f])
ax1.set_xlim(T[i],T[f])
ax1.set_ylim(y_min,y_max)
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],GA_22[i:f])
ax2.set_xlim(T[i],T[f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Ploteamos resultado final para Las Gaviotas

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 1.5
fig = plt.figure(figsize=(25,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],GA_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],GA_22[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

# Agregamos serie a df modificado
HCNM_m['Gaviotas'] = GA_22

#%% Junta de Vecinos #%%

### NO USAR!! ###
HCNM_m['Junta_Vecinos'] = Corr_Ser(T,HCNM['Junta_Vecinos'],'2018-01-01','00','2023-12-31','23'\
                  ,'nan',0)

JV_or = HCNM['Junta_Vecinos']    

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 1.5
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


#%% Loncura #%%

### NO USAR!! ###
HCNM_m['Loncura'] = Corr_Ser(T,HCNM['Loncura'],'2018-01-01','00','2023-12-31','23'\
                  ,'nan',0)
    
LO_or = HCNM['Loncura']    

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 1.5
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

#%% Los Maitenes #%%

# Ver figura: evaluar usar 2019, cortar serie desde año a determinar 
# (en la figura sale desde el 2020 pero se quiere ver si se salva 2019)
# y por último corregir 2021 e inicios del 2022.

# Serie Original
LM_or = HCNM['Los_Maitenes']
i = T.get_loc('2021-10-05 00:00:00')
f = T.get_loc('2021-10-06 00:00:00')
y_min = 0.025
y_max = 0.1
fig = plt.figure(figsize=(15,5))
plt.plot(T[i:f],LM_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% 1: Evaluamos 2019

# Tomamos desde 2019-06-01 00
LM_11 = Corr_Ser(T,LM_or,'2018-01-01','00','2019-05-31','23','nan',0)

# Corregir valores entre [2019-06-01 00:00, 2019-07-03 08:00]
# LM_12 = Corr_Ser(T,LM_11,'2019-06-01','00','2019-07-03','08','mult',1.1)
# LM_12 = Corr_Ser(T,LM_12,'2019-06-01','00','2019-07-03','08','sum',0.005)
LM_12 = Corr_Ser(T,LM_11,'2019-06-01','00','2019-07-03','08','sum',0.0055)

# Corregir valores entre [2019-07-03 10:00, 2019-09-24 16:00]
# LM_13 = Corr_Ser(T,LM_12,'2019-07-03','10','2019-09-24','16','mult',0.9)
# LM_13 = Corr_Ser(T,LM_13,'2019-07-03','10','2019-09-24','16','sum',-0.015)
LM_13 = Corr_Ser(T,LM_12,'2019-07-03','10','2019-09-24','16','sum',-0.022)


# Ploteamos para ver diferencia
i = T.get_loc('2019-01-01 00:00:00')
f = T.get_loc('2020-01-01 00:00:00')
y_min = 0
y_max = 0.1
fig = plt.figure(figsize=(18,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],LM_or[i:f])
ax1.set_xlim(T[i],T[f])
ax1.set_ylim(y_min,y_max)
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],LM_13[i:f])
ax2.set_xlim(T[i],T[f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

# Se decide utilizar 2019 desde junio

#%% 2: Corregir 2021 e inicios de 2022

# Corregimos periodo [2021-02-02 19:00, 2021-05-22 00:00]
LM_21 = Corr_Ser(T,LM_12,'2021-02-02','19','2021-05-22','00','sum',-0.01)

# Corregimos periodo [2021-08-06 18:00 , 2021-10-05 10:00]
LM_22 = Corr_Ser(T,LM_21,'2021-08-06','18','2021-10-05','10','sum',-0.005)


# Corregimos periodo [2021-05-22 12:00, 2021-09-28 12:00]
# LM_23 = Corr_Ser(T,LM_22,'2021-05-22','12','2021-09-28','12','mult',2.0)
# LM_23 = Corr_Ser(T,LM_22,'2021-05-22','12','2021-09-28','12','sum',-0.06)
LM_23 = Corr_Ser(T,LM_22,'2021-05-22','12','2021-09-28','12','nan',0)

# Corregimos periodo [2021-09-28 12:00, 2022-01-14 12:00]
LM_24 = Corr_Ser(T,LM_23,'2021-09-28','12','2022-01-14','12','sum',-0.02)


# Ploteamos para ver diferencia
i = T.get_loc('2021-01-01 00:00:00')
f = T.get_loc('2022-03-01 00:00:00')
y_min = 0
y_max = 0.1
fig = plt.figure(figsize=(18,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],LM_or[i:f])
ax1.set_xlim(T[i],T[f])
ax1.set_ylim(y_min,y_max)
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],LM_24[i:f])
ax2.set_xlim(T[i],T[f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Ploteamos resultado final para Los Maitenes

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 1.0
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
ax2.plot(T[i:f],LM_24[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

# Agregamos serie a df modificado
HCNM_m['Los_Maitenes'] = LM_24

#%% Sur ###

# No tomar periodo entre [2021-06 , 2022-05]

# Serie Original
SU_or = HCNM['Sur']
i = T.get_loc('2021-01-01 00:00:00')
f = T.get_loc('2022-12-01 00:00:00')
y_min = 0
y_max = 2.0
fig = plt.figure(figsize=(18,10))
plt.plot(T[i:f],SU_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% 1: Eliminamos periodo entre [2021-02-02 18:00, 2022-07-15 00:00]

SU_1 = Corr_Ser(T,SU_or,'2021-02-02','18','2022-07-15','00','nan',0)

# Ploteamos para ver diferencia
i = T.get_loc('2021-01-01 00:00:00')
f = T.get_loc('2023-01-01 00:00:00')
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
ax2.plot(T[i:f],SU_1[i:f])
ax2.set_xlim(T[i],T[f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% 2: Corregimos periodo entre [2022-09-28 12:00, 2022-10-12 11:00]

SU_2 = Corr_Ser(T,SU_1,'2022-09-28','12','2022-10-12','10','sum',-0.011)

# Ploteamos para ver diferencia
i = T.get_loc('2022-09-01 00:00:00')
f = T.get_loc('2022-11-01 00:00:00')
y_min = 0
y_max = 0.2
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
ax2.plot(T[i:f],SU_2[i:f])
ax2.set_xlim(T[i],T[f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% 3: Corregimos periodo entre [2022-11-03 17:00, 2022-11-11 12:00]

SU_3 = Corr_Ser(T,SU_2,'2022-11-03','17','2022-11-11','12','sum',-0.01)

# Ploteamos para ver diferencia
i = T.get_loc('2022-11-01 00:00:00')
f = T.get_loc('2022-11-15 00:00:00')
y_min = 0
y_max = 0.15
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
ax2.plot(T[i:f],SU_3[i:f])
ax2.set_xlim(T[i],T[f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Ploteamos resultado final para Sur

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 1.5
fig = plt.figure(figsize=(25,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],SU_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],SU_3[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

# Agregamos serie a df modificado
HCNM_m['Sur'] = SU_3

#%% Ventanas #%%

# tomamos a partir de 2018-10-26 00:00

# Serie Original
VE_or = HCNM['Ventanas']
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 0.5
fig = plt.figure(figsize=(15,10))
plt.plot(T[i:f],VE_or[i:f])
plt.ylim(y_min,y_max)
plt.xticks(rotation=20)
plt.title('Serie Original')
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

#%% 1: Eliminamos datos entre [2018-01-01 00:00, 2018-10-25 23:00]

VE_1 = Corr_Ser(T,VE_or,'2018-01-01','00','2018-10-25','23','nan',0)

# Ploteamos para ver diferencia
i = T.get_loc('2018-10-01 00:00:00')
f = T.get_loc('2018-11-01 23:00:00')
y_min = 0
y_max = 0.15
fig = plt.figure(figsize=(18,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],VE_or[i:f])
ax1.set_xlim(T[i],T[f])
ax1.set_ylim(y_min,y_max)
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],VE_1[i:f])
ax2.set_xlim(T[i],T[f])
ax2.set_ylim(y_min,y_max)
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

#%% Ploteamos resultado final para Sur

# Serie Original
i = T.get_loc('2018-01-01 00:00:00')
f = T.get_loc('2023-12-31 23:00:00')
y_min = 0
y_max = 1.5
fig = plt.figure(figsize=(25,10))
# Serie Original
ax1 = plt.subplot(2,1,1)
ax1.plot(T[i:f],VE_or[i:f])
ax1.set_ylim(y_min,y_max)
ax1.set_xlim(T[i],T[f])
ax1.set_title('Serie Original')
plt.xticks(rotation=20)
# Serie Modificada
ax2 = plt.subplot(2,1,2)
ax2.plot(T[i:f],VE_1[i:f])
ax2.set_ylim(y_min,y_max)
ax2.set_xlim(T[i],T[f])
ax2.set_title('Serie Modificada')
plt.xticks(rotation=20)
# Ajustamos figura
fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
plt.show()

# Agregamos serie a df modificado
HCNM_m['Ventanas'] = VE_1

#%% Creamos Tabla de Estadísticos de interés para series modificadas

# Asignamos 
HCNM_or_estd = HCNM.apply(lambda x: x.describe([.05,.25,.5,.75,.95]))
# HCNM_or_estd = HCNM_or_estd.drop(['freq','top','unique'],axis='index')
index = list(HCNM_or_estd.index); a, b = index[1], index[0]
index[0], index[1] = a, b
HCNM_or_estd = HCNM_or_estd.reindex(index)

HCNM_m_estd = HCNM_m.apply(lambda x: x.describe([.05,.25,.5,.75,.95]))
# HCNM_m_estd = HCNM_m_estd.drop(['freq','top','unique'],axis='index')
index = list(HCNM_m_estd.index); a, b = index[1], index[0]
index[0], index[1] = a, b
HCNM_m_estd = HCNM_m_estd.reindex(index)

# Exportamos a excell a carpeta de figuras
path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Estad/Total/'
HCNM_or_estd.to_excel(path+'HCNM_orig_estd.xlsx')
path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/Estad/Total/'
HCNM_m_estd.to_excel(path+'HCNM_mod_estd.xlsx')

# Guardamos df original, modificado y tabla de estadísticos
# como pkl en carpeta de datos sinca, además de el excell
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
HCNM.to_pickle(path+'HCNM_orig_df.pkl')
HCNM_m.to_pickle(path+'HCNM_mod_df.pkl')
HCNM_or_estd.to_pickle(path+'HCNM_orig_estd_df.pkl')
HCNM_or_estd.to_excel(path+'HCNM_orig_estd.xlsx')
HCNM_m_estd.to_pickle(path+'HCNM_mod_estd_df.pkl')
HCNM_m_estd.to_excel(path+'HCNM_mod_estd.xlsx')
