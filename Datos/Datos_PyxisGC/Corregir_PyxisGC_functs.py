# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 10:26:25 2024

@author: felip

Código para plotear y corregir datos Pyxis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

## Plotear

# Plot_per: función para plotear periodo con T[i] y T[f]
def Plot_per(Cont, Est_str, Est_df, FC_df, T, ti, tf, ymax, save, OGoML):
    # Cont: recibe string de 'BETX' para plotear todos,
    # o recibe 1 contaminante, tal cómo salen escritos en las columnas.
    # Est_str: string de estación a seleccionar de el diccionario de estaciones.
    # Est_df: df de estación a utilizar.
    # FC_df: df de factor de conversión de ug/m3 a ppb. Contiene factores y LODs.
    # T: Serie de tiempo creada para idnexar DFs.
    # ti/tf: fecha inicial/final escrita cómo string ('2023-06-01 00:00:00').
    # ymax: valor máximo en eje y para plots.
    # save: True para guardar, False para no guardar.
    # OGoML: strings 'OG' o 'ML', que significan Original o Modificado y con
    # aplicación de LOD, que se usan para el guardado de los plots.
    
    
    # Parametros
    ymax_fold = str(ymax).replace('.',',')
    lod_df = FC_df['LOD']
    
    # Definimos fechas especificas
    i = T.get_loc(ti)
    f = T.get_loc(tf)

    
    if Cont == 'BETX':
        cols = Est_df.columns
        ax = Est_df.loc[T[i]:T[f],cols]\
            .plot(subplots=True, layout=(4,1), ylabel='[ppb]'\
            , grid=True, figsize=(15,13), ylim=(0,ymax))
        ai = 0
        for axis in ax.flatten():
            axis.axhline(y=lod_df[cols[ai]], color='r', linestyle='--'\
                , label='LOD='+str('{0:.4f}'.format(lod_df[cols[ai]]))\
                , alpha=0.5)
            axis.legend()
            ai = ai+1
        plt.suptitle(Est_str+', BETX')
        plt.tight_layout()
        
        if save == True and OGoML in ['OG','ML']:
            path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Pyxis_GC/'+Est_str\
                    +'/'+OGoML+Cont+'/ymax '+ymax_fold+'/'
            os.makedirs(path, exist_ok=True) 
            plt.savefig(ti[0:-3]+'.png',dpi=300)
    
    # Plotear 1 contaminantes
    elif Cont in Est_df.columns:
        fig = plt.figure(figsize=(20,9))
        plt.plot(T[i:f+1],Est_df.loc[T[i]:T[f],Cont])
        plt.hlines(lod_df[Cont],T[i],T[f], color='r',linestyles='dashed'
                   , label='LOD='+str('{0:.4f}'.format(lod_df[Cont]))
                   , alpha=0.5)
        plt.ylim(0,ymax)
        plt.xticks(rotation=20)
        plt.ylabel('[ppb]')
        plt.title(Est_str+', '+Cont+'.')
        plt.legend()
        fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

        if save == True and OGoML in ['OG','ML']:
            path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Pyxis_GC/'+Est_str\
                    +'/'+OGoML+Cont+'/ymax '+ymax_fold+'/'
            os.makedirs(path, exist_ok=True) 
            plt.savefig(ti[0:-3]+'.png',dpi=300)
            
    else:
        print('Contaminante no se encontró. Revisar escritura de Cont.')
        

# Plot_dias: Plotear n días desde una fecha especifica
def Plot_dias(Cont, Est_str, Est_df, FC_df, T, ti, ndias, ymax, save, OGoML):
    # Cont: recibe string de 'BETX' para plotear todos,
    # o recibe 1 contaminante, tal cómo salen escritos en las columnas.
    # Est_str: string de estación a seleccionar de el diccionario de estaciones.
    # Est_df: df de estación a utilizar.
    # FC_df: df de factor de conversión de ug/m3 a ppb. Contiene factores y LODs.
    # T: Serie de tiempo creada para idnexar DFs.
    # ti: fecha inicial escrita cómo string ('2023-06-01').
    # ndias: cantidad de días (int) a plotear a partir de ti.
    # ymax: valor máximo en eje y para plots.
    # save: True para guardar, False para no guardar.
    # OGoML: strings 'OG' o 'ML', que significan Original o Modificado y con
    # aplicación de LOD, que se usan para el guardado de los plots.
    
    
    # Parametros
    ymax_fold = str(ymax).replace('.',',')
    lod_df = FC_df['LOD']
    
    # Definimos fechas especificas
    i = T.get_loc(pd.to_datetime(ti+' 00:00:00'))
    f = T.get_loc(pd.to_datetime(ti+' 00:00:00')
                  +datetime.timedelta(days=ndias))

    
    if Cont == 'BETX':
        cols = Est_df.columns
        ax = Est_df.loc[T[i]:T[f],cols]\
            .plot(subplots=True, layout=(4,1), ylabel='[ppb]'\
            , grid=True, figsize=(15,13), ylim=(0,ymax))
        ai = 0
        for axis in ax.flatten():
            axis.axhline(y=lod_df[cols[ai]], color='r', linestyle='--'\
                , label='LOD='+str('{0:.4f}'.format(lod_df[cols[ai]]))\
                , alpha=0.5)
            axis.legend()
            ai = ai+1
        plt.suptitle(Est_str+', BETX')
        plt.tight_layout()
        
        if save == True and OGoML in ['OG','ML']:
            path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Pyxis_GC/'+Est_str\
                    +'/'+OGoML+Cont+'/ymax '+ymax_fold+'/'
            os.makedirs(path, exist_ok=True) 
            plt.savefig(ti[0:-3]+'.png',dpi=300)
    
    # Plotear 1 contaminantes
    elif Cont in Est_df.columns:
        fig = plt.figure(figsize=(20,9))
        plt.plot(T[i:f+1],Est_df.loc[T[i]:T[f],Cont])
        plt.hlines(lod_df[Cont],T[i],T[f], color='r',linestyles='dashed'
                   , label='LOD='+str('{0:.4f}'.format(lod_df[Cont]))
                   , alpha=0.5)
        plt.ylim(0,ymax)
        plt.xticks(rotation=20)
        plt.ylabel('[ppb]')
        plt.title(Est_str+', '+Cont+'.')
        plt.legend()
        fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])

        if save == True and OGoML in ['OG','ML']:
            path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Pyxis_GC/'+Est_str\
                    +'/'+OGoML+Cont+'/ymax '+ymax_fold+'/'
            os.makedirs(path, exist_ok=True) 
            plt.savefig(ti[0:-3]+'.png',dpi=300)
            
    else:
        print('Contaminante no se encontró. Revisar escritura de Cont.')
        

