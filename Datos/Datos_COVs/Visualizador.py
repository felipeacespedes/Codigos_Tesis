# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 13:22:53 2024

@author: felip
"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime
# import seaborn as sns
# from statsmodels.tsa.seasonal import seasonal_decompose, STL
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()

# sns.set_style("darkgrid")

# plt.rc("figure", figsize=(16, 12))
# plt.rc("font", size=13)

#%% importamos datos PTR
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
# file = 'datos_ver/ver_data_1min.csv'; freq = '1m'
# file = 'datos_inv/voc_5min_UTC_meteo.csv'; freq = '5m'
# COV = pd.read_csv(path+file,delimiter=';')
# COV['date'] = pd.to_datetime(COV['date'],format='%d/%m/%Y %H:%M:%S')
# COV['date'] = pd.to_datetime(COV['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
# COV = COV.set_index('date')

# file = 'datos_inv/inv_data_1min.csv'; freq = '1m'
# # file = 'datos_ver/ver_data_1min.csv'; freq = '1m'
# COV_1m = pd.read_csv(path+file,delimiter=';')
# COV_1m['date'] = pd.to_datetime(COV_1m['date'],format='%d/%m/%Y %H:%M:%S')
# COV_1m['date'] = pd.to_datetime(COV_1m['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
# COV_1m = COV_1m.set_index('date')
# file = 'datos_inv/inv_data_prelim_5seg.csv'; freq = '5s'
# COV_5s = pd.read_csv(path+file,delimiter=';')
# COV_5s['date'] = pd.to_datetime(COV_5s['date'],format='%d/%m/%Y %H:%M:%S')
# COV_5s['date'] = pd.to_datetime(COV_5s['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
# COV_5s = COV_5s.set_index('date')
file = 'datos_inv/inv_data_prelim_1seg.csv'; freq = '1s'
COV_1s = pd.read_csv(path+file,delimiter=';')
COV_1s['date'] = pd.to_datetime(COV_1s['date'],format='%d/%m/%Y %H:%M:%S')
COV_1s['date'] = pd.to_datetime(COV_1s['date'].dt.strftime('%Y-%m-%d %H:%M:%S'))
COV_1s = COV_1s.set_index('date')
del path, file, freq
#%%
BETX = ['Benzene','Toluene','Ethyl.benzene_Xylenes']
    
COV_tot = ['Propene_Cyclopropane','Acetaldehyde',
           'Butenes','Acetone_propanal',
           'Methacrolein_MVK','Butanone_Butanal',
           'Acetic.acid_Glycolaldehyde',
           'Benzene','Toluene','Ethyl.benzene_Xylenes','C9_Aromatics',
           'Methanol','Ethanol','Styrene','Dimethyl.sulfide','Formaldehyde',
           'Isoprene','Furan','Phenol',#'Cresol',
           'Benzonitrile','Benzofuran',
           'Naphthalene', 'Monoterpenes','Acetonitrile']
    
# COVs de interés
COV_int = ['Propene_Cyclopropane','Acetaldehyde',
           'Butenes','Acetone_propanal',
           'Methacrolein_MVK','Butanone_Butanal',
           'Acetic.acid_Glycolaldehyde','Methanol',
           'Benzene','Toluene','Ethyl.benzene_Xylenes','C9_Aromatics']

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


#%% Ploteamos COVs

date_1 = pd.to_datetime('2022-10-23 23:30:00')
date_2 = pd.to_datetime('2022-10-24 00:30:00')
#%% COVS ### 
#%% 1 PLot
ax = COV_1s.loc[date_1:date_2,COV_tot].plot(grid=True, figsize=(10,5),
                                            ylim=(0,80))
                                            # color=[colors[compound]\ usando COV_int! por colores
                                            # for compound in COV_int])
plt.ylabel('[ppb]')
plt.title(str(date_1)+' a '+str(date_2))
plt.tight_layout()
#%% 25 PLots Horizontal
ax = COV_1s.loc[date_1:date_2,COV_tot].plot(subplots=True, layout=(8,3),
                                            grid=True, figsize=(20,10.5))#,ylim=(0,100))
plt.tight_layout()

#%% importamos datos SINCA

#%% DF HCNM
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_SINCA/'
HCNM = pd.read_csv(path+'HCNM_mod_df.csv') # mod_lod
HCNM['date'] = pd.to_datetime(HCNM['date'])
HCNM = HCNM.set_index('date')

