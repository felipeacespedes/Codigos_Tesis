# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 18:06:19 2024

@author: felip

Código para plotear eventos de contaminación a alta resolución para 
ver cómo evolucionan los COVs frescos a productos
"""

# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
from Plot_covs_functs import Plot_COV, Plot_MET

#%% Cargamos datos secundarios

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
file = 'datos_inv/inv_data_prelim_1min.csv'
COV_s = pd.read_csv(path+file,delimiter=';')
COV_s['date'] = pd.to_datetime(COV_s['date'],format='%d/%m/%Y %H:%M:%S')
COV_s['date'] = pd.to_datetime(COV_s['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV_s = COV_s.set_index('date')

#%% Ploteamos eventos

# Directorio de guardado
path = 'C:/Users/felip/Desktop/Avances/12/peaks alta resolución/'

## Definimos listas de columnas de interés
# BETX
betx = ['Benzene', 'Toluene', 'Ethyl.benzene_Xylenes']
# COVs de interés
cov_int = ['Butenes','Acetaldehyde','Propene_Cyclopropane','Acetone_propanal']
# COVs de emisión
cov_emi = ['Butenes','Propene_Cyclopropane','Toluene','Methanol','Ethanol']
# COVs productos
cov_prd = ['Acetaldehyde','Acetone_propanal','Butanone_Butanal',
           'Methacrolein_MVK','Formaldehyde','Acetic.acid_Glycolaldehyde']
# Reacción 1
r1 = ['Propene_Cyclopropane','Acetaldehyde']
# Reacción 2
r2 = ['Butenes','Acetone_propanal']

# Definimos un diccionario de colores
colors = {
    'Butenes': 'tab:pink',
    'Propene_Cyclopropane': 'tab:red',
    'Toluene': 'tab:brown',
    'Methanol': 'tab:orange',
    'Ethanol': 'tab:green',
    'Acetaldehyde': 'tab:purple',
    'Acetone_propanal': 'tab:gray',
    'Butanone_Butanal': 'tab:olive',
    'Methacrolein_MVK': 'tab:cyan',
    'Formaldehyde': 'tab:blue',
    'Acetic.acid_Glycolaldehyde': 'tab:brown'
}

#%% 12-09

# Definmos momentos inicial y final

# Peak 1
peak = 1
date_1 = pd.to_datetime('2022-09-12 06:00:00')
date_2 = pd.to_datetime('2022-09-12 10:00:00')
ymin = -2
ymax = 62

# Ploteamos
fig, axs = plt.subplots(2, 2, sharey=True, sharex=True, figsize=(20, 10))

# Frescos
COV_s.loc[date_1:date_2, cov_emi].plot(ax=axs[0, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_emi])
axs[0, 0].grid(visible=True, which='both', axis='both')
axs[0, 0].set_title('Frescos')

# Productos
COV_s.loc[date_1:date_2, cov_prd].plot(ax=axs[1, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_prd])
axs[1, 0].grid(visible=True, which='both', axis='both')
axs[1, 0].set_title('Productos')

# Reacción 1
COV_s.loc[date_1:date_2, r1].plot(ax=axs[0, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r1])
axs[0, 1].grid(visible=True, which='both', axis='both')
axs[0, 1].set_title('Reacción Propene -> Acetaldehyde')

# Reacción 2
COV_s.loc[date_1:date_2, r2].plot(ax=axs[1, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r2])
axs[1, 1].grid(visible=True, which='both', axis='both')
axs[1, 1].set_title('Reacción 1-Butene -> Propanal')

# Set the figure title and layout
fig.suptitle('Peak'+str(peak)+' '+ date_1.strftime('%Y-%m-%d, %H:%M:%S')+
             ' a '+date_2.strftime('%Y-%m-%d, %H:%M:%S.'))
fig.tight_layout(rect=[0, 0, 1, 0.99])
# fig.savefig(path+date_1.strftime('%d%m')+'/Peak'+str(peak)+' '+
#             date_1.strftime('%Y-%m-%d %H%M%S a ')+
#             date_2.strftime('%H%M%S')+'.png', dpi=300)

#%% 

# date_1 = pd.to_datetime('2022-09-12 06:00:00')
# date_2 = pd.to_datetime('2022-09-12 12:00:00')

date_1 = pd.to_datetime('2022-09-11 22:00:00')
date_2 = pd.to_datetime('2022-09-12 23:59:00')

ymin = -2
ymax = 62
COV_s.loc[date_1:date_2, cov_int].plot(figsize=(20,10),ylabel='ppb',
                                       ylim=(ymin, ymax),grid=True)
# Set the figure title and layout
plt.suptitle('Peak '+ date_1.strftime('%Y-%m-%d, %H:%M:%S')+
             ' a '+date_2.strftime('%Y-%m-%d, %H:%M:%S.'))
plt.tight_layout(rect=[0, 0, 1, 0.99])


  #%% 04-10

# Definmos momentos inicial y final

# Peak 1
# peak = 1
# date_1 = pd.to_datetime('2022-10-04 05:25:00')
# date_2 = pd.to_datetime('2022-10-04 05:26:30')
# ymin = -2
# ymax = 77

# Peak 2
# peak = 2
# date_1 = pd.to_datetime('2022-10-04 05:53:00')
# date_2 = pd.to_datetime('2022-10-04 05:54:30')
# ymin = -2
# ymax = 82

# Peak 3
peak = 3
date_1 = pd.to_datetime('2022-10-04 08:47:00')
date_2 = pd.to_datetime('2022-10-04 08:48:30')
ymin = -2
ymax = 60

# Ploteamos
fig, axs = plt.subplots(2, 2, sharey=True, sharex=True, figsize=(10,10))

# Frescos
COV_s.loc[date_1:date_2, cov_emi].plot(ax=axs[0, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_emi])
axs[0, 0].grid(visible=True, which='both', axis='both')
axs[0, 0].set_title('Frescos')

# Productos
COV_s.loc[date_1:date_2, cov_prd].plot(ax=axs[1, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_prd])
axs[1, 0].grid(visible=True, which='both', axis='both')
axs[1, 0].set_title('Productos')

# Reacción 1
COV_s.loc[date_1:date_2, r1].plot(ax=axs[0, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r1])
axs[0, 1].grid(visible=True, which='both', axis='both')
axs[0, 1].set_title('Reacción Propene -> Acetaldehyde')

# Reacción 2
COV_s.loc[date_1:date_2, r2].plot(ax=axs[1, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r2])
axs[1, 1].grid(visible=True, which='both', axis='both')
axs[1, 1].set_title('Reacción 1-Butene -> Propanal')

# Set the figure title and layout
fig.suptitle('Peak'+str(peak)+' '+ date_1.strftime('%Y-%m-%d, %H:%M:%S')+
             ' a '+date_2.strftime('%Y-%m-%d, %H:%M:%S.'))
fig.tight_layout(rect=[0, 0, 1, 0.99])
fig.savefig(path+date_1.strftime('%d%m')+'/Peak'+str(peak)+' '+
            date_1.strftime('%Y-%m-%d %H%M%S a ')+
            date_2.strftime('%H%M%S')+'.png', dpi=300)
#%%
date_1 = pd.to_datetime('2022-10-04 05:00:00')
date_2 = pd.to_datetime('2022-10-04 11:00:00')
ymin = -2
ymax = 180

fig, ax = plt.subplots(figsize=(20,10))

COV_s.loc[date_1:date_2, cov_int].plot(ax = ax, ylabel='ppb',
                                       ylim=(ymin, ymax),grid=True,
                                       color=[colors[compound]\
                                             for compound in cov_int])
# Set the figure title and layout
fig.suptitle('Peak'+str(peak)+' '+ date_1.strftime('%Y-%m-%d, %H:%M:%S')+
             ' a '+date_2.strftime('%Y-%m-%d, %H:%M:%S.'))
fig.tight_layout(rect=[0, 0, 1, 0.99])

#%% 07-10

# Definmos momentos inicial y final

# Peak 1
# peak = 1
# date_1 = pd.to_datetime('2022-10-07 05:17:00')
# date_2 = pd.to_datetime('2022-10-07 05:19:30')
# ymin = -2
# ymax = 85

# Peak 2
# peak = 2
# date_1 = pd.to_datetime('2022-10-07 06:54:00')
# date_2 = pd.to_datetime('2022-10-07 07:00:00')
# ymin = -2
# ymax = 325

# Peak 3
# peak = 3
# date_1 = pd.to_datetime('2022-10-07 08:16:00')
# date_2 = pd.to_datetime('2022-10-07 08:20:30')
# ymin = -2
# ymax = 85

# Peak 4
peak = 4
date_1 = pd.to_datetime('2022-10-07 08:31:00')
date_2 = pd.to_datetime('2022-10-07 08:32:30')
ymin = -2
ymax = 60

# Ploteamos
fig, axs = plt.subplots(2, 2, sharey=True, sharex=True, figsize=(10, 10))

# Frescos
COV_s.loc[date_1:date_2, cov_emi].plot(ax=axs[0, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_emi])
axs[0, 0].grid(visible=True, which='both', axis='both')
axs[0, 0].set_title('Frescos')

# Productos
COV_s.loc[date_1:date_2, cov_prd].plot(ax=axs[1, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_prd])
axs[1, 0].grid(visible=True, which='both', axis='both')
axs[1, 0].set_title('Productos')

# Reacción 1
COV_s.loc[date_1:date_2, r1].plot(ax=axs[0, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r1])
axs[0, 1].grid(visible=True, which='both', axis='both')
axs[0, 1].set_title('Reacción Propene -> Acetaldehyde')

# Reacción 2
COV_s.loc[date_1:date_2, r2].plot(ax=axs[1, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r2])
axs[1, 1].grid(visible=True, which='both', axis='both')
axs[1, 1].set_title('Reacción 1-Butene -> Propanal')

# Set the figure title and layout
fig.suptitle('Peak'+str(peak)+' '+ date_1.strftime('%Y-%m-%d, %H:%M:%S')+
             ' a '+date_2.strftime('%Y-%m-%d, %H:%M:%S.'))
fig.tight_layout(rect=[0, 0, 1, 0.99])
fig.savefig(path+date_1.strftime('%d%m')+'/Peak'+str(peak)+' '+
            date_1.strftime('%Y-%m-%d %H%M%S a ')+
            date_2.strftime('%H%M%S')+'.png', dpi=300)

#%% 19-10

# Definmos momentos inicial y final

# Peak 1
peak = 1
date_1 = pd.to_datetime('2022-10-19 03:54:00')
date_2 = pd.to_datetime('2022-10-19 03:59:00')
ymin = -2
ymax = 22


# Ploteamos
fig, axs = plt.subplots(2, 2, sharey=True, sharex=True, figsize=(10, 10))

# Frescos
COV_s.loc[date_1:date_2, cov_emi].plot(ax=axs[0, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_emi])
axs[0, 0].grid(visible=True, which='both', axis='both')
axs[0, 0].set_title('Frescos')

# Productos
COV_s.loc[date_1:date_2, cov_prd].plot(ax=axs[1, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_prd])
axs[1, 0].grid(visible=True, which='both', axis='both')
axs[1, 0].set_title('Productos')

# Reacción 1
COV_s.loc[date_1:date_2, r1].plot(ax=axs[0, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r1])
axs[0, 1].grid(visible=True, which='both', axis='both')
axs[0, 1].set_title('Reacción Propene -> Acetaldehyde')

# Reacción 2
COV_s.loc[date_1:date_2, r2].plot(ax=axs[1, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r2])
axs[1, 1].grid(visible=True, which='both', axis='both')
axs[1, 1].set_title('Reacción 1-Butene -> Propanal')

# Set the figure title and layout
fig.suptitle('Peak'+str(peak)+' '+ date_1.strftime('%Y-%m-%d, %H:%M:%S')+
             ' a '+date_2.strftime('%Y-%m-%d, %H:%M:%S.'))
fig.tight_layout(rect=[0, 0, 1, 0.99])
# fig.savefig(path+date_1.strftime('%d%m')+'/Peak'+str(peak)+' '+
#             date_1.strftime('%Y-%m-%d %H%M%S a ')+
#             date_2.strftime('%H%M%S')+'.png', dpi=300)

#%% 22-10

# Definmos momentos inicial y final

# Peak 1
# peak = 1
# date_1 = pd.to_datetime('2022-10-22 07:40:00')
# date_2 = pd.to_datetime('2022-10-22 07:59:00')
# ymin = -2
# ymax = 52

date_1 = pd.to_datetime('2022-08-31 06:15:00')
date_2 = pd.to_datetime('2022-08-31 06:20:00')
ymin = -2
ymax = 82
# Ploteamos
fig, axs = plt.subplots(2, 2, sharey=True, sharex=True, figsize=(10, 10))

# Frescos
COV_s.loc[date_1:date_2, cov_emi].plot(ax=axs[0, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_emi])
axs[0, 0].grid(visible=True, which='both', axis='both')
axs[0, 0].set_title('Frescos')

# Productos
COV_s.loc[date_1:date_2, cov_prd].plot(ax=axs[1, 0], ylim=(ymin, ymax),
                                        ylabel='ppb', color=[colors[compound]\
                                                    for compound in cov_prd])
axs[1, 0].grid(visible=True, which='both', axis='both')
axs[1, 0].set_title('Productos')

# Reacción 1
COV_s.loc[date_1:date_2, r1].plot(ax=axs[0, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r1])
axs[0, 1].grid(visible=True, which='both', axis='both')
axs[0, 1].set_title('Reacción Propene -> Acetaldehyde')

# Reacción 2
COV_s.loc[date_1:date_2, r2].plot(ax=axs[1, 1], ylim=(ymin, ymax),
                                   ylabel='ppb', color=[colors[compound]\
                                                        for compound in r2])
axs[1, 1].grid(visible=True, which='both', axis='both')
axs[1, 1].set_title('Reacción 1-Butene -> Propanal')

# Set the figure title and layout
fig.suptitle('Peak'+str(peak)+' '+ date_1.strftime('%Y-%m-%d, %H:%M:%S')+
             ' a '+date_2.strftime('%Y-%m-%d, %H:%M:%S.'))
fig.tight_layout(rect=[0, 0, 1, 0.99])
# fig.savefig(path+date_1.strftime('%d%m')+'/Peak'+str(peak)+' '+
#             date_1.strftime('%Y-%m-%d %H%M%S a ')+
#             date_2.strftime('%H%M%S')+'.png', dpi=300)