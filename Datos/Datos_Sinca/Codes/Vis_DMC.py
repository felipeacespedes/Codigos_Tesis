# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 09:11:05 2023

@author: felip
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Vis_DMC(file_pkl,var,un,ToPA):
    # Las variablesa usar son:
    # file_pkl = nombre de archivo pkl para cargar data frame (string).
    # var: variable a utilizar (string de columna).
    # un: unidades de variable (string).
    # ToPA: si se ploteal serie Total o por Año.
    
    # importamos datos
    Vdat = pd.read_pickle(file_pkl)
    
    # separamos en matris de calomuna de interés y timepo
    V = np.array(Vdat[var])
    T = Vdat['momento']
    

    # definimos fechas para titulo y ruta de guardado
    Ti = T[0].strftime('%y%m%d')
    Tf = T[len(T)-1].strftime('%y%m%d')
    
    # Por último, ploteamos como serie total o por año:
    
    # Serie total
    if ToPA == 'Total':
        # definimos los límites inferior y superior de fecha
        Li=pd.date_range(str(T.year[0])+'-01-01 00:00:00' \
                    ,str(T.year[0])+'-01-01 00:00:00',freq='15min')
        Ls=pd.date_range(str(T.year[len(T)-1])+'-12-31 23:45:00' \
                    ,str(T.year[len(T)-1])+'-12-31 23:45:00',freq='15min')
        
        fig = plt.figure(figsize=(15,5))
        plt.plot(T,V)
        plt.grid()
        # plt.ylim([-0.2,4])
        plt.xlim(Li-T.freq*300,Ls+T.freq*300)
        plt.ylabel(var+' ['+un+']')
        plt.xlabel('Tiempo [15m]')
        plt.title(var+', Quintero Climatológica, '+Ti[4:6]+'/'+Ti[2:4] \
                  +'/'+Ti[0:2] +' - '+Tf[4:6]+'/'+Tf[2:4]+'/'+Tf[0:2])
        fig.tight_layout(pad=1.5)

        plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/DMC/' \
        +'/Total/'+var+'_'+Ti+'_'+Tf+'.png', bbox_inches='tight',dpi=300) 
        plt.show()
            
    elif ToPA == 'PorAño':
        # Encontramos cantidad de años a plotear para poder 
        # diseñar subplots acorde a esta cantidad 
        yi=T.year[0]; yf=T.year[len(T)-1]; ys = yf-yi
        # creamos figura
        fig = plt.figure(figsize=(15,5*ys))
                
        # Debemos rellenar los años que no están completos 
        # para que en los subplots aparezcan a escala
        # o sea que se debe rellenar con nans los datos
        # no existentes y usar una T que cubra todo el año
        
        # creamos matriz auxiliar para comparar qué datos faltan para tener
        # años completos
        Tfull = pd.date_range(str(yi)+'-01-01 00:00:00',str(yf) \
                             +'-12-31 23:15:00',freq='15min')
        # comparamaos Taux con T con tal de ver qué datos faltan
        Kfull = np.in1d(Tfull,T)
        # rellenamos datos de Vr con Nan
        Vfull = np.tile(np.nan,len(Kfull))
        Vfull[Kfull] = V
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
                plt.xlabel('Tiempo [15m]')
        # asignamos titulo y guardamos
        plt.suptitle(var+', Quintero Climatológica, '+Ti[4:6]+'/'+Ti[2:4] \
                  +'/'+Ti[0:2] +' - '+Tf[4:6]+'/'+Tf[2:4]+'/'+Tf[0:2])
        fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
        plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/' \
        '/PorAño/'+var+'_'+Ti+'_'+Tf+'.png', bbox_inches='tight',dpi=300)
        plt.show