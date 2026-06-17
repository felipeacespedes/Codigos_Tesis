# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 13:34:03 2024

@author: felip
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

#%% Importamos datos horarios de HCNM por estación 

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
HCNM = pd.read_csv(path+'HCNM_mod_df.csv',# HCNM_mod_lod_df ó HCNM_orig_df
                   index_col='date',parse_dates=True,
                   usecols=['date','Ventanas','Centro_Quintero',
                            'Concón','Colmo'])

#%% Ploteamos Boxplot total por estación con mpl 

ax = HCNM.plot(kind='box',figsize=(15,10))
plt.ylim(0,1)
plt.grid()
plt.tight_layout()

#%% Ploteamos Boxplot total por estación con SNS

date_1 = pd.to_datetime('2019-01-01 00:00:00')
date_2 = pd.to_datetime('2023-12-31 23:59:00')

sns.set_theme(style='darkgrid')
fig, ax = plt.subplots(figsize = (4.5,6))
sns.boxplot(data=HCNM.loc[date_1:date_2], showfliers=True,
            showmeans=True,
            meanprops={
            'marker': 'o',          # Marker shape (circle)
            'markerfacecolor': 'black', # Marker fill color
            'markeredgecolor': 'white', # Marker edge color
            'markersize': '8'       # Marker size
            })
ax.set_ylabel('[ppm]')
ax.set_xlabel('Estaciones')
ax.tick_params(axis='x', labelrotation=7)
# plt.ylim(0.0,0.9)
plt.title('Boxplot por estación Red SINCA HCNM horario')
plt.tight_layout()
plt.show()

#%% Ploteamos en log scale

fig = plt.subplots(figsize = (10,8))
sns.set_style('ticks')
sns.boxplot(HCNM)
plt.yscale('log')
plt.ylabel('HCNM [ppm]')
plt.xlabel('Estaciones')
plt.title('Boxplot por estación Red SINCA HCNM horario')
plt.tight_layout()
plt.show()
#%% Ploteamos diferencia entre Verano e Invierno

# Filtramos por rangos de fechas
HCNM_apr_aug = HCNM[(HCNM.index.month >= 4) & (HCNM.index.month <= 8)].copy()
HCNM_apr_aug['period'] = 'Cold Season [Abr-Ago]'

HCNM_oct_mar = HCNM[(HCNM.index.month >= 10) | (HCNM.index.month <= 3)].copy()
HCNM_oct_mar['period'] = 'Warm Season [Sep-Mar]'

# Combinamos los dataframes
HCNM_combined = pd.concat([HCNM_apr_aug, HCNM_oct_mar])

# Convertimos a formato largo
HCNM_melted = HCNM_combined.reset_index().melt(id_vars=['date', 'period']\
                                    , var_name='Station', value_name='HCNM')

# Ploteamos el boxplot
plt.figure(figsize=(10, 8))
sns.set_theme(style='darkgrid')
sns.boxplot(data=HCNM_melted, x='Station', y='HCNM', hue='period'\
            , showfliers=False)
plt.ylabel('HCNM [ppm]')
plt.xlabel('Estaciones')
# plt.ylim(0.0, 1.2)
plt.title('Boxplot por estación Red SINCA HCNM, Cold-Warm Season.')
plt.tight_layout()
plt.show()

#%% Ploteamos boxplot por año
# Extraemos el año de la fecha
HCNM['year'] = HCNM.index.year

# Convertimos a formato largo
HCNM_melted = HCNM.reset_index().melt(id_vars=['date', 'year']\
                                      , var_name='Station', value_name='HCNM')

# Ploteamos el boxplot
plt.figure(figsize=(20, 10))
sns.set_theme(style='darkgrid')
sns.boxplot(data=HCNM_melted, x='year', y='HCNM', hue='Station'\
            , showfliers=False)
