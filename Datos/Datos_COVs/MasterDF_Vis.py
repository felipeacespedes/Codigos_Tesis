# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 11:39:36 2024

@author: felip

Codigo para visualizar datos de MasterDF
"""
# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Importamos MasterDF
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/datos_inv/'
DATA = pd.read_csv(path+'MasterDF_inv_data_1m_ak.csv',delimiter=';')
DATA['date'] = pd.to_datetime(DATA['date'],format='%d/%m/%Y %H:%M:%S')
DATA['date'] = pd.to_datetime(DATA['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
DATA = DATA.set_index('date')

#%% Resampleamos

DATA_1h = DATA.resample('h').mean()

#%% Definimos listas de contmaintes y variables de interes

# compuestos buque
comp_bu = ['CO','NO2','Methanol','Toluene','wd','ws']

# compuestos que reaccionan en eventos
comp_re = ['Butenes','Acetone_propanal','Propene_Cyclopropane','Acetaldehyde',
           'NO','sr']

# compuestos que aumentan en eventos
comp_ae = ['Butenes','Acetone_propanal','Propene_Cyclopropane','Acetaldehyde',
            'Formaldehyde','Methanol','Ethanol','Styrene',
            'Toluene','Benzene','Ethyl.benzene_Xylenes',
            'CO','NO2',
           # 'NO','O3',
           'wd','ws','sr']

# Methacrolein/MVK and Butanone/Butanal affinity compunds
comp_MMBB = ['Methacrolein_MVK','Propene_Cyclopropane','Benzene','Acetonitrile',
             'Butenes','Isoprene','Furan','Butanone_Butanal','Acetaldehyde',
             'Acetone_propanal']

# compuestos de interes
comp_int = ['Propene_Cyclopropane','Acetaldehyde',
           'Butenes','Acetone_propanal',
           'Methacrolein_MVK','Butanone_Butanal',
           'Benzene','Toluene','Ethyl.benzene_Xylenes',
           'Methanol','Styrene','Dimethyl.sulfide','Formaldehyde','Isoprene',
           'Furan','Phenol','Acetic.acid_Glycolaldehyde']

# Meteo
met = ['p', 't', 'rh','sr', 'ws', 'wd']
met_int = ['sr', 'ws', 'wd']

#%% compuestos totales sin meteo
comp_tot = [
            'Propene_Cyclopropane','Butenes','Methacrolein_MVK',
            'Acetaldehyde','Acetone_propanal','Butanone_Butanal',
            'Acetic.acid_Glycolaldehyde','Formaldehyde',
            'Methanol','Ethanol','Styrene','Dimethyl.sulfide',
            'Toluene','Benzene','Ethyl.benzene_Xylenes',
            'NO','NO2','O3','HCNM','CO','CH4',
            'sr','ws','wd',
            # 'rh','t','rh'
            ]

comp_int = [
            'Propene_Cyclopropane','Butenes','Methacrolein_MVK',
            'Acetaldehyde','Acetone_propanal','Butanone_Butanal',
            ]

#%% Fechas de interes

# date_1 = pd.to_datetime('2022-08-30 18:00:00')
# date_2 = pd.to_datetime('2022-08-31 11:00:00')
# date_1 = pd.to_datetime('2022-09-01 00:00:00')
# date_2 = pd.to_datetime('2022-09-02 23:59:00')
# date_1 = pd.to_datetime('2022-08-27 00:00:00')
# date_2 = pd.to_datetime('2022-11-03 23:59:00')

### Eventos a estudiar ###

## Madrugada y mañana
# date_1 = pd.to_datetime('2022-09-12 02:00:00')
# date_2 = pd.to_datetime('2022-09-12 11:59:00')
# date_1 = pd.to_datetime('2022-10-04 02:00:00')
# date_2 = pd.to_datetime('2022-10-04 11:59:00')

## Primer peak madrugada
# date_1 = pd.to_datetime('2022-09-12 03:00:00')
# date_2 = pd.to_datetime('2022-09-12 03:59:00')
# date_1 = pd.to_datetime('2022-10-04 05:00:00')
# date_2 = pd.to_datetime('2022-10-04 05:59:00')

## Evolución mañana evolución
# date_1 = pd.to_datetime('2022-09-12 06:00:00')
# date_2 = pd.to_datetime('2022-09-12 10:59:00')
# date_1 = pd.to_datetime('2022-10-04 07:00:00')
# date_2 = pd.to_datetime('2022-10-04 10:59:00')


#%% Definimos path y fecha

path_fig = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 3/1/'

# +-1 día
# date_1 = pd.to_datetime('2022-10-03 00:00:00')
# date_2 = pd.to_datetime('2022-10-06 00:00:00')

# día completo
date_1 = pd.to_datetime('2022-10-04 00:00:00')
date_2 = pd.to_datetime('2022-10-04 23:59:00')

# evento
# date_1 = pd.to_datetime('2022-10-04 04:00:00')
# date_2 = pd.to_datetime('2022-10-04 10:59:00')


################################################
#%%### Usamos MPL para modificar cositas #######

#%% Ploteamos subplot

fig, axes = plt.subplots(nrows=8, ncols=3, figsize=(10, 13), sharex=True)
axes = axes.flatten() 

plot_data = DATA.loc[date_1:date_2]

# Grab the default pandas/matplotlib color cycle (which has 10 colors)
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

for i, comp in enumerate(comp_tot):
    ax = axes[i]
    
    # Pick a color from the cycle (the modulo % ensures it loops back to the start if i > 9)
    plot_color = colors[i % len(colors)]
    
    plot_data_dn = plot_data[comp].dropna()
    
    # Plot the series with the assigned color
    ax.plot(plot_data_dn.index, plot_data_dn, color=plot_color)
    
    # Make the title bold and set the font size
    ax.set_title(comp, fontsize=13, fontweight='bold')
    ax.set_xlabel('Hora',fontsize=12)
    
    # Modify the tick label sizes
    ax.tick_params(axis='both', which='major', labelsize=11)
    
    # Format the x-axis to only show Hours and Minutes
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    
    # Force perfect borders
    ax.set_xlim(date_1, date_2)
    
    ax.grid(True)

# Rotate the x-ticks AND center them directly under the tick marks
fig.autofmt_xdate(rotation=30, ha='center')

fig.suptitle('Series 04-10, interpolación Akima', fontsize=14)
# fig.suptitle('Series 04-10, horas evento, interpolación Akima', fontsize=14)

# fig.suptitle('Series 04-10, ±1 día, series originales', fontsize=14)
# fig.suptitle('Series 04-10, series originales', fontsize=14)
# fig.suptitle('Series 04-10, horas evento, series originales', fontsize=14)




# fig.subplots_adjust(top=0.21)


plt.tight_layout()

### FILENAME:

# AK
filename = f"Series_ak_{date_1.strftime('%m-%d-%H%M')}_a_{date_2.strftime('%m-%d-%H%M')}.png"

# OG
# filename = f"Series_og_{date_1.strftime('%m-%d-%H%M')}_a_{date_2.strftime('%m-%d-%H%M')}.png"

plt.savefig(path_fig + filename, dpi=300)

plt.show()

#%% 

DATA_test = DATA.loc[date_1:date_2,comp_tot]

#%% Ploteamos subplot

fig = DATA.loc[date_1:date_2,comp_tot].plot(subplots=True,grid=True,figsize=(10,10),layout=(8,3))
# DATA.loc[date_1:date_2,comp_int].plot(subplots=True,grid=True,figsize=(15,4),layout=(2,3))
for i in range(3):  
    fig[7,i].set_xticks(fig[7,i].get_xticks())
    fig[7,i].set_xticklabels(fig[7,i].get_xticklabels(),rotation=30)
    # fig[7,i].tick_params('x',rotation=20)
plt.tight_layout()
plt.savefig(path_fig+'Series_ak_'+date_1.strftime('%m-%d-%H%M')+'_a_'+
            date_2.strftime('%m-%d-%H%M')+'.png',dpi=300)


#%% Cada plot por separado para abordar diferentes frecuencias

# Creamos figura
fig, axes = plt.subplots(nrows=8, ncols=3, figsize=(15, 10), sharex=True)
axes = axes.flatten() # Aplanamos para iterar más facil 
cmap = plt.get_cmap('tab10') # cmap tab para 10 colores

cols = DATA.loc[date_1:date_2, comp_tot].columns
# 
for i, col in enumerate(cols):
    # usamos operador % para iterar de 0 a 9
    color_index = i % 10
    series_to_plot = DATA.loc[date_1:date_2, col].dropna()
    series_to_plot.plot(ax=axes[i], grid=True, legend=True,
                        color=cmap(color_index))

plt.tight_layout()
plt.savefig(path_fig+'Series_og_'+date_1.strftime('%m-%d-%H%M')+'_a_'+
            date_2.strftime('%m-%d-%H%M')+'.png',dpi=300)


#%% Ploteamos en plot conjunto

# 1er peak
# N = 1
# date_1 = pd.to_datetime('2022-10-04 05:00:00')
# date_2 = pd.to_datetime('2022-10-04 07:30:00')

# 2do peak
N = 2
date_1 = pd.to_datetime('2022-10-04 08:00:00')
date_2 = pd.to_datetime('2022-10-04 10:59:00')

DATA.loc[date_1:date_2,comp_int].plot(subplots=False,grid=True,figsize=(8,5),
                                      ylabel='ppb')
plt.tight_layout()
plt.savefig(path_fig+'COV_p'+str(N)+'_'+date_1.strftime('%m-%d-%H%M')+'_a_'+
            date_2.strftime('%m-%d-%H%M')+'.png',dpi=300)

#%% 1 compuesto

DATA.loc[date_1:date_2,'NO2'].plot(subplots=False,grid=True,figsize=(8,5),
                                      ylabel='ppb',ylim=(0,10))
plt.tight_layout()





