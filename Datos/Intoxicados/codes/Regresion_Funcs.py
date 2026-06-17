# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 16:57:04 2025

@author: felip
"""

import pandas as pd
import numpy as np

# computar anomalia para data diaría
def anomalia_d(DF):
    df = DF.copy()
    DF_dA = pd.DataFrame(index=df.index)
    DF_dCA = pd.DataFrame(index=df.index)
    df = df.asfreq('D')
    for var in df.columns:
        if var in ['T59','Comuna']:
            continue
        
        series = df[var]

        # Skip if all NaN
        if series.isna().all():
            continue
        
        # If the series starts with NaNs, find the first valid index
        first_valid = series.first_valid_index()
        series = series.loc[first_valid:]  # cut off leading NaNs
        
        # Now fill possible gaps inside (but not at the start)
        series = series.interpolate()

        y = series.values
        N = len(y)

        # FFT
        fft_vals = np.fft.fft(y)
        freqs = np.fft.fftfreq(N, d=1)  # 1 day step

        # Target frequencies
        annual_freq = 1 / 365
        semiannual_freq = 2 / 365

        pos_freqs = freqs[:N//2]
        annual_idx = np.argmin(np.abs(pos_freqs - annual_freq))
        semiannual_idx = np.argmin(np.abs(pos_freqs - semiannual_freq))

        # Filter
        fft_filtered = np.zeros_like(fft_vals)
        fft_filtered[0] = fft_vals[0]
        fft_filtered[annual_idx] = fft_vals[annual_idx]
        fft_filtered[-annual_idx] = fft_vals[-annual_idx]
        fft_filtered[semiannual_idx] = fft_vals[semiannual_idx]
        fft_filtered[-semiannual_idx] = fft_vals[-semiannual_idx]


        seasonal_cycle = np.fft.ifft(fft_filtered).real
        anomaly_filtered = y - seasonal_cycle

        # Write result back into DF_da at correct location
        DF_dCA.loc[series.index, var] = seasonal_cycle
        DF_dA.loc[series.index, var] = anomaly_filtered
        
    return DF_dA, DF_dCA
