"""Reader for the published CHETNA-Road Chandigarh 2021 NetCDF products."""
from __future__ import annotations
from pathlib import Path
import numpy as np

POLLUTANTS=('CO2','NOx','PM2.5','PM10','CO','VOC','CH4','N2O','NH3','Pb','BC')

def summarize(path: str|Path) -> dict:
    try:
        import xarray as xr
    except ImportError as e:
        raise RuntimeError('xarray is required to read CHETNA-Road NetCDF') from e
    ds=xr.open_dataset(path)
    return {
      'source':'CHETNA-Road', 'city':'Chandigarh', 'year':2021,
      'dimensions':dict(ds.sizes), 'variables':list(ds.data_vars),
      'time_start':str(ds.time.values[0]) if 'time' in ds else None,
      'time_end':str(ds.time.values[-1]) if 'time' in ds else None,
    }

def daily_city_total(path: str|Path, variable: str) -> list[dict]:
    try:
        import xarray as xr
    except ImportError as e:
        raise RuntimeError('xarray is required') from e
    ds=xr.open_dataset(path)
    if variable not in ds: raise KeyError(variable)
    da=ds[variable]
    spatial=[d for d in da.dims if d != 'time']
    vals=da.sum(dim=spatial,skipna=True).values
    times=ds.time.values
    return [{'date':str(t)[:10], 'value':float(v) if np.isfinite(v) else None} for t,v in zip(times,vals)]
