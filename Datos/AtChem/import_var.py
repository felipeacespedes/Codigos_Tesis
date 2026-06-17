# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 17:10:56 2023

@author: felip

Función que importa variables de un csv y entrega una serie de tiempo con
valores entre las fechas pedidas, de no tener valor el archivo importado 
entonces se rellena con NAns (NO ES A AÑOS ENTEROS)
"""
import pandas as pd
import numpy as np


def import_var(est,CoM,var,Fi,Ff):
    # Las variablesa usar son:
    # est: estación (string).
    # CoM: var. Contaminantes o Meteorologica (string).
    # var: variable/contaminantes a utilizar (string).
    # Fi: fecha inicial como "2018-01-01" (string).
    # Ff: fecha final como "2018-01-01" (string).
    
    # Primero definimos ruta para acceder a variable en base a
    # estación y variable requeridas y definimos variable V
    # Ya que en las variables Cont y Meteo los datos vienen en
    # las columnas 4 y 2, respectivamente, definimos if para 
    # cambiar este input para cada caso:
    col=4 if CoM=='Cont' else 2
    Vdat = pd.read_csv('C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/' \
                      +est+'/'+CoM+'/'+var+'.csv'
                     , delimiter=";"
                     , dtype={'a': str, 'b': str, 'c': float} 
                     , skiprows=23
                     , skipfooter=24
                     , usecols=(0,1,col)     
                     , decimal=","
                     , names=['Fecha','Hora','V']
                     , header=0
                     , engine='python'
                     )
    
    # Creamos matriz de fechas T y Tr
    # a priori utilizamos: 01/01/18 - 31/07/23
    tr1 = str(Vdat.Fecha[0]); tr1='0'+tr1 if len(tr1)==5 else tr1
    tr2 = str(Vdat.Fecha[len(Vdat.Fecha)-1])

    t1 = '20'+tr1[0:2]+'-'+tr1[2:4]+'-'+tr1[4:6]
    
    t2 = '20'+tr2[0:2]+'-'+tr2[2:4]+'-'+tr2[4:6]
    

    # Matriz de tiempo acorde a fechas de variable
    T = pd.date_range(t1+' 00:00:00', t2+' 23:00:00', freq='H')

    # Matriz de tiempo acorde a fechas requeridas Fi y Ff
    Tr = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')
    
    
    # Ahora hacemos la intersección, de manera que en Vr queden 
    # todos los datos necesarios de V y se desechen los que no
    # indices T
    Kt = np.in1d(T,Tr)
    # indices Tr
    Ktr = np.in1d(Tr,T)
    
    # Array de datos original
    V = np.array(Vdat.V)

    # Array de datos requerida
    # primero la rellenamos con Nans
    Vr = np.tile(np.nan,len(Ktr))
    
    # Rellenamos Vr con datos de V de interés
    Vr[Ktr] = V[Kt]

    
    return Vr

def import_var_pf(CoM,path_file,Fi,Ff):
    # Las variablesa usar son:
    # est: estación (string).
    # CoM: var. Contaminantes o Meteorologica (string).
    # path_file: path y nombre de archivo (string).
    # Fi: fecha inicial como "2018-01-01 00:00:00" (string).
    # Ff: fecha final como "2018-01-01 00:00:00" (string).
    
    # Primero definimos ruta para acceder a variable en base a
    # estación y variable requeridas y definimos variable V
    # Ya que en las variables Cont y Meteo los datos vienen en
    # las columnas 4 y 2, respectivamente, definimos if para 
    # cambiar este input para cada caso:
    col=4 if CoM=='Cont' else 2
    Vdat = pd.read_csv(path_file
                     , delimiter=";"
                     , dtype={'a': str, 'b': str, 'c': float} 
                     , skiprows=0
                     , skipfooter=0
                     , usecols=(0,1,col)     
                     , decimal=","
                     , names=['Fecha','Hora','V']
                     , header=0
                     , engine='python'
                     )
    
    # Creamos matriz de fechas T y Tr
    # a priori utilizamos: 01/01/18 - 31/07/23
    tr1 = str(Vdat.Fecha[0]); tr1='0'+tr1 if len(tr1)==5 else tr1
    tr2 = str(Vdat.Fecha[len(Vdat.Fecha)-1])

    t1 = '20'+tr1[0:2]+'-'+tr1[2:4]+'-'+tr1[4:6]
    
    t2 = '20'+tr2[0:2]+'-'+tr2[2:4]+'-'+tr2[4:6]
    

    # Matriz de tiempo acorde a fechas de variable
    # Esta vez lo dejamos en 01 a 23 ya que así viene de SINCA
    T = pd.date_range(t1+' 01:00:00', t2+' 23:00:00', freq='H')

    # Matriz de tiempo acorde a fechas requeridas Fi y Ff
    Tr = pd.date_range(Fi,Ff, freq='H')
    
    print('Fechas de csv: '+str(T[0])+' a '+str(T[len(T)-1]))
    print('Fechas ingresadas: '+str(Tr[0])+' a '+str(Tr[len(Tr)-1]))

    
    
    # Ahora hacemos la intersección, de manera que en Vr queden 
    # todos los datos necesarios de V y se desechen los que no
    # indices T
    Kt = np.in1d(T,Tr)
    # indices Tr
    Ktr = np.in1d(Tr,T)
    
    # Array de datos original
    V = np.array(Vdat.V)

    # Array de datos requerida
    # primero la rellenamos con Nans
    Vr = np.tile(np.nan,len(Ktr))
    
    # Rellenamos Vr con datos de V de interés
    Vr[Ktr] = V[Kt]
    
    
    
    return Vr