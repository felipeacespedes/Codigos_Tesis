# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 15:31:32 2024

@author: felip

Código para introducir 2 fechas en las que se restará un valor a determinar 
con tal de corregir el nivel base de ese periodo
"""
## Librerías
import pandas as pd
import numpy as np

## Funcnión Corr_Ser
def Corr_Ser(T, var,Fi_str, Hi, Ff_str, Hf, op, val):
    ## Variables:
        # - Fi_str: Fechas inicial en formato string 'YYYY-MM-DD'.
        # - Hi: Hora de Fi desde la que se realizará la corrección.
        # - Ff_str: Fecha final en formato string 'YYYY-MM-DD'.
        # - Hf: Hora de Ff hasta la que se realizará la corrección.
        # - file: Archivo de variable a corregir.
        # - val: Valor de corrección a aplicar.
        # - op: Operación a aplicar (sum or mult)
        
    # Definimos timestamps
    Fi = pd.Timestamp(Fi_str+' '+Hi+':00:00')
    Ff = pd.Timestamp(Ff_str+' '+Hf+':00:00')
    
    ## Importamos variable: Serie original sin corregir (Ser_or)
    Ser_df = pd.DataFrame({'T': T})
    Ser_df = Ser_df.set_index('T')
    Ser_df['Ser_or'] = var    
    
    ## Obtenemos serie de periodo a corregir (Ser_pc)
    # Mascara
    mask = (Ser_df.index >= Fi) & (Ser_df.index <= Ff)

    # Serie corregida
    Ser_df['Ser_corr'] = Ser_df['Ser_or'].copy()
    # Operación de suma
    if op == 'sum':
        Ser_df.loc[mask, 'Ser_corr'] += val
    # Operación de multiplicación 
    elif op == 'mult':
        Ser_df.loc[mask, 'Ser_corr'] *= val
    elif op == 'nan':
        Ser_df.loc[mask, 'Ser_corr'] *= np.nan
    else:
        print('Operación desconocida, introduzca sum o mult en formato str.')
    
    ## Retornamos Serie Corregida
    return Ser_df['Ser_corr']
    
    # Ser_df.loc[mask,'Ser_or']: selecciona sección de df entre Fi y Ff  
    
    
