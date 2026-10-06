from __future__ import annotations

import io
import json
import zipfile
from typing import Any

import geopandas as gpd
import pandas as pd

# CITYNEXUS documentation identifies these output families. The decoder accepts
# common spelling variants because the exact model-output property names can
# vary by deployed model version.
ALIASES = {
    "no2_g": ["NO2", "NO2_g", "no2", "no2_grams"],
    "co2_g": ["CO2", "CO2_g", "co2", "co2_grams"],
    "nox_g": ["NOx", "NOX", "NOx_g", "nox", "nox_grams"],
    "pmx_g": ["PMx", "PMX", "PMx_g", "pmx", "pmx_grams"],
    "hc_g": ["HC", "HC_g", "hc", "hc_grams"],
    "co_g": ["CO", "CO_g", "co", "co_grams"],
    "fuel_g": ["fuel_consumption", "fuel_consumption_g", "fuel", "fuel_g"],
    "speed_kmh": ["traffic_speed", "traffic_speed_kmh", "speed", "speed_kmh", "avg_speed"],
    "occupancy": ["occupancy", "vehicle_occupancy"],
}


def _find_column(columns: list[str], aliases: list[str]) -> str | None:
    exact = {str(c): c for c in columns}
    lower = {str(c).lower(): c for c in columns}
    for alias in aliases:
        if alias in exact:
            return exact[alias]
        if alias.lower() in lower:
            return lower[alias.lower()]
    return None


def decode_result_zip(payload: bytes) -> dict[str, Any]:
    """Decode CITYNEXUS result ZIPs into a normalized KPI summary.

    Raw files are retained in the response metadata; KPI values are only
    produced when the corresponding properties actually exist.
    """
    frames: list[gpd.GeoDataFrame] = []
    files: list[str] = []
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            files.append(name)
            if name.lower().endswith((".geojson", ".json")):
                try:
                    raw = zf.read(name)
                    if name.lower().endswith(".geojson"):
                        frames.append(gpd.read_file(io.BytesIO(raw)))
                    else:
                        obj = json.loads(raw.decode("utf-8"))
                        if isinstance(obj, dict) and obj.get("type") in {"FeatureCollection", "Feature"}:
                            frames.append(gpd.read_file(io.BytesIO(raw)))
                except Exception:
                    # Keep the raw member listed; an unrelated JSON file should
                    # never prevent useful GeoJSON outputs from being decoded.
                    continue

    if not frames:
        return {"model": "citynexus", "files": files, "kpis": {}, "rows": 0}

    # Prefer the largest frame because model result ZIPs can contain metadata
    # alongside the road-level result layer.
    frame = max(frames, key=len).copy()
    return {
        "model": "citynexus",
        "files": files,
        "kpis": summarize(frame),
        "rows": int(len(frame)),
    }


def summarize(frame: gpd.GeoDataFrame) -> dict[str, float | int]:
    result: dict[str, float | int] = {}
    for kpi, aliases in ALIASES.items():
        col = _find_column(list(frame.columns), aliases)
        if not col:
            continue
        values = pd.to_numeric(frame[col], errors="coerce").dropna()
        if values.empty:
            continue
        if kpi in {"speed_kmh", "occupancy"}:
            result[kpi] = round(float(values.mean()), 4)
        else:
            result[kpi] = round(float(values.sum()), 4)
    return result
