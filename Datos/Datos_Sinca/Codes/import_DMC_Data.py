# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:41:01 2023

@author: felip

Código para descargar datos de EMAs de la DMC por mes. 
Para esto se debe especificar el:
    -Código de estación
    -Año
    -Mes
"""


import requests
import json
import pandas as pd
import numpy as np
    
#%% Definimos función para obtener datos de la DMC

def import_DMC(F1,F2,num_est,correo,apikey):
    # Variables:
    # F1: año y mes de inicio en formato '2020/01' (string).
    # F2: año y mes de termino en formato '2020/02' (string).
    # num_est: número de código de estación DMC.
    # correo: correo electronico de cuenta DMC.
    # apikey: apikey de cuenta DMC.
    
    # creamos lista con YYYY/MM a usar
    YM = pd.date_range(F1,F2,freq='M').strftime('%Y/%m')
    
    # creamos data frame 
    cols = ['momento', 'fuerzaDelViento','direccionDelViento'\
            ,'temperatura','puntoDeRocio','humedadRelativa' \
            ,'presionEstacion','presionNivelDelMar','radiacionGlobalInst']
    
    dat = pd.DataFrame(columns=cols)
    
    for ym in YM:
        # Cargamos JSON del link
        JSON = json.loads(requests.get("https://climatologia.meteochile.gob.cl/" \
                                +"application/servicios/getDatosRecientesEma/" \
                                +num_est+"/"+ym+"?usuario=" \
                                +correo+"&token="+apikey).text)
        # normalizamos datos JSON a data frame
        norm = pd.json_normalize( JSON['datosEstaciones']['datos'] )

        # extraemos variables de interés a dat_r
        dat_r = norm.loc[:,['momento', 'fuerzaDelViento','direccionDelViento'\
                        ,'temperatura','puntoDeRocio','humedadRelativa' \
                        ,'presionEstacion','presionNivelDelMar','radiacionGlobalInst']]
        
        # concatenamos dat con dat_r según momento
        dat = pd.concat([dat,dat_r]).sort_values('momento')
        
    # reseteamos indice, ya que al concatenar este se acumula
    dat = dat.reset_index()
    del dat['index']
    
    # ahora, separamos los strings y nos quedamos con la parte inicial
    # o sea, sin unidades, para luego transformar a floats, esto debe
    # realizarse por columna
    for c in cols[1:len(cols)]:
        dat[c] = dat[c].str.split(n=1).str[0].astype(float)
        
    # Chequeamos qué elementos faltan en la matriz T qué se encuentran en Tr
    T = dat['momento']
    Tr = pd.date_range(dat['momento'][0] \
        ,dat['momento'][len(dat['momento'])-1] \
            ,freq='15min')

    # len(set(Tr) - set(T))

    # rellenamos DAtos faltantes con NAn
    # Ahora hacemos la intersección, de manera que en Vr queden 
    # todos los datos necesarios de V y se desechen los que no
    # indices T
    Kt = np.in1d(T,Tr)
    # indices Tr
    Ktr = np.in1d(Tr,T)

    # creamos dataframe con variable T
    DMC_df = pd.DataFrame({'T': Tr})
    V =   ['fuerzaDelViento','direccionDelViento'\
         ,'temperatura','puntoDeRocio','humedadRelativa' \
         ,'presionEstacion','presionNivelDelMar','radiacionGlobalInst']
        
    Vnuevo = ['Velocidad','Dirección'\
             ,'T','Tpr','HR' \
             ,'P','Pnm','Rgi']
    i = 0
    for v in V: 

        # Array de datos original
        V = np.array(dat[v])

        # Array de datos requerida
        # primero la rellenamos con Nans
        Vr = np.tile(np.nan,len(Ktr))

        # Rellenamos Vr con datos de V de interés
        Vr[Ktr] = V[Kt]
        
        # Readjudicamos matriz con Nan a df
        DMC_df[Vnuevo[i]] = Vr
        
        # Conteo para cambiar columnas de DF 
        i = i + 1
    
    # Guardamos entregamos dataframe con datos requeridos
    DMC_df.to_pickle('DMC_df.pkl')
    return DMC_df
    