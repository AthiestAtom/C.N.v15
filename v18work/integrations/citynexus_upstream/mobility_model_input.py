"""Selected upstream CITYNEXUS mobility API contract.

Source: destination-earth/DestinE_ESA_CityNexus
Path: images/mobility-model-api/mobility_model_api/model/mobility_model_input.py
License: Apache-2.0
"""
from typing import Any, Optional
from pydantic import BaseModel


class XAIInput(BaseModel):
    area_of_interest: list[list[float]] = []
    attribute: str
    day_type: str
    time_slot: int


class MobilityModelInput(BaseModel):
    simulation_id: Any
    mobility_model_input: dict[str, Any]
    flood_model_input: Optional[bool] = False
    xai_input: Optional[XAIInput] = None
    create_trajectories: Optional[bool] = False
