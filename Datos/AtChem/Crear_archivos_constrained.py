# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 10:42:40 2024

@author: felip

Código para crear archivos de input AtChem que van en carpeta conststrains.
"""
# importamos librerías
import pandas as pd
import numpy as np
import sys

# Creamos función que reciba MasterDF y cree archivo de frecuencia minutaria o 
# o horaria (pero en segundos) para el compuesto o variable meteo que se pida. 
def AtChem_ConstrainFile(DF, names_AtChem, Met_bool, freq, path):
    ## unused variables:
    # name_ptr, date_i, date_f, s_i
    ### Variables ###
    # - DF: Data Frame
    # - name_ptr: string de variable en DF.
    # - date_i/date_f: fechas string inicial/final a utilizar de DF.
    # - names_AtChem: nombres de variables en AtChem entre las que se
    #                 dividirá la razón de mezcla de la variable name_ptr.
    # - s_i: segundos a partir de los que se toma el inicio en AtChem, 
    #        considerando un desface de 4 horas (para UTC-4 son 14400).
    # - Met_bool: True si es variable meteo y False si es compuesto.
    # - freq: frecuencia de la variable, horaria o minutaria, hor o min.
    # - path: string de path con todos los slash ('C:/user/bla/.../')
    
    
    # Definimos variable a extraer del DF entre fechas de interes, pasamos de 
    # ppb a moleculas por cm3 y dividimos entre número de variables, en caso
    # ser un compuesto. De ser variable meteo, solo se entrega variable:
    if type(names_AtChem)==str:
        var = (DF*(2.46*10**10)) if Met_bool==False else DF
    else:
        var = (DF*(2.46*10**10))/len(names_AtChem) if Met_bool==False else DF

    # Parar código en caso de que frecuencia sea erronea
    if freq not in ['min','5min','60min']:
        sys.exit("freq no encontrada, debe ser 'min', '5min' o '60min'. ") 

    # Definimos los valores iniciales y finales para los segundos
    T = DF.asfreq(freq); T = T.index; 
    # contamos horas desde media noche
    hi = T[0].hour
    # creamos variable con segundos desde media noche UTC-4
    si = 14400+(hi*3600)
       
    # sys.exit("Error message")
    
    # Creamos lista de segundos según frecuencia
    if freq == 'min':
        delta = 60
        time = np.arange(si,si+(len(T)*delta),delta)

    elif freq == '5min':
        delta = 300
        time = np.arange(si,si+(len(T)*delta),delta)
        var = var.resample('5min').mean()
        
    elif freq == '60min': 
        delta = 3600
        time = np.arange(si,si+(len(T)*delta),delta)
        var = var.resample('60min').mean()
   
    
    # Guardamos archivos 
    if type(names_AtChem)==str:
        # Definimos df a guardar en archivo 
        file = pd.DataFrame(columns=['time','var'])
        file['time'] = time; file['var'] = var.round(2).values
        # Quitamos cualquier fila que contenga un archivo
        nan = np.nan
        file = file.drop(file[pd.isna(file['var'])].index)
        print(names_AtChem)
        for value in file['var']:
            print(value)
        # file = file.drop(file[file['var']==].index)
        # Guardamos con nombre
        file.to_csv(path+names_AtChem, sep=' ', index=False, header=False)
    else:
        for name in names_AtChem:
            # Definimos df a guardar en archivo 
            file = pd.DataFrame(columns=['time','var'])
            file['time'] = time; file['var'] = var.round(2).values
            # Quitamos cualquier fila que contenga un archivo
            nan = np.nan
            file = file.drop(file[file['var']==nan].index)
            # Guardamos con nombre
            file.to_csv(path+name, sep=' ', index=False, header=False)
            
#
