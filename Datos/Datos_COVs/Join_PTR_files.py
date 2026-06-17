# -*- coding: utf-8 -*-
"""
Created on Thu May  9 13:29:16 2024

@author: felip

Código para unir los archivos del PTR diarios de salida .txt en un archivo
 .csv que contenga toda la serie de tiempo para los compuestos de interés
"""

#%% Importamos librerías 

import pandas as pd
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt

#%% Preparamos importación archivos de texto 

# Señalamos el path al directorio de los archivos .txt
path_f = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'+\
       'rawdata_invierno/daily_files_invierno/'
       
# Enlistamos los archivos existentes
files = os.listdir(path_f)
names=[];months=[]
for f in files: 
    names.append(f[0:-4])
    months.append(f[0:3])
    
# Pasamos a np.array() para facilitar tratamiento
names = np.array(names)
months = np.array(months)

# Ordenamos nombres de archivos por fechas
mes_abrev = ['jan','feb','mar','apr','may','jun'\
             ,'jul','aug','sep','oct','nov','dec'] 
names_srtd = np.empty(0)
for m in mes_abrev:
    names_srtd = np.append(names_srtd,names[m==months])

# Definimos variable de nombres de files, ya ordenados
names_f = names_srtd

del f, m, mes_abrev, months, files, names, names_srtd
#%% Importamos archivos .txt a DataFrames por día

# Creamos diccionario para importar cómo DataFrame cada archivo diario 
# y asignarle su respectivo nombre en dict_files y guardando los nombres
# de las  columnas en diccionario dict_cols
dict_files = {}
dict_cols = {}
for n in names_f:
    # leemos archivos .txt
    dict_files[n] = pd.read_csv(path_f+n+'.txt', sep="	")
    # extraemos nombres de la columnas para modificarlos
    dict_cols[n] = list(dict_files[n].columns)
    ci = 3
    # modificamos nombre de los compuestos
    for c in dict_cols[n][3:len(dict_cols[n])]:
        if float(c[1:8]) < 100:
            dict_files[n].rename(columns={c:c[9:-8]},inplace=True)
            dict_cols[n][ci] = c[9:-8]; ci = ci+1
        else:
            dict_files[n].rename(columns={c:c[10:-8]},inplace=True)
            dict_cols[n][ci] = c[10:-8]; ci = ci+1
del n, c, ci, path_f
#%% Inspeccionamos y decidimos qué columnas dejar 

# Para homogeneizar los dataframes diarios se escoger una lista de columnas
# tipo para aplicar a todos, de manera de reemplazar los nombres de compuestos
# necesarios (cómo C4H8 por Butenes), extraer las columnas sobrantes y añadir
# las columnas faltantes con valores Nan.

# Las columnas tipo utilizar serán las de aug_28_22:
cols_use =  np.array(dict_cols['aug_28_22'])

# ['AbsTime', 'RelTime', 'Cycle', 'Formaldehyde', 'Methanol',
# 'Acetonitrile', 'Propene_Cyclopropane', 'Acetaldehyde', 'Ethanol',
# 'Butenes', 'Acetone_propanal', 'Acetic_acid_Glycolaldehyde',
# 'Dimethyl sulfide', 'Furan', 'Isoprene', 'Methacrolein_MVK',
# 'Butanone_Butanal', 'Benzene', 'Toluene', 'Phenol', 'Benzonitrile',
# 'Styrene', 'Ethyl benzene_Xylenes', 'Cresol', 'Benzofuran',
# 'C9_Aromatics', 'Naphthalene', 'Monoterpenes']

# , las de aug_27_22 trae C4H8 y C9H12 en vez de Butenes y C9_Aromatics
# , respectivamente, que son las que traen el resto de archivos, excepto
# por oct_27_22 y oct_30_22 que traen Peroxyacetyl nitrate.


# Modificamos los DataFrames que tengan columnas diferentes a la elegida
# agregando columnas de Nan a las inexistentes y quitando las sobrantes.
# Se deben reemplazar también los compuestos:
# C4H8 -> Butenes
# C9H12 -> C9_Aromatics

