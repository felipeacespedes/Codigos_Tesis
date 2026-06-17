# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 08:52:00 2025

@author: felip
"""

# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LogNorm
from AtChem_functs import Plot_Prod, Plot_Prod_find, Plot_Loss,\
                            Plot_Loss_find, Plot_Conc, Return_Prod,\
                                Return_Loss, DF_reacts, Calc_Prod, Calc_Loss,\
                                    Calc_find

# Path guardar figuras
path_fig = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 3/2/'                          

#%% Importamos datos

# path = 'C:/Users/felip/Desktop/U/Tesis/Datos/AtChem/Output/output_041022/'
# path = 'C:/Users/felip/Desktop/U/Tesis/Datos/AtChem/Output/output_041022_bad/'
# path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida_1/model/output/'
# path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida_2/model/output_120922/'
# path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida_2/model/output_120922_akima/'
# path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida_2/model/output_041022_akima_2/'
# path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida_2/model/output_270822_akima_5min/'
path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_AtChem/Corrida_3/model/output/'



### Fecha para pasar columna time de segundos a datetime ###
# d0 = '2022-09-11 22:00:00'
d0 = '2022-10-03 22:00:00'
# d0 = '2022-08-27 00:10:00'



### dates para plots ###
# date_1 = '2022-09-11 22:00:00'
# date_2 = '2022-09-12 23:59:00'
date_1 = '2022-10-03 22:00:00'
date_2 = '2022-10-04 23:59:00'
# date_1 = '2022-08-27 00:00:00'
# date_2 = '2022-08-28 23:59:00'

### delta y n_steps para figuras ###
delta = 24
n_steps = 312
# delta = 48
# n_steps = 600

#%% CCS

# Concentrations of the chemical species:
file = 'speciesConcentrations.output'
with open(path+file) as x:
    ncols=len(x.readline().split(','))
CCS = pd.read_table(path+file,sep=',',
                    usecols=range(1,ncols))
CCS['t'] = pd.to_datetime(d0) + \
                pd.to_timedelta(CCS['t']-CCS['t'][0],unit='s')
CCS = CCS.set_index('t')
# pasamos a ppb
CCS_ppb = CCS/(2.46*10**10)

#%% Loss and Poduction rates

file = 'productionRates.output'
with open(path+file) as x:
    ncols=len(x.readline().split(','))
PrR = pd.read_table(path+file,sep=',',usecols=range(1,ncols))    
PrR['time'] = pd.to_datetime(d0) + \
                pd.to_timedelta(PrR['time']-PrR['time'][0],unit='s')            
file = 'lossRates.output'
with open(path+file) as x:
    ncols=len(x.readline().split(','))
LoR = pd.read_table(path+file,sep=',',usecols=range(1,ncols))
LoR['time'] = pd.to_datetime(d0) + \
                pd.to_timedelta(LoR['time']-LoR['time'][0],unit='s')
                
#%% Environment variables and RO2 sum:

file = 'environmentVariables.output'
with open(path+file) as x:
    ncols=len(x.readline().split(','))
EV = pd.read_table(path+file,sep=',',usecols=range(1,ncols))
EV['t'] = pd.to_datetime(d0) + \
                pd.to_timedelta(EV['t']-EV['t'][0],unit='s')
EV = EV.set_index('t')

################################################################
################################################################
#%% Seguimos produccion y destruccion de Aldehydos y Cetonas ###
################################################################

# Periodo de estudio
d1 = '2022-10-04 05:00:00'
d2 = '2022-10-04 11:00:00'

############
#%% HCHO ###

################
## Producción ##
Plot_Prod(PrR, 'Formaldehyde', 'HCHO',(15,8),10,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'Formaldehyde', 'HCHO',(15,8),10,0,delta,d1,d2,d0,n_steps)
PRs = Calc_Loss(PrR,'HCHO',d0,d1,d2,n_steps)
PRs = Calc_Loss(PrR,'CH3CO3',d0,d1,d2,n_steps)

PRs = Calc_Prod(PrR,'PAN',d0,d1,d2,n_steps)
LRs = Calc_Loss(LoR,'PAN',d0,d1,d2,n_steps)


## Hay harto HCHO que se produce por CH3O, siguamos las reacciones:
# CH3O
Plot_Prod(PrR, 'CH3O', 'CH3O',(15,8),10,0,delta,d1,d2,d0,n_steps)
PRs = Calc_Prod(PrR,'CH3O',d0,d1,d2,n_steps)
# CH3O2
Plot_Prod(PrR, 'CH3O2', 'CH3O2',(15,8),10,0,delta,d1,d2,d0,n_steps)
PRs = Calc_Prod(PrR,'CH3O2',d0,d1,d2,n_steps)
LRs = Calc_Loss(LoR,'CH3O2',d0,d1,d2,n_steps)



PRs = Calc_Prod(PrR,'CH3O2',d0,d1,d2,n_steps)




# Su principal producción viene de la mano de la mano de la producción de 
# acetone (CH3COcH3) y radical peroxido (HO2) y la descomposición de
# IBUTOLBO, que viene de IBUTOLBO2, que viene de MEPROPENE (Isobuteno):
#               MEPROPENE + OH -> IBUTOlBO2
#             IBUTOLBO2 + NO -> IBUTOLBO + NO2
#              IBUTOLBO -> CH3COCH3 + HCHO + HO2
# ** Esto mismo ocurre pero en menor orden oxidando MEPROPENE a TBUTOLO2,
#             luego a TBUTOLO y luego a CH3COCH3 + HCHO + HO2 **
Plot_Loss(LoR, 'Isobutene', 'MEPROPENE',(15,5),5,0,delta,date_1,date_2,d0,n_steps)


# Su segunda gran producción viene de la mano de la producción de propanal 
# (C2H5CHO) y HO2, y de la descomposición de NBUTOLAO, que viene de NBUTOLAO2,
# que viene de BUT1ENE (1-buteno):
#                BUT1ENE + OH -> NBUTOLAO2
#             NBUTOLAO2 + NO -> NBUTOLAO + NO2
#             NBUTOLAO -> C2H5CHO + HCHO + HO2
# ** Esto mismo ocurre pero en menor orden oxidando BUT1ENE a HO3C4O2,
#             luegoa HO3C4O y luego a C2H5CHO + HCHO + HO2 **
Plot_Loss(LoR, '1-butene', 'BUT1ENE',(15,5),5,0,delta,date_1,date_2,d0,n_steps)

# Su tercera viene de la mano de la producción de acetaldehido (CH3CHO) y HO2,
# y la destrucción de de HYPROPO, que viene de HYPROPO2, que viene de C3H6 (propene):
#                   C3H6 + OH -> HYPROPO2
#             HYPROPO2 + NO -> HYPROPO + NO2
#             HYPROPO -> CH3CHO + HCHO + HO2
Plot_Loss(LoR, 'Propene', 'C3H6',(15,5),5,0,delta,date_1,date_2,d0,n_steps)

# Por úlitmo, hay un aporte leve pero prolongado a lo largo del día acompañado
# de la producción de HO2 y de la destrucción de CH3O (radical methoxy), el 
# cual viene de CH3O2 (radical methyl peroxy), el cual viene del CH4:
#                  CH4 + OH -> CH3O2 + H2O
#                 CH3O2 + NO -> CH3O + NO2
#                  CH3O + O2 -> HCHO + HO2
# ** Aquí cabe mencionar que existe un gran aporte a CH3O2 por parte de 
#   de la oxidación de CH3CHO + OH -> CH3CO3, y CH3CO3 + NO -> NO2 + CH3O2 **
Plot_Loss(LoR, 'Methano', 'CH4',(15,5),5,0,delta,date_1,date_2,d0,n_steps)

# Luego, vienen algunos aportes menores de oxidación por O3 de alquenos, los
# mismos de arriba, creando abductos de Criegee y aldehidos, HCHO y CH3CHO
Plot_Prod_find(PrR, 'Formaldehyde', 'HCHO','O3',(15,8),5,0,delta,date_1,date_2,d0,n_steps)

# Y otro pequeño por oxidación de STYRENE como los 3 alquenos del comienzo, 
# por OH, por NO y luego descomposición de BENZALdehido + HCHO y HO2
Plot_Loss(LoR, 'Styreno', 'STYRENE',(15,5),5,0,delta,date_1,date_2,d0,n_steps)



#############
## Perdida ##
Plot_Loss(LoR, 'Formaldehyde', 'HCHO',(15,8),20,0,delta,date_1,date_2,d0,n_steps)
LRs = Calc_Loss(LoR,'HCHO',d0,d1,d2,n_steps)

# Todo el formaldeido se descompone en CO y HOx, principalmente en CO y H2
# De día se descompone por OH y fotolisis
# De noche se descompone por NO3


##############
#%% CH3CHO ###

################
## Producción ##
Plot_Prod(PrR, 'Acetaldehyde', 'CH3CHO',(15,8),10,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'Acetaldehyde', 'CH3CHO',(15,8),6,0,delta,d1,d2,d0,n_steps)


PRs = Calc_Loss(PrR,'CH3CHO',d0,d1,d2,n_steps)


# El principal aporte a la producción viene de la oxidación por OH de C3H6:
#                   C3H6 + OH -> HYPROPO2
#             HYPROPO2 + NO -> HYPROPO + NO2
#             HYPROPO -> CH3CHO + HCHO + HO2
Plot_Loss(LoR, 'Propene', 'C3H6',(15,5),5,0,delta,date_1,date_2,d0,n_steps)


# El 2do es el aporte por propanal, el cual produce C2H5O2 (radical ethyl peroxy)
# por 2 mecánismos, el mayor es la oxidación por OH de C2H5CHO (propanal):
#               C2H5CHO + OH -> C2H5CO3
#            C2H5CO3 + NO -> NO2 + C2H5O2
# , y el menor es la fotolisis de C2H5CHO (propanal):
#          C2H5CHO + hv -> C2H5O2 + CO + HO2
# , finalmente, C2H5O2 sigue los sgtes mecanismos:
#           C2H5O2 + NO -> C2H5O + NO2
#           C2H5O + O2 -> CH3CHO + HO2
Plot_Loss(LoR, 'Propanal', 'C2H5CHO',(15,8),10,0,delta,date_1,date_2,d0,n_steps)

# En 3er lugar viene el aporte de oxidación por OH de C3H6 (propene):
#             C3H6 + OH -> IPROPOLO2
#        IPROPOLO2 + NO -> IPROPOLO + NO2
#         IPROPOLO -> CH3CHO + HCHO + HO2
Plot_Loss(LoR, 'Propene', 'C3H6',(15,5),5,0,delta,date_1,date_2,d0,n_steps)

# En 4to lugar se encuentra la occidación por O3 de C3H6, la cual lleva
# directamente a un abducto de Criegee y a Acetaldehido:
#          OH + C3H6 ->  + CH2OOB + CH3CHO

# En 5to lugar se aprecia un aporte en la tarde debido a un peak de etanol:
#             C2H5OH + OH -> CH3CHO + HO2
Plot_Loss(LoR, 'Ethanol', 'C2H5OH',(15,5),5,0,delta,date_1,date_2,d0,n_steps)

# Por último, se observa un leve aporte de C3H7CHO (Butanal):
#            C3H7CHO -> C2H4 + CH3CHO
Plot_Loss(LoR, 'Butanal', 'C3H7CHO',(15,5),5,0,delta,date_1,date_2,d0,n_steps)
# ** Aquí también es relevante el aporte de BUTANAL a PROPANAL por OH y NO (2do) **


#############
## Perdida ##
Plot_Loss(LoR, 'Acetaldehyde', 'CH3CHO',(15,8),20,0,delta,date_1,date_2,d0,n_steps)

# Principal perdida es por OH a CH3CO3:
#          CH3CHO + OH -> CH3CO3
# , la cual es relevante para la producción de HCHO por
#   CH3CHO + OH -> CH3CO3, y CH3CO3 + NO -> NO2 + CH3O2

# Luego sigue la fotolisis a CH3O2 (relevante para HCHO):
#          CH3CHO + hv -> CH3O2 + CO + HO2

# Y por ultimo la oxidación por OH a HCOCH2O2 (también produce HCHO):
#          CH3CHO + OH -> HCOCH2O2
#       HCOCH2O2 + NO -> HCOCH2O + NO2
#         HCOCH2O -> HCHO + CO + HO2


###############
#%% C2H5CHO ### Propanal

################
## Producción ##
Plot_Prod(PrR, 'Propanal', 'C2H5CHO',(15,8),5,0,delta,date_1,date_2,d0,n_steps)
PRs = Calc_Loss(PrR,'C2H5CHO',d0,d1,d2,n_steps)


# El principal aporte viene de la mano de la producción de formaldehido
# (HCHO) y HO2, y de la descomposición de NBUTOLAO, que viene de NBUTOLAO2,
# que viene de BUT1ENE (1-buteno):
#                BUT1ENE + OH -> NBUTOLAO2
#             NBUTOLAO2 + NO -> NBUTOLAO + NO2
#             NBUTOLAO -> C2H5CHO + HCHO + HO2

# El 2do mayor aporte va de la mano con el anterior, pues también es
# oxidación por OH de 1-buteno, pero por un mecanismo de menor orden 
# (0.13, el anterior es 0.87). Así, OH oxida BUT1ENE a HO3C4O2, luego 
# a HO3C4O y luego a C2H5CHO + HCHO + HO2:
#                BUT1ENE + OH -> HO3C4O2
#             HO3C4O2 + NO -> HO3C4O + NO2
#             HO3C4O -> C2H5CHO + HCHO + HO2

# El 3ro mayor corresponde a también a occidación de 1-buteno pero por O3,
# produciendo así propanal y un absucto de Criegee, CH2OOB:
#             BUT1ENE + O3 -> C2H5CHO + CH2OOB
Plot_Loss(LoR, '1-butene', 'BUT1ENE',(15,5),5,0,delta,date_1,date_2,d0,n_steps)

# El último aporte aporte, pese a ser leve por venir solo de butanal (C3H7CHO),
# existe una ruta directa para su producción de la oxidación por OH de Propane:
#                   OH + C3H8 -> NC3H7O2
# , lo que indica que las mediciones de propanal podrían estarse atribuyendo
# a otros mecanismos por falta de el input Propane. Pese a esto, la ruta sugerida
# por Atchem es la producción de NC3H7O2 por oxidación OH de butanal:
#               C3H7CHO + OH -> C3H7CO3
#             C3H7CO3 + NO -> NC3H7O2 + NO2
# , o la descomposición por fotolisis de butanal
#            C3H7CHO + hv -> NC3H7O2 + CO + HO2
# , luego NC3H7O2 sigue la sgte ruta:
#              NC3H7O2 + NO -> NC3H7O + NO2
#                NC3H7O -> C2H5CHO + HO2





LRs = Calc_Loss(LoR,'C2H5CHO',d0,d1,d2,n_steps)
LRs = Calc_Loss(LoR,'C2H5O2',d0,d1,d2,n_steps)
LRs = Calc_Loss(LoR,'C2H5O',d0,d1,d2,n_steps)

PRs = Calc_Prod(PrR,'C2H5CO3',d0,d1,d2,n_steps)
PRs = Calc_Prod(PrR,'C2H5O2',d0,d1,d2,n_steps)
PRs = Calc_Prod(PrR,'C2H5O',d0,d1,d2,n_steps)




#############
## Perdida ##
Plot_Loss(LoR, 'Propanal', 'C2H5CHO',(15,8),5,0,delta,date_1,date_2,d0,n_steps)

# Como se vio en la sección de CH3CHO, aquí hay 2 rutas que terminan por 
# producir CH3CHO vía la producción de C2H5O2. La ruta más relevante es 
# la oxidación por OH:
#              C2H5CHO + OH -> C2H5CO3
#            C2H5CO3 + NO -> NO2 + C2H5O2
# , y luego viene la menos relevante, por fotolisis:
#          C2H5CHO + hv -> C2H5O2 + CO + HO2
# , ambas 2 siguen la ruta:
#             C2H5O2 + NO -> C2H5O + NO2
#             C2H5O + O2 -> CH3CHO + HO2


###############
#%% C3H7CHO ### Butanal

################
## Producción ##
Plot_Prod(PrR, 'Butanal', 'C3H7CHO',(15,8),5,0,delta,date_1,date_2,d0,n_steps)
PRs = Calc_Loss(PrR,'C3H7CHO',d0,d1,d2,n_steps)

 
# Las 3 producciones relvantes vienen de 1-Penteno, 2 de oxidación por OH 
# y la última de oxidación por O3.

#############
## Perdida ##
Plot_Loss(LoR, 'Butanal', 'C3H7CHO',(15,8),10,0,delta,date_1,date_2,d0,n_steps)

# Las 2 perdidas más relevantes de Butanal son las mencionadas en producción 
# de propanal, que corresponden a la oxidación por OH y fotolisis de butanal.

LRs = Calc_Loss(LoR,'C3H7CHO',d0,d1,d2,n_steps)
LRs = Calc_Loss(LoR,'NC3H7O',d0,d1,d2,n_steps)



PRs = Calc_Prod(PrR,'NC3H7O',d0,d1,d2,n_steps)
PRs = Calc_Prod(PrR,'NC3H7O2',d0,d1,d2,n_steps)

################
#%% CH3COCH3 ### Acetone


################
## Producción ##
Plot_Prod(PrR, 'Acetona', 'CH3COCH3',(15,8),5,0,delta,date_1,date_2,d0,n_steps)
PRs = Calc_Prod(PrR,'CH3COCH3',d0,d1,d2,n_steps)
PRs = Calc_Prod(PrR,'CH3CO3',d0,d1,d2,n_steps)


# La Acetone se forma principalmente por oxidación OH de isobutene/MEPROPENE
#              MEPROPENE + OH -> IBUTOLBO2 
#             IBUTOLBO2 + NO -> IBUTOLBO + NO2
#               IBUTOLBO -> CH3COCH3 + HCHO + HO2

# Las siguientes 2 son por occidación OH a otro isomero y por occidación por O3
# pero son mucho menos relevantes.


#############
## Perdida ##
Plot_Loss(LoR, 'Acetona', 'CH3COCH3',(15,8),5,0,delta,date_1,date_2,d0,n_steps)
LRs = Calc_Loss(LoR,'CH3COCH3',d0,d1,d2,n_steps)


# Las unicas 2 perdidas, ambas poco relevantes (~5*10^5) son por OH:
#              CH3COCH3 + OH -> CH3COCH2O2
# , y por fotolisis:
#              CH3COCH3 + hv -> CH3CO3 + CH3O2 
# , siendo ambas rutas para la producción de HCHO.

###################
#%% Formic Acid ###

################
## Producción ##
Plot_Prod(PrR, 'Formic Acid', 'HCOOH',(15,8),5,0,delta,date_1,date_2,d0,n_steps)
PRs = Calc_Loss(PrR,'HCOOH',d0,d1,d2,n_steps)
PRs = Calc_Loss(PrR,'CH2OO',d0,d1,d2,n_steps)

LRs = Calc_Loss(LoR,'C3H6',d0,d1,d2,n_steps)
LRs = Calc_Loss(LoR,'BUT1ENE',d0,d1,d2,n_steps)




#############
## Perdida ##
Plot_Loss(LoR, 'Formic Acid', 'HCOOH',(15,8),5,0,delta,date_1,date_2,d0,n_steps)



###################
#%% Acetic Acid ###

################
## Producción ##
Plot_Prod(PrR, 'Acetic Acid', 'CH3CO2H',(15,8),5,0,delta,date_1,date_2,d0,n_steps)
PRs = Calc_Prod(PrR,'CH3CO2H',d0,d1,d2,n_steps)
PRs = Calc_Prod(PrR,'CH3CHOO',d0,d1,d2,n_steps)



# El mecanismo principal de producción es la oxidación por O3 de propeno,
# produciendo CH3CHOO (abducto de Criegee A):
#             C3H6 + O3 -> CH3CHOOA + CH3CHO
#                 CH3CHOOA -> CH3CHOO
#              CH3CHOO + H2O -> CH3CO2H

Plot_Loss_find(LoR, 'Ozone', 'O3','CH3CHOOA',(15,8),5,0,delta,date_1,date_2,d0,n_steps)


#############
## Perdida ##
Plot_Loss(LoR, 'Acetic Acid', 'CH3CO2H',(15,8),5,0,delta,date_1,date_2,d0,n_steps)

# La unica perdida, aunque leve (1.2*10^5), es por oxidación por OH:
#              CH3CO2H + OH -> CH3O2
# , CH3O2 relevante para HCHO.

###########################################
###########################################
#%% Seguimos el Ciclo NOx-HOx-O3-CO-CH4 ###
###########################################

##########
#%% NO ###

################
## Producción ##
Plot_Prod(PrR, 'NO', 'NO',(15,8),5,2,delta,date_1,date_2,d0,n_steps)
PRs = Calc_Prod(PrR,'NO',d0,d1,d2,n_steps)


# Cómo sabemos, la principal producción de NO es por emisiones antropogénicas
# , ya sean de tráfico o industriales. Fuera de esto, se quiere ver cuanto NO
# el modelo atribuye a mecanismos de producción atmosférica. Así, el principal
# mécanismo de producción atmosférica de NO es la fotolisis de NO2:
#               NO2 + hv -> NO + O        (~1.6*10^9)

# El segundo mécanismo es la fotolisis de HONO:
#              HONO + hv -> OH + NO    (~2.5*10^6)

# Todo el resto de producciones son de ordenes ~10^5 o menores, quizá la más 
# relevante a mencionar sea la oxidación de CH3S por NO2:
#          CH3S + NO2 -> CH3SO + NO   (~10^5)
# , relevante en la producción de SO3 por DMS.



#############
## Perdida ##
Plot_Loss(LoR, 'NO', 'NO',(15,8),10,2,delta,date_1,date_2,d0,n_steps)
LRs = Calc_Loss(LoR,'NO',d0,d1,d2,n_steps)

LRs = Calc_find(LoR,'NO','\.NO\+|\+NO\=','NO\+O3\=|HO2\+NO\=','R',d0,d1,d2,n_steps)


# todos los aportes de radicales
LRs, nm = Calc_find(LoR,'NO2','\.NO\+|\+NO\=','NO\+O3\=|HO2\+NO\=|NO\+NO3\=|NO\+NO\=|NO\+O\=',
                    'R',d0,d1,d2,n_steps)


# solo aportes de alquenos
inc = '\=HYPROPO\+|\+HYPROPO\.|\=IPROPOLO\+|\+IPROPOLO\.|'+\
    '\=NBUTOLAO\+|\+NBUTOLAO\.|\=HO3C4O\+|\+HO3C4O\.|'+\
    '\=IBUTOLBO\+|\+IBUTOLBO\.|\=TBUTOLO\+|\+TBUTOLO\.|'+\
    '\=PE1ENEAO\+|\+PE1ENEAO\.|\=PE1ENEBO\+|\+PE1ENEBO\.'
exc = 'NO\+O3\=|HO2\+NO\=|NO\+NO3\=|NO\+NO\=|NO\+O\=|NO3'
LRs, nm = Calc_find(LoR,'NO',inc,exc,'P',d0,d1,d2,n_steps)

# solo aportes de alquenos y carbonilos
inc = '\.HYPROPO2\+|\+HYPROPO2\=|\.IPROPOLO2\+|\+IPROPOLO2\=|'+\
    '\.NBUTOLAO2\+|\+NBUTOLAO2\=|\.HO3C4O2\+|\+HO3C4O2\=|'+\
    '\.IBUTOLBO2\+|\+IBUTOLBO2\=|\.TBUTOLO2\+|\+TBUTOLO2\=|'+\
    '\.PE1ENEAO2\+|\+PE1ENEAO2\=|\.PE1ENEBO2\+|\+PE1ENEBO2\='+\
    '\.HCOCH2O2\+|\+HCOCH2O2\=|\.CH3CO3\+|\+CH3CO3\='+\
    '\.C2H5CO3\+|\+C2H5CO3\=|\.C2H5O2\+|\+C2H5O2\='+\
    '\.C3H7CO3\+|\+C3H7CO3\=|\.NC3H7O2\+|\+NC3H7O2\='+\
    '\.CH3O2\+|\+CH3O2\=|\.CH3COCH2O2\+|\+CH3COCH2O2\='
exc = 'NO\+O3\=|HO2\+NO\=|NO\+NO3\=|NO\+NO\=|NO\+O\=|NO3'
LRs, nm = Calc_find(LoR,'NO',inc,exc,'R',d0,d1,d2,n_steps)



# La perdida más relevante, y esperada, es la oxidación por O3, o también 
# llamada regeneración de NO2:
#                NO + O3 -> NO2 + O2      (~2.5*10^9)

# Luego le sigue la extracción NO por HO2 del ciclo de NOx, responsable 
# del "estado-estable de O3". Así, al extraer NO de este ciclo, se produce
# NO2 sin gastar O3, convirtiendo la zona en una fuente de O3. Esta es:
#               HO2 + NO -> NO2 + OH       (~1.7*10^8)
# , este mecánismo toma real importancia cuando la regeneración de NO2 por O3
# ha comenzado a disminuir.

# El mismo rol que cumple HO2 en la extracción de NO del ciclo de NOx lo
# lo pueden cumplir también los radicales alkyl-peroxy producido por alcanos
# (solo incluido como CH4) y alquenos (propeno, 1-buteno, isobuteno y 1-penteno)
# , los que se caracterizan por la falta de un atomo H y tener 2 atomos O.
# Estos tienen ordenes de 1-5*10^7, en particular los más relevantes son 
# IBUTOLBO2, NBUTOLAO2, HYPROPO2 y CH3O2, producidos por MEPROPENE, BUT1ENE,
# C3H6 y CH4 respetivamente, de la siguiente manera:
#                RH + OH -> R. + H2O
#             R. + O2 + M -> RO2. + M
#             RO2. + NO -> RO. + NO2

##########
#%% NO2 ##

################
## Producción ##
Plot_Prod(PrR, 'NO2', 'NO2',(15,8),10,2,delta,date_1,date_2,d0,n_steps)
PRs = Calc_Prod(PrR,'NO2',d0,d1,d2,n_steps)


# todos los aportes de radicales
PRs, nm = Calc_find(PrR,'NO2','\.NO\+|\+NO\=','NO\+O3\=|HO2\+NO\=|NO\+NO3\=|NO\+NO\=|NO\+O\=',
                    'R',d0,d1,d2,n_steps)


# solo aportes de alquenos
inc = '\.HYPROPO2\+|\+HYPROPO2\=|\.IPROPOLO2\+|\+IPROPOLO2\=|'+\
    '\.NBUTOLAO2\+|\+NBUTOLAO2\=|\.HO3C4O2\+|\+HO3C4O2\=|'+\
    '\.IBUTOLBO2\+|\+IBUTOLBO2\=|\.TBUTOLO2\+|\+TBUTOLO2\=|'+\
    '\.PE1ENEAO2\+|\+PE1ENEAO2\=|\.PE1ENEBO2\+|\+PE1ENEBO2\='
exc = 'NO\+O3\=|HO2\+NO\=|NO\+NO3\=|NO\+NO\=|NO\+O\=|NO3'
PRs, nm = Calc_find(PrR,'NO2',inc,exc,'R',d0,d1,d2,n_steps)

# solo aportes de alquenos y carbonilos
inc = '\.HYPROPO2\+|\+HYPROPO2\=|\.IPROPOLO2\+|\+IPROPOLO2\=|'+\
    '\.NBUTOLAO2\+|\+NBUTOLAO2\=|\.HO3C4O2\+|\+HO3C4O2\=|'+\
    '\.IBUTOLBO2\+|\+IBUTOLBO2\=|\.TBUTOLO2\+|\+TBUTOLO2\=|'+\
    '\.PE1ENEAO2\+|\+PE1ENEAO2\=|\.PE1ENEBO2\+|\+PE1ENEBO2\='+\
    '\.HCOCH2O2\+|\+HCOCH2O2\=|\.CH3CO3\+|\+CH3CO3\='+\
    '\.C2H5CO3\+|\+C2H5CO3\=|\.C2H5O2\+|\+C2H5O2\='+\
    '\.C3H7CO3\+|\+C3H7CO3\=|\.NC3H7O2\+|\+NC3H7O2\='+\
    '\.CH3O2\+|\+CH3O2\=|\.CH3COCH2O2\+|\+CH3COCH2O2\='
exc = 'NO\+O3\=|HO2\+NO\=|NO\+NO3\=|NO\+NO\=|NO\+O\=|NO3'
PRs, nm = Calc_find(PrR,'NO2',inc,exc,'R',d0,d1,d2,n_steps)



# La principal producción de NO2 es la esperada oxidación por O3:
#                 NO + O3 -> NO2 + O2      (~2.5*10^9)

# A esta le sigue la anteriormente mencionada extracción NO por HO2 del
# ciclo NOx, generando NO2 sin gastar O3:
#                NO + HO2 -> NO2 + OH      (~1.7*10^8)

# Luego vienen las ya mencionadas extracciones de NO por radicales
# alkyl-peroxy del ciclo NOx, radicales producidos por los alquenos y alcano
# ya mencionados, en ese orden.

# Cabe mencionar que entre las magnitudes de oxidación por radicales 
# alkyl-peroxy, en particular justo despues de el primero, se observa 
# el aporte por disolución de Acido Peroxinítrico (HO2NO2):
#              HO2NO2 -> HO2 + NO2        (~3*10^7)



#############
## Perdida ##
Plot_Loss(LoR, 'NO2', 'NO2',(15,8),10,5,delta,date_1,date_2,d0,n_steps)
LRs = Calc_Loss(LoR,'NO2',d0,d1,d2,n_steps)

 
# La principal perdida es la esperada Fotolisis de NO2:
#               NO2 + hv -> NO + O           (~1.6*10^9)

# A esta le sigue la formación de Acido Peroxinítrico:
#              HO2 + NO2 -> HO2NO2           (~3*10^7)

# Luego viene la formación de nitroperoxy metano (CH3O2NO2), algo similar a 
# lo ocurrido en la reacción anterior, un tipo de reservorio para CH3O2 y NO2,
# mismo CH3O2 que actua de radical alkyl-peroxy del metano para sacar NO del 
# ciclo NOx(compiten?). Dicho esto, la reacción atingente es:
#             CH3O2 + NO2 -> CH3O2NO2       (~2*10^7)

# Las últimas 3, poco relevantes en terminos aporte relativo, pero relevantes
# en terminos de caracterización de mecanismos son, en su orden de aporte:

# 1. Producción de PAN:  Peroxy Acetyl Nitrato proviene de la oxidación por OH 
# de CH3CHO y actúa como un breve reservorio de CH3CO3 (radical acetyl-perory) 
# y NO2 en superficie, ya que es descompuesto térmicamente en 3H (depende de T).
#              CH3CO3 + NO2 -> PAN         (~8*10^6)

# 2. Producción de NO3: 
#               NO2 + O3 -> NO3            (~5*10^6)

# 3. Producción de HNO3: Ácido nítrico es la forma de extracción de NO2 del
# ciclo NOx que mantiene el "estado estable de O3". El mecanismo responsable
# de su producción es la oxidación por OH de NO2:
#              NO2 + OH -> HNO3             (~3.5*10^6)

# Cabe mencionar que también se observa producción de PPN y PBN (variaciones
# de PAN) mediante la reacción de C2H5CO3 y C3H7CO3, respectivamente, con NO2,
# con ordenes de (2 y 3)*10^6.


##########
#%% O3 ### 

################
## Producción ##
Plot_Prod(PrR, 'Ozono', 'O3',(15,8),10,0,delta,date_1,date_2,d0,n_steps)

## Para esto miramos a O (O3P) y O1D:
# O3P
Plot_Prod(PrR, 'O3P', 'O',(15,8),2,2,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'O3P', 'O',(15,8),10,0,delta,date_1,date_2,d0,n_steps)

# O1D
Plot_Prod(PrR, 'O1D', 'O1D',(15,8),10,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'O1D', 'O1D',(15,8),10,0,delta,date_1,date_2,d0,n_steps)



PR, nm = Return_Prod(PrR,'O3',d0,n_steps)

LRs = Calc_Loss(LoR,'O3',d0,d1,d2,n_steps)
PRs= Calc_Prod(PrR,'O3',d0,d1,d2,n_steps)
PRs= Calc_Prod(PrR,'O1D',d0,d1,d2,n_steps)
PRs= Calc_Prod(PrR,'O',d0,d1,d2,n_steps)

# prod de OH por O1D
LRs= Calc_Loss(LoR,'O1D',d0,d1,d2,n_steps)
PRs= Calc_Prod(PrR,'OH',d0,d1,d2,n_steps)
LRs= Calc_Loss(LoR,'OH',d0,d1,d2,n_steps)

PRs= Calc_Prod(PrR,'HONO',d0,d1,d2,n_steps)
LRs= Calc_Loss(LoR,'HONO',d0,d1,d2,n_steps)




# Primero que todo, es necesario explicar que para Atchem:
# 1. O1D solo se produce por fotolisis de O3.
# 2. O3 puede producir O1D y O (O3P).
# 2. El paso de O1D a O (O3P) puede hacerse mediante O2 o N2.
# 3. El paso de O (O3P) a O3 trae también diferentes rates 
#    para los O producidos por O1D con N2 y con O2, asumo
#    que para poder diferencias el M que cambio el estado
#    de el O1D producido por el O3. 
# 3. La producción de la fotolisis de NO2 es NO + O (O3P).

# , dicho esto:

# La primera fuente mencionada es:
#         O  -K{N2*O2}->  O3     (~1.3*10^9)
# , o sea, el O3P producido por colisión de O1D contra N2, que luego 
# reaccionó con O2.

# La segunda mayor fuente mencionada es:
#         O  -K{O2*O2}->  O3     (~3.7*10^8)
# , o sea, el O3P producido por colisión de O1D contra O2, que luego
# reaccionó con O2.

# Luego de estas 2, todo el resto se asume como despreciable (la sgte
# tiene un order de 10^3). Se cree que esto puede ser por estar mirando
# a la producción de O3 como tal, cuando debería mirarse a la producción
# de O3P. ??



#############
## Perdida ##
Plot_Loss(LoR, 'Ozono', 'O3',(15,8),10,2,delta,date_1,date_2,d0,n_steps)
LR, nm = Return_Loss(LoR,'O3',d0,n_steps)
LRs = Calc_Loss(LoR,'O3',d0,d1,d2,n_steps)


# La principal perdida de O3 es por oxidación de NO a NO2:
#               NO + O3 -> NO2 + O2     (~2.5*10^9)

# A esta le sigue la fotolisis de O3 a O3P:
#           O3 -> O + O2          (~3*10^8)

# Por último, la fotolisis de O3 a O1D:
#          O3 -> O1D + O2         (1.8*10^7)



###########
#%% CH4 ### 

################
## Producción ##
Plot_Prod(PrR, 'CH4', 'CH4',(15,8),10,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'CH4', 'CH4',(15,8),10,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'CH4',d0,d1,d2,n_steps)


# No hay fuente relevante


#############
## Perdida ##
Plot_Loss(LoR, 'CH4', 'CH4',(15,8),10,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'CH4', 'CH4',(15,8),10,0,delta,d1,d2,d0,n_steps)

# La única perdida, y poco relevante, es la abstracción de H por OH a CH3O2, 
# más es relevante para la producción de HCHO:
#          CH4 + OH + O2 -> CH3O2 + H2O         (~9*10^5)
#            CH3O2 + NO - > CH3O + NO2
#            CH3O + O2 -> HCHO + HO2 

LRs = Calc_Loss(LoR,'NO',d0,d1,d2,n_steps)
LRs = Calc_Loss(LoR,'CH3O2',d0,d1,d2,n_steps)

PRs = Calc_Loss(PrR,'CH3O2',d0,d1,d2,n_steps)
PRs = Calc_Loss(PrR,'CH3CO3',d0,d1,d2,n_steps)
##########
#%% CO ### 

################
## Producción ##
Plot_Prod(PrR, 'CO', 'CO',(15,8),10,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'CO', 'CO',(15,8),10,0,delta,d1,d2,d0,n_steps)
PRs = Calc_Prod(PrR,'CO',d0,d1,d2,n_steps)


# El primer aporte, pese a ser leve (10^6) viene de el abducto de criegee
# producido por la oxidación de Isobuteno por O3:
#            MEPROPENE + O3 -> CH2OOC + CH3COCH3
#                CH2OOC -> CO + HO2 + OH            (~2*10^6)
# ** Solo importante al en la mañana cuando hay latos niveles de O3 y Butenos **

# Le sigue la producción de CO por formaldehido:
#                     HCHO -> CO + H2               (~1.8*10^6)

# Luego vienen más abductos de criegee de isobuteno.


PRs= Calc_Prod(PrR,'CO',d0,d1,d2,n_steps)

#############
## Perdida ##
Plot_Loss(LoR, 'CO', 'CO',(15,8),10,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'CO', 'CO',(15,8),10,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'CO',d0,d1,d2,n_steps)

# La única perdida relevante, que se hace relevante a medida que crece la
# disponibilidad de OH, es la oxidación por OH:
#                      CO + OH -O2-> CO2 + HO2       (~3*10^6)


##########
#%% OH ###    (de aquí para abajo comenze a suar el real max acumuado)

################
## Producción ##
Plot_Prod(PrR, 'OH', 'OH',(15,8),5,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'OH', 'OH',(15,8),5,0,delta,d1,d2,d0,n_steps)
PRs= Calc_Prod(PrR,'OH',d0,d1,d2,n_steps)
PRs= Calc_Prod(PrR,'H2O2',d0,d1,d2,n_steps)


# La mayor producción viene de oxidación por HO2 de NO:
#           HO2 + NO -> NO2 + OH       (~1.7*10^8)

# A esta le sigue la fotolisis de HONO:
#             HONO -> NO + OH          (~2.8*10^6)     


# producción de OH por occidación de MEPROPENE (isobutileno) por O3
Plot_Loss(LoR, 'MEPROPENE', 'MEPROPENE',(15,8),10,0,delta,d1,d2,d0,n_steps)

# este se occida por O3 a CH2OOC y CH3CCH3OOA, Criege intermediates, que
# quienes luego se descomponene a un radical y OH



#############
## Perdida ##
Plot_Loss(LoR, 'OH', 'OH',(15,8),10,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'OH', 'OH',(15,8),10,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'OH',d0,d1,d2,n_steps)
LRs = Calc_Loss(LoR,'H2O2',d0,d1,d2,n_steps)



# La mayor perdida de OH ocurre por oxidación de isobuteno:
#          MEPROPENE + OH -> IBUTOLBO2        (1.24*10^11)

# La siguiente mayor perdida es la oxidación de acetaldehido:
#         CH3CHO + OH -> CH3CO3            (7.3*10^10)

# Luego la oxidación por OH de 1-buteno:
#        BUT1ENE + OH -> NBUTOLAO2          (7.12*10**10)

# Luego la oxidación por OH de propeno:
#       C3H6 + OH -> HYPROPO2             (4.66e10)

# Luego la oxidación por OH de NO2 a HNO3:
#        NO2 + OH -> HNO3                 (4.25e10)

# El resto no es tan relevante, excepto por:
# - CO + OH -> HO2    (2.5e10)
# - NO + OH -> HONO   (2.4e10)

##########
#%% HO2 ### 

################
## Producción ##
Plot_Prod(PrR, 'HO2', 'HO2',(15,8),20,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'HO2', 'HO2',(15,8),20,0,delta,d1,d2,d0,n_steps)
PRs= Calc_Prod(PrR,'HO2',d0,d1,d2,n_steps)




#############
## Perdida ##
Plot_Loss(LoR, 'HO2', 'HO2',(15,8),20,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'HO2', 'HO2',(15,8),20,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'HO2',d0,d1,d2,n_steps)



############
#%% HNO3 ### 

################
## Producción ##
Plot_Prod(PrR, 'HNO3', 'HNO3',(15,8),20,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'HNO3', 'HNO3',(15,8),20,0,delta,d1,d2,d0,n_steps)
PRs= Calc_Prod(PrR,'HNO3',d0,d1,d2,n_steps)




#############
## Perdida ##
Plot_Loss(LoR, 'HNO3', 'HNO3',(15,8),20,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'HNO3', 'HNO3',(15,8),20,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'HNO3',d0,d1,d2,n_steps)



###########
#%% NO3 ### 

################
## Producción ##
Plot_Prod(PrR, 'NO3', 'NO3',(15,8),20,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'NO3', 'NO3',(15,8),20,0,delta,d1,d2,d0,n_steps)
PRs= Calc_Prod(PrR,'NO3',d0,d1,d2,n_steps)



#############
## Perdida ##
Plot_Loss(LoR, 'NO3', 'NO3',(15,8),20,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'NO3', 'NO3',(15,8),20,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'NO3',d0,d1,d2,n_steps)

###########
#%% HONO ### 

################
## Producción ##
Plot_Prod(PrR, 'HONO', 'HONO',(15,8),1,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'HONO', 'HONO',(15,8),1,0,delta,d1,d2,d0,n_steps)
PRs= Calc_Prod(PrR,'HONO',d0,d1,d2,n_steps)



#############
## Perdida ##
Plot_Loss(LoR, 'HONO', 'HONO',(15,8),1,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'HONO', 'HONO',(15,8),1,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'HONO',d0,d1,d2,n_steps)

#%% PAN

################
## Producción ##
Plot_Prod(PrR, 'PAN', 'PAN',(15,8),1,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'PAN', 'PAN',(15,8),1,0,delta,d1,d2,d0,n_steps)
PRs= Calc_Prod(PrR,'PAN',d0,d1,d2,n_steps)



#############
## Perdida ##
Plot_Loss(LoR, 'PAN', 'PAN',(15,8),1,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'PAN', 'PAN',(15,8),1,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'PAN',d0,d1,d2,n_steps)

#%% CH3CO3

################
## Producción ##
Plot_Prod(PrR, 'CH3CO3', 'CH3CO3',(15,8),1,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'CH3CO3', 'CH3CO3',(15,8),1,0,delta,d1,d2,d0,n_steps)
PRs= Calc_Prod(PrR,'CH3CO3',d0,d1,d2,n_steps)




#############
## Perdida ##
Plot_Loss(LoR, 'CH3CO3', 'CH3CO3',(15,8),1,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'CH3CO3', 'CH3CO3',(15,8),1,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'CH3CO3',d0,d1,d2,n_steps)

#%% SO3

################
## Producción ##
Plot_Prod(PrR, 'SO3', 'SO3',(15,8),1,0,delta,date_1,date_2,d0,n_steps)
Plot_Prod(PrR, 'SO3', 'SO3',(15,8),1,0,delta,d1,d2,d0,n_steps)
PRs= Calc_Prod(PrR,'HSO3',d0,d1,d2,n_steps)
PRs= Calc_Prod(PrR,'SO3',d0,d1,d2,n_steps)
PRs= Calc_Prod(PrR,'SA',d0,d1,d2,n_steps)




#############
## Perdida ##
Plot_Loss(LoR, 'SO3', 'SO3',(15,8),1,0,delta,date_1,date_2,d0,n_steps)
Plot_Loss(LoR, 'SO3', 'SO3',(15,8),1,0,delta,d1,d2,d0,n_steps)
LRs = Calc_Loss(LoR,'SO3',d0,d1,d2,n_steps)


#################################################
#%% Series de tiempo de compuestos de interes ###
#################################################

d1 = '2022-10-04 05:00:00'
d2 = '2022-10-04 11:00:00'
# d1 = '2022-10-04 08:30:00'
# d2 = '2022-10-04 10:30:00'

#%% Compuestos oxidación alquenos
comp_oa = [# Oxidación de alquenos por OH
            'C3H6','BUT1ENE','MEPROPENE',
            'CH3CHO','C2H5CHO','CH3COCH3',
            'PENT1ENE','OH','HO2',
            'C3H7CHO','HCHO','NO3',
            # oxidantes relevantes
            'NO','NO2','O3',
            'CO','CH4','HNO3',
            'CH3CO2H','HCOOH','CH3CO3'
            # 'HCOOH','CH3CO2H','O'
            # SA
            # 'CH3SO3','SO2','HSO3','SO3','SA'
            ]

CCS_ppb.loc[d1:d2,comp_oa].plot(subplots=True,grid=True, 
                                        figsize=(20,10.5),ylabel='ppb',
                                        layout=(7,3))
plt.tight_layout()

#%% Compuestos SA
comp_sa = [
            # oxidantes relevantes
            'OH','HO2',
            'NO','NO2','NO3',
            # 'O3',
            'H2O2',
            # DMS
            'DMS',
            'CH3SCH2O2','CH3SCH2O','CH3SO','CH3SO','CH3SO2O2','CH3SO2','CH3SO3',
            'HODMSO2','DMSO','MSIA',
            # producción H2SO4
            'SO2','HSO3','SO3','SA'
            ]

CCS_ppb.loc[date_1:date_2,comp_sa].plot(subplots=True,grid=True, 
                                        figsize=(20,10.5),ylabel='ppb',
                                        layout=(7,3))
plt.tight_layout()

#%% NOx-O3
# CCS_ppb['CH4'] = CCS_ppb['CH4']-1850

ls = ['NO','NO2','O3','C3H6','BUT1ENE','PENT1ENE','CH3CHO']#,'C2H5CHO','C3H7CHO','CH3COCH3','HCHO']
CCS_ppb.loc[d1:d2,ls].plot(figsize=(10,5), grid=True, ylabel='ppb')
plt.tight_layout()

#%% 1 compound

CCS_ppb.loc[date_1:date_2,['OH']].plot(figsize=(10,5), grid=True, ylabel='ppb')
plt.tight_layout()

##############
#%% 1 axis ###

comp = 'O3'
# comp = 'SA'

# comp = ['PAN','CH3CO2H','SA']

#%% Conc

# Definimos unidades a utilizar
unit = 'ppb'

D1 = pd.to_datetime(d1)
D2 = pd.to_datetime(d2)

# Definimos compuestos a plotear
if unit == 'ppb':
    ax = CCS_ppb.loc[date_1:date_2,comp].plot(figsize=(10,4),grid=True
                                     # ,title='Concentración '+comp
                                     )
    label = '[ppb]'
else:
    ax = CCS.loc[date_1:date_2,comp].plot(figsize=(10,4),grid=True
                                     # ,title='Concentración '+comp
                                     )
    label = r'[$moléculas \ s^{-1}$]'
    
ax.legend(fontsize=9,loc='best')
ax.set_ylabel(label)

plt.tight_layout()
# plt.savefig(path_fig+'Prod_'+comp+'_'+D1.strftime('%m-%d-%H%M')+'_a_'+
#             D2.strftime('%m-%d-%H%M')+'.png',dpi=300)


#%% Prod

PR, nm = DF_reacts(PrR,comp,n_steps,d0,d1,d2)
D1 = pd.to_datetime(d1)
D2 = pd.to_datetime(d2)


# entregamos nomnbre a columnas
name_map = nm['name'].to_dict()
PR = PR.rename(columns=name_map)

# Definimos compuestos a plotear y a dejar en el eje derecho
comp_tot = PR.columns[0:6]#.to_list(); del comp_tot[1]
ax = PR.loc[d1:d2,comp_tot].plot(figsize=(11,3.5),grid=True,
                                 # xlabel='[hora]',
                                 ylabel=r'[$moléculas \ s^{-1}$]'
                                 # ,title='Mecanismos de producción '+comp
                                 )
ax.legend(fontsize=9,loc='best')

plt.tight_layout()
# plt.savefig(path_fig+'Prod_'+comp+'_'+D1.strftime('%m-%d-%H%M')+'_a_'+
#             D2.strftime('%m-%d-%H%M')+'.png',dpi=300)

#%% Perd

LR, nm = DF_reacts(LoR,comp,n_steps,d0,d1,d2)
D1 = pd.to_datetime(d1)
D2 = pd.to_datetime(d2)

# entregamos nomnbre a columnas
name_map = nm['name'].to_dict()
LR = LR.rename(columns=name_map)

# Definimos compuestos a plotear y a dejar en el eje derecho
comp_tot = LR.columns[0:5]
ax = LR.loc[d1:d2,comp_tot].plot(figsize=(10,4),grid=True,
                                 title='Mecanismos de perdida '+comp)
ax.legend(fontsize=8,loc='upper left')

label = r'[$moléculas \ s^{-1}$]'
ax.set_ylabel(label)

plt.tight_layout()
# plt.savefig(path_fig+'Perd_'+comp+'_'+D1.strftime('%m-%d-%H%M')+'_a_'+
#             D2.strftime('%m-%d-%H%M')+'.png',dpi=300)

##############
#%% 2 axis ###


comp = 'O3'
# comp = 'CH3CO2H'
# comp = 'SO3'

#%% Conc

# Colormap para los ejes-y
color=0
cmap = plt.get_cmap('tab10')

# Definimos compuestos a plotear y a dejar en el eje derecho
comp_tot = ['PAN','CH3CO2H','SA']
comp_sa = ['SA']

ax = CCS_ppb.loc[date_1:date_2,comp_tot].plot(figsize=(10,5), grid=True, xlabel='[hora]',
                                      secondary_y=comp_sa, mark_right=False)
ax.legend(loc='upper left')
ax.right_ax.legend(loc='upper right')
ax.set_title('Razones de mezcla '+'-'.join(comp_tot))

if color == 0:
    ax.set_ylabel('[ppb]')
    ax.right_ax.set_ylabel('[ppb]')
else:
    ax.set_ylabel('[ppb]',color=cmap(0))
    ax.right_ax.set_ylabel('[ppb]',color=cmap(1))
    ax.tick_params(axis='y',labelcolor=cmap(0))
    ax.right_ax.tick_params(axis='y',labelcolor=cmap(1))


plt.tight_layout()
# plt.savefig(path_fig+'Conc_'+'-'.join(comp_tot)+'_'+D1.strftime('%m-%d-%H%M')+
#             '_a_'+D2.strftime('%m-%d-%H%M')+'.png',dpi=300)


#%% Prod

# comp = 'NO2'
PR, nm = DF_reacts(PrR,comp,n_steps,d0,d1,d2)
D1 = pd.to_datetime(d1)
D2 = pd.to_datetime(d2)

# entregamos nomnbre a columnas
name_map = nm['name'].to_dict()
PR = PR.rename(columns=name_map)

# Colormap para los ejes-y
color=0
cmap = plt.get_cmap('tab10')

# Definimos compuestos a plotear y a dejar en el eje derecho
n=6
comp_left = PR.columns[0:2]
comp_right = PR.columns[2:n]
# ax = PR.loc[d1:d2,comp_tot].plot(figsize=(10,4),grid=True, 
#                                  secondary_y=comp_sa, mark_right=False
#                                  # ,title='Mecanismos de producción '+comp
#                                  )

ax = PR.loc[d1:d2, comp_left].plot(figsize=(10,5), grid=True)
PR.loc[d1:d2, comp_right].plot(ax=ax, secondary_y=True, mark_right=False)


ax.legend(comp_left,fontsize=9,loc='upper left')
ax.right_ax.legend(comp_right,fontsize=9,loc='upper right')

label = r'[$moléculas \ s^{-1}$]'
# los 2 ejes-y en color negro (más de una curva en eje-y izquierdo)
if color == 0:
    ax.set_ylabel(label)
    ax.right_ax.set_ylabel(label)
# el eje-y izquierdo en azul en referencia a la primera curva (1 curva en izquierda)
elif color==1:
    ax.set_ylabel(label,color=cmap(0))
    ax.right_ax.set_ylabel(label)
    ax.tick_params(axis='y',labelcolor=cmap(0))
# eje-y izquierdo azul y derecho en naranjo (solo 2 curvas)
else:
    ax.set_ylabel(label,color=cmap(0))
    ax.right_ax.set_ylabel(label,color=cmap(1))
    ax.tick_params(axis='y',labelcolor=cmap(0))
    ax.right_ax.tick_params(axis='y',labelcolor=cmap(1))


plt.tight_layout()
# plt.savefig(path_fig+'Prod_'+comp+'_'+D1.strftime('%m-%d-%H%M')+'_a_'+
#             D2.strftime('%m-%d-%H%M')+'.png',dpi=300)

#%% Perd
comp = 'O3'
LR, nm = DF_reacts(LoR,comp,n_steps,d0,d1,d2)
D1 = pd.to_datetime(d1)
D2 = pd.to_datetime(d2)

# entregamos nomnbre a columnas
name_map = nm['name'].to_dict()
LR = LR.rename(columns=name_map)

# Colormap para los ejes-y
color=0
cmap = plt.get_cmap('tab10')

# Definimos compuestos a plotear y a dejar en el eje derecho
n = 10
comp_tot = LR.columns[0:n]
comp_sa = LR.columns[2:n]
ax = LR.loc[d1:d2,comp_tot].plot(figsize=(10,4),grid=True, 
                                 secondary_y=comp_sa,mark_right=False,
                                 title='Mecanismos de perdida '+comp)
ax.legend(fontsize=9,loc='upper left')
ax.right_ax.legend(fontsize=9,loc='upper right')

label = r'[$moléculas \ s^{-1}$]'
# los 2 ejes-y en color negro (más de una curva en eje-y izquierdo)
if color == 0:
    ax.set_ylabel(label)
    ax.right_ax.set_ylabel(label)
# el eje-y izquierdo en azul en referencia a la primera curva (1 curva en izquierda)  
elif color==1:
    ax.set_ylabel(label,color=cmap(0))
    ax.right_ax.set_ylabel(label)
    ax.tick_params(axis='y',labelcolor=cmap(0))
# eje-y izquierdo azul y derecho en naranjo (solo 2 curvas)   
else:
    ax.set_ylabel(label,color=cmap(0))
    ax.right_ax.set_ylabel(label,color=cmap(1))
    ax.tick_params(axis='y',labelcolor=cmap(0))
    ax.right_ax.tick_params(axis='y',labelcolor=cmap(1))


plt.tight_layout()
# plt.savefig(path_fig+'Perd_'+comp+'_'+D1.strftime('%m-%d-%H%M')+'_a_'+
#             D2.strftime('%m-%d-%H%M')+'.png',dpi=300)

