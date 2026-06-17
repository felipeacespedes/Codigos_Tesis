# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 11:18:23 2025

@author: felip
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import seaborn as sns

# Define a fixed color palette for consistent station colors
COLOR_MAP = sns.color_palette("Set2", 4)  # Adjust if you have more columns

def min_max_scale(series):
    return (series - series.min()) / (series.max() - series.min())

def plot_cycle(df, freq, normalize=False, shared_y=False):
    
    # Definimos variables en base a freq
    if freq == 'ME':
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
        if freq == 'ME':
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
    if freq:
        series = series.resample(freq).mean() # AQUI SE CAMBIA MEDIA O MEDIANA!!!

    grouped = series.groupby(group_by)
    mean = grouped.mean()
    median = grouped.median()
    q10 = grouped.quantile(0.10)
    q25 = grouped.quantile(0.25)
    q75 = grouped.quantile(0.75)
    q90 = grouped.quantile(0.90)

    if normalize:
        mean = min_max_scale(mean)
        median = min_max_scale(median)
        q10 = min_max_scale(q10)
        q25 = min_max_scale(q25)
        q75 = min_max_scale(q75)
        q90 = min_max_scale(q90)

    return mean, median, q10, q25, q75, q90

def plot_all_cycles(df, normalize=False, shared_y=False):
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

    fig, axs = plt.subplots(len(stations), 3, figsize=(12, 10), sharey=shared_y,sharex='col')
    if len(stations) == 1:
        axs = [axs]  # Wrap in list if only one station

    for row, col in enumerate(stations):
        color = COLOR_MAP[row % len(COLOR_MAP)]

        for col_idx in range(3):
            ax = axs[row][col_idx]
            mean, median, q10, q25, q75, q90 = get_cycle_data(
                df[col], freqs[col_idx], group_by_fns[col_idx], normalize
            )

            x = median.index
            ax.fill_between(x, q10.values, q90.values, color=color, alpha=0.2)
            ax.fill_between(x, q25.values, q75.values, color=color, alpha=0.3)
            ax.plot(x, median.values, marker=None,ls=':',lw=2.5, color=color)
            ax.plot(x, mean.values, marker='o',lw=0,ms=5, color=color,alpha=0.7)

            if row == 0:
                ax.set_title(f"Ciclo {cycles[col_idx]}", fontsize=15, weight='bold')
            if row == len(stations) - 1:
                ax.set_xlabel(xlabels[col_idx], fontsize=14)
            if col_idx == 0:
                ax.set_ylabel(f"{stations[row]}", rotation=90,
                              labelpad=10, fontsize=15, weight='bold')

            # Custom legend per subplot
            if col_idx == 2 and row == 0:
                legend_elements = [
                    Line2D([0], [0], color=color, marker='o',lw=0,ms=5, label='Media',alpha=0.7),
                    Line2D([0], [0], color=color,marker=None,ls=':',lw=2.5, label='Mediana'),
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
                ax.set_xticks(range(0, 7))
                ax.set_xticklabels(['L', 'M', 'M', 'J', 'V', 'S','D'])
            elif col_idx == 2:
                ax.set_xticks(range(1, 13))
                # ax.set_xticklabels(['E', 'F', 'M', 'A', 'M', 'J','J',
                #                     'A','S','O','N','D'])
                
            ax.tick_params(axis='both',labelsize=13)
            ax.tick_params(axis='x',labelrotation=10)


    # title = "Ciclos por estación" + (" (Normalized)" if normalize else "")\
    #         + (" (y-compartido)" if shared_y else " (y-libre)")
    # fig.suptitle(title, fontsize=18)
    plt.tight_layout()
    # plt.subplots_adjust(top=0.93)
    plt.show()