plt.ylabel('HCNM [ppm]')
plt.xlabel('Año')
# plt.ylim(0.0, 1.2)
plt.title('Boxplot por año y estación Red SINCA HCNM')
plt.legend(title='Estación', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.tight_layout()
plt.show()

#%% Ahora queda identificar episodios de contaminación

# Estos son:
    # 2018 (D83):
        # - 2.4 ppm en CC 2018-08-23, con 180 personas
        # - 2.13 ppm en CQ 2018-09-03, con 155 personas (el 04)
        # - 1.48 ppm en CC 2018-09-12, con 792 personas
    # 2023 (D61):
        # - 4.53 ppm en CQ 2023-03-17, en marzo 315 personas
        # - 3.27 ppm en CQ 2023-04-29, en abril 233 personas
        # - 5.82 ppm en CQ 2023-05-23, en mayo 177 personas (102 el 23-05)
        
fig = plt.subplots(figsize = (10,12))
sns.set_theme(style='darkgrid')
sns.boxplot(data=HCNM,showfliers=True)
plt.ylabel('HCNM [ppm]')
plt.xlabel('Estaciones')
plt.ylim(0.0,6)

# Episodios
# 2018
plt.axhline(y=2.4 , linestyle='-.', color='lightsteelblue'\
            , label='CC 2018-08-23, 180 cs.')
plt.axhline(y=2.13, linestyle='-.', color='cornflowerblue'\
            , label='CQ 2018-09-03, 150 cs.')
plt.axhline(y=1.48, linestyle='-.', color='royalblue'\
            , label='CC 2018-09-12, 792 cs. hasta la fecha.')
#2023
plt.axhline(y=4.53 , linestyle='--', color='lightsteelblue'\
            , label='CQ 2023-03-23, 315 cs. en marzo.')
plt.axhline(y=3.27 , linestyle='--', color='cornflowerblue'\
            , label='CQ 2023-04-29, 233 cs. en abril.')
plt.axhline(y=5.82 , linestyle='--', color='royalblue'\
            , label='CQ 2023-05-23, 177/102 cs. en mayo/ese día.')

plt.title('Boxplot por estación Red SINCA HCNM horario')
plt.legend()
plt.tight_layout()
plt.show()

#%% Ahora incorporamos peticiones de Rodrigo

#%% Ploteamos distribución por episodios

# La idea aquí es plotear boxplots por eventos de contaminación, o sea,
# en el caso del 2018 y 2023, la idea es plotear los 2 o 3 meses de extención

# Extensión de eventos de contaminación:
    # 2018: Los eventos del 2018 comienzan el 21-08 y terminan el 12-09,
    #       por lo que se tomó desde 3 días antes y después.

    # 2023: Los eventos del 2023 comienzan el 17-03 y terminan el 23-05,
    #       por lo que se tomó desde 3 días antes y después.

# Centro Quintero

# Concón

# Creamos lista con nombres de las 2 estación a usar
le = ['Centro_Quintero','Concón']

# Filtramos por los dos rangos de fechas
HCNM_period1 = HCNM.loc['2018-08-21 00:00:00':'2018-09-12 00:00:00',le].copy()
HCNM_period1['period'] = '2018-08-21 to 2018-09-12'

HCNM_period2 = HCNM.loc['2023-03-17 00:00:00':'2023-05-23 00:00:00',le].copy()
HCNM_period2['period'] = '2023-03-17 to 2023-05-23'

# Combinamos los dataframes
HCNM_combined = pd.concat([HCNM_period1, HCNM_period2])

# Convertimos a formato largo
HCNM_melted = HCNM_combined.reset_index()\
    .melt(id_vars=['date', 'period'], var_name='Station', value_name='HCNM')

# Ploteamos el boxplot
plt.figure(figsize=(14, 8))
sns.set_theme(style='darkgrid')
sns.boxplot(data=HCNM_melted, x='period', y='HCNM', hue='Station'\
            ,showfliers=False)
plt.ylabel('HCNM [ppm]')
plt.xlabel('Periodo')
# plt.ylim(0.0, 1.2)
plt.title('Boxplot por periodo y estación Red SINCA HCNM, Serie Modificada')
plt.legend(title='Estación', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

#%% Ploteamos periodos

date_1 = pd.to_datetime('2018-08-21 00:00:00')
date_2 = pd.to_datetime('2018-09-13 00:00:00')
plt.figure()
ax = HCNM.loc[date_1:date_2].plot(subplots=True, layout=(4,1),grid=True,
                                  ylim=(-0.01,2))
fig.title('Valores en estaciones para periodo de eventos 2018')
plt.legend()
plt.tight_layout()


###############################
#%% Definimos que es un peak ##
###############################

est = 'Ventanas'
# est = 'Centro_Quintero'

# Se definira un peak de evento de contaminación, a todo lo que sobrepase 
# la cota inferior de:

# 3 std = 99.8 th percentile (se conversó al comenzar la tesis con Rodrigo):
peak_3std = HCNM[est].quantile(0.998)

# 99 th percentile (extreme event according to Johnston 2011)
peak_99perc = HCNM[est].quantile(0.99)

# 95 th percentile (solo exploratorio, fue preguntado por Rodrigo):
peak_95perc = HCNM[est].quantile(0.95)

print('Los 3 valores a considerar son:')
print('3 std: '+str(peak_3std))
print('99th perc: '+str(peak_99perc))
print('95th_perc: '+str(peak_95perc))

# Para mostrar estos valores en perspectiva, se comparan con

#%% Eventos 2018:

# date_1 = pd.to_datetime('2018-09-24 00:00:00')
# date_2 = pd.to_datetime('2018-09-26 00:00:00')
date_1 = pd.to_datetime('2018-08-21 00:00:00')
date_2 = pd.to_datetime('2018-11-28 00:00:00')
ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(13,5),ylim=(-0.01,4))
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('HCNM [ppm]')
plt.title('Valores de Cota Inferior de Razón de Mezcla para Evento de'\
          +f' Contaminación por HCNM en {est}, Eventos 2018')
plt.legend()
plt.tight_layout()
    
#%% Campaña verano 2022:
    
date_1 = pd.to_datetime('2022-01-01 00:00:00')
date_2 = pd.to_datetime('2022-01-31 23:00:00')
ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(13,5),ylim=(-0.01,4))
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('HCNM [ppm]')
plt.title('Valores de Cota Inferior de Razón de Mezcla para Evento de'\
          +f' Contaminación por HCNM en {est}, Campaña Verano 2022')
