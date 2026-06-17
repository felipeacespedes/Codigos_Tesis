# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:04:30 2024

Código para plotear diagramas ternarios de las estaciones Pyxis GC
utilizando las funciones creadas en Tern_PyxisGC.
"""
# Importamos librerias y funciones de interés
from Tern_PyxisGC_functs import COV_TimeSeries\
                                , COV_Ternary_ColoredPeriods\
                                , COV_Ternary_ColoredMoments
import pickle

#%% Importamos datos 

# Importamos diccionario con dataframes de estaciones en ppb
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_PyxisGC/'
with open(path+'Py_og_ppb.pkl', 'rb') as file:
    Py_og = pickle.load(file)

del file
#%% Identificamos periodos de altas rm en HCNM

# Recordamos las estaciones de SINCA que tienen estaciones Pyxis en cercanías
    #  SINCA   |   PyxisGC
    # --------------------
    #    VE    |   PU_FLR
    #    CQ    |   QU_CQ
    #    CC    |   CC_JIC
    #    CO    |   CO_EPC

# Así, anotamos periodos de altas rm por estación
cols = Py_og['QU_CQ'].columns

# Ventanas:
VE = ['2024-03-26 04:00:00','2024-05-24 10:00:00','2024-06-24 06:00:00']

# Centro Quintero:
CQ = ['2024-03-15 11:00:00','2024-04-17 21:00:00','2024-04-18 07:00:00'
     ,'2024-05-14 03:00:00','2024-05-14 04:00:00','2024-05-14 05:00:00'
     ,'2024-05-15 22:00:00','2024-05-16 23:00:00','2024-05-17 05:00:00'
     ,'2024-05-17 07:00:00','2024-05-25 06:00:00','2024-06-11 08:00:00'
     ,'2024-06-29 09:00:00','2024-06-30 01:00:00','2024-07-12 20:00:00'
     ,'2024-07-17 21:00:00','2024-07-18 03:00:00','2024-07-18 06:00:00'
     ,'2024-07-18 09:00:00']

# Concón
# No tiene datos uwu

# Colmo
CO = ['2024-03-15 04:00:00','2024-03-16 00:00:00','2024-05-19 17:00:00'
     ,'2024-06-02 21:00:00','2024-06-07 20:00:00','2024-06-12 18:00:00'
     ,'2024-06-29 19:00:00','2024-06-30 11:00:00','2024-07-01 18:00:00'
     ,'2024-07-19 14:00:00','2024-07-24 18:00:00','2024-07-24 19:00:00']

#%% Ploteamos periodos de interés en diagrama ternario
# Definimos un path para guardar los plots
path = 'C:/Users/felip/Desktop/Avances/10/2024/DT/'
#%% VE
est = 'PU_FLR'
Py_VE = Py_og[est].loc['2024-03-01 00:00:00':'2024-07-31 23:00:00',cols]
ni = 0; nf = 3
ran = int(len(VE)/4)
for i in range(ran+1):
    if nf < len(VE):
        COV_Ternary_ColoredMoments(Py_VE,VE[ni:nf+1],path+est+'_'+str(i+1))
    else:
        COV_Ternary_ColoredMoments(Py_VE,VE[ni:len(VE)+1],path+est+'_'\
                                   +str(i+1))
    ni = ni+4
    nf = nf+4
del est, Py_VE, ni, nf, ran, i
#%% CQ
est = 'QU_CQ'
Py_CQ = Py_og[est].loc['2024-03-01 00:00:00':'2024-07-31 23:00:00',cols]
ni = 0; nf = 3
ran = int(len(CQ)/4)
for i in range(ran+1):
    if nf < len(CQ):
        COV_Ternary_ColoredMoments(Py_CQ,CQ[ni:nf+1],path+est+'_'+str(i+1))
    else:
        COV_Ternary_ColoredMoments(Py_CQ,CQ[ni:len(CQ)+1],path+est+'_'\
                                   +str(i+1))
    ni = ni+4
    nf = nf+4
del est, Py_CQ, ni, nf, ran, i
#%% CO
est = 'CO_EPC'
Py_CO = Py_og[est].loc['2024-03-01 00:00:00':'2024-07-31 23:00:00',cols]
ni = 0; nf = 3
ran = int(len(CO)/4)
for i in range(ran+1):
    if nf < len(CO):
        COV_Ternary_ColoredMoments(Py_CO,CO[ni:nf+1],path+est+'_'+str(i+1))
    else:
        COV_Ternary_ColoredMoments(Py_CO,CO[ni:len(CO)+1],path+est+'_'\
                                   +str(i+1))
    ni = ni+4
    nf = nf+4
del est, Py_CO, ni, nf, ran, i

#%% Ploteamos periodos de interes en serie de tiempo 
path = 'C:/Users/felip/Desktop/Avances/10/2024/TS/'
#%% VE
est = 'PU_FLR'
COV_TimeSeries( Py_og[est], '2024-03-01 00:00:00'
               , '2024-07-31 23:00:00', path+est)
del est
#%% CQ
est = 'QU_CQ'
COV_TimeSeries( Py_og[est], '2024-03-01 00:00:00'
               , '2024-07-31 23:00:00', path+est)
del est
#%% CO
est = 'CO_EPC'
COV_TimeSeries( Py_og[est], '2024-03-01 00:00:00'
               , '2024-07-31 23:00:00', path+est)
del est




