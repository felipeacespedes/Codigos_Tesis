# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 17:34:23 2025

@author: felip
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def vector_mean_deg(series):
    """Computes the mean wind direction in degrees from a pandas Series."""
    radians = np.deg2rad(series.dropna())
    u = np.sin(radians)
    v = np.cos(radians)

    u_mean = u.mean()
    v_mean = v.mean()

    mean_rad = np.arctan2(u_mean, v_mean)
    mean_deg = np.rad2deg(mean_rad) % 360  # Wrap to 0–360°
    return mean_deg

def plot_wind_cycles(df, shared_y=False):
    stations = df.columns
    cycles = ['Diario', 'Anual']
    group_by_fns = [
        lambda x: x.hour,   # Daily
        lambda x: x.month   # Yearly
    ]
    xlabels = ['Hora', 'Mes']

    COLOR_MAP = sns.color_palette("Set2", len(stations))

    fig, axs = plt.subplots(len(stations), 2, figsize=(10, 10), sharey=shared_y)

    for row, station in enumerate(stations):
        color = COLOR_MAP[row % len(COLOR_MAP)]

        for col in range(2):  # daily & yearly
            ax = axs[row][col] if len(stations) > 1 else axs[col]
            group = df[station].groupby(group_by_fns[col](df.index))
            mean_angles = group.apply(vector_mean_deg)

            x = mean_angles.index
            y = mean_angles.values

            ax.plot(x, y, marker='o', color=color)
                
                
            if row == 0:
                ax.set_title(f"Ciclo {cycles[col]}", fontsize=15, weight='bold')
            if row == len(stations) - 1:
                ax.set_xlabel(xlabels[col])
            if col == 0:
                ax.set_ylabel(f"{stations[row]}", rotation=90,
                              labelpad=10, fontsize=15, weight='bold')

            if col == 0:
                ax.set_xticks(range(0, 24)[::2])
            else:
                ax.set_xticks(range(1, 13))

            ax.set_ylim(0, 360)
            ax.grid(True)


    plt.tight_layout()
    plt.show()

def plot_polar_wind_cycles(df, cycle='daily'):
    """
    Plot wind direction over a daily or yearly cycle using polar plots.
    cycle: 'daily' (by hour) or 'yearly' (by month)
    """
    import matplotlib.pyplot as plt
    import numpy as np

    group_by = df.index.hour if cycle == 'daily' else df.index.month
    cycle_label = 'Hour' if cycle == 'daily' else 'Month'
    theta_labels = range(0, 360, 45)

    stations = df.columns
    n_stations = len(stations)

    fig, axs = plt.subplots(1, n_stations, subplot_kw={'projection': 'polar'}, figsize=(5 * n_stations, 5))

    if n_stations == 1:
        axs = [axs]

    for i, station in enumerate(stations):
        ax = axs[i]
        color = sns.color_palette("Set2")[i % 8]

        group = df[station].groupby(group_by)
        mean_wind = group.apply(vector_mean_deg)

        # Angle in radians
        theta = np.deg2rad(mean_wind.values)
        # Radius = time (hour or month)
        r = mean_wind.index

        # Normalize radius if needed for aesthetics
        r = np.array(r)

        ax.plot(theta, r, marker='o', color=color, label=station)
        ax.set_theta_zero_location('N')  # 0° at top
        ax.set_theta_direction(-1)       # Clockwise
        ax.set_title(station, fontsize=14)
        ax.set_xticks(np.deg2rad(theta_labels))
        ax.set_xticklabels([f"{d}°" for d in theta_labels])
        ax.set_rlabel_position(225)
        ax.grid(True)

    fig.suptitle(f"Wind Direction Polar Plot ({cycle.capitalize()} Cycle)", fontsize=16)
    plt.tight_layout()
    plt.show()



def plot_wind_direction_and_speed(df_wd, df_ws, cycle='daily'):
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

    if cycle == 'daily':
        group_key = df_wd.index.hour
        x_vals = np.arange(0, 24)
        xi_d = 6
        xi_s = 6
        xi = 0
        x_label = "Hora"
        title = "Ciclo Diario"
    elif cycle == 'yearly':
        group_key = df_wd.index.month
        x_vals = np.arange(1, 13)
        xi_d = 3
        xi_s = 3
        xi = -10
        x_label = "Mes"
        title = "Ciclo Anual"
    else:
        raise ValueError("Cycle must be 'daily' or 'yearly'")

    # Create empty grid
    fig, axs = plt.subplots(2, n_stations, figsize=(3 * n_stations, 6), 
                            constrained_layout=True, sharey=True)

    # Replace first row with polar subplots
    for i in range(n_stations):
        fig.delaxes(axs[0, i])
        axs[0, i] = fig.add_subplot(2, n_stations, i + 1, projection='polar')

    for i, station in enumerate(stations):
        color = colors[i]


        # Wind direction (polar)
        wd_grouped = df_wd[station].groupby(group_key)
        mean_dir = wd_grouped.apply(vector_mean_deg)
        theta = np.deg2rad(mean_dir.values)
        r = mean_dir.index

        ax_dir = axs[0, i]
        ax_dir.plot(theta, r, marker='o', color=color)
        ax_dir.set_title(f"{station}", fontsize=15, weight='bold')
        ax_dir.set_theta_zero_location("N")
        ax_dir.set_theta_direction(-1)
        ax_dir.set_yticks(x_vals[xi::xi_d])
        ax_dir.set_xticks(np.deg2rad(np.arange(0, 360, 45)))
        ax_dir.set_xticklabels([f"{d}°" for d in np.arange(0, 360, 45)])
        ax_dir.set_rlabel_position(30)

        # Wind speed (line plot)
        ws_grouped = df_ws[station].groupby(group_key)
        mean_speed = ws_grouped.mean()

        ax_ws = axs[1, i]
        ax_ws.plot(mean_speed.index, mean_speed.values, marker='o', color=color)
        ax_ws.set_xlabel(x_label)
        # ax_ws.set_ylabel("[m/s]") if station == 'Ventanas' else None
        ax_ws.set_xticks(x_vals[xi::xi_s])
        ax_ws.grid(True)

    # fig.suptitle(f"{title}", fontsize=15, weight='bold')
    fig.supylabel(" Velocidad                      "+
                  "Dirección", fontsize=15, weight='bold')

    plt.show()

