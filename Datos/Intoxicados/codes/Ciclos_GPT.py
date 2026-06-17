# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 11:18:23 2025

@author: felip
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.gridspec import GridSpec
import seaborn as sns

# Define a fixed color palette for consistent station colors
COLOR_MAP = sns.color_palette("Set2", 4)  # Adjust if you have more columns

def min_max_scale(series):
    return (series - series.min()) / (series.max() - series.min())

def plot_cycle(df, freq, normalize=False, shared_y=False):
    
    # Definimos variables en base a freq
    if freq == 'M':
        group_by = lambda x: x.month
        title_prefix = "Anual"
    elif freq == 'D':
        group_by = lambda x: x.weekday()
        title_prefix = "Semanal"
    else:
        group_by = lambda x: x.hour
        title_prefix = "Diario"
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 10), sharey=shared_y)
    axs = axs.flatten()

    for i, col in enumerate(df.columns):
        # Resample if needed
        if freq:
            data = df[col].resample(freq).median()
        else:
            data = df[col]

        # Get group index
        index = data.groupby(group_by).median().index

        # Median and IQR
        grouped = data.groupby(group_by)
        median = grouped.median()
        # Percentiles
        q10 = grouped.quantile(0.10)
        q25 = grouped.quantile(0.25)
        q75 = grouped.quantile(0.75)
        q90 = grouped.quantile(0.90)
        
        if normalize:
            median = min_max_scale(median)
            q10 = min_max_scale(q10)
            q25 = min_max_scale(q25)
            q75 = min_max_scale(q75)
            q90 = min_max_scale(q90)

        # Plot
        ax = axs[i]
        color = COLOR_MAP[i % len(COLOR_MAP)]
        
        # 10–90 percentile band (lightest)
        ax.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
        
        # 25–75 percentile band (darker)
        ax.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
        
        # Median line
        ax.plot(index, median.values, marker='o', color=color, label='Mediana')
        # Legend
        legend_elements = [
            Line2D([0], [0], color=color, marker='o', label='Mediana'),
            Patch(facecolor=color, alpha=0.3, label='pctl. 25–75'),
            Patch(facecolor=color, alpha=0.15, label='pctl. 10–90')
        ]
        ax.legend(handles=legend_elements, loc='upper right', frameon=True)
        ax.set_title(col)
        ax.grid(True)

        # Set x-ticks
        if freq == 'M':
            ax.set_xticks(range(1, 13))
            ax.set_xlabel('Mes')
        elif freq == 'D':
            ax.set_xticks(range(0, 7))
            ax.set_xticklabels(['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'])
            ax.set_xlabel('Día')
        else:
            ax.set_xticks(range(0, 24))
            ax.set_xlabel('Hora')

        ax.set_ylabel('ppm')

    title = f"Ciclo {title_prefix}" + (" (Normalizado)" if normalize else "")\
            + (" (y-compartido)" if shared_y else " (y-libre)")
    fig.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()


def get_cycle_data(series, freq, group_by, normalize=False):
     
    # Resample if needed
    # if freq:
    #     series = series.resample(freq).median()

    grouped = series.groupby(group_by)
    median = grouped.median()
    q10 = grouped.quantile(0.10)
    q25 = grouped.quantile(0.25)
    q75 = grouped.quantile(0.75)
    q90 = grouped.quantile(0.90)

    if normalize:
        median = min_max_scale(median)
        q10 = min_max_scale(q10)
        q25 = min_max_scale(q25)
        q75 = min_max_scale(q75)
        q90 = min_max_scale(q90)

    return median, q10, q25, q75, q90

def get_mean(series, freq, group_by, normalize=False):
     
    # Resample if needed
    # if freq:
    #     series = series.resample(freq).mean()

    grouped = series.groupby(group_by)
    mean = grouped.mean()

    return mean

