# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 14:52:04 2025

@author: felip
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#%% Importamos datos de intoxicados

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'

T59_raw = pd.read_csv(path+'serie_T59.csv')
T59_raw['date'] =  pd.to_datetime(T59_raw['date'],format='%d-%m-%Y')
T59_raw = T59_raw.set_index('date')

#%% Periodo de estudio

# Fechas inicial y final
date_1 = pd.to_datetime('01-01-2022',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2023',format='%d-%m-%Y')

T59_raw_F = T59_raw.loc[date_1:date_2]


#%% Rellenar datos serie de tiempo

# Fechas inicial y final
date_1 = pd.to_datetime('01-01-2018',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2024',format='%d-%m-%Y')


# Create full daily date range
full_range = pd.date_range(start=date_1, end=date_2, freq='D')

# Ensure your index is datetime and sorted
T59_raw.index = pd.to_datetime(T59_raw.index, format='%d-%m-%Y')
T59_raw = T59_raw.sort_index()

# Reindex to full date range
T59_full = T59_raw.reindex(full_range)

# Fill missing values
T59_full['T59'] = T59_full['T59'].fillna(0)

#%% Chequeo estadísticos
date_1 = pd.to_datetime('01-01-2022',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2023',format='%d-%m-%Y')
data = T59_raw.loc[date_1:date_2].copy()

# comuna = 'Quintero'
# comuna = 'Puchuncaví'
comuna = 'Quintero y Puchuncaví'
mask = (data['Comuna'] == comuna)
print(comuna)
print('Largo: '+str(len(data[mask])))
print('Mediana: '+str(data.loc[mask,'T59'].quantile(0.5)))
print('Mediana: '+str(data['T59'].quantile(0.5)))

#%% Serie
fig, ax = plt.subplots()
date_1 = pd.to_datetime('22-05-2023',format='%d-%m-%Y')
date_2 = pd.to_datetime('26-05-2023',format='%d-%m-%Y')
T59_raw.loc[date_1:date_2,'T59'].plot(grid=True, figsize=(12,5),
                                      ylabel='Nro. de personas',
                                      lw=0, marker='o', ms=10,
                                      xlim=(date_1,date_2))
ax.set_title('Serie diaria rotulo T59')
fig.tight_layout()


#%% Plot serie de tiempo

fig, ax = plt.subplots()
date_1 = pd.to_datetime('01-01-2018',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2024',format='%d-%m-%Y')
T59_raw.loc[date_1:date_2,'T59'].plot(grid=True, figsize=(12,5),
                                      ylabel='Nro. de personas',
                                      lw=0, marker='.', ms=5)
ax.set_title('Serie diaria rótulo T59')
# Sección utilizada 
x = [pd.to_datetime('01-01-2019'),pd.to_datetime('01-01-2024')]
ax.fill_between(x, -20, 300, color='blue', alpha=0.1)
ax.axvline(x=x[0], color='grey', ls='--',lw=2)
ax.axvline(x=x[1], color='grey', ls='--',lw=2)
ax.set_ylim(-10,250)
fig.tight_layout()

#%% Plot Serie de Tiempo color por comuna

fig ,ax= plt.subplots(figsize=(10,4))
date_1 = pd.to_datetime('01-01-2018',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2024',format='%d-%m-%Y')
data = T59_raw[date_1:date_2].copy()
mask = (data['Comuna']!='Quintero')&(data['Comuna']!='Puchuncaví')&\
       (data['Comuna']!='Quintero y Puchuncaví')
data.loc[mask,'Comuna'] = 'No se menciona'
hue_order = ['Quintero','Puchuncaví','Quintero y Puchuncaví','No se menciona']

sns.scatterplot(data=data,ax=ax, x='date', y='T59', hue='Comuna',
                hue_order=hue_order,palette='muted')

ax.set_title('Serie intoxicaciones diarias', fontsize=14)
# Sección utilizada 
x = [pd.to_datetime('01-01-2022'),pd.to_datetime('01-01-2021'),
     pd.to_datetime('01-01-2024')]
ax.fill_between(x[::2], -20, 300, color='blue', alpha=0.1)
ax.axvline(x=x[1], color='grey', ls='--',lw=2,alpha=0.8)
# ax.axvline(x=x[2], color='grey', ls='--',lw=2,alpha=0.8)
ax.set_ylim(-10,250)
ax.set_ylabel('Nro. de Personas',fontsize=13)
ax.set_xlabel('Fecha',fontsize=13)
ax.tick_params('both',labelsize=11)
ax.grid()
fig.tight_layout()
path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/datos/'
fig.savefig(path+'SerieT59.png', dpi=300)

#%% Plot Serie de Tiempo color por comuna # Plot Simposio

fig ,ax= plt.subplots(figsize=(8,5))
date_1 = pd.to_datetime('01-01-2022',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2023',format='%d-%m-%Y')
data = T59_raw[date_1:date_2].copy()
mask = (data['Comuna']!='Quintero')&(data['Comuna']!='Puchuncaví')&\
       (data['Comuna']!='Quintero y Puchuncaví')
# data.loc[mask,'Comuna'] = 'No se menciona'
hue_order = ['Quintero','Quintero y Puchuncaví','Puchuncaví']#,'No se menciona']
custom_palette = ['blue','red','gold']#,'grey']
sns.scatterplot(data=data,ax=ax, x='date', y='T59', hue='Comuna',
                hue_order=hue_order,palette=custom_palette)

ax.set_title('Serie intoxicaciones diarias por comuna')
# Sección utilizada 
# x = [pd.to_datetime('01-01-2019'),pd.to_datetime('01-01-2021'),
#      pd.to_datetime('01-01-2024')]
# ax.fill_between(x[::2], -20, 300, color='blue', alpha=0.1)
# ax.axvline(x=x[1], color='grey', ls='--',lw=2,alpha=0.8)
# ax.axvline(x=x[2], color='grey', ls='--',lw=2,alpha=0.8)
ax.set_xlim(date_1,date_2)
ax.set_ylim(-10,250)
ax.set_ylabel('Nro. de Personas')
ax.tick_params(axis='x', labelrotation=20)
ax.set_xlabel('Fecha')
ax.legend(loc='upper left')
ax.grid()
fig.tight_layout()
path = 'C:/Users/felip/Desktop/U/Tesis/Simposio_CR2/figs/'
fig.savefig(path+'SerieT59.png', dpi=300)

#%% Histograma por comuna

date_1 = pd.to_datetime('01-01-2022',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2023',format='%d-%m-%Y')
T59_raw['Comuna'].hist(figsize=(7,5),grid=True)
plt.title('Histograma casos por comuna')
plt.tight_layout()

#%% Histograma por Año (sum of intoxicated people)

# --- SETTINGS ---
data = T59_raw.copy()
data['Año'] = data.index.year.astype(int)

# --- Handle comunas ---
mask = (data['Comuna'] != 'Quintero') & (data['Comuna'] != 'Puchuncaví') & \
       (data['Comuna'] != 'Quintero y Puchuncaví')
data.loc[mask, 'Comuna'] = 'No se menciona'
hue_order = ['Quintero', 'Puchuncaví', 'Quintero y Puchuncaví', 'No se menciona']
data['Comuna'] = pd.Categorical(data['Comuna'], hue_order)

# --- Ensure all years exist ---
all_years = range(data['Año'].min(), data['Año'].max() + 1)
empty_rows = pd.DataFrame({'Año': list(all_years), 'T59': 0, 'Comuna': hue_order[0]})
missing = set(all_years) - set(data['Año'])
data = pd.concat([data, empty_rows[empty_rows['Año'].isin(missing)]], ignore_index=True)

# --- Aggregate for labels ---
agg_df = data.groupby(['Año', 'Comuna'], observed=True)['T59'].sum().reset_index()
total_df = agg_df.groupby('Año', observed=True)['T59'].sum().reset_index()

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(
    data=data,
    x='Año',
    hue='Comuna',
    weights='T59',
    multiple='stack',
    discrete=True,
    shrink=0.6,
    palette='muted',
    hue_order=hue_order,
    ax=ax
)

# --- Add labels ---
bar_width = 0.6  # matches shrink=0.6
for year in all_years:
    year_data = agg_df[agg_df['Año'] == year].set_index('Comuna')
    year_total = total_df.loc[total_df['Año'] == year, 'T59'].values[0]
    
    bottom = 0
    # reverse hue order to match stack plotting order
    for comuna in reversed(hue_order): 
        val = year_data.loc[comuna, 'T59'] if comuna in year_data.index else 0
        if val > 5:
            ax.text(
                x=year,
                y=bottom + val / 2,
                s=int(val),
                ha='center', va='center',
                fontsize=9, color='white', fontweight='bold'
            )
        bottom += val

    # top total
    if year_total >= 0:
        ax.text(
            x=year,
            y=bottom + max(total_df['T59']) * 0.02 - 25,
            s=int(year_total),
            ha='center', va='bottom',
            fontsize=10, fontweight='bold'
        )
# --- Final touches ---
ax.set_ylabel('Nro. de Personas',fontsize=13)
ax.set_xlabel('Año',fontsize=13)
ax.tick_params('both',labelsize=11)
# ax.set_title('Total personas intoxicadas por año')
ax.grid(axis='y', zorder=0)

fig.tight_layout()
path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 2/Hist/PorAño/'
fig.savefig(path + '/Hist_PorAño_Nintx.png', dpi=300)

#%% Histograma por Año nro. de eventos

# Settings
N_int = 1
date_1 = pd.to_datetime('01-01-2018',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2024',format='%d-%m-%Y')
mask = (T59_raw['T59']>=N_int)
data = T59_raw[mask].copy()
data.loc[mask,'T59'] = 1
data = data[date_1:date_2]
data['Año'] = data.index.year.astype(int)



# --- Handle comunas ---
mask = (data['Comuna'] != 'Quintero') & (data['Comuna'] != 'Puchuncaví') & \
       (data['Comuna'] != 'Quintero y Puchuncaví')
data.loc[mask, 'Comuna'] = 'No se menciona'
hue_order = ['Quintero', 'Puchuncaví', 'Quintero y Puchuncaví', 'No se menciona']
data['Comuna'] = pd.Categorical(data['Comuna'], hue_order)



# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(
    data=data,
    x='Año',
    hue='Comuna',
    weights='T59',
    multiple='stack',
    discrete=True,
    shrink=0.6,
    palette='muted',
    hue_order=hue_order,
    ax=ax
)

# --- Final touches ---
ax.set_ylabel('Nro. de Eventos',fontsize=13)
ax.set_xlabel('Año',fontsize=13)
ax.tick_params('both',labelsize=11)

ax.grid(axis='y', zorder=0)

fig.suptitle('Total personas intoxicadas por año', fontsize=13)
fig.tight_layout()
path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 2/Hist/PorAño/'
fig.savefig(path + '/Hist_PorAño_min1intx.png', dpi=300)

#%% Histograma por comuna y Mes del año

# Settings
N_int = 1
date_1 = pd.to_datetime('01-01-2022',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2023',format='%d-%m-%Y')
mask = (T59_raw['T59']>=N_int)
data = T59_raw[mask].copy()
data = data[date_1:date_2]
# mes
data['Mes'] = data.index.month_name(locale='es_ES.UTF-8')
data['Mes'] = data['Mes'].astype('category')
Mes = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio',
         'Agosto','Septiembre','Octubre','Noviembre', 'Diciembre']
data['Mes'] = pd.Categorical(data['Mes'], Mes)
# comuna
mask = (data['Comuna']!='Quintero')&(data['Comuna']!='Puchuncaví')&\
       (data['Comuna']!='Quintero y Puchuncaví')
if len(data.loc[mask,'Comuna'])==0:
    hue_order = ['Quintero','Puchuncaví','Quintero y Puchuncaví']
    c_label = ['Q','P','Q&P']
    data['Comuna'] = pd.Categorical(data['Comuna'], hue_order)
else:
    data.loc[mask,'Comuna'] = 'No se menciona'
    hue_order = ['Quintero','Puchuncaví','Quintero y Puchuncaví','No se menciona']
    c_label = ['Q','P','Q&P','NM']
    data['Comuna'] = pd.Categorical(data['Comuna'], hue_order)

# Ploteamos
fig, ax = plt.subplots(1,2, figsize=(10,5),width_ratios=[1,4])

# ax[0]: por comuna
sns.histplot(data=data,x='Comuna',hue='Comuna',ax=ax[0],shrink=0.6,zorder=2,
             palette='bright',hue_order=hue_order,legend=False)
ax[0].set_xticks(ax[0].get_xticks())
ax[0].set_xticklabels(c_label)
ax[0].set_xlabel('Comuna', fontsize=13)
ax[0].set_ylabel('Nro. de Eventos', fontsize=13)
ax[0].tick_params('both',labelsize=11)
ax[0].grid(zorder=0)

# ax[1]: por Mes del año
sns.histplot(data=data,x='Mes',hue='Comuna',ax=ax[1], multiple='stack',
             palette='muted',shrink=0.6,hue_order=hue_order,zorder=2)
ax[1].set_xticks(ax[1].get_xticks());m_label=[]
for m in ax[1].get_xticklabels(): m_label.append(m.get_text()[0:3])
ax[1].set_xticklabels(m_label)
ax[1].set_ylabel('Nro. de Eventos', fontsize=13)
ax[1].set_xlabel('Mes', fontsize=13)
ax[1].tick_params('both',labelsize=11)
ax[1].grid(zorder=0)

# fig
y1 = str(date_1.year); y2 = str(date_2.year)
fig.suptitle(y1+' a '+y2
             #+', min. '+str(N_int)+' intx.'
             , fontsize=13)
fig.tight_layout()
path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 2/Hist/'
fig.savefig(path+y1+'-'+y2+'/Hist_'+y1+'-'+y2+'_min'+
            str(N_int)+'intx.png', dpi=300)

#%% Boxplot por comuna y total

# Settings
data = T59_raw.copy()
hue_order = ['Quintero','Puchuncaví','Quintero y Puchuncaví']
data['Comuna'] = pd.Categorical(data['Comuna'], hue_order)

# Plot
fig, ax = plt.subplots(1,3,figsize=(10,5),sharey=True,width_ratios=[3,1,1])

meanprops={"marker":"D", "markerfacecolor":"white","zorder":3,
           "markeredgecolor":"black","markersize":"8"}

# ax[0]: Casos por comuna
date_1 = pd.to_datetime('01-01-2022',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2023',format='%d-%m-%Y')
sns.boxplot(data=data[date_1:date_2],y='T59',x='Comuna',hue='Comuna',
            legend=False,ax=ax[0],palette='muted',zorder=1,showfliers=False,
            showmeans=True,linewidth=2,meanprops=meanprops)
# sns.violinplot(data=data,y='T59',x='Comuna',ax=ax[0],
#                palette='Set1',linewidth=3,fill=False,inner='quart',
#                inner_kws=dict(color="k",linewidth=2))
sns.stripplot(data=data[date_1:date_2],y='T59',x='Comuna',ax=ax[0],zorder=2,
              hue='Comuna',legend=False,palette='muted',edgecolor='auto',
              size=6,linewidth=1)
ax[0].grid(zorder=0,alpha=0.7)
ax[0].set_title('Eventos por comuna [2022-2023]', fontweight='bold')
ax[0].set_ylim(-10,250)
ax[0].set_ylabel('Nro. de Personas',fontsize=13)
ax[0].set_xlabel('Comuna',fontsize=13)
ax[0].set_xticks(ax[0].get_xticks())
ax[0].set_xticklabels(hue_order,fontsize=11)
ax[0].tick_params('y',labelsize=11)

# ax[1]: Casos en periodo utilizado 2021-2023
date_1 = pd.to_datetime('01-01-2022',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2023',format='%d-%m-%Y')
sns.boxplot(data=data[date_1:date_2],y='T59',ax=ax[1],zorder=1,
            showfliers=False,linewidth=2,color='tab:pink',showmeans=True,
            meanprops=meanprops)
# sns.violinplot(data=data,y='T59',ax=ax[1],color='darkorange',linewidth=3,
#               fill=False,inner='quart',inner_kws=dict(color="k",linewidth=1.5))
sns.stripplot(data=data[date_1:date_2],y='T59',ax=ax[1],zorder=2,
              color='tab:pink',edgecolor='auto', size=6, linewidth=1)
ax[1].grid(zorder=0,alpha=0.7)
ax[1].set_title('Eventos [2022-2023]', fontweight='bold')
ax[1].set_xticks(ax[1].get_xticks())
ax[1].set_xticklabels(['Total'],fontsize=11)

# ax[2]: Casos en periodo total 2018-2024
sns.boxplot(data=data,y='T59',ax=ax[2],zorder=1,showfliers=False,
            linewidth=2,color='tab:brown',showmeans=True,meanprops=meanprops)
# sns.violinplot(data=data,y='T59',ax=ax[2],color='darkorange',linewidth=3,
#               fill=False,inner='quart',inner_kws=dict(color="k",linewidth=1.5))
sns.stripplot(data=data,y='T59',ax=ax[2],zorder=2,color='tab:brown',
             edgecolor='auto', size=6, linewidth=1)
ax[2].grid(zorder=0,alpha=0.7)
ax[2].set_title('Eventos [2018-2024]', fontweight='bold')
ax[2].set_xticks(ax[2].get_xticks())
ax[2].set_xticklabels(['Total'],fontsize=11)

# fig
# fig.suptitle('Boxplots Rotulo T59 entre 2021-2024',fontsize=14)
fig.tight_layout()
path = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/Resultados/Sección 2/'
# fig.savefig(path+'BoxplotsT59.png', dpi=300)

#%% Total

date_1 = pd.to_datetime('01-01-2018',format='%d-%m-%Y')
date_2 = pd.to_datetime('31-12-2024',format='%d-%m-%Y')
data = T59_raw[date_1:date_2]
fig, ax = plt.subplots(figsize=(7,7))

meanprops={"marker":"D", "markerfacecolor":"white","zorder":3,
           "markeredgecolor":"black","markersize":"8"}

# ax
sns.boxplot(data=data,y='T59',ax=ax,zorder=1,showfliers=False,linewidth=2,
            color='darkorange',showmeans=True,meanprops=meanprops)
sns.stripplot(data=data,y='T59',ax=ax,zorder=2,color='darkorange',
             edgecolor="gray", size=6, linewidth=1)
ax.grid(zorder=0,alpha=0.5)
ax.set_xticklabels(['Total'])

# fig
fig.suptitle('Boxplots Rotulo T59 entre 2018-2024',fontsize=14)
fig.tight_layout()

#%% Guardamos datos de T59 con serie completa
T59_full.index.names = ['date']
T59_full.to_csv(path+'serie_t59full.csv')