# -*- coding: utf-8 -*-
"""
Wind comparison plotting functions for seasonal and monthly comparisons.
Created for comparing wind cycles between summer vs winter and January vs June.

@author: felip
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


def get_cycle_data(grouped):
    """Extract statistical measures from grouped data."""
    mean = grouped.mean()
    median = grouped.median()
    q10 = grouped.quantile(0.10)
    q25 = grouped.quantile(0.25)
    q75 = grouped.quantile(0.75)
    q90 = grouped.quantile(0.90)
    return mean, median, q10, q25, q75, q90


def get_cycle_uv(wd, ws, group_by, uv):
    """Calculate U or V component from wind direction and speed."""
    radians = np.deg2rad(wd)
    if uv == 'u':
        series = np.sin(radians) * -1 * ws
    elif uv == 'v':
        series = np.cos(radians) * -1 * ws
    else:
        raise ValueError("uv must be 'u' or 'v'")
    
    grouped = series.groupby(group_by)
    mean = grouped.mean()
    median = grouped.median()
    q10 = grouped.quantile(0.10)
    q25 = grouped.quantile(0.25)
    q75 = grouped.quantile(0.75)
    q90 = grouped.quantile(0.90)
    
    return mean, median, q10, q25, q75, q90


def vector_mean_deg(series):
    """Compute the mean wind direction in radians from a pandas Series."""
    radians = np.deg2rad(series.dropna())
    u = np.sin(radians)
    v = np.cos(radians)
    
    u_mean = u.mean()
    v_mean = v.mean()
    
    mean_rad = np.arctan2(u_mean, v_mean)
    return mean_rad % (2 * np.pi)


def plot_comparison_2x2(station, wd1, ws1, wd2, ws2, label1, label2, 
                        color1='tab:blue', color2='tab:orange', save_path=None, show=False):
    """
    Create a 2x2 comparison plot for wind parameters (WD, WS, U, V).
    
    Parameters:
    - station: station name (string)
    - wd1, ws1: DataFrame slices for period 1 (e.g., winter)
    - wd2, ws2: DataFrame slices for period 2 (e.g., summer)
    - label1: label for period 1 (e.g., "Invierno")
    - label2: label for period 2 (e.g., "Verano")
    - color1: color for period 1 (default: tab:blue)
    - color2: color for period 2 (default: tab:orange)
    - save_path: path to save the figure
    - show: whether to display the plot
    """
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    
    group_key1 = wd1.index.hour
    group_key2 = wd2.index.hour
    x_vals = np.arange(0, 24)
    
    # Plot 1: Wind Direction (hours vs degrees)
    ax_wd = axs[0, 0]
    wd_grouped1 = wd1.groupby(group_key1)
    wd_grouped2 = wd2.groupby(group_key2)
    
    mean_dir1 = wd_grouped1.apply(vector_mean_deg)
    mean_dir2 = wd_grouped2.apply(vector_mean_deg)
    
    # Convert back to degrees for plotting
    mean_deg1 = np.rad2deg(mean_dir1.values) % 360
    mean_deg2 = np.rad2deg(mean_dir2.values) % 360
    
    ax_wd.plot(mean_dir1.index, mean_deg1, marker='o', lw=2, ms=6,
               color=color1, label=f'{label1} - Media', alpha=0.8)
    ax_wd.plot(mean_dir2.index, mean_deg2, marker='s', lw=2, ms=6,
               color=color2, label=f'{label2} - Media', alpha=0.8)
    
    # Add median
    wd_median1 = wd_grouped1.median()
    wd_median2 = wd_grouped2.median()
    
    ax_wd.plot(wd_median1.index, wd_median1.values, marker='o', lw=1.5, ls='--',
               color=color1, alpha=0.5, ms=4)
    ax_wd.plot(wd_median2.index, wd_median2.values, marker='s', lw=1.5, ls='--',
               color=color2, alpha=0.5, ms=4)
    
    ax_wd.set_xlabel('Hora', fontsize=12)
    ax_wd.set_ylabel('Dirección del Viento (°)', fontsize=12)
    ax_wd.set_title('Dirección del Viento', fontsize=13, weight='bold')
    ax_wd.set_xticks(x_vals[::6])
    ax_wd.set_ylim(0, 360)
    ax_wd.grid(True, alpha=0.6)
    
    # Plot 2: Wind Speed (with statistics)
    ax_ws = axs[0, 1]
    ws_grouped1 = ws1.groupby(group_key1)
    ws_grouped2 = ws2.groupby(group_key2)
    
    mean_ws1, median_ws1, q10_ws1, q25_ws1, q75_ws1, q90_ws1 = get_cycle_data(ws_grouped1)
    mean_ws2, median_ws2, q10_ws2, q25_ws2, q75_ws2, q90_ws2 = get_cycle_data(ws_grouped2)
    
    index1 = mean_ws1.index
    index2 = mean_ws2.index
    
    # Period 1
    ax_ws.plot(index1, mean_ws1.values, marker='o', lw=2, ms=6,
               color=color1, label=f'{label1} - Media', alpha=0.8)
    ax_ws.plot(index1, median_ws1.values, marker='o', lw=1.5, ls='--',
               color=color1, alpha=0.5, ms=4)
    ax_ws.fill_between(index1, q25_ws1.values, q75_ws1.values, color=color1, alpha=0.2)
    
    # Period 2
    ax_ws.plot(index2, mean_ws2.values, marker='s', lw=2, ms=6,
               color=color2, label=f'{label2} - Media', alpha=0.8)
    ax_ws.plot(index2, median_ws2.values, marker='s', lw=1.5, ls='--',
               color=color2, alpha=0.5, ms=4)
    ax_ws.fill_between(index2, q25_ws2.values, q75_ws2.values, color=color2, alpha=0.2)
    
    ax_ws.set_xlabel('Hora', fontsize=12)
    ax_ws.set_ylabel('Velocidad del Viento (m/s)', fontsize=12)
    ax_ws.set_title('Velocidad del Viento', fontsize=13, weight='bold')
    ax_ws.set_xticks(x_vals[::6])
    ax_ws.set_ylim(0, 6)
    ax_ws.grid(True, alpha=0.6)
    
    # Create comprehensive legend for all subplots
    legend_elements = [
        Line2D([0], [0], marker='o', lw=2, ms=6, color=color1, label=f'{label1} - Media', alpha=0.8),
        Line2D([0], [0], marker='o', lw=1.5, ls='--', color=color1, ms=4, label=f'{label1} - Mediana', alpha=0.5),
        Line2D([0], [0], marker='s', lw=2, ms=6, color=color2, label=f'{label2} - Media', alpha=0.8),
        Line2D([0], [0], marker='s', lw=1.5, ls='--', color=color2, ms=4, label=f'{label2} - Mediana', alpha=0.5),
    ]
    ax_ws.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Plot 3: U component
    ax_u = axs[1, 0]
    mean_u1, median_u1, q10_u1, q25_u1, q75_u1, q90_u1 = get_cycle_uv(wd1, ws1, group_key1, 'u')
    mean_u2, median_u2, q10_u2, q25_u2, q75_u2, q90_u2 = get_cycle_uv(wd2, ws2, group_key2, 'u')
    
    # Period 1
    ax_u.plot(mean_u1.index, mean_u1.values, marker='o', lw=2, ms=6,
              color=color1, label=f'{label1} - Media', alpha=0.8)
    ax_u.plot(mean_u1.index, median_u1.values, marker='o', lw=1.5, ls='--',
              color=color1, alpha=0.5, ms=4)
    ax_u.fill_between(mean_u1.index, q25_u1.values, q75_u1.values, color=color1, alpha=0.2)
    
    # Period 2
    ax_u.plot(mean_u2.index, mean_u2.values, marker='s', lw=2, ms=6,
              color=color2, label=f'{label2} - Media', alpha=0.8)
    ax_u.plot(mean_u2.index, median_u2.values, marker='s', lw=1.5, ls='--',
              color=color2, alpha=0.5, ms=4)
    ax_u.fill_between(mean_u2.index, q25_u2.values, q75_u2.values, color=color2, alpha=0.2)
    
    ax_u.axhline(0, color='grey', ls='--', alpha=0.5)
    ax_u.set_xlabel('Hora', fontsize=12)
    ax_u.set_ylabel('Componente U (m/s)', fontsize=12)
    ax_u.set_title('Componente U', fontsize=13, weight='bold')
    ax_u.set_xticks(x_vals[::6])
    ax_u.set_ylim(-4.5, 4.5)
    ax_u.grid(True, alpha=0.6)
    
    # Plot 4: V component
    ax_v = axs[1, 1]
    mean_v1, median_v1, q10_v1, q25_v1, q75_v1, q90_v1 = get_cycle_uv(wd1, ws1, group_key1, 'v')
    mean_v2, median_v2, q10_v2, q25_v2, q75_v2, q90_v2 = get_cycle_uv(wd2, ws2, group_key2, 'v')
    
    # Period 1
    ax_v.plot(mean_v1.index, mean_v1.values, marker='o', lw=2, ms=6,
              color=color1, label=f'{label1} - Media', alpha=0.8)
    ax_v.plot(mean_v1.index, median_v1.values, marker='o', lw=1.5, ls='--',
              color=color1, alpha=0.5, ms=4)
    ax_v.fill_between(mean_v1.index, q25_v1.values, q75_v1.values, color=color1, alpha=0.2)
    
    # Period 2
    ax_v.plot(mean_v2.index, mean_v2.values, marker='s', lw=2, ms=6,
              color=color2, label=f'{label2} - Media', alpha=0.8)
    ax_v.plot(mean_v2.index, median_v2.values, marker='s', lw=1.5, ls='--',
              color=color2, alpha=0.5, ms=4)
    ax_v.fill_between(mean_v2.index, q25_v2.values, q75_v2.values, color=color2, alpha=0.2)
    
    ax_v.axhline(0, color='grey', ls='--', alpha=0.5)
    ax_v.set_xlabel('Hora', fontsize=12)
    ax_v.set_ylabel('Componente V (m/s)', fontsize=12)
    ax_v.set_title('Componente V', fontsize=13, weight='bold')
    ax_v.set_xticks(x_vals[::6])
    ax_v.set_ylim(-4.5, 4.5)
    ax_v.grid(True, alpha=0.6)
    
    # Main title
    fig.suptitle(f'Ciclo Diario de Viento - Estación: {station}', 
                 fontsize=16, weight='bold', y=1.05)
    
    if save_path:
        save_path = os.path.expanduser(save_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=200, bbox_inches='tight')
        print(f"Saved comparison plot to {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close(fig)


def plot_seasonal_comparison(df_wd, df_ws, stations, save_dir=None, show=False):
    """
    Create seasonal comparison plots (Summer vs Winter) for specified stations.
    
    Parameters:
    - df_wd: DataFrame of wind direction in degrees
    - df_ws: DataFrame of wind speed in m/s
    - stations: list of station names to plot
    - save_dir: directory to save the figures
    - show: whether to display plots
    """
    
    if save_dir is None:
        save_dir = os.getcwd()
    
    save_dir = os.path.expanduser(save_dir)
    os.makedirs(save_dir, exist_ok=True)
    
    # Winter: June, July, August (months 6, 7, 8)
    winter_mask = df_wd.index.month.isin([6, 7, 8])
    
    # Summer: December, January, February (months 12, 1, 2)
    summer_mask = df_wd.index.month.isin([12, 1, 2])
    
    for station in stations:
        if station not in df_wd.columns or station not in df_ws.columns:
            print(f"Station {station} not found in DataFrames; skipping.")
            continue
        
        wd_winter = df_wd.loc[winter_mask, station]
        ws_winter = df_ws.loc[winter_mask, station]
        
        wd_summer = df_wd.loc[summer_mask, station]
        ws_summer = df_ws.loc[summer_mask, station]
        
        if wd_winter.empty or ws_winter.empty or wd_summer.empty or ws_summer.empty:
            print(f"Insufficient data for {station}; skipping.")
            continue
        
        file_name = f"comparison_season_{station.replace(' ', '_')}.png"
        save_path = os.path.join(save_dir, file_name)
        
        plot_comparison_2x2(
            station=station,
            wd1=wd_winter, ws1=ws_winter,
            wd2=wd_summer, ws2=ws_summer,
            label1='Invierno (JJA)',
            label2='Verano (DEF)',
            color1='tab:blue',
            color2='tab:orange',
            save_path=save_path,
            show=show
        )


def plot_monthly_comparison(df_wd, df_ws, stations, save_dir=None, show=False):
    """
    Create monthly comparison plots (January vs June) for specified stations.
    
    Parameters:
    - df_wd: DataFrame of wind direction in degrees
    - df_ws: DataFrame of wind speed in m/s
    - stations: list of station names to plot
    - save_dir: directory to save the figures
    - show: whether to display plots
    """
    
    if save_dir is None:
        save_dir = os.getcwd()
    
    save_dir = os.path.expanduser(save_dir)
    os.makedirs(save_dir, exist_ok=True)
    
    # January: month 1
    january_mask = df_wd.index.month == 1
    
    # June: month 6
    june_mask = df_wd.index.month == 6
    
    for station in stations:
        if station not in df_wd.columns or station not in df_ws.columns:
            print(f"Station {station} not found in DataFrames; skipping.")
            continue
        
        wd_january = df_wd.loc[january_mask, station]
        ws_january = df_ws.loc[january_mask, station]
        
        wd_june = df_wd.loc[june_mask, station]
        ws_june = df_ws.loc[june_mask, station]
        
        if wd_january.empty or ws_january.empty or wd_june.empty or ws_june.empty:
            print(f"Insufficient data for {station}; skipping.")
            continue
        
        file_name = f"comparison_month_{station.replace(' ', '_')}.png"
        save_path = os.path.join(save_dir, file_name)
        
        plot_comparison_2x2(
            station=station,
            wd1=wd_june, ws1=ws_june,
            wd2=wd_january, ws2=ws_january,
            label1='Junio',
            label2='Enero',
            color1='tab:blue',
            color2='tab:orange',
            save_path=save_path,
            show=show
        )
