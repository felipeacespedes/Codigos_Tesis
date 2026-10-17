from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch
from statsmodels.formula.api import quantreg

sns.set_theme(style="whitegrid", context="talk")

BASE_DIR = Path(r"C:\Users\felip\Desktop\U\Tesis")
DATA_DIR = BASE_DIR / "Datos" / "HCNM_2026"
PLOTS_DIR = DATA_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = DATA_DIR / "HCNM_2026_hourly_all_stations.csv"
ORDER = ["Ventanas", "Centro Quintero", "Concón"]
STATION_COLORS = {
    "Ventanas": "tab:blue",
    "Centro Quintero": "tab:orange",
    "Concón": "tab:green",
}


def load_data() -> pd.DataFrame:
    df = pd.read_csv(INPUT_FILE, parse_dates=["datetime"])
    # Filter to keep only data from 2019 onwards
    df = df[df["datetime"].dt.year >= 2019]

    if "station" in df.columns:
        df["station"] = df["station"].astype(str)
        df["station"] = pd.Categorical(df["station"], categories=ORDER, ordered=True)
        df = df.sort_values(["station", "datetime"]).reset_index(drop=True)
        return df

    wide_df = df.set_index("datetime").reindex(columns=ORDER)
    long_df = wide_df.stack().reset_index()
    long_df.columns = ["datetime", "station", "HCNM_ppm"]
    long_df["station"] = pd.Categorical(long_df["station"], categories=ORDER, ordered=True)
    long_df = long_df.sort_values(["station", "datetime"]).reset_index(drop=True)
    return long_df


def style_boxplot(bp: dict, station_colors: dict[str, str]) -> None:
    for idx, station in enumerate(ORDER):
        color = station_colors[station]
        bp["boxes"][idx].set(facecolor=color, edgecolor=color, alpha=0.8)
        bp["whiskers"][2 * idx].set(color=color)
        bp["whiskers"][2 * idx + 1].set(color=color)
        bp["caps"][2 * idx].set(color=color)
        bp["caps"][2 * idx + 1].set(color=color)
        bp["medians"][idx].set(color=color, linewidth=2)


def style_boxplot_station(bp: dict, color: str) -> None:
    for box in bp["boxes"]:
        box.set(facecolor=color, edgecolor=color, alpha=0.9)
    for whisker in bp["whiskers"]:
        whisker.set(color=color)
    for cap in bp["caps"]:
        cap.set(color=color)
    for median in bp["medians"]:
        median.set(color=color, linewidth=2)


