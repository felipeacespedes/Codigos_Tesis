# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:19:06 2023

@author: felip

Cóigo para plotear figuras de Rodrigo:

    Plotear HCNM de 9 estaciones de red SINCA entre el 27/09/22-23/11/22
"""

from import_var import import_var
import matplotlib.pyplot as plt
import pandas as pd


#%% Importamos HCNM de 9 estaciones

# Diccionario de estaciones
Dic = {}

Dic['Estaciones'] = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura'\
                     ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo']
    
# Creamos vector de tiempo
Fi = '2022-08-27'
Ff = '2022-11-23'
T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='H')

# importamos HCNM entre 27/09/22 y 23/11/22
HCNM = pd.DataFrame({'T':T})
HCNM = HCNM.set_index('T')
for est in Dic['Estaciones']:
    HCNM[est] = import_var(est,'Cont','HCNM',Fi,Ff)
    
#%% Ploteamos

# creamos figura
fig = plt.figure(figsize=(15,3*9))

# ploteamos subplots
for i in range(9):
    plt.subplot(9,1,i+1)
    plt.plot(T,HCNM[Dic['Estaciones'][i]],zorder=1,label='Value')
    plt.axhline(HCNM[Dic['Estaciones'][i]].median() \
        ,color='r',linestyle='--',linewidth=0.7,zorder=2,label='Median')
    plt.ylabel(Dic['Estaciones'][i].replace('_',' '))
    plt.ylim(0-0.1,2+0.1)
    plt.locator_params(axis='y', nbins=5)
    plt.grid()
    if i+1 == 1: 
        plt.legend(bbox_to_anchor=(0.98, 1.25))
    
    if i+1 < 9:
        plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)
    else:
        plt.xlabel('Time [h]')

# asignamos titulo y guardamos

plt.suptitle('HCNM [ppm], 27/08/22 - 23/11/22')
fig.tight_layout(pad=0.5,rect=[0, 0, 1, 0.99])
plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/HCNM_270822_231122.png'\
            , bbox_inches='tight',dpi=300)
plt.show

#%% Identificamos qué fechas muestran peaks sobre la media

# A partir de la desviación estandar de cada serie, realizamos caracterización
# de los días que sobrepasan 3 std partir de la mediana

peaks = pd.DataFrame({'T':T})
for est in Dic['Estaciones']:
    peaks[est] = HCNM[est] >= (HCNM[est].median()+(3*HCNM[est].std()))
    

#%% Ploteamos

# creamos figura
fig = plt.figure(figsize=(15,3*9))

# ploteamos subplots
for i in range(9):
    plt.subplot(9,1,i+1)
    plt.plot(T,peaks[Dic['Estaciones'][i]],zorder=1,label='Value')
    plt.axhline(HCNM[Dic['Estaciones'][i]].median() \
        ,color='r',linestyle='--',linewidth=0.7,zorder=2,label='Median')
    plt.ylabel(Dic['Estaciones'][i].replace('_',' '))
    plt.ylim(0-0.1,2+0.1)
    plt.locator_params(axis='y', nbins=5)
    plt.grid()
    if i+1 == 1:
        plt.legend(bbox_to_anchor=(0.98, 1.25))
    
    if i+1 < 9:
        plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)
    else:
        plt.xlabel('Time [h]')

# asignamos titulo y guardamos

plt.suptitle('peaks HCNM, 27/08/22 - 23/11/22')
fig.tight_layout(pad=0.5,rect=[0, 0, 1, 0.99])
plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/peaks_HCNM_270822_231122.png'\
            , bbox_inches='tight',dpi=300)
plt.show

#%% Histograma

# 
ax = peaks.resample('D').sum().plot(kind='bar',figsize=(15,5))
# ax.set_xticklabels(peaks.index.strftime('%Y-%m'))

# peaks_sum = peaks.sum(axis=1)

# fig = plt.figure(figsize=(15,3))
# plt.hist(T,peaks_sum)





