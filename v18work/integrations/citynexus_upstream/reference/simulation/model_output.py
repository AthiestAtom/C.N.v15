import json
import logging
import os
import zipfile
from numbers import Number
from pathlib import Path
from typing import IO, Callable, List, Tuple, TypeVar
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely import Polygon
from shapely.geometry import box

T = TypeVar("T")
MODEL_OUTPUT_BASE_PATH = Path("/model_output")
TargetAreaType = List[Tuple[Number, Number]]

def load_result_zip(result_path: Path, type_loader: Callable[[IO[bytes]], T]) -> T:
    with zipfile.ZipFile(result_path, "r") as zip_file:
        result_file = zip_file.namelist()[0]
        with zip_file.open(result_file) as unzipped_file:
            return type_loader(unzipped_file)

def load_geojson(file_path: Path, type_loader: Callable[[IO[bytes]], T]) -> T:
    with file_path.open("rb") as file:
        return type_loader(file)

def load_as_dict(file_bytes: IO[bytes]) -> dict:
    return json.loads(file_bytes.read().decode("utf-8"))

def load_as_geodf(file_bytes: IO[bytes]) -> GeoDataFrame:
    return gpd.read_file(file_bytes)

def find_latest_file(file_path: Path, file_pattern: str) -> Path:
    logging.info(f"Requested file path: {file_path}")
    try:
        file_path.resolve().relative_to(MODEL_OUTPUT_BASE_PATH.resolve())
    except ValueError:
        raise ValueError(f"{file_path} is not a subdirectory of the model output path.")
    files_found = list(file_path.glob(file_pattern))
    if not files_found:
        raise FileNotFoundError(f"No result files match {file_pattern}")
    return max(files_found, key=os.path.getmtime)

def get_output_prefix(road_id: str) -> str:
    return f"XAI_{road_id}"

def get_target_area(gdf: GeoDataFrame, target_area: TargetAreaType) -> GeoDataFrame:
    if not target_area or len(target_area) < 2:
        target_geometry = box(*gdf.total_bounds.tolist())
    elif len(target_area) == 2:
        target_geometry = box(*target_area[0], *target_area[1])
    else:
        target_geometry = Polygon(target_area)
    return gdf[gdf.geometry.within(target_geometry)].copy()

def filter_time_slot(result_file: GeoDataFrame, day_type: str, time_slot: int) -> GeoDataFrame:
    requested = f"{day_type.strip().lower()}_{time_slot}"
    if "time_window" not in result_file.columns:
        raise ValueError("time_window not found in model result")
    if requested not in {str(x) for x in result_file["time_window"].unique()}:
        raise ValueError(f"Time window {requested} not found in model result file.")
    return result_file[result_file["time_window"] == requested]

def derive_output_path(simulation_id, is_xai: bool = False):
    output_path = MODEL_OUTPUT_BASE_PATH / simulation_id.user_id / "predictions" / simulation_id.prediction_id
    if is_xai:
        output_path /= "xai"
    return output_path
