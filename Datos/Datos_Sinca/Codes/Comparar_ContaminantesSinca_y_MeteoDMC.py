# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 13:34:55 2023

@author: felip

Código para comparar comportamiento de contaminantes y variables 
meteorológicas de estación DMC
"""

#%% Importamos librerías
import pandas as pd
from import_var import import_var
import numpy as np
import matplotlib.pyplot as plt
import os.path


#%% Definimos variables

## Lista de estaciones, contaminantes y unidades de contaminantes

# Estaciones
le = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura' \
     ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo']

# Contaminantes
lv = ['HCNM', 'MP25', 'CO']
# Unidades de contaminantes
lu = ['ppm', r'$\mu g/m^{3}$', 'ppm']

## Fechas ('2018-01-01')

# Total
# Fi = '2019-01-01'
# Ff = '2023-12-31'

# Periodo de interes
# Fi = '2022-08-27'
# Ff = '2022-11-23'

# Episodio 31/08/22
# Fi = '2022-08-31'
# Ff = '2022-08-31'

# Episodio 02/09/22
Fi = '2022-09-02'
Ff = '2022-09-02'

## Vector de tiempo
# T
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

#%% Importamos datos

# Creamos diccionario de estaciones
Var= {}

# Creamos array con Nans para rellenar las variables que no existan
nan = np.empty(len(T)); nan[:] = np.nan
        
# Importamos variables de contaminantes a dataframe de cada estación
lv.append('Dir')
for v in range(len(lv)):
    Var[lv[v]] = pd.DataFrame({'T': T})
    Var[lv[v]] = Var[lv[v]].set_index('T')
    for e in range(len(le)):
        
        file_c = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
        +'Estaciones/'+le[e]+'/Cont/'+lv[v]+'.csv'
        file_m = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
        +'Estaciones/'+le[e]+'/Meteo/'+lv[v]+'.csv'
        if os.path.isfile(file_c) == True:
            Var[lv[v]][le[e]] = import_var(\
                le[e],'Cont',lv[v],Fi,Ff)
                
        elif os.path.isfile(file_m) == True:
            Var[lv[v]][le[e]] = import_var(\
                le[e],'Meteo',lv[v],Fi,Ff)
        else:
            Var[lv[v]][le[e]] = nan
            
        del file_c, file_m
        
lv.remove('Dir')
 
#%% Scatter plots

# Definímos variable meteorologica a examinar y su unidad
met = 'Dir'
met_u = '°'

# Tipo de variable tiempo a examinar
tipo = 'hora' # 'día_año', 'día_semana', 'hora', None

# Carpeta en Scatter para especificar el PERIODO de tiempo
period_dir = '020922' #'Total', 'Interes', '310822', '020922'

for c in lv:
    plt.style.use('fivethirtyeight')
    plt.rcParams.update({'font.size': 10}) # debe estar al comienzo
    cm = plt.cm.get_cmap('hsv')
    for e in le:
        fig, ax = plt.subplots(figsize=(10,8))
        if tipo == 'día_año':
            sc = ax.scatter(x=Var[c][e], y=Var[met][e]\
                            , c=Var[c].index.dayofyear, cmap=cm)
            cb = plt.colorbar(sc, label='[Día del año]') 
        elif tipo == 'día_semana':
            sc = ax.scatter(x=Var[c][e], y=Var[met][e]
                            , c=Var[c].index.dayofweek, cmap=cm)
            cb = plt.colorbar(sc, label='[Día de semana]') 
        elif tipo == 'hora':
            sc = ax.scatter(x=Var[c][e], y=Var[met][e]\
                            , c=Var[c].index.hour, cmap=cm)
            cb = plt.colorbar(sc, label='[Hora del día]') 
        else:
            sc = ax.scatter(x=Var[c][e], y=Var[met][e], c='blue' ,cmap=cm)
            
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.85,0.95,'corr = '+str('%.2f'%Var[c][e].corr(Var[met][e]))\
                , transform=ax.transAxes,fontsize=14,verticalalignment='top'\
                , bbox=props)
        ax.set_title('Series Horarias: '+c+' vs '+met+', '+e+', '+Fi+' a '+Ff\
                     ,fontsize=12)
        plt.xlabel(c+' [ppm]')
        plt.ylabel(met+' ['+met_u+']')
        
        fig.tight_layout(pad=1.1)
        
        # Directorio para guardar figuras
        directory = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/'+ \
                    e+'/Meteo/Scatter/'+period_dir
        
        # Creamos directorios si no existe
        if os.path.isdir(directory) == False:
            os.makedirs(directory)
        
        # Guardamos figuras
        plt.savefig(directory+'/scatter_'+c+'_vs_'+met+'_'+Fi+'_'+Ff+'_'\
                    +tipo+'.png', bbox_inches='tight',dpi=300)
    del e
    
    