plt.legend()
plt.tight_layout()

#%% Campaña invierno 2022:
    
date_1 = pd.to_datetime('2022-06-05 00:00:00')
date_2 = pd.to_datetime('2022-06-15 00:00:00')
    
# date_1 = pd.to_datetime('2022-08-27 00:00:00')
# date_2 = pd.to_datetime('2022-11-03 23:00:00')
ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(13,5),ylim=(-0.01,4)
                                      ,marker='o')
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('HCNM [ppm]')
plt.title('Valores de Cota Inferior de Razón de Mezcla para Evento de'\
          +f' Contaminación por HCNM en {est}, Campaña Invierno 2022')
plt.legend()
plt.tight_layout()

#%% Eventos 2023:
    
## 14 de marzo:
# date_1 = pd.to_datetime('2023-03-13 18:00:00')
# date_2 = pd.to_datetime('2023-03-14 23:00:00')
    
## 17 de marzo:
# date_1 = pd.to_datetime('2023-03-16 18:00:00')
# date_2 = pd.to_datetime('2023-03-17 23:00:00')

## 23 de marzo:
date_1 = pd.to_datetime('2023-03-22 18:00:00')
date_2 = pd.to_datetime('2023-03-23 18:00:00')

## 29-31 de marzo:
# date_1 = pd.to_datetime('2023-03-29 18:00:00')
# date_2 = pd.to_datetime('2023-03-31 23:00:00')

## 3-4 de abril:
# date_1 = pd.to_datetime('2023-05-02 18:00:00')
# date_2 = pd.to_datetime('2023-05-04 23:00:00')

## 23 de mayo:
# date_1 = pd.to_datetime('2023-05-22 18:00:00')
# date_2 = pd.to_datetime('2023-05-23 23:00:00')

## 29 de mayo:
# date_1 = pd.to_datetime('2023-05-28 18:00:00')
# date_2 = pd.to_datetime('2023-05-29 23:00:00')

