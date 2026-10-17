# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 16:16:08 2026

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
    
    mean = grouped.mean()
    median = grouped.median()
    q10 = grouped.quantile(0.10)
    q25 = grouped.quantile(0.25)
    q75 = grouped.quantile(0.75)
    q90 = grouped.quantile(0.90)


    return mean, median, q10, q25, q75, q90

def get_cycle_uv(wd,ws,group_by,uv):
    
    
    
    radians = np.deg2rad(wd)
    if uv=='u':
        series = np.sin(radians)*-1*ws
    elif uv=='v':
        series = np.cos(radians)*-1*ws
    else:
        print("uv debe ser 'u' o 'v'")
    
    # agrupamos serie
    grouped = series.groupby(group_by)
    #calculamos estadisticos
    mean = grouped.mean()
    median = grouped.median()
    q10 = grouped.quantile(0.10)
    q25 = grouped.quantile(0.25)
    q75 = grouped.quantile(0.75)
    q90 = grouped.quantile(0.90)

    return mean, median, q10, q25, q75, q90

def vector_mean_deg(series):
    """Computes the mean wind direction in degrees from a pandas Series."""
    radians = np.deg2rad(series.dropna())
    u = np.sin(radians)
    v = np.cos(radians)

    u_mean = u.mean()
    v_mean = v.mean()

    mean_rad = np.arctan2(u_mean, v_mean)
    # mean_deg = np.rad2deg(mean_rad) % 360  # Wrap to 0–360°
    return mean_rad % (2 * np.pi) #mean_deg

def vector_median_deg(series):
    """Computes the median wind direction in degrees from a pandas Series."""
    radians = np.deg2rad(series.dropna())
    u = np.sin(radians)
    v = np.cos(radians)

    u_median = u.median()
    v_median = v.median()

    median_rad = np.arctan2(u_median, v_median)
    # median_deg = np.rad2deg(median_rad) % 360  # Wrap to 0–360°
    return median_rad % (2 * np.pi) #median_deg

def vector_mean_u(series):
    """Computes the mean wind direction in degrees from a pandas Series."""
    radians = np.deg2rad(series.dropna())
    u = np.sin(radians)*-1
    u_mean = u.mean()
    return u_mean

def vector_mean_v(series):
    """Computes the mean wind direction in degrees from a pandas Series."""
    radians = np.deg2rad(series.dropna())
    v = np.cos(radians)*-1
    v_mean = v.mean()
    return v_mean