# Plot_mes: Plotear todos los meses de la serie.
def Plot_mes(Cont, Est_str, Est_df, FC_df, T, ymax, save, OGoML):
    # Cont: recibe string de 'BETX' para plotear todos,
    # o recibe 1 contaminante, tal cómo salen escritos en las columnas.
    # Est_str: string de estación a seleccionar de el diccionario de estaciones.
    # Est_df: df de estación a utilizar.
    # FC_df: df de factor de conversión de ug/m3 a ppb. Contiene factores y LODs.
    # T: Serie de tiempo creada para idnexar DFs.
    # ymax: valor máximo en eje y para plots.
    # save: True para guardar, False para no guardar.
    # OGoML: strings 'OG' o 'ML', que significan Original o Modificado y con
    # aplicación de LOD, que se usan para el guardado de los plots.


    # 2023
    for m in np.arange(4,13,1):
        # Definimos parametros de fechas
        mes = '0'+str(m) if m<10 else str(m)
        date = '2023-'+mes+'-01'
        days = 29
        
        # Ploteamos
        Plot_dias(Cont, Est_str, Est_df, FC_df, T, date, days, ymax, save, OGoML)

    # 2023
    for m in np.arange(1,9,1):
        # Definimos parametros de fechas
        mes = '0'+str(m) if m<10 else str(m)
        date = '2024-'+mes+'-01'
        days = 29
        
        # Ploteamos
        Plot_dias(Cont, Est_str, Est_df, FC_df, T, date, days, ymax, save, OGoML)



# Corr_ser: Corregir series, esto es, hacer Nan los valores entre fechas 
#           de interés.
def Corr_ser(Est_str, Est_df, fi, hi, ff, hf):
    ## Variables:
        # Est_str: string de estación a seleccionar de el diccionario de estaciones.
        # Est_df: df de estación a utilizar.
        # fi: Fechas inicial en formato string 'YYYY-MM-DD'.
        # hi: Hora de Fi desde la que se realizará la corrección.
        # ff: Fecha final en formato string 'YYYY-MM-DD'.
        # hf: Hora de Ff hasta la que se realizará la corrección.


    # Definimos lista de BETX
    cont = Est_df.columns

    # Definimos timestamps
    Fi = pd.Timestamp(fi+' '+hi+':00:00')
    Ff = pd.Timestamp(ff+' '+hf+':00:00')
        
    ## Generamos variable: 
    # Serie original sin corregir (Ser_or)
    Ser_og = Est_df.copy()
    # Serie corregida
    Ser_corr = Est_df.copy()
    
    ## Obtenemos serie de periodo a corregir (Ser_corr)
    # Mascara
    mask = (Ser_og.index >= Fi) & (Ser_og.index <= Ff)
    
    ## Hacemos Nan sección:
    Ser_corr.loc[mask, cont] *= np.nan

    ## Retornamos Serie Corregida
    return Ser_corr

# LOD_betx: Aplicar LOD a cada uno de los 4 compuestos según corresponda, y
#           entregar DF de vuelta.
def LOD(Est_df, FC_df):
    ## Variables:
        # Est_df: df de estación a aplicar LOD.
        # FC_df: df de factor de conversión de ug/m3 a ppb.
        #        Contiene factores y LODs.
    
    # Creamos copia de DF para rellenar
    Est_ml_df = pd.DataFrame().reindex_like(Est_df)
    
    # Contaminantes
    cont = Est_df.columns     
    
    # Iteramos en contaminantes
    for c in cont:
        lod = FC_df.loc[c,'LOD']
        cov = Est_df.loc[Est_df.index,c].copy()
        cov[cov <= lod] = lod
        Est_ml_df[c] = cov
        del cov
    
    # Regresamos DF con LOD aplicado para cada BETX
    return Est_ml_df
        
    
    
    
    
    