#%% DF CO CQ
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_COVs/'
CO = pd.read_csv(path+'CO-CQ_2018-2023.csv', delimiter=';', decimal=',',
                 skiprows=23, skipfooter=24)
CO = CO.iloc[:,4]; CO = CO.rename('Centro_Quintero')
CO = CO.astype('float64'); CO = CO
CO.index = pd.date_range('2018-01-01 00:00:00', '2023-12-31 23:00:00',freq='H')

#%% DF por estación con vientos
le = ['VE','CQ','CC','GA','CO']
for e in le:
    globals()[f'{e}_df'] = pd.read_csv(path+e+'_df.csv')
    globals()[f'{e}_df']['date'] = pd.to_datetime(globals()[f'{e}_df']['date'])
    globals()[f'{e}_df'] = globals()[f'{e}_df'].set_index('date')
    
del le, e, path
######################
#%% Ploteamos HCNM ###
######################
#%% Todas las estaciones
le = ['Ventanas','Centro_Quintero','Concón','Colmo']
# le = HCNM.columns

# Periodo total
date_1 = pd.to_datetime('2019-01-01 00:00:00')
date_2 = pd.to_datetime('2023-12-31 23:00:00')

# Eventos de contaminación 2018
# date_1 = pd.to_datetime('2018-08-20 00:00:00')
# date_2 = pd.to_datetime('2018-09-30 00:00:00')

# Eventos de contaminación 2023
# date_1 = pd.to_datetime('2023-03-15 00:00:00')
# date_2 = pd.to_datetime('2023-05-25 00:00:00')
# date_1 = pd.to_datetime('2019-01-01 00:00:00')
# date_2 = pd.to_datetime('2019-01-31 23:00:00')


# Periodo campaña 2022
# date_1 = pd.to_datetime('2022-08-27 00:00:00')
# date_2 = pd.to_datetime('2022-11-03 23:00:00')

# 2024
# date_1 = pd.to_datetime('2024-03-01 00:00:00')
# date_2 = pd.to_datetime('2024-07-30 00:00:00')

# date = '2023-06-01'
# days = 31
# date_1 = pd.to_datetime(date+' 00:00:00')
# date_2 = date_1 + datetime.timedelta(days=days)



# Plot data
ymax= 1
ax = HCNM.loc[date_1:date_2, le].plot(subplots=True, layout=(4, 1),
            ylabel='[ppm]', grid=True, figsize=(11, 8), ylim=(0, ymax))

# Add a horizontal line at y=0.02 to each subplot
for axis in ax.flatten():
    axis.axhline(y=0.05, color='r', linestyle='--', alpha=0.5)

# Add title and adjust layout
plt.suptitle('HCNM horario')
plt.tight_layout()
# path para guardar figuras
path_fig = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 1/'
plt.savefig(path_fig+'HCNM_horario_max'+str(ymax)+'ppm.png',dpi=300)


#%% Centro Quintero y Concón
le = ['Centro_Quintero','Concón']

date = '2023-03-01'
days = 2

date_1 = pd.to_datetime(date+' 12:00:00')
date_2 = date_1 + datetime.timedelta(days=days)

# Eventos de contaminación 2018
# date_1 = pd.to_datetime('2018-08-20 00:00:00')
# date_2 = pd.to_datetime('2018-09-13 00:00:00')
# Eventos de contaminación 2023
# date_1 = pd.to_datetime('2023-05-20 00:00:00')
# date_2 = pd.to_datetime('2023-05-25 00:00:00')
ax = HCNM.loc[date_1:date_2,le].plot(subplots=True, layout=(2,1), ylabel='[ppm]'\
                                    ,grid=True, figsize=(10,5),ylim=(0,4))
plt.suptitle('HCNM horario '+date_1.strftime('%d de %b')+' al '\
             +date_2.strftime('%d de %b')\
             +date_2.strftime(', %Y')+', serie modificada')
plt.tight_layout()

print(HCNM.loc[date_1:date_2,'Concón'].mean())

#%%
# Se definira un peak de evento de contaminación, a todo lo que sobrepase 
# la cota inferior de:
est = 'Centro_Quintero'

# 3 std = 99.8 th percentile (se conversó al comenzar la tesis con Rodrigo):
peak_3std = HCNM[est].quantile(0.998)

# 99 th percentile (extreme event according to Johnston 2011)
peak_99perc = HCNM[est].quantile(0.99)