def plot_wd_ws_u_v(df_wd, df_ws, cycle='daily'):
    """
    Plot wind direction (polar) and wind speed (line) for multiple stations
    over daily or yearly cycle.
    
    Parameters:
    - df_wd: DataFrame of wind direction in degrees
    - df_ws: DataFrame of wind speed in m/s
    - cycle: 'daily' or 'yearly'
    """
    assert df_wd.columns.equals(df_ws.columns), "DataFrames must have same columns"
    stations = df_wd.columns
    n_stations = len(stations)
    colors = sns.color_palette("Set2", n_stations)
    
    #########################################
    ### Definig daily or yearly variables ###
    if cycle == 'daily':
        group_key = df_wd.index.hour
        x_vals = np.arange(0, 24)
        xt_vals = np.arange(1, 25)
        xi_d = 6
        xi_s = 6
        xi = 0
        x_label = "Hora"
        
    elif cycle == 'yearly':
        group_key = df_wd.index.month
        x_vals = np.arange(1, 13)
        xi_d = 3
        xi_s = 3
        xi = 2
        x_label = "Mes"
    else:
        raise ValueError("Cycle must be 'daily' or 'yearly'")

    ##########################################
    
    
    # Create empty grid
    # fig, axs = plt.subplots(4, n_stations, figsize=(2.5 * n_stations, 10), 
    #                         constrained_layout=True, sharex=True)
    fig, axs = plt.subplots(4, n_stations, figsize=(2.5 * n_stations, 8), 
                            constrained_layout=True, sharex=True, sharey='row',
                            gridspec_kw={'height_ratios': [0.9, 0.7, 0.7, 0.7]}) # <--- ADD THIS

    # Replace first row with polar subplots
    for i in range(n_stations):
        fig.delaxes(axs[0, i])
        axs[0, i] = fig.add_subplot(4, n_stations, i + 1, projection='polar')

    for i, station in enumerate(stations):
        color = colors[i]
        
        ##### Wind direction (polar) ###########
        wd_grouped = df_wd[station].groupby(group_key)
        
        # Calculate means
        mean_dir = wd_grouped.apply(vector_mean_deg)
        theta_md = mean_dir.values
        # Shift R values +1 for daily so it doesn't start at the dead center
        r_md = mean_dir.index + 1 if cycle == 'daily' else mean_dir.index

        ax_dir = axs[0, i]
        ax_dir.plot(theta_md, r_md, marker='o',lw=0,ms=5,
                    markerfacecolor=color,markeredgecolor='lightgrey',
                    markeredgewidth=0.5)

        ax_dir.set_title(f"{station}", fontsize=15, weight='bold', pad=10)
        ax_dir.set_theta_zero_location("N")
        ax_dir.set_theta_direction(-1)
        ax_dir.set_rorigin(-1)
        
        # Caso para 'daily' y 'yearly':
        if cycle == 'daily':
            # Place the physical grid circles at 1, 7, 13, 19
            ax_dir.set_yticks(xt_vals[xi::xi_d])
            # Override the text labels to read "0", "6", "12", "18"
            ax_dir.set_yticklabels([str(val) for val in x_vals[xi::xi_d]])
        else:    
            ax_dir.set_yticks(x_vals[xi::xi_d])
        
        ax_dir.set_xticks(np.deg2rad(np.arange(0, 360, 45)))
        ax_dir.set_xticklabels([])
        ax_dir.set_rlabel_position(30)
        ax_dir.grid(True,alpha=0.6)
        ###########################################
        ###########################################
        

        # Wind speed (line plot)
        ws_grouped = df_ws[station].groupby(group_key)
        mean, median, q10, q25, q75, q90 = get_cycle_data(ws_grouped)

        ax_ws = axs[1, i]
        index = mean.index
        ax_ws.plot(index, mean.values,marker='o',lw=0,color=color,ms=5,alpha=0.8)
        ax_ws.plot(index, median.values, marker=None,ls=':', color=color,lw=2.3)
        ax_ws.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
        ax_ws.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
        ax_ws.set_xticks(x_vals[xi::xi_s])
        ax_ws.set_ylim(0,4.5) if cycle=='yearly' else ax_ws.set_ylim(0,6)
        ax_ws.grid(True,alpha=0.6)
        
        # U (line plot)
        mean, median, q10, q25, q75, q90 = \
            get_cycle_uv(df_wd[station],df_ws[station],group_key,'u')
        
        ax_u = axs[2, i]
        index = mean.index
        ax_u.plot(index, mean.values, marker='o',lw=0,color=color,ms=5,alpha=0.8)
        ax_u.plot(index, median.values, marker=None,ls=':', color=color,lw=2.3)
        ax_u.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
        ax_u.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
        ax_u.axhline(0,color='grey',ls='--',alpha=0.5)
        ax_u.set_xticks(x_vals[xi::xi_s])
        ax_u.set_ylim(-3,3) if cycle=='yearly' else ax_u.set_ylim(-4.5,4.5)
        ax_u.grid(True,alpha=0.6)
        
        # V (line plot)
        mean, median, q10, q25, q75, q90 = \
            get_cycle_uv(df_wd[station],df_ws[station],group_key,'v')

        
        ax_v = axs[3, i]
        index = mean.index
        ax_v.plot(index, mean.values,marker='o',lw=0,color=color,ms=5,alpha=0.8)
        ax_v.plot(index, median.values, marker=None,ls=':',color=color,lw=2.3)
        ax_v.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
        ax_v.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
        ax_v.axhline(0,color='grey',ls='--',alpha=0.5)
        ax_v.set_xlabel(x_label,fontsize=14)
        ax_v.set_xticks(x_vals[xi::xi_s])
        ax_v.set_ylim(-3,3) if cycle=='yearly' else ax_v.set_ylim(-4.5,4.5)
        ax_v.grid(True,alpha=0.6)
        
        if i==n_stations-1:
            legend_elements = [
                Line2D([0], [0], marker='o',lw=0, color=color, label='Media',ms=5,alpha=0.8),
                Line2D([0], [0], color=color, marker=None,ls=':', label='Mediana',lw=2.3),
                Patch(facecolor=color, alpha=0.3, label='pctl. 25–75'),
                Patch(facecolor=color, alpha=0.15, label='pctl. 10–90')
            ]

            ax_v.legend(handles=legend_elements, loc='upper right', 
                      framealpha=0.4,handlelength=1.2)
        
        # Agrandamos ticks
        ax_dir.tick_params(axis='both',labelsize=10)
        ax_ws.tick_params(axis='both',labelsize=13)
        ax_u.tick_params(axis='both',labelsize=13)
        ax_v.tick_params(axis='both',labelsize=13)
        
    fig.supylabel("         "+
                  "V                      "+
                  "U              "+
                  "Intensidad            "+
                  "Dirección ",
                  fontsize=15, weight='bold',va='center')

    plt.show()