def plot_all_cycles(df, name='', normalize=False, shared_y=False):
    stations = df.columns
    cycles = ['Diario', 'Semanal', 'Anual']
    group_by_fns = [
        lambda x: x.hour,         # Daily
        lambda x: x.weekday(),    # Weekly
        lambda x: x.month         # Yearly
    ]
    freqs = [
        None,     # Hourly
        'D',      # Daily
        'ME'       # Monthly
    ]
    xlabels = ['Hora', 'Día', 'Mes']
    n = len(stations)
    fig, axs = plt.subplots(n, 3, figsize=(12, n*2.5), sharey=shared_y,sharex='col')
    if len(stations) == 1:
        axs = [axs]  # Wrap in list if only one station

    for row, col in enumerate(stations):
        print(row,col)
        color = COLOR_MAP[row % len(COLOR_MAP)]

        for col_idx in range(3):
            ax = axs[row][col_idx]
            median, q10, q25, q75, q90 = get_cycle_data(
                df[col], freqs[col_idx], group_by_fns[col_idx], normalize)
            mean = get_mean(df[col], freqs[col_idx], group_by_fns[col_idx],
                            normalize)

            x = median.index
            # if col_idx!=1:
            ax.fill_between(x, q10.values, q90.values, color=color, alpha=0.2)
            ax.fill_between(x, q25.values, q75.values, color=color, alpha=0.3)
            ax.plot(x, median.values, marker=None,ls=':',lw=2, color=color)
            ax.plot(x, mean.values, marker='o',lw=0,ms=5, color=color,alpha=0.7)

            if row == 0:
                ax.set_title(f"Ciclo {cycles[col_idx]}", fontsize=15, weight='bold')
            if row == len(stations) - 1:
                ax.set_xlabel(xlabels[col_idx],fontsize=14)
            if col_idx == 0:
                ax.set_ylabel(f"{stations[row]}", rotation=90,
                              labelpad=10, fontsize=15, weight='bold')

            # Custom legend per subplot
            if col_idx == 2 and row==0:
                legend_elements = [
                    Line2D([0], [0], color=color, marker='o',lw=0,ms=5, label='Media',alpha=0.7),
                    Line2D([0], [0], color=color,marker=None,ls=':',lw=2, label='Mediana'),
                    Patch(facecolor=color, alpha=0.3, label='pctl. 25–75'),
                    Patch(facecolor=color, alpha=0.2, label='pctl. 10–90')
                ]
                ax.legend(handles=legend_elements, loc='upper right', 
                          framealpha=0.6,handlelength=1.2)

            ax.grid(True, alpha=0.6)
                
            # Ticks formatting
            if col_idx == 0:
                ax.set_xticks(range(0, 24)[::3])
            elif col_idx == 1:
                ax.set_xticks(range(0, 7))
                ax.set_xticklabels(['L', 'M', 'M', 'J', 'V', 'S','D'])
            elif col_idx == 2:
                ax.set_xticks(range(1, 13))
                # ax.set_xticklabels(['E', 'F', 'M', 'A', 'M', 'J','J',
                #                     'A','S','O','N','D'])
                
            ax.tick_params(axis='both',labelsize=13)
            ax.tick_params(axis='x',labelrotation=10)


    fig.tight_layout()
    path = 'C:/Users/felip/Desktop/'
    if name in ['VE','CQ','CC']:
        fig.savefig(path+'ciclos_cont_'+name+'.png',dpi=300)
    else:
        fig.savefig(path+'ciclos_cont_'+name+'.png',dpi=300)
    # plt.show()
    