## 30 de mayo:
# date_1 = pd.to_datetime('2023-05-29 18:00:00')
# date_2 = pd.to_datetime('2023-05-30 23:00:00')

## Periodo completo:
# date_1 = pd.to_datetime('2023-03-14 00:00:00')
# date_2 = pd.to_datetime('2023-05-30 00:00:00')



ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(15,5),ylim=(-0.01,6)
                                      ,marker='o')
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('HCNM [ppm]')
plt.title('Valores de Cota Inferior de Razón de Mezcla para Evento de'\
          +f' Contaminación por HCNM en {est}, Eventos 2023')
plt.legend()
plt.tight_layout()

#%% Serie 2018-2023

date_1 = pd.to_datetime('2018-01-01 00:00:00')
date_2 = pd.to_datetime('2023-12-31 23:59:59')
ax = HCNM.loc[date_1:date_2,est].plot(grid=True, figsize=(15,5)\
                                      , ylim=(-0.01,10))
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('HCNM [ppm]')
plt.title('Valores de Cota Inferior de Razón de Mezcla para Evento de'\
          +f' Contaminación por HCNM en {est}, Serie 2018-2023')
plt.legend()
plt.tight_layout()

#%% Ver promedios 24 horas previas para episodio 2023

#%% Calculamos

# Queremos promediar los valores para las 24 horas previas de cada hora en el episodio de
# 2023

# Fechas de interes
date = pd.date_range('2023-03-15 00:00:00','2023-05-25 00:00:00',freq='1h')

# Creamos DF con columna de HCNM e índice de fechas
HCNM_CQ23 = pd.DataFrame(index=date, columns=['HCNM'])

for d in date:
    delta = datetime.timedelta(days=1)
    HCNM_CQ23.loc[d,'HCNM'] = HCNM.loc[d-delta:d,'Centro_Quintero'].mean()

#%% Ploteamos

date_1 = pd.to_datetime('2023-03-15 00:00:00')
date_2 = pd.to_datetime('2023-05-25 00:00:00')
ax = HCNM_CQ23.plot(grid=True, figsize=(13,5),ylim=(-0.01,3))
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('HCNM [ppm]')
plt.title('Promedios 24h previas y Valores de Cota Inferior de '\
          +'Razón de Mezcla para Evento de '\
          +'Contaminación por HCNM en '+est+'\n, Eventos 2023')
plt.legend()
plt.tight_layout()

#%% Ver promedios 24 horas previas para campaña de ivnierno 2022

#%% Calculamos

# Queremos promediar los valores para las 24 horas previas de cada hora en la
# campaña de invierno del 2022

# Fechas de interes
date = pd.date_range('2022-08-27 00:00:00','2022-11-03 00:00:00',freq='1h')

# Creamos DF con columna de HCNM e índice de fechas
HCNM_CQinv22 = pd.DataFrame(index=date, columns=['HCNM'])

for d in date:
    delta = datetime.timedelta(days=1)
    HCNM_CQinv22.loc[d,'HCNM'] = HCNM.loc[d-delta:d,'Centro_Quintero'].mean()
    
#%% Ploteamos

date_1 = pd.to_datetime('2022-08-27 00:00:00')
date_2 = pd.to_datetime('2022-11-03 00:00:00')
ax = HCNM_CQinv22.plot(grid=True, figsize=(13,5),ylim=(-0.01,0.3))
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('HCNM [ppm]')
plt.title('Promedios 24h previas y Valores de Cota Inferior de '
          +'Razón de Mezcla para Evento de '\
          +'Contaminación por HCNM en '+est+'\n, Campaña Invierno 2022')
plt.legend()
plt.tight_layout()

#%% Ver promedios 24 horas para serie 2018-2023

#%% Calculamos

# Queremos promediar los valores para las 24 horas previas de cada hora en
# toda la serie disponible, o sea 2018-2023

# Fechas de interes
date = pd.date_range('2018-01-01 00:00:00','2023-12-31 23:00:00',freq='1h')

# Creamos DF con columna de HCNM e índice de fechas
HCNM_CQ1823 = pd.DataFrame(index=date, columns=['HCNM'])

