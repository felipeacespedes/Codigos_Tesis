# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 13:33:16 2023

@author: felip

Código para visualizar serie completa de variables 

"""
# Librerías 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Vis(est,CoM,var,un,Fi,Ff,ToPA):
    # Las variablesa usar son:
    # est: estación (string).
    # CoM: var. Contaminantes o Meteorologica (string).
    # var: variable/contaminantes a utilizar (string).
    # un: unidades de variable (string).
    # Fi: fecha inicial como "2018-01-01" (string).
    # Ff: fecha final como "2018-01-01" (string).
    # ToPA: si se ploteal serie Total o por Año.
    
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
    
    # Serie total
    if ToPA == 'Total':
        # definimos los límites inferior y superior de fecha
        Li=pd.date_range(str(Tr.year[0])+'-01-01 00:00:00' \
                    ,str(Tr.year[0])+'-01-01 00:00:00',freq='H')
        Ls=pd.date_range(str(Tr.year[-1])+'-12-31 23:00:00' \
                    ,str(Tr.year[-1])+'-12-31 23:00:00',freq='H')
        
        fig = plt.figure(figsize=(15,5))
        plt.plot(Tr,Vr)
        plt.grid()
        # plt.ylim([-0.2,4])
        plt.xlim(Li-Tr.freq*300,Ls+Tr.freq*300)
        # asignamos ymax por contmainante
        if var == 'HCNM':
            plt.ylim(0,2.5)
        elif var == 'MP25':
            plt.ylim(0,200)
        elif var == 'CO':
            plt.ylim(0,2.5)
        plt.ylabel(var+' ['+un+']')
        plt.xlabel('Tiempo [h]')
        plt.title(var+', '+est.replace('_',' ')+', '+Ti[4:6]+'/'+Ti[2:4] \
                  +'/'+Ti[0:2] +' - '+Tf[4:6]+'/'+Tf[2:4]+'/'+Tf[0:2])
        fig.tight_layout(pad=1.5)

        plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+est+'/' \
        +CoM+'/Total/'+var+'_'+Ti+'_'+Tf+'.png', bbox_inches='tight',dpi=300) 
        plt.show()
            
    elif ToPA == 'PorAño':
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
            # asignamos ymax por contmainante
            if var == 'HCNM':
                plt.ylim(0,2.5)
            elif var == 'MP25':
                plt.ylim(0,200)
            elif var == 'CO':
                plt.ylim(0,2.5)
            if i == ys:
                plt.xlabel('Tiempo [h]')
                

            
        # asignamos titulo y guardamos
        plt.suptitle(var+', '+est.replace('_',' ')+', '+Ti[4:6]+'/'+Ti[2:4] \
                  +'/'+Ti[0:2] +' - '+Tf[4:6]+'/'+Tf[2:4]+'/'+Tf[0:2])
        fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
        plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+est+'/' \
        +CoM+'/PorAño/'+var+'_'+Ti+'_'+Tf+'.png', bbox_inches='tight',dpi=300)
        plt.show
            
        

def Vis_Est( var_df, var_str, un_str, Fi_str, Hi, Ff_str, Hf, ymin, ymax):
    ## Variables:
        # - var_df: data frame con index cómo serie de tiempo y columnas
        #           cómo series de estaciones.
        # - var_str: variable a plotear (string).
        # - un_str: unidad de var_str (string).
        # - Fi_str: Fechas inicial en formato string 'YYYY-MM-DD'.
        # - Hi: Hora de Fi desde la que se realizará la corrección.
        # - Ff_str: Fecha final en formato string 'YYYY-MM-DD'.
        # - Hf: Hora de Ff hasta la que se realizará la corrección.
        # - ymin: valor mínimo de y.
        # - ymax: valor máximo de y.
        
    # Definimos timestamps
    Fi = pd.Timestamp(Fi_str+' '+Hi+':00:00')
    Ff = pd.Timestamp(Ff_str+' '+Hf+':00:00')
    mask = (var_df.index >= Fi) & (var_df.index <= Ff)
    
    # Creamos figura
    plt.style.use('bmh')
    fig = plt.figure(figsize=(15,3*len(var_df.columns)))
    ei = 0
    for e in var_df.columns: 
        
        ax = plt.subplot(len(var_df.columns),1,ei+1)
        ax.plot(var_df.loc[mask,e])
        ax.set_title(e)
        ax.set_ylabel(var_str+' ['+un_str+']')
        ax.set_ylim(ymin,ymax)
        # plt.xticks(rotation=20)
        

        if ei == len(var_df.columns):
            ax.set_xlabel('Tiempo [h]')
            
        fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
        ei += 1

    plt.show()
        
            
        
            
        