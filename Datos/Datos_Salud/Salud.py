# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 12:50:14 2024

@author: felip
"""

import pandas as pd

#%% Importamos datos egresos 

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Salud/Egresos_Hospitalarios/'
file = 'EGRE_DATOS_ABIERTOS_2022.csv'
Eg_2022 = pd.read_csv(path+file,delimiter=';',encoding='latin-1')

#%% Seleccionamos datos de interés (Región Valaparaiso)