for d in date:
    delta = datetime.timedelta(days=1)
    HCNM_CQ1823.loc[d,'HCNM'] = HCNM.loc[d-delta:d,'Centro_Quintero'].mean()


#%% Ploteamos

date_1 = pd.to_datetime('2018-01-01 00:00:00')
date_2 = pd.to_datetime('2023-12-31 23:00:00')
ax = HCNM_CQ1823.plot(grid=True, figsize=(13,5),ylim=(-0.01,3))
plt.hlines(peak_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(peak_3std), linestyle='dashed', color='m')
plt.hlines(peak_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(peak_99perc), linestyle='dashed', color='g')
plt.hlines(peak_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(peak_95perc), linestyle='dashed', color='c')
plt.ylabel('HCNM [ppm]')
plt.title('Promedios 24h previas y Valores de Cota Inferior de '\
          +'Razón de Mezcla para Evento de '\
          +'Contaminación por HCNM en '+est+'\n, Serie 2018-2023')
plt.legend()
plt.tight_layout()

#%% Estudiar valores de promedios 24h previas 
### Esto para percentiles de serie completa y eventos de contaminación
### conocidos, con el fin de comparar las concentraciones de 24h cr a ellas

#%% Percentiles de serie completa

# Se definira un evento de contaminación a todo lo que sobrepase 
# la cota inferior de:

# 3 std = 99.8 th percentile (se conversó al comenzar la tesis con Rodrigo):
epi_3std = HCNM_CQ1823['HCNM'].quantile(0.998)

# 99 th percentile (extreme event according to Johnston 2011)
epi_99perc = HCNM_CQ1823['HCNM'].quantile(0.99)

# 95 th percentile (solo exploratorio, fue preguntado por Rodrigo):
epi_95perc = HCNM_CQ1823['HCNM'].quantile(0.95)

print('Los 3 valores a considerar son:')
print('3 std: '+str(epi_3std))
print('99th perc: '+str(epi_99perc))
print('95th_perc: '+str(epi_95perc))

#%% Ploteamos

# Serie Completa 2018-2023
date_1 = pd.to_datetime('2018-01-01 00:00:00')
date_2 = pd.to_datetime('2023-12-31 23:00:00')
per = 'Serie 2018-2023'

# Campaña verano 2022
# date_1 = pd.to_datetime('2022-01-01 00:00:00')
# date_2 = pd.to_datetime('2022-01-31 23:00:00')
# per = 'Campaña Verano 2022'

# Campaña Invierno 2022
# date_1 = pd.to_datetime('2022-08-27 00:00:00')
# date_2 = pd.to_datetime('2022-11-03 23:00:00')
# per = 'Campaña Invierno 2022'

# Eventos 2023
# date_1 = pd.to_datetime('2023-03-15 00:00:00')
# date_2 = pd.to_datetime('2023-05-25 00:00:00')
# per = 'Eventos 2023'

ax = HCNM_CQ1823.loc[date_1:date_2,'HCNM'].plot(grid=True, figsize=(13,5)\
                                                ,ylim=(-0.01,1))
plt.hlines(epi_3std,date_1,date_2,label='3std(99.8): '+'{0:.2f}'\
           .format(epi_3std), linestyle='dashed', color='m')
plt.hlines(epi_99perc,date_1,date_2,label='99th perc.: '+'{0:.2f}'\
           .format(epi_99perc), linestyle='dashed', color='g')
plt.hlines(epi_95perc,date_1,date_2,label='95th perc.: '+'{0:.2f}'\
           .format(epi_95perc), linestyle='dashed', color='c')
plt.ylabel('HCNM [ppm]')
plt.title('Promedios 24h previas y Valores de Cota Inferior de prom. 24h de '\
          +'Razón de Mezcla para Evento de '\
          +'Contaminación por HCNM en Centro_Quintero\n, '+per)
plt.legend()
plt.tight_layout()

#%% imprimir valores de interés

# Eventos 2023
date_1 = pd.to_datetime('2023-05-23 00:00:00')
date_2 = pd.to_datetime('2023-05-25 00:00:00')
HCNM_CQ1823.loc[date_1:date_2,'HCNM']

#%% Episodios 2023