def plot_DA_cycles(df, normalize=False, shared_y=False):
    stations = df.columns
    cycles = ['Diario', 'Anual']
    group_by_fns = [
        lambda x: x.hour,         # Daily
        lambda x: x.month         # Yearly
    ]
    freqs = [
        None,     # Hourly
        'ME'       # Monthly
    ]
    xlabels = ['Hora', 'Mes']
    n = len(stations)
    fig, axs = plt.subplots(n, 2, figsize=(12, n*2.2), sharey=shared_y, sharex='col')
    if len(stations) == 1:
        axs = [axs]  # Wrap in list if only one station

    for row, col in enumerate(stations):
        print(row,col)
        color = COLOR_MAP[row % len(COLOR_MAP)]

        for col_idx in range(2):
            ax = axs[row][col_idx]
            median, q10, q25, q75, q90 = get_cycle_data(
                df[col], freqs[col_idx], group_by_fns[col_idx], normalize)
            mean = get_mean(df[col], freqs[col_idx], group_by_fns[col_idx],
                            normalize)

            x = median.index
            ax.fill_between(x, q10.values, q90.values, color=color, alpha=0.2)
            ax.fill_between(x, q25.values, q75.values, color=color, alpha=0.3)
            ax.plot(x, median.values, marker=None,ls=':',lw=2, color=color)
            if stations[row][-4:-1] == 'era' and col_idx==0:
                era_h = [2,8,14,20];era_mean=[]
                for i in range(24):
                    if i in era_h:
                        era_mean.append(mean.values[i])
                    else: 
                        era_mean.append(float('nan'))

                ax.plot(x, era_mean, marker='o',lw=0,ms=7, color=color,alpha=0.7)
            else:
                ax.plot(x, mean.values, marker='o',lw=0,ms=5, color=color,alpha=0.7)


            if row == 0:
                ax.set_title(f"Ciclo {cycles[col_idx]}", fontsize=15, weight='bold')
            if row == len(stations) - 1:
                ax.set_xlabel(xlabels[col_idx], fontsize=14)
            if col_idx == 0:
                ax.set_ylabel(f"{stations[row]}", rotation=90,
                              labelpad=10, fontsize=15, weight='bold')

            # Custom legend per subplot
            if col_idx == 1 and row==0:
                legend_elements = [
                    Line2D([0], [0], color=color, marker='o',lw=0,ms=5, label='Media',alpha=0.7),
                    Line2D([0], [0], color=color,marker=None,ls=':',lw=2, label='Mediana'),
                    Patch(facecolor=color, alpha=0.3, label='pctl. 25–75'),
                    Patch(facecolor=color, alpha=0.2, label='pctl. 10–90')
                ]
                ax.legend(handles=legend_elements, loc='upper right', 
                          framealpha=0.6,handlelength=1.2)

            ax.grid(True,alpha=0.6)

            # Ticks formatting
            if col_idx == 0:
                ax.set_xticks(range(0, 24)[::3])
            elif col_idx == 1:
                ax.set_xticks(range(1, 13))
                
            # p_era5
            # if stations[row] == 'p_era5' and col_idx==0:
            #     ax.set_ylim(1008,1012)
            
            ax.tick_params(axis='both',labelsize=13)
            ax.tick_params(axis='x',labelrotation=10)

    plt.tight_layout()
    plt.show()
    
    
    


####################################################
######### Seasonal Daily Cycle con Heatmap #########
####################################################

# definimos funciones alternativas para estadisticos (agg_func)
def iqr(x):
    return np.nanpercentile(x, 75) - np.nanpercentile(x, 25)
def perc(x,p):
    return np.nanpercentile(x, p)


