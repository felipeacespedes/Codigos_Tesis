# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:15:24 2024

@author: felip

Codigo para procesar los archivos diarios del SODAR y juntarlos en un solo
archivo .csv
"""

# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%

dia = '220904'

# '220825' '220904' '221006'

# Load data
df = pd.read_table('RawSodar/'+dia+'.txt',skiprows=10,na_values='*')

# Assuming `time` column is in datetime format
df['time'] = pd.to_datetime(df['time'])

# Define the full range for `time`, starting from 00:15 to exclude 00:00 of the current day
start_time = df['time'].min().replace(hour=0, minute=15)
end_time = start_time + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)
full_time_range = pd.date_range(start=start_time, end=end_time, freq='15T')

# Define the full range for `z`
z_levels = np.arange(30, 1010, 10)  # 30 to 1000 meters in steps of 10

# Create a complete grid of time and z
full_index = pd.MultiIndex.from_product([full_time_range, z_levels], names=['time', 'z'])
full_df = pd.DataFrame(index=full_index).reset_index()

# Merge with your original dataframe
merged_df = pd.merge(full_df, df, on=['time', 'z'], how='left')

# Save or work with `merged_df` as needed
print(merged_df.head())