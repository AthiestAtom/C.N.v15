import json
from copy import deepcopy
from pathlib import Path
from typing import Any

MODEL_INPUT_BASE_PATH = Path("/model_input")

def store_input_file(input_file: Path, content: dict[str, Any]) -> None:
    input_file.parent.mkdir(parents=True, exist_ok=True)
    with open(input_file, "w") as file:
        json.dump(content, file, indent=2)

def get_road_ids(model_input: dict[str, Any]) -> set[str]:
    return {road_id for road_id in model_input["road_network"]}

def derive_input_file_path(simulation_id, xai_suffix: str = ""):
    suffix = f"_{xai_suffix}" if xai_suffix else ""
    return MODEL_INPUT_BASE_PATH / f"{simulation_id.user_id}_{simulation_id.prediction_id}{suffix}.json"

def derive_flood_model_file_path(simulation_id):
    return MODEL_INPUT_BASE_PATH / f"{simulation_id.user_id}_{simulation_id.prediction_id}_flood_model.tiff"

def create_model_input_modification(model_input: dict[str, Any], road_id: str, day_type: str, time_slot: int) -> dict[str, Any]:
    model_input_modified = deepcopy(model_input)
    del model_input_modified["road_network"][road_id]
    model_input_modified["scenario"]["day type"] = [day_type.strip().lower()]
    model_input_modified["scenario"]["time slots"] = [time_slot]
    return model_input_modified
