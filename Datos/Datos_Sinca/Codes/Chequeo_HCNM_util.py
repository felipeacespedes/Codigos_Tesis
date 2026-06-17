# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 13:25:43 2023

@author: felip

Código para evaluar qué partes de la serie de HCNM sirve ya que en su mayoria
se encuentra con saltos de nivel base 
"""
# Librerías
import pandas as pd
import matplotlib.pyplot as plt
from import_var import import_var
from Vis_AD_fun import Vis_IQR
from adtk.detector import LevelShiftAD
from adtk.data import validate_series
from adtk.visualization import plot

#%% Cargamos datos de series de timepo de HCNM para 9 estaciones

# Diccionario
Dic = {}

Dic['Estaciones'] = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura','Sur' \
              ,'Junta_Vecinos','Concón','Gaviotas','Colmo']
    
Dic['Variables_Cont'] = ['SO2','CH4','HCNM','HCT','CO',]

Dic['Unidades_Cont'] = ['ppb','ppm','ppm','ppm','ppm']

Dic['Variables_Meteo'] = ['Velocidad','Dirección']

Dic['Unidades_Meteo'] = ['m/s','°']

# Fechas
Fi = '2018-01-01'
Ff = '2023-07-31'

# T: vector de tiempo con Nans si no se tiene el valor 
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

# importamos HCNM entre 27/09/22 y 23/11/22
HCNM = pd.DataFrame({'T':T})
HCNM = HCNM.set_index('T')
for est in Dic['Estaciones']:
    HCNM[est] = import_var(est,'Cont','HCNM',Fi,Ff)



#%% Método IQR

IQR_df = pd.DataFrame({'T':T})
IQR_df = IQR_df.set_index('T')

for est in Dic['Estaciones']:

    Q1 = HCNM[est].quantile(0.25)
    Q3 = HCNM[est].quantile(0.75)
    IQR = Q3- Q1
    c = 2
    min_t = Q1 - c*IQR
    max_t = Q3 + c*IQR
    IQR_df[est] = (HCNM[est].clip(lower = min_t,upper=max_t) != HCNM[est])
    

#%% ploteamos

fig = plt.figure(figsize=(15,5))
plt.plot(HCNM['Ventanas'])
plt.grid()

for i in range(len(IQR_df['Ventanas'])):
    
    if IQR_df['Ventanas'][i] == False:
        continue
    else:
        li = i
        
        while i+1 == True:
            i=i+1
        lf = i
        plt.axvspan(T[li], T[lf], color='red', alpha=0.5)
plt.title('Método IQR aplicado HCNM Ventanas, c ='+str(c))
plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/IQR_Ventanas_c'+str(c)\
            +'.png', bbox_inches='tight',dpi=300)

#%% Probamos función Vis_IQR

Vis_IQR('Ventanas','Cont','HCNM','ppm',Fi,Ff,30)

#%% probamos con librería ADTK

# level shift AD
#https://adtk.readthedocs.io/en/stable/notebooks/demo.html#InterQuartileRangeAD

# s = pd.read_csv('./data/cpu.csv', index_col="Time", parse_dates=True, squeeze=True)
s = HCNM['Ventanas']
s = validate_series(s)
c = 10

level_shift_ad = LevelShiftAD(c=c, side='both', window=5)
anomalies = level_shift_ad.fit_detect(s)
plot(s, anomaly=anomalies, anomaly_color='red'
      ,figsize=(15,3))

plt.title('Método IQR aplicado HCNM Ventanas, c ='+str(c))
plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/LS_Ventanas_c'+str(c)\
            +'.png', bbox_inches='tight',dpi=300)




#%% Ahora intentamos identificar qué parámetros usar


#%% La verdad vamos a probar isolation forest para cambios colectivos 









