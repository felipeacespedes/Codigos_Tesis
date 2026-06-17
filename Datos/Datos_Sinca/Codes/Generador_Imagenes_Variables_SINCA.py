# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 18:50:00 2023

@author: felip

Código para utilizar las funciones que plotean los datos de estaciones SINCA
y definir diccionario de estaciones con 1 dataframe por estación que incluye
una columna de vector tiempo como datetimeindex, y el resto de las columnas
corresponde a las variables por estación
"""

import pandas as pd
from Vis_fun import Vis
from import_var import import_var
import numpy as np
import matplotlib.pyplot as plt

# from statsmodels.tsa.seasonal import seasonal_decompose
# import seaborn as sns
# color_pal = sns.color_palette()
# plt.style.use('fivethirtyeight')
# plt.style.use('classic')

#%% Creamos diccionarios de estaciones, variables y unidades
### , definimos fechas y vector T

# Diccionario
Dic = {}

Dic['Estaciones'] = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura' \
                     ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo']
    
Dic['Variables_Cont'] = ['HCNM','CO','MP25']

Dic['Unidades_Cont'] = ['ppm','ppm',r'$\mu g/m^{3}$']


Dic['Variables_Meteo'] = ['Velocidad','Dirección']

Dic['Unidades_Meteo'] = ['m/s','°']

Dic['Variables'] = ['SO2','CH4','HCNM','HCT','CO','Velocidad','Dirección']


# por ahora usamos el periodo que sabemos que esta relativamente bien
Fi = '2018-01-01'
Ff = '2023-12-31'

# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

#%% Cargamos datos validados de SNIFA para años disponibles

#%% Generamos imagenes de 9 estaciones sinca para las variables disponibles 

# Contaminantes:
for e in range(len(Dic['Estaciones'])):
    for v in range(len(Dic['Variables_Cont'])):
        if Dic['Estaciones'][e] == 'Ventanas' \
            and Dic['Variables_Cont'][v] == 'CO':
            continue
        elif Dic['Estaciones'][e] in ['Sur','Junta_Vecinos','Gaviotas','Colmo']\
            and Dic['Variables_Cont'][v] == 'MP25':
                continue
        Vis(Dic['Estaciones'][e],'Cont',Dic['Variables_Cont'][v] \
            ,Dic['Unidades_Cont'][v],Fi,Ff,'Total')
        Vis(Dic['Estaciones'][e],'Cont',Dic['Variables_Cont'][v] \
            ,Dic['Unidades_Cont'][v],Fi,Ff,'PorAño')

# # Meteorologicas:
# for e in range(len(Dic['Estaciones'])):
#     for v in range(len(Dic['Variables_Meteo'])):
#         Vis(Dic['Estaciones'][e],'Meteo',Dic['Variables_Meteo'][v][0:3] \
#             ,Dic['Unidades_Meteo'][v],Fi,Ff,'Total')
#         Vis(Dic['Estaciones'][e],'Meteo',Dic['Variables_Meteo'][v][0:3] \
#             ,Dic['Unidades_Meteo'][v],Fi,Ff,'PorAño')


#%% Diccionario de dataframes de estaciones 

# Creamos data frame por estación para luego crear diccionario de 
# estaciones(data frames)

# Creamos diccionario de estaciones
Est = {}

# Importamos variables de contaminantes a dataframe de cada estación
for e in range(len(Dic['Estaciones'])):
    Est[Dic['Estaciones'][e]] = pd.DataFrame({'T': T})
    Est[Dic['Estaciones'][e]] = Est[Dic['Estaciones'][e]].set_index('T')
    for v in range(len(Dic['Variables_Cont'])):
        if Dic['Estaciones'][e] == 'Ventanas' \
            and Dic['Variables_Cont'][v] == 'CO':
            continue
        elif Dic['Estaciones'][e] in ['Sur','Junta_Vecinos','Gaviotas','Colmo']\
            and Dic['Variables_Cont'][v] == 'MP25':
                continue
        Est[Dic['Estaciones'][e]][Dic['Variables_Cont'][v]] = import_var(
            Dic['Estaciones'][e],'Cont',Dic['Variables_Cont'][v],Fi,Ff)
        
# Añadimos variables meteorológicas
# for e in range(len(Dic['Estaciones'])):
#     for v in range(len(Dic['Variables_Meteo'])):
#         Est[Dic['Estaciones'][e]][Dic['Variables_Meteo'][v]] = import_var(
#             Dic['Estaciones'][e],'Meteo',Dic['Variables_Meteo'][v][0:3],Fi,Ff)

del v, e

#%% Estadísticos

# Describe: guardamos todos los describe en diccionario Desc
dire = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Stats_estaciones/'
Desc = {}
for e in Dic['Estaciones']:
    Desc[e] = Est[e].describe()
    Desc[e].to_excel(dire + 'Stats_'+e+'.xlsx')
    
del dire
    
# guardamos estadístico
# Desc['Centro_Quintero'].to_excel('Stats_CQ.xlsx')

    
    
    
    
#%% Pruebas

# Hay que inspeccionar qué vola los vientos
# Corremos función import por parte
# extracción de fechas: bien
# ie=0
# iv=0
# est = Dic['Estaciones'][ie]
# CoM = 'Meteo'
# var = Dic['Variables_Meteo'][iv][0:3]
# Viento = import_var(est,CoM,var,Fi,Ff)

# hay un problema en la importación de las matrices por los nombres de las columnas
# col=4 if CoM=='Cont' else 2
# Viento  = pd.read_csv('C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/' \
#                   +est+'/'+CoM+'/'+var+'.csv'
#                  , delimiter=";"
#                  , dtype={'a': str, 'b': str, 'c': float} 
#                  , skiprows=23
#                  , skipfooter=24
#                  , usecols=(0,1,col)     
#                  , decimal=","
#                  , names=['Fecha','Hora','V']
#                  , header=0
#                  )

#%% Generamos ciclo diario, semanal y estacional

# ciclo anual:
# debemos calcular los promedios diarios para caclular el ciclo anual

# Creamos diccionario de estaciones para series diarias
Est_d= {}

# Resampleamos a promedios diarios el dataframe de cada estación
for e in range(len(Dic['Estaciones'])):
    Est_d[Dic['Estaciones'][e]] = pd.DataFrame({'T': T})
    Est_d[Dic['Estaciones'][e]] = Est_d[Dic['Estaciones'][e]].set_index('T')
    Est_d[Dic['Estaciones'][e]] = Est[Dic['Estaciones'][e]].resample('D').mean()

del e
# Listo!!

# Quitamos los 29 de febrero

# for e in Dic['Estaciones']:
#     Est_d[e] = Est_d[e].loc[~((Est_d[e].index.month==2) \
#                               & (Est_d[e].index.day==29))]
#     Est_d[e].sort_index(inplace=True)
    
# del e

#%% Probamos con librería StatsModels

# importamos librería y aplicamos código de artículo:
# https://medium.com/@khairulomar/deconstructing-time-series-using-fourier-transform-e52dd535a44e


data = Est_d['Ventanas']['HCNM']#.sort_index(inplace=True)
data.sort_index(inplace=True)
decomposition = seasonal_decompose(data , model='additive')#, model='multiplicative')
trend    = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

trend.plot(figsize=(15,5))
seasonal.plot(figsize=(15,5))
residual.plot(figsize=(15,5))

# aqui intentamos usar el método pero quitando el 29 de febrero, aunque no se 
# se obtivo un resultado aparente

# Haciendo mayor resolución se observa un marcado ciclo semanas, cumpliendo 
# un poco más de 52 semanas

seasonal[0:7].plot(figsize=(15,5))


    
#%% Probamos con metodo tradicional: 


# para conferir si efectivamente el ciclo anual obtenido con StatsModels tiene
# intentaremos hacerlo de manera tradicional, o sea promediando cada día del año
# para los 4 años disponibles


# probamos day of year
dias = Est_d['Ventanas'][0:365].index.dayofyear


# intentamos crear matriz de largo [365,n_contaminantes]
# para eso usaremo el mismo método con el que sacamos los días
# 29 de febrero:

# diccionario con ciclo anual para cada estación y contaminante/variable 
Est_ca = {}

for e in Dic['Estaciones']:
    Est_ca[e] = pd.DataFrame({'T':dias})
    Est_ca[e] = Est_ca[e].set_index('T')
    for d in range(365):
        Est_ca[e].loc[d+1,Dic['Variables']] = Est_d[e]\
            .loc[(Est_d[e].index.dayofyear==d+1)].mean()
        
            
# ahora ploteamos todas las estaciones para la variable HCNM
for e in Dic['Estaciones']:
    plt.figure()
    Est_ca[e]['HCNM'].plot(figsize=(13,5),style='.',title=e)
        

# tengo que:
    # - ver si dayofweek entrega los días de la semana para calcular
    #   el ciclo semanal
    # - ver cómo asignar las columnas y valores a cada días del año en 
    #   Est_ca (ciclo anual, dataframes por estación con 365 días para
    #   asignar los promedios de cada día)
    
#%% ciclo semanal

# aplicamos mismo código aplicado a ciclo anual pero ahora por día de semana:
    
# diccionario con ciclo semanal para cada estación y contaminante/variable 
Est_cs = {}

for e in Dic['Estaciones']:
    Est_cs[e] = pd.DataFrame({'T':dias[0:7]})
    Est_cs[e] = Est_cs[e].set_index('T')
    for d in range(7):
        Est_cs[e].loc[d+1,Dic['Variables']] = Est_d[e].loc[(Est_d[e].index.dayofweek==d)].mean()
        

# ahora ploteamos todas las estaciones para la variable HCNM
for e in Dic['Estaciones']:
    # plt.figure()
    Est_cs[e]['HCNM'].plot(figsize=(15,5),style='-')#,title=e)


#%% Ciclo diario

# ahora creamos ciclo diario

horas = T[0:24].hour

# diccionario con ciclo diario para cada estación y contaminante/variable 
Est_cd = {}

for e in Dic['Estaciones']:
    Est_cd[e] = pd.DataFrame({'T':horas})
    Est_cd[e] = Est_cd[e].set_index('T')
    for h in range(24):
        Est_cd[e].loc[h,Dic['Variables']] = Est[e].loc[(Est[e].index.hour==h)].mean()
        
#%% ploteamos ciclos diarios  
c=1
for e in Dic['Estaciones']:
    plt.figure()
    Est_cd[e]['HCNM'].plot(figsize=(13,6),style='-',title=e)
    # (Est_cd[e]['HCT']*c).plot(figsize=(13,6),style='-',title=e)
    (Est_cd[e]['CO']*c).plot(figsize=(13,6),style='-',title=e)

    
# examinamos ciclos diarios de otras variables

    
#%% Inspeccionar correlación con MP2.5 y MP10

# Intentamos cargar los datos de SNIFA para los años disponible,
# a priori: 2019, 2020, 2021 
        
# Ya, vienen por años separados, así que hay que cargarlos y hacerles append
# Son las estaciones de Centro Quintero y Loncura entre 2019-2022.

# cargamos primero un solo arhcivo para ver cómo tratarlo:

años = [2019,2020,2021,2022]
estaciones = ['Centro Quintero', 'Loncura']
    
# PM = pd.read_excel('C:/Users/felip/Desktop/U/Tesis/Datos/Datos_SNIFA/MP_util/'+ \
#                  estaciones[0]+'_'+str(años[0])+'_DatosValidados.xlsx')
#                  # , encoding='unicode_escape')
        
        
xlsx = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_SNIFA/MP_util/'+ \
                 estaciones[0]+'_'+str(años[0])+'_DatosValidados.xlsx'
                 
df = pd.read_excel(xlsx, sheet_name = ['Registros SO2','Registros MP10'])
        
del xlsx, años, estaciones

# plt.figure()
MP10 = df['Registros MP10']['Unnamed: 7'][5:-1]
        
        
        
# Al final, vienen con promedio diario cada tres días, por lo que preferimos 
# intentarlo con las series de SINCA para las estaciones Centro Quintero 
# y Loncura. 

#%% Ahora intentamos ver la correlación con las series de datos de MP25 y MP10
### de la red SINCA:

##############################################################################
#######################    CORRER DESDE AQUI!!    ############################
##############################################################################

# Para esto modificaremos el diccionario incial con el fin de facilitar el 
# desarrollo del código.

# Diccionario
Dic = {}

# solo estaciones que tengan MP 2.5 y MP 10
Dic['Estaciones'] = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura' \
                     ,'Concón']
    
Dic['Variables_Cont'] = ['SO2','CH4','HCNM','HCT','CO','MP25','MP10']

Dic['Unidades_Cont'] = ['ppb','ppm','ppm','ppm','ppm' \
                        ,r'$\mu g/m^{3}$',r'$\mu g/m^{3}$']

Dic['Variables_Meteo'] = ['Velocidad','Dirección']

Dic['Unidades_Meteo'] = ['m/s','°']

Dic['Variables'] = ['SO2','CH4','HCNM','HCT','CO','MP25','MP10' \
                    ,'Velocidad','Dirección']

# por ahora usamos el periodo que sabemos que esta relativamente bien
Fi = '2020-01-01'
Ff = '2022-12-31'

# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

#%% Ahora, debemos crear los DFs

# Creamos diccionario de estaciones
Est = {}

# Importamos variables de contaminantes a dataframe de cada estación
for e in range(len(Dic['Estaciones'])):
    Est[Dic['Estaciones'][e]] = pd.DataFrame({'T': T})
    Est[Dic['Estaciones'][e]] = Est[Dic['Estaciones'][e]].set_index('T')
    for v in range(len(Dic['Variables_Cont'])):
        if Dic['Estaciones'][e] == 'Ventanas' and Dic['Variables_Cont'][v] == 'CO':
            continue
        Est[Dic['Estaciones'][e]][Dic['Variables_Cont'][v]] = import_var(
            Dic['Estaciones'][e],'Cont',Dic['Variables_Cont'][v],Fi,Ff)
        
# Añadimos variables meteorológicas
for e in range(len(Dic['Estaciones'])):
    for v in range(len(Dic['Variables_Meteo'])):
        Est[Dic['Estaciones'][e]][Dic['Variables_Meteo'][v]] = import_var(
            Dic['Estaciones'][e],'Meteo',Dic['Variables_Meteo'][v][0:3],Fi,Ff)

del v, e

#%% Pasamos MP25 de ng/m3 a ppm

# El factor de conversión es 1/2500

# for e in Dic['Estaciones']:
#     Est[e]['MP25'] = Est[e]['MP25']*(1/2500)

# Era broma, el material particulado no se puede dejar en ppm:
# "Because particulate matter varies in size (unlike a gas molecule)
# , ppm isn’t a valid unit of measurement. Therefore, the true unit 
# for the PM measurement is always in mg/m3."
    
#%% Vemos distribución de datos menores a 0.5 ppm

LOD = '0.1' #ppm

qu = Est['Centro_Quintero'].query('HCNM < '+LOD)

plt.figure()
qu['HCNM'].plot(figsize=(15,5),style='.')
plt.title('Serie horaria de rm HCNM < '+LOD+' ppm')

plt.figure()
qu['HCNM'].plot(figsize=(15,5),kind='hist',bins=500)
plt.title('Distribución de rm de HCNM horarias < '+LOD+' ppm')

# Contamos datos menores a 0.05 ppm y menores a 0.1 ppm

# porcentage datos menores a 0.05
LOD = '0.05'
Cant_005 = 100*len(Est['Centro_Quintero'].query('HCNM < '+LOD))/ \
            len(Est['Centro_Quintero']['HCNM'])
print(Cant_005)

LOD = '0.1'
Cant_01 = 100*len(Est['Centro_Quintero'].query('HCNM < '+LOD))/ \
            len(Est['Centro_Quintero']['HCNM'])
            
print(Cant_01)

# nos quedamos con menores a 0.05
#%% Tratamiento datos HCNM

# Eliminamos todos los datos que sean menores a LOD = 0.5 ppm
# y los reemplazamos por Nan

for e in Dic['Estaciones']:
    Est[e]['HCNM'].loc[(Est[e]['HCNM'] < 0.05)] = np.nan

#%% Chequeamos que se hayan extraido

# chequeamos que no hayan outliers, para eso vemos qué datos se encuentran 
# bajo los 0.5 ppm

qu = Est['Centro_Quintero'].query('HCNM < 0.5')

plt.figure()
qu['HCNM'].plot(figsize=(15,5),style='.')

plt.figure()
qu['HCNM'].plot(figsize=(15,5),kind='hist',bins=500)

# SI!!

#%% Ahora recreamos los plots de ciclo diario, semanal y anual, comparando
### HCNM con MP 2.5 y MP10

# Creamos diccionario de estaciones para series diarias
Est_d= {}

# Resampleamos a promedios diarios el dataframe de cada estación
for e in range(len(Dic['Estaciones'])):
    Est_d[Dic['Estaciones'][e]] = pd.DataFrame({'T': T})
    Est_d[Dic['Estaciones'][e]] = Est_d[Dic['Estaciones'][e]].set_index('T')
    Est_d[Dic['Estaciones'][e]] = Est[Dic['Estaciones'][e]].resample('D').mean()

del e

# creamos matriz de días

dias = Est_d['Centro_Quintero'][0:365].index.dayofyear

#%% Ciclo Anual

# diccionario con ciclo anual para cada estación y contaminante/variable 
Est_ca = {}

for e in Dic['Estaciones']:
    Est_ca[e] = pd.DataFrame({'T':dias})
    Est_ca[e] = Est_ca[e].set_index('T')
    for d in range(365):
        Est_ca[e].loc[d+1,Dic['Variables']] = \
            Est_d[e].loc[(Est_d[e].index.dayofyear==d+1)].mean()

del e
            
# comparamos la variable HCNM y MP25
plt.style.use('default')
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize = (12,5))
    ax.tick_params(axis='y',direction='in',labelcolor='blue')
    ax.set_ylabel(Dic['Unidades_Cont'][2],color='blue')
    ax2 = ax.twinx()
    ax2.tick_params(axis='y',direction='in',labelcolor='orange')
    ax2.set_ylabel(Dic['Unidades_Cont'][5],color='orange')
    ln1 = ax.plot(Est_ca[e]['HCNM'],marker='.', color='blue',linewidth=0 \
                  ,label=Est_ca[e]['HCNM'].name)
    ln2 = ax2.plot(Est_ca[e]['MP25'],marker='.', color='orange',linewidth=0 \
                   ,label=Est_ca[e]['MP25'].name)
    leg = ln1+ln2
    labs =[l.get_label() for l in leg]
    ax.legend(leg,labs,loc=0)
    plt.title('Ciclo Estacional: HCNM vs MP25, '+e)
    plt.tight_layout()
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CA/'+Est_ca[e]['HCNM'].name
                +'_vs_'+Est_ca[e]['MP25'].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e

# MP2.5 y HCNM parecieran tener buena correlación!
    
# comparamos la variable HCNM y CO
plt.style.use('default')
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize = (12,5))
    ax.tick_params(axis='y',direction='in',labelcolor='blue')
    ax.set_ylabel(Dic['Unidades_Cont'][2],color='blue')
    ax2 = ax.twinx()
    ax2.tick_params(axis='y',direction='in',labelcolor='orange')
    ax2.set_ylabel(Dic['Unidades_Cont'][4],color='orange')
    ln1 = ax.plot(Est_ca[e]['HCNM'],marker='.', color='blue',linewidth=0 \
                  ,label=Est_ca[e]['HCNM'].name)
    ln2 = ax2.plot(Est_ca[e]['CO'],marker='.', color='orange',linewidth=0 \
                   ,label=Est_ca[e]['CO'].name)
    leg = ln1+ln2
    labs =[l.get_label() for l in leg]
    ax.legend(leg,labs,loc=0)
    plt.title('Ciclo Estacional: HCNM vs CO, '+e)
    plt.tight_layout()
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CA/'+Est_ca[e]['HCNM'].name
                +'_vs_'+Est_ca[e]['CO'].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e

#%% Ciclo semanal:

# aplicamos mismo código aplicado a ciclo anual pero ahora por día de semana:
    
# diccionario con ciclo semanal para cada estación y contaminante/variable 
Est_cs = {}

for e in Dic['Estaciones']:
    Est_cs[e] = pd.DataFrame({'T':dias[0:7]})
    Est_cs[e] = Est_cs[e].set_index('T')
    for d in range(7):
        Est_cs[e].loc[d+1,Dic['Variables']] = Est_d[e].loc[(Est_d[e]\
                                            .index.dayofweek==d)].mean()
        
del e

# comparamos las variables HCNM y MP25
plt.style.use('default')
for e in Dic['Estaciones']:
    plt.figure()
    fig, ax = plt.subplots(figsize = (12,5))
    ax.tick_params(axis='y',direction='in',labelcolor='blue')
    ax.set_ylabel(Dic['Unidades_Cont'][2],color='blue')
    ax2 = ax.twinx()
    ax2.tick_params(axis='y',direction='in',labelcolor='orange')
    ax2.set_ylabel(Dic['Unidades_Cont'][5],color='orange')
    ln1 = ax.plot(Est_cs[e]['HCNM'], color='blue',linewidth=1.8 \
                  ,label=Est_cs[e]['HCNM'].name)
    ln2 = ax2.plot(Est_cs[e]['MP25'], color='orange',linewidth=1.8 \
                   ,label=Est_cs[e]['MP25'].name)
    leg = ln1+ln2
    labs =[l.get_label() for l in leg]
    ax.legend(leg,labs,loc=0)
    plt.title('Ciclo Semanal: HCNM vs MP25, '+e)
    plt.tight_layout()
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CS/'+Est_cs[e]['HCNM'].name
                +'_vs_'+Est_cs[e]['MP25'].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e

    
# comparamos las variables HCNM y CO
plt.style.use('default')
for e in Dic['Estaciones']:
    plt.figure()
    fig, ax = plt.subplots(figsize = (12,5))
    ax.tick_params(axis='y',direction='in',labelcolor='blue')
    ax.set_ylabel(Dic['Unidades_Cont'][2],color='blue')
    ax2 = ax.twinx()
    ax2.tick_params(axis='y',direction='in',labelcolor='orange')
    ax2.set_ylabel(Dic['Unidades_Cont'][5],color='orange')
    ln1 = ax.plot(Est_cs[e]['HCNM'], color='blue',linewidth=1.8 \
                  ,label=Est_cs[e]['HCNM'].name)
    ln2 = ax2.plot(Est_cs[e]['CO'], color='orange',linewidth=1.8 \
                   ,label=Est_cs[e]['CO'].name)
    leg = ln1+ln2
    labs =[l.get_label() for l in leg]
    ax.legend(leg,labs,loc=0)
    plt.title('Ciclo Semanal: HCNM vs CO, '+e)
    plt.tight_layout()
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CS/'+Est_cs[e]['HCNM'].name
                +'_vs_'+Est_cs[e]['CO'].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e

#%% Ciclo diario:

# vector de tiempo con 24 horas
horas = T[0:24].hour

# diccionario con ciclo diario para cada estación y contaminante/variable 
Est_cd = {}

for e in Dic['Estaciones']:
    Est_cd[e] = pd.DataFrame({'T':horas})
    Est_cd[e] = Est_cd[e].set_index('T')
    for h in range(24):
        Est_cd[e].loc[h,Dic['Variables']] = Est[e].loc[(Est[e].index.hour==h)].mean()
del e

# comparamos las variables HCNM y MP25
plt.style.use('default')
for e in Dic['Estaciones']:
    plt.figure()
    fig, ax = plt.subplots(figsize = (12,5))
    ax.tick_params(axis='y',direction='in',labelcolor='blue')
    ax.set_ylabel(Dic['Unidades_Cont'][2],color='blue')
    ax2 = ax.twinx()
    ax2.tick_params(axis='y',direction='in',labelcolor='orange')
    ax2.set_ylabel(Dic['Unidades_Cont'][5],color='orange')
    ln1 = ax.plot(Est_cd[e]['HCNM'], color='blue',linewidth=1.8 \
                  ,label=Est_cd[e]['HCNM'].name)
    ln2 = ax2.plot(Est_cd[e]['MP25'], color='orange',linewidth=1.8 \
                   ,label=Est_cd[e]['MP25'].name)
    leg = ln1+ln2
    labs =[l.get_label() for l in leg]
    ax.legend(leg,labs,loc=0)
    plt.title('Ciclo Diario: HCNM vs MP25, '+e)
    plt.tight_layout()
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CD/'+Est_cd[e]['HCNM'].name
                +'_vs_'+Est_cd[e]['MP25'].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e
        
# encontramos resultados favorables, por lo que queda bajar los datos de  
# MP2.5 y MP10 para todas las estaciones disponibles, REVISAR EXCELL.

# comparamos las variables HCNM y CO
plt.style.use('default')
for e in Dic['Estaciones']:
    plt.figure()
    fig, ax = plt.subplots(figsize = (12,5))
    ax.tick_params(axis='y',direction='in',labelcolor='blue')
    ax.set_ylabel(Dic['Unidades_Cont'][2],color='blue')
    ax2 = ax.twinx()
    ax2.tick_params(axis='y',direction='in',labelcolor='orange')
    ax2.set_ylabel(Dic['Unidades_Cont'][5],color='orange')
    ln1 = ax.plot(Est_cd[e]['HCNM'], color='blue',linewidth=1.8 \
                  ,label=Est_cd[e]['HCNM'].name)
    ln2 = ax2.plot(Est_cd[e]['CO'], color='orange',linewidth=1.8 \
                   ,label=Est_cd[e]['CO'].name)
    leg = ln1+ln2
    labs =[l.get_label() for l in leg]
    ax.legend(leg,labs,loc=0)
    plt.title('Ciclo Diario: HCNM vs CO, '+e)
    plt.tight_layout()
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CD/'+Est_cd[e]['HCNM'].name
                +'_vs_'+Est_cd[e]['CO'].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e

#%% Creamos scatter plots entre variables HCNM y MP25/CO

# Scatter Ejemplo
# intentamos un scatter de prueba para crear el original
# plt.style.use('fivethirtyeight')
# plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
# cm = plt.cm.get_cmap('hsv')
# e = 'Ventanas'
# fig, ax = plt.subplots(figsize=(10,8))
# sc = ax.scatter(x=Est_ca[e]['HCNM'], y=Est_ca[e]['MP25'], c=Est_ca[e].index \
#                             ,cmap=cm)
# cb = plt.colorbar(sc, label='[Día del año]')
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# ax.text(0.05,0.95,'corr = '+str('%.2f'%Est_ca[e]['HCNM'].corr(Est_ca[e]['MP25']))\
#         ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
# ax.set_title('Ciclo Estacional: HCNM vs MP25, '+e,fontsize=12)
# plt.xlabel(Est_ca[e]['HCNM'].name)
# plt.ylabel(Est_ca[e]['MP25'].name)

# fig.tight_layout(pad=1.1)

# Listo!

#%% Scatter Ciclo Anual

# HCNM vs MP25
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'MP25'
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est_ca[e]['HCNM'], y=Est_ca[e][var], c=Est_ca[e].index \
                                ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est_ca[e]['HCNM']\
            .corr(Est_ca[e][var])),transform=ax.transAxes \
            ,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Ciclo Estacional: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est_ca[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CA/scatter'+Est_ca[e]['HCNM'].name
                +'_vs_'+Est_ca[e][var].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e
  
# HCNM vs CO
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'CO'
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est_ca[e]['HCNM'], y=Est_ca[e][var], c=Est_ca[e].index \
                                ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est_ca[e]['HCNM'].corr(Est_ca[e][var]))\
            ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Ciclo Estacional: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est_ca[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CA/scatter_'+Est_ca[e]['HCNM'].name
                +'_vs_'+Est_ca[e][var].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e


#%% Scatter Ciclo Semanal

# HCNM vs MP25
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'MP25'
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est_cs[e]['HCNM'], y=Est_cs[e][var], c=Est_cs[e].index \
                                ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est_cs[e]['HCNM'].corr(Est_cs[e][var]))\
            ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Ciclo Estacional: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est_ca[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CS/scatter_'+Est_cs[e]['HCNM'].name
                +'_vs_'+Est_cs[e][var].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e
  
# HCNM vs CO
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'CO'
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est_cs[e]['HCNM'], y=Est_cs[e][var], c=Est_cs[e].index \
                                ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est_cs[e]['HCNM'].corr(Est_cs[e][var]))\
            ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Ciclo Semanal: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est_ca[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CS/scatter_'+Est_cs[e]['HCNM'].name
                +'_vs_'+Est_cs[e][var].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e

#%% Scatter Ciclo Diario

# HCNM vs MP25
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'MP25'
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est_cd[e]['HCNM'], y=Est_cd[e][var], c=Est_cd[e].index \
                                ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est_cd[e]['HCNM'].corr(Est_cd[e][var]))\
            ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Ciclo Diario: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est_ca[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CD/scatter_'+Est_cd[e]['HCNM'].name
                +'_vs_'+Est_cd[e][var].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e
  
# HCNM vs CO
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'CO'
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est_cd[e]['HCNM'], y=Est_cd[e][var], c=Est_cd[e].index \
                                ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est_cd[e]['HCNM'].corr(Est_cd[e][var]))\
            ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Ciclo Diario: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est_ca[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/CD/scatter_'+Est_cd[e]['HCNM'].name
                +'_vs_'+Est_cd[e][var].name+'.png' \
                    , bbox_inches='tight',dpi=300)
del e

#%% 

#%% Queda ver qué vola HCT!!

#%% Ver Scatter plots entre series originales de HCNM vs MP25/CO, tal vez HCT

#%% Series Horarias

# HCNM vs MP25
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'MP25'
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est[e]['HCNM'], y=Est[e][var], c=Est[e].index.dayofyear \
                    ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est[e]['HCNM'].corr(Est[e][var]))\
            ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Series Horarias: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/Total/scatter_'+Est[e]['HCNM'].name
                +'_vs_'+Est[e][var].name+'horaria.png' \
                    , bbox_inches='tight',dpi=300)
del e
  
# HCNM vs CO
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'CO'
for e in Dic['Estaciones']:
    if e == 'Ventanas':
        continue
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est[e]['HCNM'], y=Est[e][var], c=Est[e].index.dayofyear \
                    ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est[e]['HCNM'].corr(Est[e][var]))\
            ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Series Horarias: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/Total/scatter_'+Est[e]['HCNM'].name
                +'_vs_'+Est[e][var].name+'horaria.png' \
                    , bbox_inches='tight',dpi=300)
del e

        
#%% Series Diarias
        
# HCNM vs MP25
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'MP25'
for e in Dic['Estaciones']:
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est_d[e]['HCNM'], y=Est_d[e][var], c=Est_d[e].index.dayofyear \
                    ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est_d[e]['HCNM'].corr(Est_d[e][var]))\
            ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Series Diarias: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est_d[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/Total/scatter_'+Est_d[e]['HCNM'].name
                +'_vs_'+Est_d[e][var].name+'_diaria.png' \
                    , bbox_inches='tight',dpi=300)
del e
  
# HCNM vs CO
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
cm = plt.cm.get_cmap('hsv')
var = 'CO'
for e in Dic['Estaciones']:
    if e == 'Ventanas':
        continue
    fig, ax = plt.subplots(figsize=(10,8))
    sc = ax.scatter(x=Est_d[e]['HCNM'], y=Est_d[e][var], c=Est_d[e].index.dayofyear \
                    ,cmap=cm)
    cb = plt.colorbar(sc, label='[Día del año]')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05,0.95,'corr = '+str('%.2f'%Est_d[e]['HCNM'].corr(Est_d[e][var]))\
            ,transform=ax.transAxes,fontsize=14,verticalalignment='top',bbox=props)
    ax.set_title('Series Diarias: HCNM vs '+var+', '+e,fontsize=12)
    plt.xlabel('HCNM [ppm]')
    plt.ylabel(Est_d[e][var].name+' ['+Dic['Unidades_Cont']\
               [Dic['Variables'].index(var)]+']')
    
    fig.tight_layout(pad=1.1)
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                e+'/Cont/Total/scatter_'+Est_d[e]['HCNM'].name
                +'_vs_'+Est_d[e][var].name+'_diaria.png' \
                    , bbox_inches='tight',dpi=300)
del e
        
#%% Por último, ploteamos histogramas

for e in Dic['Estaciones']:
    

        

        
        
        
        
        
        
        
  
        




    