def plot_wd_ws_u_v_seasonal(df_wd, df_ws, save_dir=None, show=False):
    """
    Plot daily seasonal wind cycles with U/V decomposition and save figures for each season.

    Parameters:
    - df_wd: DataFrame of wind direction in degrees
    - df_ws: DataFrame of wind speed in m/s
    - save_dir: directory to save the seasonal plots
    - show: whether to display each plot
    """
    assert df_wd.columns.equals(df_ws.columns), "DataFrames must have same columns"

    if save_dir is None:
        save_dir = os.getcwd()

    save_dir = os.path.expanduser(save_dir)
    os.makedirs(save_dir, exist_ok=True)

    seasons = {
        'verano': {'months': [12, 1, 2], 'code': 'DEF','n': 1},
        'otono': {'months': [3, 4, 5], 'code': 'MAM','n': 2},
        'invierno': {'months': [6, 7, 8], 'code': 'JJA','n': 3},
        'primavera': {'months': [9, 10, 11], 'code': 'SON','n': 4},
    }

    for season_name, season_info in seasons.items():
        months = season_info['months']
        season_code = season_info['code']
        season_index = season_info['n']

        season_mask = df_wd.index.month.isin(months)
        wd_season = df_wd.loc[season_mask]
        ws_season = df_ws.loc[season_mask]

        if wd_season.empty or ws_season.empty:
            print(f"No data available for {season_name}; skipping.")
            continue

        assert wd_season.columns.equals(ws_season.columns), "DataFrames must have same columns"
        stations = wd_season.columns
        n_stations = len(stations)
        colors = sns.color_palette("Set2", n_stations)

        group_key = wd_season.index.hour
        x_vals = np.arange(0, 24)
        xt_vals = np.arange(1, 25)
        xi_d = 6
        xi_s = 6
        xi = 0
        x_label = "Hora"

        fig, axs = plt.subplots(4, n_stations, figsize=(2.5 * n_stations, 8), 
                                constrained_layout=True, sharex=True, sharey='row',
                                gridspec_kw={'height_ratios': [0.9, 0.7, 0.7, 0.7]})

        for i in range(n_stations):
            fig.delaxes(axs[0, i])
            axs[0, i] = fig.add_subplot(4, n_stations, i + 1, projection='polar')

        for i, station in enumerate(stations):
            color = colors[i]
            wd_grouped = wd_season[station].groupby(group_key)
            mean_dir = wd_grouped.apply(vector_mean_deg)
            theta_md = mean_dir.values
            r_md = mean_dir.index + 1

            ax_dir = axs[0, i]
            ax_dir.plot(theta_md, r_md, marker='o', lw=0, ms=5,
                        markerfacecolor=color, markeredgecolor='lightgrey',
                        markeredgewidth=0.5)

            ax_dir.set_title(f"{station}", fontsize=15, weight='bold', pad=10)
            ax_dir.set_theta_zero_location("N")
            ax_dir.set_theta_direction(-1)
            ax_dir.set_rorigin(-1)
            ax_dir.set_yticks(xt_vals[xi::xi_d])
            ax_dir.set_yticklabels([str(val) for val in x_vals[xi::xi_d]])
            ax_dir.set_xticks(np.deg2rad(np.arange(0, 360, 45)))
            ax_dir.set_xticklabels([])
            ax_dir.set_rlabel_position(30)
            ax_dir.grid(True, alpha=0.6)

            ws_grouped = ws_season[station].groupby(group_key)
            mean, median, q10, q25, q75, q90 = get_cycle_data(ws_grouped)

            ax_ws = axs[1, i]
            index = mean.index
            ax_ws.plot(index, mean.values, marker='o', lw=0, color=color, ms=5, alpha=0.8)
            ax_ws.plot(index, median.values, marker=None, ls=':', color=color, lw=2.3)
            ax_ws.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
            ax_ws.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
            ax_ws.set_xticks(x_vals[xi::xi_s])
            ax_ws.set_ylim(0, 6)
            ax_ws.grid(True, alpha=0.6)

            mean, median, q10, q25, q75, q90 = get_cycle_uv(wd_season[station], ws_season[station], group_key, 'u')
            ax_u = axs[2, i]
            index = mean.index
            ax_u.plot(index, mean.values, marker='o', lw=0, color=color, ms=5, alpha=0.8)
            ax_u.plot(index, median.values, marker=None, ls=':', color=color, lw=2.3)
            ax_u.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
            ax_u.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
            ax_u.axhline(0, color='grey', ls='--', alpha=0.5)
            ax_u.set_xticks(x_vals[xi::xi_s])
            ax_u.set_ylim(-4.5, 4.5)
            ax_u.grid(True, alpha=0.6)

            mean, median, q10, q25, q75, q90 = get_cycle_uv(wd_season[station], ws_season[station], group_key, 'v')
            ax_v = axs[3, i]
            index = mean.index
            ax_v.plot(index, mean.values, marker='o', lw=0, color=color, ms=5, alpha=0.8)
            ax_v.plot(index, median.values, marker=None, ls=':', color=color, lw=2.3)
            ax_v.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
            ax_v.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
            ax_v.axhline(0, color='grey', ls='--', alpha=0.5)
            ax_v.set_xlabel(x_label, fontsize=14)
            ax_v.set_xticks(x_vals[xi::xi_s])
            ax_v.set_ylim(-4.5, 4.5)
            ax_v.grid(True, alpha=0.6)

            if i == n_stations - 1:
                legend_elements = [
                    Line2D([0], [0], marker='o', lw=0, color=color, label='Media', ms=5, alpha=0.8),
                    Line2D([0], [0], color=color, marker=None, ls=':', label='Mediana', lw=2.3),
                    Patch(facecolor=color, alpha=0.3, label='pctl. 25–75'),
                    Patch(facecolor=color, alpha=0.15, label='pctl. 10–90')
                ]

                ax_v.legend(handles=legend_elements, loc='upper right', 
                            framealpha=0.4, handlelength=1.2)

            ax_dir.tick_params(axis='both', labelsize=10)
            ax_ws.tick_params(axis='both', labelsize=13)
            ax_u.tick_params(axis='both', labelsize=13)
            ax_v.tick_params(axis='both', labelsize=13)

        fig.text(
            0.02,
            0.99,
            season_code,
            transform=fig.transFigure,
            fontsize=10,
            fontweight='normal',
            ha='left',
            va='top',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1)
        )

        fig.supylabel("        " +
                      "V                     " +
                      "U               " +
                      "Velocidad             " +
                      "Dirección ",
                      fontsize=15, weight='bold', va='center')

        file_name = f"daily_wind_u_v_{season_index}.png"
        save_path = os.path.join(save_dir, file_name)
        fig.savefig(save_path, dpi=200, bbox_inches='tight')
        print(f"Saved seasonal wind plot to {save_path}")

        if show:
            plt.show()
        else:
            plt.close(fig)


