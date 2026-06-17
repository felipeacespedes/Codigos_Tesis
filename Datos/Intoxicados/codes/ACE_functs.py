# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 09:04:25 2025

@author: felip
"""

import numpy as np
import pandas as pd


def compute_wd_from_uv(u, v, ws):
    """Convierte u,v a dirección de viento (grados) con tu convención."""
    with np.errstate(invalid='ignore', divide='ignore'):
        wd = (np.rad2deg(np.arctan2(-1*(u/ws), -1*(v/ws))) / 360.0)
    return wd

def get_72h_window(DFh, date_center, var):
    """Extrae 72h (día n-1, n, n+1) para una variable var."""
    start = (pd.to_datetime(date_center).normalize() - pd.Timedelta(days=1))
    end   = start + pd.Timedelta(hours=72-1)
    rng = pd.date_range(start, end, freq="h")
    
    if var == "blh_era5":
        ser = DFh.loc[rng, "blh_era5"].reindex(rng)
        # Interpolación temporal; limit_direction='both' para rellenar bordes dentro de la ventana
        ser = ser.interpolate(method="time", limit_direction="both")
        return ser.values
    else:
        return DFh.loc[rng, var].reindex(rng).values

def aggregate_72h(DFh, dates, var):
    """Devuelve estadísticos (media, mediana, p25, p75) para matriz n_días x 72h."""
    mats = []
    for d in dates:
        if d in [pd.to_datetime('2022-01-01 00:00:00'),pd.to_datetime('2023-12-31 00:00:00')]:
            continue
        vals = get_72h_window(DFh, d, var)
        if len(vals) == 72:
            mats.append(vals)
    if not mats:
        return None
    A = np.array(mats)
    return dict(
        mean=np.nanmean(A, axis=0),
        median=np.nanmedian(A, axis=0),
        p25=np.nanpercentile(A, 25, axis=0),
        p75=np.nanpercentile(A, 75, axis=0),
        )
def aggregate_72h_p95(DFh, dates, var):
    """Devuelve estadísticos (media, mediana, p25, p75,p95) para matriz n_días x 72h."""
    mats = []
    for d in dates:
        if d in [pd.to_datetime('2022-01-01 00:00:00'),pd.to_datetime('2023-12-31 00:00:00')]:
            continue
        vals = get_72h_window(DFh, d, var)
        if len(vals) == 72:
            mats.append(vals)
    if not mats:
        return None
    A = np.array(mats)
    return dict(
        mean=np.nanmean(A, axis=0),
        median=np.nanmedian(A, axis=0),
        p25=np.nanpercentile(A, 25, axis=0),
        p75=np.nanpercentile(A, 75, axis=0),
        p95=np.nanpercentile(A, 95, axis=0)
        )

def get_24h_window(DFh, date_center, var):
    """Extrae 24h del día n para la variable var."""
    day = pd.to_datetime(date_center).normalize()
    rng = pd.date_range(day, day + pd.Timedelta(hours=23), freq="h")
    
    if var == "blh_era5":
        ser = DFh.loc[rng, "blh_era5"].reindex(rng)
        ser = ser.interpolate(method="time", limit_direction="both")
        return ser.values
    else:
        return DFh.loc[rng, var].reindex(rng).values

def aggregate_24h(DFh, dates, var):
    """Devuelve media, mediana, p25 y p75 para matriz n_días x 24h."""
    mats = []
    for d in dates:
        vals = get_24h_window(DFh, d, var)
        if len(vals) == 24:
            mats.append(vals)
    if not mats:
        return None
    A = np.array(mats)
    return dict(
        mean=np.nanmean(A, axis=0),
        median=np.nanmedian(A, axis=0),
        p25=np.nanpercentile(A, 25, axis=0),
        p75=np.nanpercentile(A, 75, axis=0),
        )