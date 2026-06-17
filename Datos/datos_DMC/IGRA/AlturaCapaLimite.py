# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 18:21:44 2025

@author: felip
"""
# Librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Importamos archivo

filepath = 'C:/Users/felip/Desktop/U/Tesis/Datos/datos_DMC/IGRA/CIM00085586-drvd.txt'
records = []

with open(filepath, 'r') as file:
    for line in file:
        if line.startswith('#'):
            # Extract datetime fields (columns 14–26 → indexes 13 to 26)
            try:
                year  = int(line[13:17])
                month = int(line[18:20])
                day   = int(line[21:23])
                hour  = int(line[24:26])
                dt = pd.Timestamp(year, month, day, hour)
            except Exception:
                continue  # Skip malformed headers

            # Extract MIXHGT (columns 68–73 → indexes 67 to 73)
            try:
                mixhgt_str = line[67:73].strip()
                mixhgt = float(mixhgt_str) if mixhgt_str != '-99999' else np.nan
            except Exception:
                mixhgt = np.nan

            records.append({'datetime': dt, 'MIXHGT': mixhgt})

# Build DataFrame
MH = pd.DataFrame(records)
MH.set_index('datetime', inplace=True)
# MH = MH.resample('12H').mean()

# Importamos datos de estación principal para ver cómo se compara con inversión
# Principal
# path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/Principal/'
# Princ = pd.read_csv(path+'Principal.csv',index_col='date',parse_dates=True,
#                     usecols=['date','t_inv'])
# Princ = Princ.resample('D').mean()

# Importamos datos de altura de capa límita por ERA5 en [-71.55,-32.83]
path = 'C:/Users/felip/Desktop/U/Tesis/Datos/ERA5/'
BLH = pd.read_csv(path+'BLH_ERA5.csv',index_col='date',parse_dates=True)
# BLH = BLH.resample('12H').mean()

# Juntamos
d1 = pd.to_datetime('2018-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
df = pd.concat([MH,BLH], axis=1)
df = df.resample('12H').mean()
df = df.loc[d1:d2]

#%% Ploteamos MIXHGT de IGRA y BLH de ERA5

d1 = pd.to_datetime('2023-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-30 23:00:00')
plt.figure(figsize=(10,7))
df.loc[d1:d2,'MIXHGT'].plot(marker='.',lw=0)
df.loc[d1:d2,'BLH'].plot(zorder=1)
plt.ylabel('m')
plt.grid()
plt.tight_layout()

#%% Ploteamos MIXHGT
d1 = pd.to_datetime('2023-05-01 00:00:00')
d2 = pd.to_datetime('2023-06-30 23:00:00')
MH.loc[d1:d2].plot(grid=True, figsize=(20,7),title='MIXHGT',ylabel='m')
plt.tight_layout()

 #%% FFT para ciclo anual y semianual

ts = BLH['BLH'].copy()

# 1. Interpolate missing values (optional, for FFT)
ts_interp = ts.interpolate(method='time')

# 2. Ensure regular frequency (e.g., daily)
ts_interp = ts_interp.asfreq('6H')

# 3. Apply FFT
n = len(ts_interp)
fft_vals = np.fft.fft(ts_interp)
freqs = np.fft.fftfreq(n, d=0.25)  # 1 = 1 day spacing

# 4. Identify annual and semiannual frequencies
# Annual cycle → frequency = 1/365, Semiannual = 2/365
f_annual = 1/365
f_semiannual = 2/365

# Create a mask to keep only annual and semiannual frequencies
mask = np.zeros(n, dtype=bool)
tol = 1e-4  # Tolerance for matching frequencies
mask[np.abs(freqs - f_annual) < tol] = True
mask[np.abs(freqs + f_annual) < tol] = True
mask[np.abs(freqs - f_semiannual) < tol] = True
mask[np.abs(freqs + f_semiannual) < tol] = True

# 5. Build filtered signal
filtered_fft = np.zeros(n, dtype=complex)
filtered_fft[mask] = fft_vals[mask]
annual_signal = np.fft.ifft(filtered_fft).real

# 6. Subtract cycles to get anomaly
anomaly = ts_interp - annual_signal

# Add results to DataFrame
result = BLH.copy()
result['anomaly'] = anomaly
result['annual+semiannual'] = annual_signal+BLH['BLH'].mean()
result['anomaly'] = result['anomaly'].resample('D').mean()

#%% Ploteamos

d1 = pd.to_datetime('2023-01-01 00:00:00')
d2 = pd.to_datetime('2023-12-31 23:00:00')
fig,axs = plt.subplots(2,1,figsize=(20,13),sharex=True)

# axs[0]
result.loc[d1:d2,'BLH'].plot(ax=axs[0],marker='.',lw=0)
result.loc[d1:d2,'annual+semiannual'].plot(ax=axs[0],lw=5)
axs[0].grid()
axs[0].legend()
axs[0].set_ylabel('m')

# axs[1]
result.loc[d1:d2,'anomaly'].plot(ax=axs[1],color='m',marker='.',lw=0) 
axs[1].grid()  
axs[1].legend()
axs[1].set_ylabel('m')

# extra
fig.suptitle("Original BLH, Annual+Semiannual Cycles, and Anomaly")
fig.tight_layout()

#%% Calculamos menor 
d1 = pd.to_datetime('2018-01-01 00:00:00')
d2 = pd.to_datetime('2018-12-31 23:00:00')
mask = result.loc[d1:d2,'annual+semiannual'] == result.loc[d1:d2,'annual+semiannual'].min()
print(result.loc[d1:d2,'annual+semiannual'][mask])
