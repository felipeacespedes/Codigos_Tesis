# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:24:31 2023

@author: felip
"""
# Librerías 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Vis_IQR(est,CoM,var,un,Fi,Ff,c):
    # Las variablesa usar son:
    # est: estación (string).
    # CoM: var. Contaminantes o Meteorologica (string).
    # var: variable/contaminantes a utilizar (string).
    # un: unidades de variable (string).
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

    # definimos fechas para titulo y ruta de guardado
    Ti = Tr[0].strftime('%y%m%d')
    Tf = Tr[-1].strftime('%y%m%d')
    
    # Por último, ploteamos como serie total o por año:
            
    # Encontramos cantidad de años a plotear para poder 
    # diseñar subplots acorde a esta cantidad 
    yi=Tr.year[0]; yf=Tr.year[-1]; ys = yf-yi
    # creamos figura
    fig = plt.figure(figsize=(15,5*ys))
            
    # Debemos rellenar los años que no están completos 
    # para que en los subplots aparezcan a escala
    # o sea que se debe rellenar con nans los datos
    # no existentes y usar una T que cubra todo el año
    
    # creamos matriz auxiliar para comparar qué datos faltan para tener
    # años completos
    Tfull = pd.date_range(str(yi)+'-01-01 00:00:00',str(yf) \
                         +'-12-31 23:00:00',freq='H')
    # comparamaos Taux con T con tal de ver qué datos faltan
    Kfull = np.in1d(Tfull,Tr)
    # rellenamos datos de Vr con Nan
    Vfull = np.tile(np.nan,len(Kfull))
    Vfull[Kfull] = Vr
    
    # ploteamos subplots
    for i in range(ys+1):
        Ty = Tfull[Tfull.year==yi+i]
        plt.subplot(ys+1,1,i+1)
        plt.plot(Ty,Vfull[Tfull.year==yi+i])
        plt.grid()
        plt.title(str(yi+i))
        plt.ylabel(var+' ['+un+']')
        plt.xlim(Ty[0]-Ty.freq*150,Ty[-1]+Ty.freq*150)
        if i == ys:
            plt.xlabel('Tiempo [h]')
            
        # creamos df para IQR y pasamos Vfull y Tfull a dataframe
        Y = pd.DataFrame({'T':Ty})
        Y['V'] = Vfull[Tfull.year==yi+i]
                
        # IQR
        Q1 = Y['V'].quantile(0.25)
        Q3 = Y['V'].quantile(0.75)
        IQR = Q3- Q1
        # c = 2
        min_t = Q1 - c*IQR
        max_t = Q3 + c*IQR
        AD_V = (Y['V'].clip(lower = min_t,upper=max_t) != Y['V'])
        # ploteamos zonas rojas con anomalías
        for j in range(len(AD_V)):
            
            if AD_V[j] == False:
                continue
            else:
                li = j
                
                while j+1 == True:
                    j=j+1
                lf = j
                plt.axvspan(Ty[li], Ty[lf], color='red', alpha=0.5)
                
    # asignamos titulo y guardamos
    plt.suptitle(var+', '+est.replace('_',' ')+', '+Ti[4:6]+'/'+Ti[2:4] \
              +'/'+Ti[0:2] +' - '+Tf[4:6]+'/'+Tf[2:4]+'/'+Tf[0:2])
    fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+est+'/' \
    +CoM+'/PorAño/'+var+'_'+Ti+'_'+Tf+'.png', bbox_inches='tight',dpi=300)
    plt.show
        
    
    
def Vis_LSAD(est,CoM,var,un,Fi,Ff,c):
    # Las variablesa usar son:
    # est: estación (string).
    # CoM: var. Contaminantes o Meteorologica (string).
    # var: variable/contaminantes a utilizar (string).
    # un: unidades de variable (string).
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

    # definimos fechas para titulo y ruta de guardado
    Ti = Tr[0].strftime('%y%m%d')
    Tf = Tr[-1].strftime('%y%m%d')
    
    # Por último, ploteamos como serie total o por año:
            
    # Encontramos cantidad de años a plotear para poder 
    # diseñar subplots acorde a esta cantidad 
    yi=Tr.year[0]; yf=Tr.year[-1]; ys = yf-yi
    # creamos figura
    fig = plt.figure(figsize=(15,5*ys))
            
    # Debemos rellenar los años que no están completos 
    # para que en los subplots aparezcan a escala
    # o sea que se debe rellenar con nans los datos
    # no existentes y usar una T que cubra todo el año
    
    # creamos matriz auxiliar para comparar qué datos faltan para tener
    # años completos
    Tfull = pd.date_range(str(yi)+'-01-01 00:00:00',str(yf) \
                         +'-12-31 23:00:00',freq='H')
    # comparamaos Taux con T con tal de ver qué datos faltan
    Kfull = np.in1d(Tfull,Tr)
    # rellenamos datos de Vr con Nan
    Vfull = np.tile(np.nan,len(Kfull))
    Vfull[Kfull] = Vr
    
    # ploteamos subplots
    for i in range(ys+1):
        Ty = Tfull[Tfull.year==yi+i]
        plt.subplot(ys+1,1,i+1)
        plt.plot(Ty,Vfull[Tfull.year==yi+i])
        plt.grid()
        plt.title(str(yi+i))
        plt.ylabel(var+' ['+un+']')
        plt.xlim(Ty[0]-Ty.freq*150,Ty[-1]+Ty.freq*150)
        if i == ys:
            plt.xlabel('Tiempo [h]')
            
        # creamos df para IQR y pasamos Vfull y Tfull a dataframe
        Y = pd.DataFrame({'T':Ty})
        Y['V'] = Vfull[Tfull.year==yi+i]
                
        # IQR
        Q1 = Y['V'].quantile(0.25)
        Q3 = Y['V'].quantile(0.75)
        IQR = Q3- Q1
        # c = 2
        min_t = Q1 - c*IQR
        max_t = Q3 + c*IQR
        AD_V = (Y['V'].clip(lower = min_t,upper=max_t) != Y['V'])
        # ploteamos zonas rojas con anomalías
        for j in range(len(AD_V)):
            
            if AD_V[j] == False:
                continue
            else:
                li = j
                
                while j+1 == True:
                    j=j+1
                lf = j
                plt.axvspan(Ty[li], Ty[lf], color='red', alpha=0.5)
                
    # asignamos titulo y guardamos
    plt.suptitle(var+', '+est.replace('_',' ')+', '+Ti[4:6]+'/'+Ti[2:4] \
              +'/'+Ti[0:2] +' - '+Tf[4:6]+'/'+Tf[2:4]+'/'+Tf[0:2])
    fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
    plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+est+'/' \
    +CoM+'/PorAño/'+var+'_'+Ti+'_'+Tf+'.png', bbox_inches='tight',dpi=300)
    plt.show
        