# 95 th percentile (solo exploratorio, fue preguntado por Rodrigo):
peak_95perc = HCNM[est].quantile(0.95)
#%% 1 estación
date_1 = pd.to_datetime('2022-08-27 00:00:00')
date_2 = pd.to_datetime('2022-11-03 23:00:00')
ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(16,7),ylim=(0,2.5))
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('[ppm]')
plt.legend()
plt.title('HCNM horario ' + date_1.strftime('%d de %b, %Y') + ' al ' +
             date_2.strftime('%d de %b') +
             date_2.strftime(', %Y')+', '+est)
plt.tight_layout()
# path = 'C:/Users/felip/Desktop/Avances/10/2024/TS/'
# plt.savefig(path+est+'.png', dpi=300)
# print(HCNM.loc[date_1:date_2,est])

#%% Lo mismo pero para peaks campaña invierno

# Definimos los momentos iniciales y finales de peaks
Pi = ['2022-09-12 04:00:00', '2022-10-04 05:00:00', '2022-10-04 20:00:00'\
      ,'2022-10-12 23:00:00','2022-10-23 20:00:00','2022-10-31 21:00:00']
Pf = ['2022-09-12 12:00:00', '2022-10-04 08:00:00', '2022-10-05 04:00:00'\
      ,'2022-10-13 09:00:00','2022-10-24 09:00:00','2022-11-01 09:00:00']
path = 'C:/Users/felip/Desktop/Avances/10/Peaks_Campaña_Invierno/HCNM/'
# Iteramos por peaks
for p in range(len(Pi)):
    # Definmos momentos inicial y final
    date_1 = pd.to_datetime(Pi[p])
    date_2 = pd.to_datetime(Pf[p])
    # Ploteamos
    plt.figure()
    ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(10,5),ylim=(-0.1,3))
    plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
               .format(peak_3std), linestyle='dashed', color='m')
    plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
               .format(peak_99perc), linestyle='dashed', color='g')
    plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
               .format(peak_95perc), linestyle='dashed', color='c')
    plt.suptitle('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
              +date_2.strftime('%Y-%m-%d, %H:%M.'))
    plt.legend()
    plt.tight_layout()
    plt.savefig(path+'CQ_'+date_1.strftime('%Y-%m-%d %H')+'.png', dpi=300)
#%%
# date_1 = pd.to_datetime('2022-09-02 00:00:00')
# date_2 = pd.to_datetime('2022-09-02 23:00:00')
date = '2022-06-04'
days = 5

date_1 = pd.to_datetime(date+' 00:00:00')
date_2 = date_1 + datetime.timedelta(days=days)
ls = ['HCNM','wd']
ax = CQ_df[ls].loc[date_1:date_2,:].plot(subplots=True, layout=(2,1)\
                                         , grid=True, figsize=(10,8), ylim=())
plt.suptitle(ls[0]+' y '+ls[1])
plt.tight_layout()

#####################
#%% Ploteamos COV ###
#####################

# definimos COV
# COV = COV_1m; freq = '1min'
COV = COV_5s; freq = '5seg'
# COV = COV_1s; freq = '1seg'


# Path de guardado de imagenes
# path = 'C:/Users/felip/Desktop/Avances/6/peaks_erroneos/'

#%% Todos los Covs en un plot
d1 = pd.to_datetime('2022-09-02 00:00:00')
d2 = pd.to_datetime('2022-09-02 23:00:00')
# cov = COV.columns[0:25]
COV.loc[d1:d2,COV_int].plot(grid=True, figsize=(10,20), subplots=True)
# plt.title('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
#           +date_2.strftime('%H:%M, ')+'freq='+freq)
plt.tight_layout()
# plt.savefig(path+date_1.strftime('%d-%m-%y, %H%M')+' a '+date_2.\
#     strftime('%H%M, ')+freq+'.png')
# print(date_1.strftime('%Y-%m-%d, %H:%M')+' a '+date_2.strftime('%H:%M'))


#%% Total

ax = COV.plot(subplots=True, layout=(25,1)\
              , grid=True, figsize=(50,30),ylim=(-1,300))
plt.tight_layout()

#%% dates
date_1 = pd.to_datetime('2022-10-07 18:00:00')
date_2 = pd.to_datetime('2022-10-07 23:00:00')