for n in names_f:
    # Transformamos a np.array para facilitar tratamiento
    dict_cols[n] = np.array(dict_cols[n])
    
    # Vemos si hay diferencias
    if len(np.setdiff1d(dict_cols[n],cols_use))>0 or \
       len(np.setdiff1d(cols_use,dict_cols[n]))>0:
           
        # Notificamos diferencia
        print('Archivo '+n+' se está modificando. ')
        
        # Renombramos columna C4H8
        if sum((dict_cols[n]=='C4H8').astype(int))>0:
            dict_cols[n][dict_cols[n]=='C4H8'] = 'Butenes'
            print('- El nombre de la columna C4H8 ha sido reemplazado'+\
                  ' por Butenes.')
            
        # Renombramos columna C9H12
        if sum((dict_cols[n]=='C9H12').astype(int))>0:
            dict_cols[n][dict_cols[n]=='C9H12'] = 'C9_Aromatics'
            print('- El nombre de la columna C9H12 ha sido reemplazado'+\
                  ' por C9_Aromatics.')
                
        # Quitamos columnas extras
        if len(np.setdiff1d(dict_cols[n],cols_use))>0:
            for d in np.setdiff1d(dict_cols[n],cols_use):
                dict_files[n] = dict_files[n].drop(columns=d)
                print('- La columna '+d+' ha sido extraída.')
            del d
                
        # Agregamos columnas faltantes
        if len(np.setdiff1d(cols_use,dict_cols[n]))>0:
            for d in np.setdiff1d(cols_use,dict_cols[n]):
                i = np.where(cols_use==d); 
                nan = np.emtpy(len(dict_files[n].index))
                nan[:] = np.nan; nan = pd.Series(nan) 
                dict_files[n] = dict_files[n].insert(i,d,nan)
                print('- La columna '+d+' ha sido añadida con valores Nan.')
            del d
del n

