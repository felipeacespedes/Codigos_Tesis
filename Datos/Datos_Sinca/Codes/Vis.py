# -*- coding: utf-8 -*-
"""
Created on Sat May  6 14:25:46 2023

@author: felip
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#### Visualizador de serie de tiempo ####

#%% Importamos csv

# Datos horarios
HCNMh = pd.read_csv('HCNMh_220101_230101.csv'
                 , delimiter=";"
                 , dtype={'a': str, 'b': str, 'c': float} 
                 , skiprows=23
                 , skipfooter=24
                 , usecols=(0,1,4)     
                 , decimal=","
                 , names=['Fecha','Hora','HCNM']
                 , header=0
                 )

# Datos diarios
HCNMd = pd.read_csv('HCNMd_220101_230101.csv'
                 , delimiter=";"
                 , dtype={ 'b': str, 'c': float} 
                  , skiprows=1
                 , usecols=(0,4)   
                 , decimal=","
                 , names=['Fecha','HCNM']
                 )

# Arreglamos serie restando el día anterior ya que viene acumulado
HCNMh = np.array(HCNMh.HCNM)
HCNMd = np.array(HCNMd.HCNM)


#%% Creamos series de tiempo horaria y diaria

t1 = '2022-01-01'; t2 = '2023-01-01'
Th = pd.date_range(start=t1, end=t2, freq='1H',inclusive='left')
Td = pd.date_range(start=t1, end=t2, inclusive='left') #.strftime('%Y-%m-%d')

#%% Ploteamos serie completa

fig = plt.figure(figsize=(15,10))

ax1 = plt.subplot(2,1,1)
plt.plot(Th,HCNMh)
plt.grid()
plt.vlines([Th[5664],Th[7392]],-0.2,4,colors='r',linestyles='dashed')
plt.ylim([-0.2,4])
plt.ylabel('HCNM [ppm]')
plt.xlabel('Tiempo [h]')
plt.title('HCNM horaria 01/01/22 - 31/12/22')
plt.text(0.005, 1.03, 'a)', transform=ax1.transAxes
         , size=10
         , weight='bold'
         )


ax2 = plt.subplot(2,1,2)
plt.plot(Td,HCNMd)
plt.grid()
plt.vlines([Td[236],Td[307]],0,0.5,colors='r',linestyles='dashed')
plt.ylim([0,0.5])
plt.ylabel('HCNM [ppm]')
plt.xlabel('Tiempo [d]')
plt.title('HCNM diario 01/01/22 - 31/12/22')
plt.text(0.005, 1.03, 'b)', transform=ax2.transAxes
         , size=10
         , weight='bold'
         )

fig.tight_layout(pad=2.0)




#%% Ploteamos solo el periodo de interes

# Dede el 31/08/22 al 04/11/22
# horario
Th_pi = Th[5664:7392]
HCNMh_pi = HCNMh[5664:7392]
#diario
Td_pi = Td[236:307]
HCNMd_pi = HCNMd[236:307]



fig = plt.figure(figsize=(15,10))

ax1 = plt.subplot(2,1,1)
plt.plot(Th_pi,HCNMh_pi)
plt.grid()
plt.title('HCNM horaria 25/08/22 - 04/11/22')
plt.ylabel('HCNM [ppm]')
plt.xlabel('Tiempo [h]')
plt.text(0.005, 1.03, 'a)', transform=ax1.transAxes
         , size=10
         , weight='bold'
         )

ax2 = plt.subplot(2,1,2)
plt.plot(Td_pi,HCNMd_pi)
plt.grid()
plt.title('HCNM diario 25/08/22 - 04/11/22')
plt.ylabel('HCNM [ppm]')
plt.xlabel('Tiempo [d]')
plt.text(0.005, 1.03, 'b)', transform=ax2.transAxes
         , size=10
         , weight='bold'
         )

fig.tight_layout(pad=2.0)

#%% Comparación años 2018, 2021 y 2022

# Datos horarios
HCNM_18f = pd.read_csv('HCNM_180101_190101.csv'
                 , delimiter=";"
                 , dtype={'a': str, 'b': str, 'c': float} 
                 , skiprows=0
                 , skipfooter=24
                 , usecols=(0,1,4)     
                 , decimal=","
                 , names=['Fecha','Hora','HCNM']
                 , header=0
                 , na_values=' '
                 )

HCNM_21f = pd.read_csv('HCNM_210101_220101.csv'
                 , delimiter=";"
                 , dtype={'a': str, 'b': str, 'c': float} 
                 , skiprows=0
                 , skipfooter=24
                 , usecols=(0,1,4)     
                 , decimal=","
                 , names=['Fecha','Hora','HCNM']
                 , header=0
                 , na_values=' '

                 )

HCNM_22f = pd.read_csv('HCNM_220101_230101.csv'
                 , delimiter=";"
                 , dtype={'a': str, 'b': str, 'c': float} 
                 , skiprows=0
                 , skipfooter=24
                 , usecols=(0,1,4)     
                 , decimal=","
                 , names=['Fecha','Hora','HCNM']
                 , header=0
                 , na_values=' '
                 )


HCNM_18 = np.array(HCNM_18f.HCNM)
HCNM_21 = np.array(HCNM_21f.HCNM)
HCNM_22 = np.array(HCNM_22f.HCNM)

# cortamos series para invierno extendido
HCNM_18i = HCNM_18[2879:7294]
HCNM_21i = HCNM_21[2879:7294]
HCNM_22i = HCNM_22[2879:7294]


#%% creación de vector tiempo
t1 = '2018-01-01'; t2 = '2019-01-01'
T18 = pd.date_range(start=t1, end=t2, freq='1H',inclusive='left')
T18 = T18[1:len(T18)]

t3 = '2021-01-01'; t4 = '2022-01-01'
T21 = pd.date_range(start=t3, end=t4, freq='1H',inclusive='left')
T21 = T21[1:len(T21)]

t5 = '2022-01-01'; t6 = '2023-01-01'
T22 = pd.date_range(start=t5, end=t6, freq='1H',inclusive='left')
T22 = T22[1:len(T22)]

# Cortamos vectores a invierno extendido
T18_i = T18[2880:7295] 
T21_i = T21[2880:7295]
T22_i = T22[2880:7295]


#%% Ploteamos 3 series

fig = plt.figure(figsize=(15,10))

ax1 = plt.subplot(3,1,1)
plt.plot(T18_i,HCNM_18i,label='HCNM')
plt.hlines([2],T18_i[0],T18_i[-1],colors='r',linestyles='dashed',label='Episodio')
plt.legend()
plt.grid()
plt.title('HCNM horaria invierno 2018')
plt.ylabel('HCNM [ppm/hr]')
plt.xlabel('Tiempo [hr]')
plt.ylim([-0.5,10])
plt.text(0.005, 1.03, 'a)', transform=ax1.transAxes
         , size=10
         , weight='bold'
         )

ax2 = plt.subplot(3,1,2)
plt.plot(T21_i,HCNM_21i,label='HCNM')
plt.hlines([2],T21_i[0],T21_i[-1],colors='r',linestyles='dashed',label='Episodio')
plt.legend()
plt.grid()
plt.title('HCNM horaria invierno 2021')
plt.ylabel('HCNM [ppm/hr]')
plt.xlabel('Tiempo [hr]')
plt.ylim([-0.5,10])
plt.text(0.005, 1.03, 'b)', transform=ax2.transAxes
         , size=10
         , weight='bold'
         )

ax3 = plt.subplot(3,1,3)
plt.plot(T22_i,HCNM_22i,label='HCNM')
plt.hlines([2],T22_i[0],T22_i[-1],colors='r',linestyles='dashed',label='Episodio')
plt.vlines([T22_i[2783],T22_i[-1]],-0.5,10,colors='g',linestyles='dashed'
           ,label='Campaña PTR-SODAR')
plt.legend(loc=2)
plt.grid()
plt.title('HCNM horaria invierno 2022 (año campaña)')
plt.ylabel('HCNM [ppm/hr]')
plt.xlabel('Tiempo [hr]')
plt.ylim([-0.5,10])
plt.text(0.005, 1.03, 'c)', transform=ax3.transAxes
         , size=10
         , weight='bold'
         )

fig.tight_layout(pad=2.0)
plt.savefig('C:/Users/felip/Desktop/U/Seguel/Datos_Sinca/Series_HCNM_18_21_22' \
            +'.png', bbox_inches='tight',dpi=300) 
    
    
#%% Ploteo de día 12/09/22

# preparamos HCNM y tiempo para solo el día 12
HCNM_120922 = HCNM

fig = plt.figure(figsize=(5,10))

ax = plt.subplot(layout='constrained')
plt.plot()

    

# hidronio, acido nitrico y acetona: 21, 29 59
# se ajusta el epsectro cada 10 minutos automaticamente con estas 3 
# masas protonadas
# el error RMS mass error debe ser menor a 10^-3
# el benzeno (masa de carbono 12 + benzeno= 79) en general se mueve en 
# los 1 ppm.
# Las masas mas bonitas son las más pesadas