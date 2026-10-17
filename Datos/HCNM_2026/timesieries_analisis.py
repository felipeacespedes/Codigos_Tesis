#%% Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Import data
data_dir = r"C:/Users/felip/Desktop/U/Tesis/Datos/HCNM_2026"

HCNM = pd.read_csv(data_dir + "/HCNM_2026_hourly_all_stations.csv", 
                   index_col=0, parse_dates=True)

#%% Explore data Centro Quintero
d1 = pd.to_datetime('2025-10-14 00:00:00')
d2 = pd.to_datetime('2025-10-18 23:00:00')
HCNM.loc[d1:d2,'Centro Quintero'].plot(ylim=(0, 20), title='HCNM Centro Quintero', 
                                       ylabel='HCNM (ppm)', xlabel='Date', 
                                       figsize=(12, 6),grid=True)


# %% Explore data Ventanas
d1 = pd.to_datetime('2023-12-18 00:00:00')
d2 = pd.to_datetime('2023-12-18 23:00:00')
HCNM.loc[d1:d2,'Ventanas'].plot(ylim=(0, 20), title='HCNM Ventanas', 
                                       ylabel='HCNM (ppm)', xlabel='Date', 
                                       figsize=(12, 6),grid=True)



# %%