# Seasonal Daily Cycle
def plot_seasonal_daily_cycle(
    df, 
    variables, 
    right_labels,
    cbar_groups, 
    agg_func='mean', 
    grid_shape=(1, 4),
    station_names=None,
    unit_labels=None,
    figsize=(16, 6)
):
    """
    Genera un gráfico de matriz de mapas de calor (heatmaps) mensuales-horarios con barras de color alineadas dinámicamente.
    """
    
    # 1. Pre-procesamiento de datos
    def get_pivot(col_name):
        temp = df[[col_name]].copy()
        temp['Mes'] = temp.index.month
        temp['Hora'] = temp.index.hour
        # Agregamos los datos
        pivot = temp.groupby(['Hora', 'Mes'])[col_name].apply(agg_func).unstack()
        return pivot

    # 2. Determinar límites de escala (vmin, vmax) por Grupo
    group_limits = {}
    unique_groups = sorted(list(set(cbar_groups)))
    pivot_cache = {} 
    
    for grp in unique_groups:
        var_indices = [i for i, x in enumerate(cbar_groups) if x == grp]
        group_vals = []
        for idx in var_indices:
            var_name = variables[idx]
            p = get_pivot(var_name)
            pivot_cache[var_name] = p
            group_vals.append(p.values)
            
        all_data = np.concatenate([v.flatten() for v in group_vals])
        all_data = all_data[~np.isnan(all_data)]
        if len(all_data) > 0:
            group_limits[grp] = (np.min(all_data), np.max(all_data))
        else:
            group_limits[grp] = (0, 1)

    # 3. Graficado
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(grid_shape[0], grid_shape[1], figure=fig)
    month_labels = ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    
    mappables = {}      # Para guardar la info de color de cada grupo
    axes_created = []   # NUEVO: Guardamos los ejes creados para leer su posición luego

    for idx, var_name in enumerate(variables):
        row = idx // grid_shape[1]
        col = idx % grid_shape[1]
        
        if row >= grid_shape[0]: 
            break 
            
        ax = fig.add_subplot(gs[row, col])
        axes_created.append(ax) # Guardamos el eje
        
        group_id = cbar_groups[idx]
        vmin, vmax = group_limits[group_id]
        
        # cmap_list = ['viridis', 'plasma', 'cividis', 'inferno']
        # cmap = cmap_list[group_id % len(cmap_list)]
        cmap = 'viridis'
        
        hm = sns.heatmap(
            pivot_cache[var_name], 
            ax=ax, 
            cmap=cmap, 
            vmin=vmin, 
            vmax=vmax,
            cbar=False,
            xticklabels=month_labels,
            yticklabels=2
        )
        
        if group_id not in mappables:
            mappables[group_id] = hm.get_children()[0]

        ax.invert_yaxis()
        
        if station_names and idx < len(station_names):
            ax.set_title(station_names[idx], fontsize=12, fontweight='bold')
            
        if col == 0:
            ax.set_ylabel("Hora (Local)", fontsize=10)
        else:
            ax.set_ylabel("")
            ax.set_yticklabels([]) 
            
        ax.set_xlabel("")
        
        # Etiqueta lateral derecha (modificación solicitada)
        if col == grid_shape[1] - 1:
            # Usamos row como índice para right_labels
            if row < len(right_labels):
                ax.text(1.05, 0.5, right_labels[row], transform=ax.transAxes, 
                        rotation=-90, va='center', fontsize=12, fontweight='bold')

    # 4. Añadir Barras de Color (Colorbars) ALINEADAS
    # Ajustamos el layout dejando espacio abajo (bottom=0.15)
    plt.tight_layout(rect=[0, 0.15, 1, 1]) 
    
    # Renderizamos el plot para calcular las posiciones exactas de los ejes
    fig.canvas.draw() 

    for i, grp_id in enumerate(unique_groups):
        # a. Identificar qué subplots pertenecen a este grupo
        idxs_in_group = [idx for idx, val in enumerate(cbar_groups) if val == grp_id]
        axes_in_group = [axes_created[idx] for idx in idxs_in_group]
        
        # b. Calcular la caja que engloba a esos subplots (el más a la izquierda y el más a la derecha)
        # Obtenemos la posición bbox de cada eje en coordenadas de la figura (0 a 1)
        bboxes = [ax.get_position() for ax in axes_in_group]
        
        x0 = min([box.x0 for box in bboxes]) # Borde izquierdo del primer plot del grupo
        x1 = max([box.x1 for box in bboxes]) # Borde derecho del último plot del grupo
        width = x1 - x0
        
        # c. Crear el eje para la colorbar justo debajo de ese ancho
        # [left, bottom, width, height]
        cbar_ax = fig.add_axes([x0, 0.08, width, 0.03]) 
        
        cbar = fig.colorbar(mappables[grp_id], cax=cbar_ax, orientation='horizontal')
        
        label_text = f"Grupo {grp_id}"
        if unit_labels and i < len(unit_labels):
            label_text = unit_labels[i]
            
        cbar.set_label(label_text, fontsize=10)

    return fig



    