# Por último, transformamos la columna de Abstime a datetime y botamos RelTime
for n in names_f:
    dict_files[n] = dict_files[n].drop(columns='RelTime')
    dict_files[n] = dict_files[n].rename(columns={'AbsTime':'date'})
    dict_files[n]['date'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(\
                            dict_files[n]['date'],unit='D')
del n

#%% Borrar secciones con un alto nivel de error

# Se usaran 2 modalidades para hacer Nan secciones de la serie con alto valor 
# de error:
    # - en base a archivos de texto RMSE
    # - en base a introducción manual de rango de segundos
    #   de días determinados, esto anotación o screenshot
# , la idea es que en procesamientos futuros SIEMPRE SE GUARDE EL ARCHIVO DE
# RMSE con tal de que este solo sea leído por el código y automaticamente 
# pueda determinar qué secciones de la serie de tiempo se deben hacer Nan.

# La cota superior para determinar un alto nivel de error corresponderá a 
# 3*10^-3.

#%% Borrar en base a archivos RMSE.txt

# Definimos path a carpeta de archivos de RMSE
path_r = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'+\
               'rawdata_invierno/rmse_masscal_invierno/'

# Enlistamos los archivos existentes
files = os.listdir(path_r)
names=[];months=[]
for f in files: 
    names.append(f[0:-4])
    months.append(f[5:8])
    
# Pasamos a np.array() para facilitar tratamiento
names = np.array(names)
months = np.array(months)

# Ordenamos nombres de archivos por fechas
mes_abrev = ['jan','feb','mar','apr','may','jun'\
             ,'jul','aug','sep','oct','nov','dec'] 
names_srtd = np.empty(0)
for m in mes_abrev:
    names_srtd = np.append(names_srtd,names[m==months])
    
# Definimos variable de nombres de RMSE, ya ordenados
names_r = names_srtd


# Importamos errores a DataFrames diarios 
dict_rmse = {}
for n in names_r:
    # leemos archivos .txt
    dict_rmse[n] = pd.read_csv(path_r+n+'.txt', sep="	")
    
    # Aplicamos cota de RMSE < 3*10^-3 a día correspondiente
    cota = (dict_rmse[n]['RMS Mass Error'] < (3*10**-3)).astype(int)
    cota = cota.replace(0,np.nan)
    dict_files[n[5:11]+'_22'].iloc[:,2:27] = dict_files[n[5:11]+'_22']\
                                             .iloc[:,2:27]*cota[:,None]
                                             
del f, m, mes_abrev, months, files, names, names_srtd, n, cota
                                       

#%% Borrar en base a introducción manual

# Se debe hacer revisión de:
    # - anotaciones de mis cuadernos (Felipe)
    # - anotaciones de Natalia
    # - screenshots de RMSE

# Seguimos utilizando el diccionario e ingresando manualmente

print('A continuación se preguntarán:\n'\
      +"    1. el día a ingresar en formato aug_31.\n"\
      +'    2. el nro. de rangos a definir cómo NaN.\n'\
      +'    3. cada rango, de menor a mayor, cómo:\n'\
      +'        3.1. ciclo inicial de rango n.\n'\
      +'        3.2. ciclo final de rango n.')
sn = 'si'
while sn == 'si' or sn == 'sí':
    # día a ingresar
    dia = str(input("Día a ingresar (ej. aug_31): "))
    
    # nro. de rangos a ingresar para ese día
    rangos = int(input('Nro. de rangos que desea ingresar para '+dia+':'))
    
    # creamos cota como array de 1s a partir del largo del día a modificar
    # y que luego se rellenará con NaNs en los rangos ingresados
    cota = np.ones(len(dict_files[dia+'_22'].index))
    
    # ahora iteramos en el nro. de días
    for n in np.arange(1,rangos+1,1):
        # definimos ciclos inicial y final
        print('Rango '+str(n)+':')
        ri = np.empty(rangos); rf = np.empty(rangos)
        ri[n-1] = int(input('Ingrese ciclo inicial:'))
        rf[n-1] = int(input('Ingrese ciclo final:'))
        if rf[n-1]<ri[n-1]:
            print('El ciclo final es menor al ciclo inicial.\n'\
                  +'Reingrese los ciclos inicial y final.')
            ri[n-1] = int(input('Ingrese ciclo inicial:'))
            rf[n-1] = int(input('Ingrese ciclo final:'))
        if n>1 and len(rf)>=2 and ri[n-1]<=rf[n-2]:
            print('El ciclo inicial ingresado es menor al ciclo final'\
                  +' anterior. Reingrese los ciclos inicial y final.')
            ri[n-1] = int(input('Ingrese ciclo inicial:'))
            rf[n-1] = int(input('Ingrese ciclo final:'))
        # aplicamos rangos a ciclos de cota
        cota[int(ri[n-1])-1:int(rf[n-1])-1] = np.nan
    # pasamos a pandas series
    cota = pd.Series(cota)
    # aplicamos el vector cota al DataFrame del día
    dict_files[dia+'_22'].iloc[:,2:27] = dict_files[dia+'_22']\
                                             .iloc[:,2:27]*cota[:,None]
    # guardamos el la serie en el diccionario de RMSE
    dict_rmse['rmse_'+dia] = cota
    
    # redefinimos sn para saber si seguimos ingresando días o no
    sn = str(input('Desea ingresar otro día? '))
    
else:
    print('Ingreso terminado.')
    



#%% Guardar y cargar diccionario dict_files en pickle file

# directorio
path_p = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'+\
                'rawdata_invierno/'
# # guardamos diccionaro
# with open(path_p+'dict_files.pkl', 'wb') as f:
#     pickle.dump(dict_files, f)
    
# cargamos de vuelta
with open(path_p+'dict_files.pkl', 'rb') as f:
    dict_files = pickle.load(f)
del path_p, f
#%% Ahora debemos unir los DFs

# Para esto debemos:
    # - concatenar todos los DFs
    # - resamplear por minuto
    # - crear data frame con fechas para ir rellenando


# Concatenamos todos los DFs por fecha
concat_df = dict_files[names_f[0]]
for n in names_f[1:len(names_f)]:
    concat_df = pd.concat([concat_df,dict_files[n]], axis=0)
    
# Reseteamos el indice, cambiamos por date, resampleamos por minuto
# y quitamos columna de index
concat_df = concat_df.reset_index()
concat_df = concat_df.set_index('date')

# hasta aquí me sirve para ver el df secundario
#%%
concat_df = concat_df.resample('1min').mean()
concat_df = concat_df.drop(columns=['index'])


# Creamos DF con fechas y aplicamos reindex, rellenando con NaN
date = pd.date_range(concat_df.index[0]\
                     ,concat_df.index[len(concat_df.index)-1]\
                     , freq = '1min')
data_df = concat_df.reindex(date,fill_value=np.nan)

del date, n 
#%% Comparamos Butenes y C9 Aromatics

# Me di cuenta que se incluye 2 variables reiteradas, se compararán
# para ver si son las mismas

# Butenes
But = ['C4H8','Butenes']
ax = data_df[But].plot(subplots=True, layout=(2,1), grid=True\
                        , figsize=(10,5))#,ylim=(-5,300))
plt.tight_layout()

# C9 Aromatics
C9Ar = ['C9H12','C9_Aromatics']
ax = data_df[C9Ar].plot(subplots=True, layout=(2,1), grid=True\
                        , figsize=(10,5))#,ylim=(-5,300))
plt.tight_layout()

# Se concluye que los nombres de moleculas solo traen el inicio de 
# la serie, mientras que los nombres de compuesto traen la serie completa.
# Además, los nombres de compuestos deben reemplazarse en los lugares 
# de los nombres de moleculas.

del But, C9Ar, ax
#%% Modificamos Butenes y C9 Aromatics, y cambiamos nombres de columnas

# Reemplazamos C4H8 y C9H12 por Butenes y C9_Aromatics, respectivamente
data_df['C4H8'] = data_df['Butenes']
data_df['C9H12'] = data_df['C9_Aromatics']
data_df = data_df.drop(columns=['Butenes','C9_Aromatics'])
data_df = data_df.rename(columns={'C4H8':'Butenes', 'C9H12':'C9_Aromatics'})

# Reemplazamos columnas por las de archivos de Rodrigo
cols_og = ['Cycle', 'Formaldehyde', 'Methanol', 'Acetonitrile',
       'Propene_Cyclopropane', 'Acetaldehyde', 'Ethanol', 'Butenes',
       'Acetone_propanal', 'Acetic.acid_Glycolaldehyde', 'Dimethyl.sulfide',
       'Furan', 'Isoprene', 'Methacrolein_MVK', 'Butanone_Butanal', 'Benzene',
       'Toluene', 'Phenol', 'Benzonitrile', 'Styrene', 'Ethyl.benzene_Xylenes',
       'Cresol', 'Benzofuran', 'C9_Aromatics', 'Naphthalene', 'Monoterpenes']
data_df.columns = cols_og

# guardamos serie secundaria
# path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
# data_df = data_df.drop('Cycle',axis=1)
# data_df.to_csv(path+'inv_data_prelim_1seg.csv',sep=';',index_label='date'\
#             , date_format='%d/%m/%Y %H:%M:%S')

# Y listo!, ahora se puede cortar y concatenar con la serie de Rodrigo
del cols_og
#%% Ploteamos exploratoriamente serie completa 
BETX = ['Benzene','Toluene','Ethyl.benzene_Xylenes']

ax = data_df[BETX].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,5),ylim=(-5,300))
plt.tight_layout()

