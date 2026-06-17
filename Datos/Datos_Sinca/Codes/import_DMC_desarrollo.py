# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 18:49:09 2023

@author: felip
"""

import requests
import json
import pandas as pd
from import_DMC_Data import import_DMC
from Vis_DMC import Vis_DMC
import numpy as np

#%% Iteramos por meses y años requeridos


# Cargamos json del link
response = json.loads(requests.get("https://climatologia.meteochile.gob.cl/" \
                        +"application/servicios/getDatosRecientesEma/" \
                        +"320056?usuario=felipeacespedes@gmail.com&" \
                        +"token=TY5NjI2NTM0NzI4Mw==agNASh").text)

# normalizamos datos JSON a data frame
norm= pd.json_normalize( response['datosEstaciones']['datos'] )

# extraemos variables de interés
dat = norm.loc[:,['momento', 'fuerzaDelViento','direccionDelViento'\
                ,'temperatura','puntoDeRocio','humedadRelativa' \
                ,'presionEstacion','presionNivelDelMar','radiacionGlobalInst']]


#%% Experimentamos juntando en tiempo dos data frames de meses seguidos

correo = 'felipeacespedes@gmail.com'
apikey = 'TY5NjI2NTM0NzI4Mw==agNASh'
num = '320056'
mes = '01'
año = '2020'

# creamos data frame
dat = pd.DataFrame(columns=['momento', 'fuerzaDelViento','direccionDelViento'\
                ,'temperatura','puntoDeRocio','humedadRelativa' \
                ,'presionEstacion','presionNivelDelMar','radiacionGlobalInst'])

# Cargamos json del link
response1 = json.loads(requests.get("https://climatologia.meteochile.gob.cl/" \
                        +"application/servicios/getDatosRecientesEma/" \
                        +num+"/"+año+"/"+mes+"?usuario=" \
                        +correo+"&token="+apikey).text)

# normalizamos datos JSON a data frame
norm1= pd.json_normalize( response1['datosEstaciones']['datos'] )

# extraemos variables de interés
dat1 = norm1.loc[:,['momento', 'fuerzaDelViento','direccionDelViento'\
                ,'temperatura','puntoDeRocio','humedadRelativa' \
                ,'presionEstacion','presionNivelDelMar','radiacionGlobalInst']]
    
# concatenamos
dat = pd.concat([dat,dat1])

#%%
mes ='02'
# Cargamos json del link
response2 = json.loads(requests.get("https://climatologia.meteochile.gob.cl/" \
                        +"application/servicios/getDatosRecientesEma/" \
                        +num+"/"+año+"/"+mes+"?usuario=" \
                        +correo+"&token="+apikey).text)

# normalizamos datos JSON a data frame
norm2= pd.json_normalize( response2['datosEstaciones']['datos'] )

# extraemos variables de interés
dat2 = norm2.loc[:,['momento', 'fuerzaDelViento','direccionDelViento'\
                ,'temperatura','puntoDeRocio','humedadRelativa' \
                ,'presionEstacion','presionNivelDelMar','radiacionGlobalInst']]
    
# unimos con pd.concat

dat = pd.concat([dat,dat2]).sort_values('momento')

#%%
mes ='03'
# Cargamos json del link
response3 = json.loads(requests.get("https://climatologia.meteochile.gob.cl/" \
                        +"application/servicios/getDatosRecientesEma/" \
                        +num+"/"+año+"/"+mes+"?usuario=" \
                        +correo+"&token="+apikey).text)

# normalizamos datos JSON a data frame
norm3= pd.json_normalize( response3['datosEstaciones']['datos'] )

# extraemos variables de interés
dat3 = norm3.loc[:,['momento', 'fuerzaDelViento','direccionDelViento'\
                ,'temperatura','puntoDeRocio','humedadRelativa' \
                ,'presionEstacion','presionNivelDelMar','radiacionGlobalInst']]
    
# unimos con pd.concat

dat = pd.concat([dat,dat3]).sort_values('momento')

#%%

dat = dat.reset_index()
del dat['index']

#%% quitar unidades y dejar en float

# split y tomar solo la primera parte
dat['fuerzaDelViento'] = dat['fuerzaDelViento'].str.split(n=1).str[0].astype(float)


#%% Ahora probamos la función import_DMC
F1 = '2019/01'
F2 = '2023/09'
correo = 'felipeacespedes@gmail.com'
apikey = 'TY5NjI2NTM0NzI4Mw==agNASh'
num = '320056'

DMC = import_DMC(F1,F2,num,correo,apikey)

# Funciona!


# Guardamos el dataframe en archivo pickle

DMC.to_pickle('DMC.pkl')

#%% Cargamos el archivo 
DMC_cargadepickle = pd.read_pickle('DMC.pkl')

#%% Ahora probamos plotear las series

# Intentamos usando la función vis

# Mejor creamos otra fucnión especializada: Vis_DMC()

Vis_DMC('DMC.pkl','fuerzaDelViento','kt','Total')

# probamos cambiar la serie de tiempo por pd.range_time
Tr = pd.date_range(DMC_cargadepickle['momento'][0] \
    ,DMC_cargadepickle['momento'][len(DMC_cargadepickle['momento'])-1] \
        ,freq='15min')

# Ahora pasa que las series de timepo no coinciden, así que veremos:
# - qué elementos se repiten en la serie original.
# - qué elementos faltan en la serie origianl (29/02?).
# - 

#%% 1: Qué elementos se repiten

# Entonces, debemos reconocer si es que hay elementos en la matriz temporal T
# que salió de la función import_DMC()

# chequeamos si hay elementos que se repiten en la matriz DMC['T']
Alist = DMC_cargadepickle['momento']
    
# Compare length for unique elements
if(len(set(Alist)) == len(Alist)):

   print("All elements are unique.")
else:
   print("All elements are not unique.")

# Todos los elementos son únicos, entonces hay que chequear qué elementos
# faltan en la matriz T que se encuentran en Tr.

#%% 2: Qué elementos faltan 

# Chequeamos qué elementos faltan en la matriz T qué se encuentran en Tr
T = DMC_cargadepickle['momento']
Tr = pd.date_range(DMC_cargadepickle['momento'][0] \
    ,DMC_cargadepickle['momento'][len(DMC_cargadepickle['momento'])-1] \
        ,freq='15min')

# len(set(Tr) - set(T))

# rellenamos DAtos faltantes con NAn
# Ahora hacemos la intersección, de manera que en Vr queden 
# todos los datos necesarios de V y se desechen los que no
# indices T
Kt = np.in1d(T,Tr)
# indices Tr
Ktr = np.in1d(Tr,T)

# creamos dataframe con variable T
DMC_df = pd.DataFrame({'T': Tr})
V =   ['fuerzaDelViento','direccionDelViento'\
     ,'temperatura','puntoDeRocio','humedadRelativa' \
     ,'presionEstacion','presionNivelDelMar','radiacionGlobalInst']
    
Vnuevo = ['Velocidad','Dirección'\
         ,'T','Tpr','HR' \
         ,'P','Pnm','Rgi']
i = 0
for v in V: 

    # Array de datos original
    V = np.array(DMC_cargadepickle[v])

    # Array de datos requerida
    # primero la rellenamos con Nans
    Vr = np.tile(np.nan,len(Ktr))

    # Rellenamos Vr con datos de V de interés
    Vr[Ktr] = V[Kt]
    
    # Readjudicamos matriz con Nan a df
    DMC_df[Vnuevo[i]] = Vr
    
    # Conteo para cambiar columnas de DF 
    i = i + 1

#%% Finalfinalmente, probamos la función import_DMC()

F1 = '2019/01'
F2 = '2024/01'
correo = 'felipeacespedes@gmail.com'
apikey = 'TY5NjI2NTM0NzI4Mw==agNASh'
num = '320056'

DMC_df = import_DMC(F1,F2,num,correo,apikey)

# Guardamos el dataframe en archivo pickle
DMC_df.to_csv('DMC.csv')
