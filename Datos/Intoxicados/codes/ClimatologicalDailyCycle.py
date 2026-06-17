# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 12:46:04 2025

@author: felip
"""

import pandas as pd
import numpy as np

def build_cdc(df, col='value', window_days=30):
    """
    Estimate a smoothed seasonal daily cycle using a ±window_days around each day-of-year,
    averaged over all years, and grouped by hour of day.

    Parameters:
        df (pd.DataFrame): Must have a datetime index and a column `col`
        col (str): Column to detrend
        window_days (int): Number of days in each direction for the moving window

    Returns:
        pd.Series: Estimated seasonal daily cycle (same index as df)
    """

    df = df.copy()
    df['doy'] = df.index.dayofyear
    df['hour'] = df.index.hour
    df['year'] = df.index.year

    # Handle leap years: treat day 366 as 365
    df.loc[df['doy'] == 366, 'doy'] = 365

    # Create empty array for smoothed seasonal cycle
    seasonal = np.zeros(len(df))

    # Loop over all time points
    for i, (doy_i, hour_i) in enumerate(zip(df['doy'], df['hour'])):
        # Define window of DOYs
        window = list(range(doy_i - window_days, doy_i + window_days + 1))
        window = [(d + 365) % 365 if d <= 0 else (d if d <= 365 else d - 365) for d in window]

        # Mask for matching window DOYs and same hour
        mask = df['doy'].isin(window) & (df['hour'] == hour_i)

        # Take the median (or mean) over all years within the window
        seasonal[i] = df.loc[mask, col].mean()  # or use .median() if noisy

    return pd.Series(seasonal, index=df.index)



def build_cdc_vect(df, col='value', window_days=30, year_agg='mean', smooth_stat='mean'):
    """
    Vectorized, multi-year, moving-window daily cycle.

    Steps:
      1) Aggregate across YEARS at identical (DOY, hour): mean/median/etc.
      2) Smooth along DOY with a circular rolling window of width = 2*window_days+1.
      3) Map back to the original index, returning the expected climatological value.

    Parameters
    ----------
    df : pd.DataFrame
        DatetimeIndex required. Must contain column `col`.
        Works for hourly, 3-hourly, 6-hourly, etc. (uses .index.hour)
    col : str
        Name of the series column.
    window_days : int
        Half-window in days for circular smoothing (±window_days).
        Use 0 to disable smoothing.
    year_agg : {'mean','median'}
        How to aggregate across years at the same (DOY, hour).
    smooth_stat : {'mean','median'}
        Statistic for the rolling smoothing along DOY.

    Returns
    -------
    pd.Series
        Seasonal climatology with same index as df.
    """
    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found in df")

    x = df[[col]].copy()
    # Keep original index for final alignment
    out_index = x.index

    # Helper keys
    x['doy'] = x.index.dayofyear
    x['hour'] = x.index.hour
    # Map leap day to 365 so it participates with late-Feb data
    x.loc[x['doy'] == 366, 'doy'] = 365

    # 1) Aggregate across years at identical (doy, hour)
    # Drop NaNs in the series so they don't bias the climatology
    g = x.dropna(subset=[col]).groupby(['doy', 'hour'])[col]
    if year_agg == 'median':
        clim = g.median().unstack('hour')
    else:
        clim = g.mean().unstack('hour')

    # Ensure we have a full DOY index 1..365 (hours become columns)
    clim = clim.reindex(range(1, 366))

    # 2) Circular rolling smoothing along DOY (per hour independently)
    w = int(window_days)
    if w > 0:
        # Wrap top/bottom to mimic circular year
        ext = pd.concat([clim.iloc[-w:], clim, clim.iloc[:w]], axis=0)
        if smooth_stat == 'median':
            smoothed = ext.rolling(window=2*w+1, center=True, min_periods=1).median()
        else:
            smoothed = ext.rolling(window=2*w+1, center=True, min_periods=1).mean()
        clim_sm = smoothed.iloc[w:-w]
    else:
        clim_sm = clim

    # 3) Map back to original timestamps (doy, hour) → value
    lookup = clim_sm.stack().rename('seasonal').reset_index()  # columns: ['doy','hour','seasonal']
    # Merge with the (doy, hour) of each row, preserving order
    seasonal = (
        x[['doy', 'hour']]
        .merge(lookup, on=['doy', 'hour'], how='left')
        .set_index(out_index)['seasonal']
    )

    return seasonal