#%% Cortamos días que nos sirven

# Días mayores a '2022-09-23 00:00:00'
newdata_df = data_df.loc[data_df.index >= \
                         pd.to_datetime('2022-09-23 00:00:00')]

#%% Ploteamos exploratoriamoente serie nueva

newdata_df.loc[pd.to_datetime('2022-10-03 00:00:00')\
               :pd.to_datetime('2022-10-05 12:00:00')\
                   ,'Propene_Cyclopropane'].plot()

#%% Pegamos días dataframe de Rodrigo con newdata_df

# Cargamos df Rodrigo
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
file = 'voc_min_UTC_4.csv'; freq = '1m'
ROD = pd.read_csv(path+file,delimiter=';')
ROD['date'] = pd.to_datetime(ROD['date'],format='%d/%m/%Y %H:%M:%S')
ROD['date'] = pd.to_datetime(ROD['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
ROD = ROD.set_index('date'); ROD= ROD.iloc[0:-1,0:26]
# Aplicamos .iloc[0:-1,0:26] para no tomar el último valor de todas las
# columnas ('2022-09-23 00:00:00'), ya que este es incluido en data df, y 
# tomamos hasta la columna 26 ya que se incluyen repeticiones a partir de esta.

# Por último, concatenamos ambos dfs
DATA = pd.concat([ROD,newdata_df], axis=0)
DATA = DATA.drop('Cycle',axis=1)
DATA.to_csv(path+'inv_data_prelim.csv',sep=';',index_label='date'\
            , date_format='%d/%m/%Y %H:%M:%S')

# Conchale y esto es todo amigues <3

#%% Cargamos Data
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
DATA = pd.read_csv(path+'inv_data_prelim_1min.csv',delimiter=';')
DATA['date'] = pd.to_datetime(DATA['date'],format='%d/%m/%Y %H:%M:%S')
DATA['date'] = pd.to_datetime(DATA['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
DATA = DATA.set_index('date')
BETX = ['Benzene','Toluene','Ethyl.benzene_Xylenes'] 
#%% Ploteamos exploratoriamente
ax = DATA[BETX].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,5),ylim=(-5,100))
plt.tight_layout()

#%% Peak 1

# Evento
date_1 = pd.to_datetime('2022-09-02 09:30:00')
date_2 = pd.to_datetime('2022-09-02 11:30:00')
# low def
ax = DATA.loc[date_1:date_2\
             ,BETX].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,5),ylim=(-5,500))
