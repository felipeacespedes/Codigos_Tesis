# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 13:09:41 2023

@author: felip
"""

# Código para ejecutar script "download_SINCA.py"
#%% Librerías

from download_SINCA import sinca_aq, sinca_met
import os

#%% Definimos variables

# Lista de contaminantes
c_aq = ['NMHC','CO','PM25']

# Lista de variables meteorologicas 
c_met = ['WDIR','WSPD']

# Regiones
R = ['RV']

# Fechas
i = '2019-01-01'
f = '2023-12-31'

os.chdir('C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Download_code')


#%% Ejecutamos

for j in R:
    print(j)
    # sinca_aq(i,f,j,c_aq)
    sinca_met(i,f,j,c_met)
    
 