# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 10:36:15 2024

@author: felip

Código para corregir peaks que son errores, se iran enlistando por aglomerado
y finalmente se dejarán cómo Nan, guardando una serie sin peaks erroneos.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% importamos datos PTR
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
# file = 'datos_ver/ver_data_1min.csv'; freq = '1m'
# file = 'datos_inv/voc_5min_UTC_meteo.csv'; freq = '5m'
# COV = pd.read_csv(path+file,delimiter=';')
# COV['date'] = pd.to_datetime(COV['date'],format='%d/%m/%Y %H:%M:%S')
# COV['date'] = pd.to_datetime(COV['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
# COV = COV.set_index('date')

# # minutarios
# file = 'datos_inv/inv_data_prelim_1min.csv'
# COV_1m = pd.read_csv(path+file,delimiter=';')
# COV_1m['date'] = pd.to_datetime(COV_1m['date'],format='%d/%m/%Y %H:%M:%S')
# COV_1m['date'] = pd.to_datetime(COV_1m['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
# COV_1m = COV_1m.set_index('date')
# # cada 5 segundos
# file = 'datos_inv/inv_data_prelim_5seg.csv'
# COV_5s = pd.read_csv(path+file,delimiter=';')
# COV_5s['date'] = pd.to_datetime(COV_5s['date'],format='%d/%m/%Y %H:%M:%S')
# COV_5s['date'] = pd.to_datetime(COV_5s['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
# COV_5s = COV_5s.set_index('date')
# secundarios
file = 'datos_inv/inv_data_prelim_1seg.csv'
COV_1s = pd.read_csv(path+file,delimiter=';')
COV_1s['date'] = pd.to_datetime(COV_1s['date'],format='%d/%m/%Y %H:%M:%S')
COV_1s['date'] = pd.to_datetime(COV_1s['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV_1s = COV_1s.set_index('date')

del file, path
#%% Ploteamos COV

# definimos COV
# COV = COV_1m; freq = '1min'
# COV = COV_5s; freq = '5seg'
COV = COV_1s; freq = '1seg'


# Path de guardado de imagenes
path = 'C:/Users/felip/Desktop/Avances/6/peaks_erroneos/' 

#%% Visualización de peaks
date_1 = pd.to_datetime('2022-09-02 10:49:00')
date_2 = pd.to_datetime('2022-09-02 10:50:00')
cov = COV.columns[0:25]
ax = COV.loc[date_1:date_2,cov].plot(grid=True, figsize=(15,10))
                                     # ,ylim=(-0.1,500000))
plt.title('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
          +date_2.strftime('%H:%M, ')+'freq='+freq)
plt.tight_layout()
# plt.savefig(path+date_1.strftime('%d-%m-%y, %H%M')+' a '+date_2.\
#     strftime('%H%M, ')+freq+'.png')
print(date_1.strftime('%Y-%m-%d, %H:%M:%S')+' a '+date_2.strftime('%H:%M:%S'))
#%% Lista de peaks

# Se aprecian los siguientes peaks:
    # - 2022-09-08, 03:08:00 a 03:10:00: ERROR
    # Tiene toda la pinta de ser error, peak de 270 ppb en 
    # Formaldehyde, y de 880 ppb en Methanol. El resto de COVs saltan pero menos.
    # date_1 = pd.to_datetime('2022-09-08 03:08:00')
    # date_2 = pd.to_datetime('2022-09-08 03:10:00')
    
    # - 2022-09-08, 13:56:00 a 13:59:00: ERROR
    # Al igual que el peak anterior, salta en Methanol y Formaldehyde
    # en un solo dato secundario cada vez, se cree que es un erros.
    # date_1 = pd.to_datetime('2022-09-08 13:56:00')
    # date_2 = pd.to_datetime('2022-09-08 13:59:00')
    
    # - 2022-09-24, 04:48:00 a 04:50:00: ERROR
    # Salta el Formaldehyde y un poco el resto. En serie secundaria se 
    # aprecia claramente que el peak dura 1 segundo, por lo que se designa
    # cómo error.
    # date_1 = pd.to_datetime('2022-09-24 04:48:00')
    # date_2 = pd.to_datetime('2022-09-24 04:50:00')

    # - 2022-10-15, 05:33:30 a 05:34:30: ERROR
    # Se dispara el Methanol y, sobre todo el Ethanol, un poco formaldehyde.
    # En serie secundaria se aprecia que los peaks son de un solo datos,
    # por lo que se determinan cómo error.
    # date_1 = pd.to_datetime('2022-10-15 05:33:30')
    # date_2 = pd.to_datetime('2022-10-15 05:34:30')
    
    # - 2022-10-15, 15:38: a 15:40: MEDICIÓN
    # Se dispara el Ethanol, Acetic.acid_Glycoladehyde y más compuestos en 
    # menor magnitud. En serie secundaria se aprecia que los peaks duran 
    # aprox 30 segundos c/u , con cambios continuos. Se cree que no es error.
    # date_1 = pd.to_datetime('2022-10-15 15:38:00')
    # date_2 = pd.to_datetime('2022-10-15 15:44:00')
    
    # - 2022-10-16, 18:08:40 a 18:09:10: ERROR
    # Se aprecia un peak enorme de Formaldehyde, de solo 1 segundo, y uno 18
    # segundos despues se aprecia un peak más pequeño de varios compuestos.
    # date_1 = pd.to_datetime('2022-10-16 18:08:40')
    # date_2 = pd.to_datetime('2022-10-16 18:09:10')
    
    # - 2022-10-16, 22:29:00 a 22:31:00: ERROR
    # Se aprecian peaks enromes de 1 seg en los compuestos Formaldehyde y
    # Methanol. Se conluye que es un error.
    # date_1 = pd.to_datetime('2022-10-16 22:29:00')
    # date_2 = pd.to_datetime('2022-10-16 22:31:00')

    # - 2022-10-17, 08:23:40 a 08:24:20: ERROR
    # Se aprecia un peak enorme de Formaldehyde de 1 seg y otro más pequeño de
    # varios compuestos de 1 seg también. Se cree que es un error.
    # date_1 = pd.to_datetime('2022-10-17 08:23:40')
    # date_2 = pd.to_datetime('2022-10-17 08:24:20')

    # - 2022-10-17, 10:17:00 a 10:18:00: ERROR
    # Se aprecia que se cortaron parte de este error previamente pero quedó
    # un retazo. Se observa un peak enorme de Formaldehyde de 1 seg, y otros 
    # más pequeños de varios compuestos. Se concluye que es un error.
    # date_1 = pd.to_datetime('2022-10-17 10:17:00')
    # date_2 = pd.to_datetime('2022-10-17 10:18:00')
    
    # - 2022-10-17, 23:17:00 a 23:18:00: ERROR
    # Se aprecia que Formaldehyde muestra un peak enorme de aprox 2 segundos 
    # , previo a esto se ven unos peaks de aprox 3 segundos. Esto es un retazo 
    # de un error quye ya se había ingresado. Se concluye que es error.
    # date_1 = pd.to_datetime('2022-10-17 23:17:00')
    # date_2 = pd.to_datetime('2022-10-17 23:18:00')

    # - 2022-10-21, 17:35:00 a 18:00:00: MEDICIÓN
    # Se aprecian varios peaks por al rededor de 30 mins, sobre todo de 
    # Ethanol. Se concluye que noe s un error.
    # date_1 = pd.to_datetime('2022-10-21 17:35:00')
    # date_2 = pd.to_datetime('2022-10-21 18:00:00')


#%% Cargamos datos invierno minutarios previos a 23-09-2022

# Cargamos df Rodrigo
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
file = 'voc_min_UTC_4.csv'#; freq = '1m'
DATA_rod = pd.read_csv(path+file,delimiter=';')
DATA_rod = DATA_rod.drop('Cycle',axis=1)
DATA_rod['date'] = pd.to_datetime(DATA_rod['date']\
                                  ,format='%d/%m/%Y %H:%M:%S')
DATA_rod['date'] = pd.to_datetime(DATA_rod['date'].dt\
                                  .strftime('%Y-%m-%d %H:%M:%S'))
DATA_rod = DATA_rod.set_index('date'); DATA_rod = DATA_rod.iloc[0:-1,0:25]
# Aplicamos .iloc[0:-1,0:25] para no tomar el último valor de todas las
# columnas ('2022-09-23 00:00:00'), ya que este es incluido en data df, y 
# tomamos hasta la columna 26 ya que se incluyen repeticiones a partir de esta.

#%% Ahora corregimos los peaks (hacerlos Nan)

# Definimos el DF de datos posteriores al 23-09-2022, cada 1 segundo
DATA_fel = COV_1s.loc[COV_1s.index >= pd.to_datetime('2022-09-23 00:00:00')]

# Corregimos primero los datos de serie nueva, cada 1 segundo
Fi_errs = ['2022-09-24 04:48:00','2022-09-24 05:54:00'\
         ,'2022-10-15 05:33:00','2022-10-16 18:08:40','2022-10-16 22:29:00'\
         ,'2022-10-17 08:23:40','2022-10-17 10:17:00','2022-10-17 23:17:00']
Ff_errs = ['2022-09-24 04:50:00','2022-09-24 05:56:00'\
         ,'2022-10-15 05:34:30','2022-10-16 18:09:10','2022-10-16 22:31:00'\
         ,'2022-10-17 08:24:20','2022-10-17 10:18:00','2022-10-17 23:18:00'] 

NaN = np.nan
for i in range(len(Fi_errs)):
    # Definimos fechas a definir cómo NaN
    date_1 = pd.to_datetime(Fi_errs[i])
    date_2 = pd.to_datetime(Ff_errs[i])
    DATA_fel.loc[date_1:date_2,DATA_fel.columns] = NaN
    print(Fi_errs[i]+' a '+Ff_errs[i]+' = NaN')

# Luego corregimos los datos de serie de Rodrigo, de 1 minuto
Fi_errm = ['2022-09-08 03:08:00','2022-09-08 13:56:00']
Ff_errm = ['2022-09-08 03:10:00','2022-09-08 13:59:00']

for i in range(len(Fi_errm)):
    # Definimos fechas a definir cómo NaN
    date_1 = pd.to_datetime(Fi_errm[i])
    date_2 = pd.to_datetime(Ff_errm[i])
    DATA_rod.loc[date_1:date_2,DATA_rod.columns] = NaN
    print(Fi_errm[i]+' a '+Ff_errm[i]+' = NaN')

#%% Ploteamos exploratoriamente

COV = DATA ; freq = '1min'
date_1 = pd.to_datetime('2022-09-24 05:50:00')
date_2 = pd.to_datetime('2022-09-24 06:00:00')

cov = COV.columns[0:25]
ax = COV.loc[date_1:date_2,cov].plot(grid=True, figsize=(30,10))
                                     # ,ylim=(-0.1,500000))
plt.title('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
          +date_2.strftime('%H:%M, ')+'freq='+freq+', '+str(cov))
plt.tight_layout()
plt.show()
# plt.savefig(path+date_1.strftime('%d-%m-%y, %H%M')+' a '+date_2.\
#     strftime('%H%M, ')+freq+'.png')
print(date_1.strftime('%Y-%m-%d, %H:%M:%S')+' a '+date_2.strftime('%H:%M:%S'))

#%%
# Ahora resampleamos los datos post 23-09-2022 a 1 minuto
DATA_fel = DATA_fel.resample('1min').mean()

# Por último, concatenamos los DFs y guardamos 
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
# DATA = pd.concat([DATA_rod,DATA_fel], axis=0)
# DATA.to_csv(path+'inv_data_1min.csv',sep=';',index_label='date'\
#             , date_format='%d/%m/%Y %H:%M:%S')

#%% Cargamos DATA
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
DATA = pd.read_csv(path+'inv_data_1min.csv',delimiter=';');freq=
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
met_int = met.iloc[:,[2,3,4,5,7]]
met_int = met_int.loc[date_1:date_2,:]
met_int.columns=['p','t','rh','ws','wd']
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
DATA_5min.loc[:,['p','t','rh','ws','wd']] = met_int[['p','t','rh','ws','wd']]

# guardamos
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/' 
DATA_5min.to_csv(path+'inv_data_5min.csv'\
               , sep=';',index_label='date'\
               , date_format='%d/%m/%Y %H:%M:%S')