plt.suptitle('Evento 02-09, tramo cortado, freq=1m')
plt.tight_layout()

# Peak enorme específico
date_1 = pd.to_datetime('2022-09-02 10:47:00')
date_2 = pd.to_datetime('2022-09-02 10:52:00')
# high def
ax = concat_df.loc[date_1:date_2\
             ,['Benzene','Toluene','Ethyl benzene_Xylenes']\
             ].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,5),ylim=(-5,2500))

plt.suptitle('Zoom a peak principal evento 02-09, freq=1s')
plt.tight_layout()
                         
#%% Peak 2

# Evento
date_1 = pd.to_datetime('2022-09-23 10:40:00')
date_2 = pd.to_datetime('2022-09-23 11:00:00')
# low def
ax = DATA.loc[date_1:date_2\
             ,BETX].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,5),ylim=(-5,50))
plt.suptitle('Evento 23-09, freq=1m')
plt.tight_layout()

#Zoom a peak
date_1 = pd.to_datetime('2022-09-23 10:48:00')
date_2 = pd.to_datetime('2022-09-23 10:53:00')
# high def
ax = concat_df.loc[date_1:date_2\
             ,['Benzene','Toluene','Ethyl benzene_Xylenes']\
             ].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,5),ylim=(-5,150))
plt.suptitle('Zoom a peak principal evento 23-09, freq=1s')
plt.tight_layout()

#%% Peak 3

# Evento 29-09
date_1 = pd.to_datetime('2022-09-29 17:00:00')
date_2 = pd.to_datetime('2022-09-29 18:30:00')
# low def
ax = DATA.loc[date_1:date_2\
             ,BETX].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,5),ylim=(-5,100))
plt.suptitle('Evento 29-09, freq=1m')
plt.tight_layout()

# Zoom a peak
date_1 = pd.to_datetime('2022-09-29 17:44:00')
date_2 = pd.to_datetime('2022-09-29 17:49:00')
# high def
ax = concat_df.loc[date_1:date_2\
             ,['Benzene','Toluene','Ethyl benzene_Xylenes']\
             ].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,5),ylim=(-5,250))
plt.suptitle('Zoom a peak principal evento 29-09, freq=1s')
plt.tight_layout()

#%% Peaks específico

ax = DATA.loc[pd.to_datetime('2022-09-24 00:00:00')\
             :pd.to_datetime('2022-09-25 00:00:00')\
             ,DATA.columns].plot(subplots=True, layout=(25,1), grid=True\
                         , figsize=(15,25),ylim=(-1,100))
plt.tight_layout()

#%% Serie