if __name__ == "__main__":
    df = load_data()
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.to_period("M").astype(str)
    df["hour"] = df["datetime"].dt.hour

    # 1. Total time series in the requested order (top to bottom)
    fig, axes = plt.subplots(len(ORDER), 1, figsize=(16, 10), sharex=True, constrained_layout=True)
    for ax, station in zip(axes, ORDER):
        sub = df[df["station"] == station].copy()
        sub = sub.loc[(sub["datetime"] >= pd.Timestamp("2019-01-01")) & (sub["datetime"] <= pd.Timestamp("2026-07-23"))]
        ax.plot(sub["datetime"], sub["HCNM_ppm"], color=STATION_COLORS[station], lw=0.8, alpha=0.8)
        max_val = float(sub["HCNM_ppm"].max()) if not sub.empty else 1.0
        ax.set_ylim(0, max_val * 1.05 if max_val > 0 else 1.0)
        ax.set_xlim(pd.Timestamp("2019-01-01"), pd.Timestamp("2026-07-23"))
        ax.set_ylabel("HCNM (ppm)")
        ax.set_title(station)
        ax.grid(True, alpha=0.25)
    axes[-1].set_xlabel("Fecha")
    fig.suptitle("HCNM hourly series (2019-present)", y=1.02)
    fig.savefig(PLOTS_DIR / "01_total_series_stacked.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # 1b. Total time series with a fixed shared y-axis range of 0–10 for all stations
    fig, axes = plt.subplots(len(ORDER), 1, figsize=(16, 10), sharex=True, constrained_layout=True)
    for ax, station in zip(axes, ORDER):
        sub = df[df["station"] == station].copy()
        sub = sub.loc[(sub["datetime"] >= pd.Timestamp("2019-01-01")) & (sub["datetime"] <= pd.Timestamp("2026-07-23"))]
        ax.plot(sub["datetime"], sub["HCNM_ppm"], color=STATION_COLORS[station], lw=0.8, alpha=0.8)
        ax.set_ylim(0, 10)
        ax.set_xlim(pd.Timestamp("2019-01-01"), pd.Timestamp("2026-07-23"))
        ax.set_ylabel("HCNM (ppm)")
        ax.set_title(station)
        ax.grid(True, alpha=0.25)
    axes[-1].set_xlabel("Fecha")
    fig.suptitle("HCNM hourly series with fixed y-limits (0–10 ppm)", y=1.02)
    fig.savefig(PLOTS_DIR / "01b_total_series_stacked_fixed_ylim_0_10.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # 2. Total boxplot
    fig, ax = plt.subplots(figsize=(8, 6))
    station_values = [df.loc[df["station"] == station, "HCNM_ppm"].dropna() for station in ORDER]
    bp = ax.boxplot(station_values, patch_artist=True, tick_labels=ORDER, showfliers=True)
    style_boxplot(bp, STATION_COLORS)
    # Add means as white diamonds
    means = [df.loc[df["station"] == station, "HCNM_ppm"].dropna().mean() for station in ORDER]
    ax.scatter(range(1, len(ORDER) + 1), means, marker="D", s=100, color="white", edgecolors="black", linewidth=1.5, zorder=3)
    handles = [Patch(facecolor=STATION_COLORS[station], label=station) for station in ORDER]
    ax.legend(handles=handles, loc="upper right")
    ax.set_title("HCNM distribution by station")
    ax.set_ylabel("HCNM (ppm)")
    ax.set_xlabel("")
    plt.xticks(rotation=20)
    fig.savefig(PLOTS_DIR / "02_boxplot_total_series.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # 2b. Total boxplot without outliers
    fig, ax = plt.subplots(figsize=(8, 6))
    station_values = [df.loc[df["station"] == station, "HCNM_ppm"].dropna() for station in ORDER]
    bp = ax.boxplot(station_values, patch_artist=True, tick_labels=ORDER, showfliers=False)
    style_boxplot(bp, STATION_COLORS)
    # Add means as white diamonds
    means = [df.loc[df["station"] == station, "HCNM_ppm"].dropna().mean() for station in ORDER]
    ax.scatter(range(1, len(ORDER) + 1), means, marker="D", s=100, color="white", edgecolors="black", linewidth=1.5, zorder=3)
    handles = [Patch(facecolor=STATION_COLORS[station], label=station) for station in ORDER]
    ax.legend(handles=handles, loc="upper left")
    ax.set_title("HCNM distribution by station (without outliers)")
    ax.set_ylabel("HCNM (ppm)")
    ax.set_xlabel("")
    plt.xticks(rotation=20)
    fig.savefig(PLOTS_DIR / "02b_boxplot_total_series_no_outliers.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # 3. Boxplot per year of the 3 stations
    years = sorted(df["year"].dropna().unique())
    fig, ax = plt.subplots(figsize=(14, 7))
    positions = list(range(1, len(years) + 1))
    for idx, station in enumerate(ORDER):
        values = [df.loc[(df["station"] == station) & (df["year"] == year), "HCNM_ppm"].dropna() for year in years]
        bp = ax.boxplot(values, positions=[p + idx * 0.15 for p in positions], widths=0.12, patch_artist=True, manage_ticks=False, showfliers=True)
        style_boxplot_station(bp, STATION_COLORS[station])
    ax.set_xticks([p + 0.15 for p in positions])
    ax.set_xticklabels(years, rotation=45)
    ax.set_xlabel("Año")
    ax.set_ylabel("HCNM (ppm)")
    ax.set_title("HCNM boxplot per year for the three stations")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(handles=[Patch(facecolor=STATION_COLORS[station], label=station) for station in ORDER], loc="upper right")
    fig.savefig(PLOTS_DIR / "03_boxplot_by_year.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # 3b. Boxplot per year without outliers
    fig, ax = plt.subplots(figsize=(14, 7))
    positions = list(range(1, len(years) + 1))
    for idx, station in enumerate(ORDER):
        values = [df.loc[(df["station"] == station) & (df["year"] == year), "HCNM_ppm"].dropna() for year in years]
        bp = ax.boxplot(values, positions=[p + idx * 0.15 for p in positions], widths=0.12, patch_artist=True, manage_ticks=False, showfliers=False)
        style_boxplot_station(bp, STATION_COLORS[station])
    ax.set_xticks([p + 0.15 for p in positions])
    ax.set_xticklabels(years, rotation=45)
    ax.set_xlabel("Año")
    ax.set_ylabel("HCNM (ppm)")
    ax.set_title("HCNM boxplot per year for the three stations (without outliers)")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(handles=[Patch(facecolor=STATION_COLORS[station], label=station) for station in ORDER], loc="upper right")
    fig.savefig(PLOTS_DIR / "03b_boxplot_by_year_no_outliers.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # 4. Monthly mean trend
    monthly = df.groupby(["station", "month"])["HCNM_ppm"].mean().reset_index()
    monthly["month_dt"] = pd.to_datetime(monthly["month"])
    fig, ax = plt.subplots(figsize=(14, 6))
    for station in ORDER:
        sub = monthly[monthly["station"] == station].sort_values("month_dt")
        ax.plot(sub["month_dt"], sub["HCNM_ppm"], marker="o", linewidth=1.5, color=STATION_COLORS[station], label=station)
    ax.set_title("Monthly mean HCNM (2019-present)")
    ax.set_ylabel("HCNM mean (ppm)")
    ax.set_xlabel("Month")
    tick_dates = pd.date_range(start="2019-01-01", end="2026-07-01", freq="6MS")
    ax.set_xticks(tick_dates)
    ax.set_xticklabels([date.strftime("%b %Y") for date in tick_dates], rotation=45)
    ax.legend()
    fig.savefig(PLOTS_DIR / "04_monthly_mean_trend.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # 5. Median diurnal profile
    hourly_profile = df.groupby(["station", "hour"])["HCNM_ppm"].median().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    for station in ORDER:
        sub = hourly_profile[hourly_profile["station"] == station]
        ax.plot(sub["hour"], sub["HCNM_ppm"], marker="o", color=STATION_COLORS[station], label=station)
    ax.set_title("Median hourly profile of HCNM")
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Median HCNM (ppm)")
    ax.set_xticks(range(0, 24))
    ax.legend()
    fig.savefig(PLOTS_DIR / "05_hourly_diurnal_cycle.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # 6. Quantile regression for each station from 2019-present
    fig, axes = plt.subplots(len(ORDER), 1, figsize=(16, 10), sharex=True, constrained_layout=True)
    for ax, station in zip(axes, ORDER):
        sub = df[df["station"] == station].copy()
        sub = sub.loc[(sub["datetime"] >= pd.Timestamp("2019-01-01")) & (sub["datetime"] <= pd.Timestamp("2026-07-23"))].copy()
        sub = sub.sort_values("datetime").reset_index(drop=True)
        sub["time_numeric"] = (sub["datetime"] - sub["datetime"].min()).dt.total_seconds() / 86400.0
        quantile_styles = {0.25: "--", 0.50: "-", 0.75: ":"}
        for q in [0.25, 0.50, 0.75]:
            model = quantreg("HCNM_ppm ~ time_numeric", sub).fit(q=q)
            preds = pd.DataFrame({"time_numeric": np.linspace(sub["time_numeric"].min(), sub["time_numeric"].max(), 300)})
            trend = model.predict(preds)
            ax.plot(preds["time_numeric"], trend, lw=1.5, color=STATION_COLORS[station], linestyle=quantile_styles[q], label=f"Q{q:.2f}")
        ax.set_xlim(0, sub["time_numeric"].max())
        ax.set_ylim(0, 1)
        ax.set_ylabel("HCNM (ppm)")
        ax.set_title(station)
        ax.grid(True, alpha=0.25)
        ax.legend(loc="upper right")
    axes[-1].set_xlabel("Days since 2019-01-01")
    fig.suptitle("Quantile regression of HCNM by station (2019-present)", y=1.02)
    fig.savefig(PLOTS_DIR / "06_quantile_regression_stacked.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

# 7. Campaign time series for selected station periods
    campaign_periods = [
        ("Concón", "Concón", pd.Timestamp("2025-04-22"), pd.Timestamp("2025-05-27")),
        ("Centro Quintero", "Quintero", pd.Timestamp("2025-07-10"), pd.Timestamp("2025-08-20")),
        ("Ventanas", "Ventanas", pd.Timestamp("2025-09-05"), pd.Timestamp("2025-10-15")),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(16, 10), sharex=False, constrained_layout=True)
    
    for ax, (station, location, start_date, end_date) in zip(axes, campaign_periods):
        sub = df[df["station"] == station].copy()
        sub = sub.loc[(sub["datetime"] >= start_date) & (sub["datetime"] <= end_date)]
        ax.plot(sub["datetime"], sub["HCNM_ppm"], color=STATION_COLORS[station], lw=0.8, alpha=0.9, label=station)
        ax.set_ylabel("HCNM (ppm)")
        ax.set_title(station)
        ax.grid(True, alpha=0.25)
        ax.legend(loc="upper right")
        ax.set_xlim(start_date, end_date)
        
        # FIX: Use DayLocator with a 4-day interval, and lowercase 'y' for a 2-digit year
        date_formatter = mdates.DateFormatter("%d-%m-%y")
        date_locator = mdates.DayLocator(interval=4)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.xaxis.set_major_locator(date_locator)
        
        # Outward facing ticks
        ax.tick_params(axis="x", which="both", bottom=True, top=False, labelbottom=True, length=4, direction="out", color="black")
        ax.tick_params(axis="y", which="both", left=True, right=False, labelleft=True, length=4, direction="out", color="black")
        
        for spine in ax.spines.values():
            spine.set_linewidth(0.8)
            
        for label in ax.get_xticklabels():
            label.set_visible(True)
            label.set_rotation(20)
            label.set_ha("right")
            
    axes[-1].set_xlabel("Fecha")
    fig.suptitle("HCNM en Campañas Concón, Quintero y Ventanas", y=1.05)
    fig.savefig(PLOTS_DIR / "07_campaign_series.png", dpi=200, bbox_inches="tight")
    plt.close(fig)