#%% BETX
ax = COV.loc[date_1:date_2,'Butenes'].plot(grid=True, figsize=(5,7),ylim=(-1,30))
plt.tight_layout()

#%% Resampleamos y aplicamos factor a Benzene

COV_h = COV.resample('1H').mean()

COV_h['Benzene_60'] = COV_h['Benzene']*0.6

#%% Interes

ax = COV_h[['Benzene_60','Isoprene']].loc[date_1:date_2,:]\
                            .plot(#subplots=True, layout=(3,1),
                                  grid=True\
                                  , figsize=(22,10),ylim=(-1,2))
plt.tight_layout()

#%% Correlación
ax = COV[COV_int].loc[date_1:date_2,:].plot(subplots=True, layout=(8,1),
                                             grid=True, figsize=(5,10),
                                             ylim=(-1,50))
plt.tight_layout()

#%% Ploteamos peaks de campaña de invierno en todos los contaminantes

# Definimos los momentos iniciales y finales de peaks
Pi = ['2022-09-12 04:00:00', '2022-10-04 05:00:00', '2022-10-04 20:00:00'\
      ,'2022-10-12 23:00:00','2022-10-23 20:00:00','2022-10-31 21:00:00']
Pf = ['2022-09-12 12:00:00', '2022-10-04 08:00:00', '2022-10-05 04:00:00'\
      ,'2022-10-13 09:00:00','2022-10-24 09:00:00','2022-11-01 09:00:00']

# Path de guardado
path = 'C:/Users/felip/Desktop/Avances/10/Peaks_Campaña_Invierno/'
ymax = 50 # 200 # 
tipo = '1plot' # '25plot' #

# Iteramos por peaks
for p in range(len(Pi)):
    # Definmos momentos inicial y final
    date_1 = pd.to_datetime(Pi[p])
    date_2 = pd.to_datetime(Pf[p])
    # Ploteamos
    # 1 Plot
    if tipo == '1plot':
        ax = COV.loc[date_1:date_2,:].plot(grid=True, figsize=(10,7)\
                                              ,ylim=(-0.1,ymax))
    # Subplots
    if tipo == '25plot':
        ax = COV.loc[date_1:date_2,:].plot(subplots=True, layout=(25,1)\
                                , grid=True, figsize=(10,20),ylim=(-0.1,ymax))
    else:
        print('Tipo debe ser 1plot o 25plot (así se llaman las carpetas).')
        quit

    plt.suptitle('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
              +date_2.strftime('%Y-%m-%d, %H:%M.'))
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(path+tipo+'/'+'ymax '+str(ymax)+'ppb/'\
                +date_1.strftime('%Y-%m-%d %H')+'.png',dpi=300)

#%% Ploteamos COVs y HCNM en CQ

# date_1 = pd.to_datetime('2022-01-18 21:00:00')
# date_2 = pd.to_datetime('2022-01-19 03:00:00')
date_1 = pd.to_datetime('2022-09-08 06:20:00')
date_2 = pd.to_datetime('2022-09-08 06:30:00')
#%% COVS ### 
#%% 1 PLot
ax = COV.loc[date_1:date_2,COV_int].plot(grid=True, figsize=(10,5),
                                            ylim=(0,80),
                                            color=[colors[compound]\
                                            for compound in COV_int])
plt.ylabel('[ppb]')
plt.title(str(date_1)+' a '+str(date_2))
plt.tight_layout()
#%% 25 PLots Horizontal
ax = COV_5s.loc[date_1:date_2,COV_tot].plot(subplots=True, layout=(8,3),
                                            grid=True, figsize=(20,10.5))#,ylim=(0,100))
plt.tight_layout()

#%% 25 PLots Vertical
ax = COV.loc[date_1:date_2,COV_int].plot(subplots=True, layout=(17,1)\
                                            , grid=True, figsize=(10,20))#,ylim=(0,100))
plt.tight_layout()
#%% HCNM ###
est = 'Centro_Quintero'
peak_3std = HCNM[est].quantile(0.998)
peak_99perc = HCNM[est].quantile(0.99)
peak_95perc = HCNM[est].quantile(0.95)
ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(16,8),ylim=(-0.1,3))
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('[ppm]')
plt.legend()
plt.title(est)
plt.tight_layout()

#%% CO ###

ax = CO[date_1:date_2].plot(grid=True, figsize=(16,8),ylim=(-0.1,3))
plt.legend()
plt.tight_layout()