ax = DATA.loc[:,DATA.columns].plot(subplots=True\
                                        , layout=(25,1), grid=True\
                                        , figsize=(50,30),ylim=(-1,10))
plt.tight_layout()

#%%
ax = DATA.loc[pd.to_datetime('2022-09-24 00:00:00')\
             :pd.to_datetime('2022-09-25 00:00:00')\
             ,'Styrene'].plot(figsize=(8,4), grid=True, ylim=(-2,50))
plt.tight_layout()

#%% Queremos ver cómo se comportan las correlacioes con COVs para
### BETX bajo un umbral, por ahora diremos 

# Create subplots
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(5, 10), sharex=True)

# Plot histograms
for ax, col in zip(axes, BETX):
    DATA[col].hist(ax=ax, bins=100, range=[-0.2,10])
    ax.set_title(col)
    ax.legend([col])

plt.tight_layout()
plt.show()

#%% Cortamos solo peak de 02-09
# Copiamos DATA y definimos NaN
DATA_sp = DATA.copy(deep=True); NaN = np.nan

# 02-09
date_1 = pd.to_datetime('2022-09-02 09:30:00')
date_2 = pd.to_datetime('2022-09-02 11:30:00')
DATA_sp.loc[date_1:date_2,DATA.columns] = NaN

# ploteamos
BETX = ['Benzene','Toluene','Ethyl.benzene_Xylenes'] 
ax = DATA[BETX].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,8),ylim=(-5,350))
plt.suptitle('Serie con peak 02-09')
plt.tight_layout()

ax = DATA_sp[BETX].plot(subplots=True, layout=(3,1), grid=True\
                        , figsize=(10,8),ylim=(-5,350))
plt.suptitle('Serie sin peak 02-09')
plt.tight_layout()

# guardamos variable
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
DATA_sp.to_csv(path+'inv_data_prelim_sinpeak0209.csv'\
               , sep=';',index_label='date'\
               , date_format='%d/%m/%Y %H:%M:%S')

#%% Cargamos datos 1m
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
DATA = pd.read_csv(path+'inv_data_1min.csv',delimiter=';')
DATA['date'] = pd.to_datetime(DATA['date'],format='%d/%m/%Y %H:%M:%S')
DATA['date'] = pd.to_datetime(DATA['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
DATA = DATA.set_index('date')

#%% Incorporación de variables meteorologicas 

# importamos datos meteo
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
met = pd.read_csv(path+'meteo.csv',sep=';',header=1,skiprows=[2,3])
met['date'] = pd.to_datetime(met['TIMESTAMP'],format='%d-%m-%Y %H:%M')
met = met.drop(columns=['TIMESTAMP','RECORD'])
met = met.set_index('date')
met = met.applymap(lambda x: float(x.replace(',', '.')))

# seleccionamosv variables y fechas de interés 
date_1 = pd.to_datetime('2022-08-27 00:05:00')
date_2 = pd.to_datetime('2022-11-03 10:20:00')
met_int = met.iloc[:,[2,3,4,5,7,9]]
met_int = met_int.loc[date_1:date_2,:]
met_int.columns=['p','t','rh','ws','wd','sr']
met_int = met_int.drop_duplicates()

#chequeamos si faltan fechas
date_c = pd.date_range(start=met_int.index.min(), end=met_int.index.max()\
                       , freq='5min')
dates_missing = date_c.difference(met_int.index)

# encontrar duplicados
met_int.iloc[met_int.index.duplicated(),:]


#%% Ploteamos
met.iloc[:,:].plot(subplots=True,layout=(11,1),grid=True,figsize=(10,20))
plt.tight_layout()

#%% Juntamos

# promediamos para juntar
DATA_5min = DATA.resample('5min').mean()

# juntamos 
DATA_5min.loc[:,['p','t','rh','ws','wd','sr']] = met_int[['p','t','rh','ws','wd','sr']]

# guardamos
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/' 
DATA_5min.to_csv(path+'inv_data_5min.csv'\
               , sep=';',index_label='date'\
               , date_format='%d/%m/%Y %H:%M:%S')
    
#%% Eliminamos peak de 

    



    