def plot_wd_ws_u_v_monthly(df_wd, df_ws, save_dir=None, show=False):
    """
    Plot daily wind cycles per month with U/V decomposition and save figures for each month.

    Parameters:
    - df_wd: DataFrame of wind direction in degrees
    - df_ws: DataFrame of wind speed in m/s
    - save_dir: directory to save the monthly plots
    - show: whether to display each plot
    """
    assert df_wd.columns.equals(df_ws.columns), "DataFrames must have same columns"

    if save_dir is None:
        save_dir = os.getcwd()

    save_dir = os.path.expanduser(save_dir)
    os.makedirs(save_dir, exist_ok=True)

    months = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    for month_number in range(1, 13):
        month_name = months[month_number]
        month_mask = df_wd.index.month == month_number
        wd_month = df_wd.loc[month_mask]
        ws_month = df_ws.loc[month_mask]

        if wd_month.empty or ws_month.empty:
            print(f"No data available for {month_name}; skipping.")
            continue

        assert wd_month.columns.equals(ws_month.columns), "DataFrames must have same columns"
        stations = wd_month.columns
        n_stations = len(stations)
        colors = sns.color_palette("Set2", n_stations)

        group_key = wd_month.index.hour
        x_vals = np.arange(0, 24)
        xt_vals = np.arange(1, 25)
        xi_d = 6
        xi_s = 6
        xi = 0
        x_label = "Hora"

        fig, axs = plt.subplots(4, n_stations, figsize=(2.5 * n_stations, 8), 
                                constrained_layout=True, sharex=True, sharey='row',
                                gridspec_kw={'height_ratios': [0.9, 0.7, 0.7, 0.7]})

        for i in range(n_stations):
            fig.delaxes(axs[0, i])
            axs[0, i] = fig.add_subplot(4, n_stations, i + 1, projection='polar')

        for i, station in enumerate(stations):
            color = colors[i]
            wd_grouped = wd_month[station].groupby(group_key)
            mean_dir = wd_grouped.apply(vector_mean_deg)
            theta_md = mean_dir.values
            r_md = mean_dir.index + 1

            ax_dir = axs[0, i]
            ax_dir.plot(theta_md, r_md, marker='o', lw=0, ms=5,
                        markerfacecolor=color, markeredgecolor='lightgrey',
                        markeredgewidth=0.5)

            ax_dir.set_title(f"{station}", fontsize=15, weight='bold', pad=10)
            ax_dir.set_theta_zero_location("N")
            ax_dir.set_theta_direction(-1)
            ax_dir.set_rorigin(-1)
            ax_dir.set_yticks(xt_vals[xi::xi_d])
            ax_dir.set_yticklabels([str(val) for val in x_vals[xi::xi_d]])
            ax_dir.set_xticks(np.deg2rad(np.arange(0, 360, 45)))
            ax_dir.set_xticklabels([])
            ax_dir.set_rlabel_position(30)
            ax_dir.grid(True, alpha=0.6)

            ws_grouped = ws_month[station].groupby(group_key)
            mean, median, q10, q25, q75, q90 = get_cycle_data(ws_grouped)

            ax_ws = axs[1, i]
            index = mean.index
            ax_ws.plot(index, mean.values, marker='o', lw=0, color=color, ms=5, alpha=0.8)
            ax_ws.plot(index, median.values, marker=None, ls=':', color=color, lw=2.3)
            ax_ws.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
            ax_ws.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
            ax_ws.set_xticks(x_vals[xi::xi_s])
            ax_ws.set_ylim(0, 6)
            ax_ws.grid(True, alpha=0.6)

            mean, median, q10, q25, q75, q90 = get_cycle_uv(wd_month[station], ws_month[station], group_key, 'u')
            ax_u = axs[2, i]
            index = mean.index
            ax_u.plot(index, mean.values, marker='o', lw=0, color=color, ms=5, alpha=0.8)
            ax_u.plot(index, median.values, marker=None, ls=':', color=color, lw=2.3)
            ax_u.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
            ax_u.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
            ax_u.axhline(0, color='grey', ls='--', alpha=0.5)
            ax_u.set_xticks(x_vals[xi::xi_s])
            ax_u.set_ylim(-4.5, 4.5)
            ax_u.grid(True, alpha=0.6)

            mean, median, q10, q25, q75, q90 = get_cycle_uv(wd_month[station], ws_month[station], group_key, 'v')
            ax_v = axs[3, i]
            index = mean.index
            ax_v.plot(index, mean.values, marker='o', lw=0, color=color, ms=5, alpha=0.8)
            ax_v.plot(index, median.values, marker=None, ls=':', color=color, lw=2.3)
            ax_v.fill_between(index, q10.values, q90.values, color=color, alpha=0.15)
            ax_v.fill_between(index, q25.values, q75.values, color=color, alpha=0.3)
            ax_v.axhline(0, color='grey', ls='--', alpha=0.5)
            ax_v.set_xlabel(x_label, fontsize=14)
            ax_v.set_xticks(x_vals[xi::xi_s])
            ax_v.set_ylim(-4.5, 4.5)
            ax_v.grid(True, alpha=0.6)

            if i == n_stations - 1:
                legend_elements = [
                    Line2D([0], [0], marker='o', lw=0, color=color, label='Media', ms=5, alpha=0.8),
                    Line2D([0], [0], color=color, marker=None, ls=':', label='Mediana', lw=2.3),
                    Patch(facecolor=color, alpha=0.3, label='pctl. 25–75'),
                    Patch(facecolor=color, alpha=0.15, label='pctl. 10–90')
                ]

                ax_v.legend(handles=legend_elements, loc='upper right', 
                            framealpha=0.4, handlelength=1.2)

            ax_dir.tick_params(axis='both', labelsize=10)
            ax_ws.tick_params(axis='both', labelsize=13)
            ax_u.tick_params(axis='both', labelsize=13)
            ax_v.tick_params(axis='both', labelsize=13)

        fig.text(
            0.02,
            0.99,
            month_name,
            transform=fig.transFigure,
            fontsize=10,
            fontweight='normal',
            ha='left',
            va='top',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1)
        )

        fig.supylabel("        " +
                      "V                     " +
                      "U               " +
                      "Velocidad             " +
                      "Dirección ",
                      fontsize=15, weight='bold', va='center')

        file_name = f"daily_wind_u_v_{month_number:02d}.png"
        save_path = os.path.join(save_dir, file_name)
        fig.savefig(save_path, dpi=200, bbox_inches='tight')
        print(f"Saved monthly wind plot to {save_path}")

        if show:
            plt.show()
        else:
            plt.close(fig)
