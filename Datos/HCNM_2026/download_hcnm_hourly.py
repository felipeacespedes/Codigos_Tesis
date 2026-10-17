from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pandas as pd
import requests

BASE_DIR = Path(r"C:\Users\felip\Desktop\U\Tesis")
DATA_DIR = BASE_DIR / "Datos" / "HCNM_2026"
DATA_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = "180101"
END_DATE = "260723"

ORDER = ["Ventanas", "Centro Quintero", "Concón"]

STATIONS = {
    "Ventanas": "548",
    "Centro Quintero": "539",
    "Concón": "509",
}


def fetch_hourly_hcnm(rv: str) -> pd.DataFrame:
    url = (
        "https://sinca.mma.gob.cl/cgi-bin/APUB-MMA/apub.tsindico2.cgi"
        "?outtype=xcl"
        f"&macro=./RV/{rv}/Cal/NMHC//NMHC.horario.horario.ic"
        f"&from={START_DATE}"
        f"&to={END_DATE}"
        "&path=/usr/airviro/data/CONAMA/"
        "&lang=esp"
        "&rsrc="
        "&macropath="
    )

    response = requests.get(url, timeout=120)
    response.raise_for_status()
    text = response.text

    df = pd.read_csv(
        io.StringIO(text),
        sep=";",
        decimal=",",
        engine="python",
    )

    if df.empty:
        raise RuntimeError(f"No rows were returned for rv={rv}.")

    value_cols = [
        "Registros preliminares",
        "Registros no validados",
    ]

    for col in value_cols:
        if col not in df.columns:
            raise RuntimeError(f"Expected column {col!r} not found in SINCA export.")

    # Prefer preliminary records first; if they are missing, fall back to non-validated values.
    # If neither is available, keep NaN.
    df["value"] = df[value_cols].apply(
        lambda row: row.dropna().iloc[0] if row.notna().any() else pd.NA,
        axis=1,
    )
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    date_series = pd.to_datetime(
        df["FECHA (YYMMDD)"].astype("string").str.zfill(6), format="%y%m%d", errors="coerce"
    )
    hour_series = df["HORA (HHMM)"].astype("string").str.zfill(4)
    hour_minute = hour_series.str.extract(r"(\d{2})(\d{2})")
    hour_minute = hour_minute.apply(pd.to_numeric, errors="coerce")

    df["datetime"] = date_series + pd.to_timedelta(hour_minute[0], unit="h")
    df["datetime"] = df["datetime"] + pd.to_timedelta(hour_minute[1], unit="m")

    df = df.loc[
        df["datetime"].between(pd.Timestamp("2018-01-01"), pd.Timestamp("2026-07-23"))
    ].copy()

    df = df[["datetime", "value"]].rename(columns={"value": "HCNM_ppm"})
    return df


if __name__ == "__main__":
    all_frames = []
    for station, rv in STATIONS.items():
        station_df = fetch_hourly_hcnm(rv)
        station_df["station"] = station
        out_path = DATA_DIR / f"{station.replace(' ', '_').lower()}_hcnm_hourly.csv"
        station_df = station_df[["datetime", "station", "HCNM_ppm"]]
        station_df.to_csv(out_path, index=False)
        all_frames.append(station_df)

    combined = pd.concat(all_frames, ignore_index=True)
    combined = combined.sort_values(["station", "datetime"]).reset_index(drop=True)

    d1 = pd.to_datetime("2025-10-14 00:00:00")
    d2 = pd.to_datetime("2025-10-18 23:00:00")
    mask = combined["station"].eq("Centro Quintero") & combined["datetime"].between(d1, d2)
    combined.loc[mask, "HCNM_ppm"] = np.nan

    wide_df = (
        combined.pivot(index="datetime", columns="station", values="HCNM_ppm")
        .reindex(columns=ORDER)
        .sort_index()
    )
    wide_df.index.name = "datetime"
    wide_df.to_csv(DATA_DIR / "HCNM_2026_hourly_all_stations.csv", index=True, index_label="datetime")

    print(f"Downloaded hourly HCNM data to: {DATA_DIR}")
    print(wide_df.head().to_string())
