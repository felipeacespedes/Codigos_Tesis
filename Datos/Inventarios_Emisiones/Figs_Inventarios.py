# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 17:05:14 2026

@author: felip
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import FI_funcs as fi

path_data = 'C:/Users/felip/Desktop/U/Tesis/Datos/Inventarios_Emisiones/'

#%% Importamos tablas

COVs_2022 = pd.read_csv(path_data+'2022/COVs_2022.csv', nrows=10)
COVs_2022.iloc[:,1] = COVs_2022.iloc[:,1].str.replace(',','.').astype(float)

Ben_2022 = pd.read_csv(path_data+'2022/Benceno_2022.csv', nrows=10)
Ben_2022.iloc[:,1] = Ben_2022.iloc[:,1].str.replace(',','.').astype(float)

Tol_2022 = pd.read_csv(path_data+'2022/Tolueno_2022.csv', nrows=10)
Tol_2022.iloc[:,1] = Tol_2022.iloc[:,1].str.replace(',','.').astype(float)

SO2_2022 = pd.read_csv(path_data+'2022/SO2_2022.csv', nrows=10)
SO2_2022.iloc[:,1] = SO2_2022.iloc[:,1].str.replace('.','')
SO2_2022.iloc[:,1] = SO2_2022.iloc[:,1].str.replace(',','.').astype(float)

COVs_2023 = pd.read_csv(path_data+'2023/COVs_2023.csv', nrows=10)
COVs_2023.iloc[:,1] = COVs_2023.iloc[:,1].str.replace(',','.').astype(float)

Ben_2023 = pd.read_csv(path_data+'2023/Benceno_2023.csv', nrows=10)
Ben_2023.iloc[:,1] = Ben_2023.iloc[:,1].str.replace(',','.').astype(float)

Tol_2023 = pd.read_csv(path_data+'2023/Tolueno_2023.csv', nrows=10)
Tol_2023.iloc[:,1] = Tol_2023.iloc[:,1].str.replace(',','.').astype(float)

SO2_2023 = pd.read_csv(path_data+'2023/SO2_2023.csv', nrows=10)
SO2_2023.iloc[:,1] = SO2_2023.iloc[:,1].str.replace('.','')
SO2_2023.iloc[:,1] = SO2_2023.iloc[:,1].str.replace(',','.').astype(float)


###############
#%% Barplot ###

############
#%% COVs ###
#%% 2022 
df = COVs_2022
df.plot.barh(x=df.columns[0],y=df.columns[1])
plt.grid(zorder=0,alpha=0.2)
#%% 2023 
df = COVs_2023
df.plot.barh(x=df.columns[0],y=df.columns[1])
plt.grid(zorder=0,alpha=0.2)

###############
#%% Benceno ###
#%% 2022 
df = Ben_2022
df.plot.barh(x=df.columns[0],y=df.columns[1])
plt.grid(zorder=0,alpha=0.2)
#%% 2023
df = Ben_2023
df.plot.barh(x=df.columns[0],y=df.columns[1])
plt.grid(zorder=0,alpha=0.2)

###############
#%% Tolueno ###
#%% 2022
df = Tol_2022
df.plot.bar(x=df.columns[0],y=df.columns[1])
plt.grid(zorder=0,alpha=0.2)
#%% 2023
df = Tol_2023
df.plot.bar(x=df.columns[0],y=df.columns[1])
plt.grid(zorder=0,alpha=0.2)

###########
#%% SO2 ###
#%% 2022
df = SO2_2022
df.plot.bar(x=df.columns[0],y=df.columns[1])
plt.grid(zorder=0,alpha=0.2)
#%% 2023
df = SO2_2023
df.plot.bar(x=df.columns[0],y=df.columns[1])
plt.grid(zorder=0,alpha=0.2)


###################
#%% 2022 y 2023 ###

#%% 1. COVs
fi.procesar_y_graficar('COVs', 'COVs (T/año)', False, 5)

#%% 2. Benceno
fi.procesar_y_graficar('Benceno', 'BENCENO (T/año)', False, 5)

#%% 3. Tolueno
fi.procesar_y_graficar('Tolueno', 'TOLUENO (T/año)', False, 5)

#%% 4. Xileno
fi.procesar_y_graficar('Xileno', 'XILENO (T/año)', False, 5)

#%% 5. SO2
fi.procesar_y_graficar('SO2', 'SO2 (T/año)', False, 5)

#%% 6. MP
fi.procesar_y_graficar('MP', 'MP (T/año)', False, 5)

#%% 7. NOx
fi.procesar_y_graficar('NOx', 'NOX (T/año)', False, 5)










