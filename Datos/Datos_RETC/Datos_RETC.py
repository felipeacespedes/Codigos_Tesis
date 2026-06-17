# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 16:43:07 2025

@author: felip
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%% Importamos datos

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_RETC/'
DF = pd.read_csv(path+'EmisionesFuentesPuntuales2022.csv',sep=';',engine='python', decimal=',', quotechar='"')

#%% Tomamos solo Región de Valparaiso

DF = DF[DF['region']=='Valparaíso']

#%% Tomamos solo comuna Puhcuncaví y Quintero

DF = DF[(DF['comuna']=='Puchuncaví') | (DF['comuna']=='Quintero')]

#%% Tomamos contaminantes de interes

# SO2
SO2 = DF[DF['id_contaminante'] == 380]

# SOx
SOx = DF[DF['id_contaminante'] == 381]

# NOX
NOx = DF[DF['id_contaminante'] == 303]

# COV
COV = DF[DF['id_contaminante'] == 417]

# MP25
MP25 = DF[DF['id_contaminante'] == 341]

                  