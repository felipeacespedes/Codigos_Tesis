# -*- coding: utf-8 -*-
"""
Execution script for wind comparison plots.
Generates seasonal (Summer vs Winter) and monthly (January vs June) comparison plots.

@author: felip
"""

# import os
import pandas as pd
import sys

# Add the codes directory to path to import the functions
sys.path.insert(0, 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/codes')

from wind_comparison_daily_cycle.wind_comparison_functs import (
    plot_seasonal_comparison,
    plot_monthly_comparison
)

#%% Load data

path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
DF_h = pd.read_csv(path + 'DF_h.csv', index_col='date', parse_dates=True)

# Define wind dataframes
WD = DF_h[['wd_VE', 'wd_princ', 'wd40_princ', 'wd_dmc', 'wd_CQ', 'wd_quint', 'wd_CC']]
WS = DF_h[['ws_VE', 'ws_princ', 'ws40_princ', 'ws_dmc', 'ws_CQ', 'ws_quint', 'ws_CC']]

WD = WD.rename(columns={
    'wd_VE': 'Ventanas',
    'wd_princ': 'Principal',
    'wd40_princ': 'Principal 40m',
    'wd_dmc': 'DMC',
    'wd_CQ': 'Centro_Quintero',
    'wd_quint': 'Quintero',
    'wd_CC': 'Concón',
})

WS = WS.rename(columns={
    'ws_VE': 'Ventanas',
    'ws_princ': 'Principal',
    'ws40_princ': 'Principal 40m',
    'ws_dmc': 'DMC',
    'ws_CQ': 'Centro_Quintero',
    'ws_quint': 'Quintero',
    'ws_CC': 'Concón'
})

# %%
# OR use the old data format if preferred
# path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
# WD = pd.read_csv(path + 'WD_df.csv', index_col='date', parse_dates=True,
#                    usecols=['date', 'Ventanas', 'Centro_Quintero',
#                             'Concón', 'Colmo'])
# WS = pd.read_csv(path + 'WS_df.csv', index_col='date', parse_dates=True,
#                    usecols=['date', 'Ventanas', 'Centro_Quintero',
#                             'Concón', 'Colmo'])

# # Limit to 2019-2023
# d1 = pd.to_datetime('2019-01-01 00:00:00')
# d2 = pd.to_datetime('2023-12-31 23:00:00')
# WD = WD.loc[d1:d2]
# WS = WS.loc[d1:d2]

# %%
# Define stations to plot
# stations = ['Ventanas', 'Centro_Quintero', 'Concón']
stations = ['Ventanas','Principal','Principal 40m','DMC','Centro_Quintero','Quintero','Concón']


# %%
# Create seasonal comparison plots (Summer vs Winter)
seasonal_save_dir = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/wind_comparison_daily_cycle/season_comparison'
print("Generating seasonal comparison plots (Summer vs Winter)...")
plot_seasonal_comparison(WD, WS, stations=stations, save_dir=seasonal_save_dir, show=False)

# %%
# Create monthly comparison plots (January vs June)
monthly_save_dir = 'C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/wind_comparison_daily_cycle/month_comparison'
print("Generating monthly comparison plots (January vs June)...")
plot_monthly_comparison(WD, WS, stations=stations, save_dir=monthly_save_dir, show=False)

print("\nDone! All comparison plots have been generated.")
print(f"Seasonal plots saved to: {seasonal_save_dir}")
print(f"Monthly plots saved to: {monthly_save_dir}")
