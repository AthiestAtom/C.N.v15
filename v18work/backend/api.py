from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .chandigarh_adapter import ChandigarhModelAdapter
from .scenario_engine import ScenarioEngine

app = FastAPI(
    title="Chandigarh Urban Digital Twin API",
    version="0.1.0",
    description="Chandigarh-specific decision layer around a CITYNEXUS-compatible mobility model.",
)

engine = ScenarioEngine()
adapter = ChandigarhModelAdapter()


class SimulationRequest(BaseModel):
    city: str
    day_type: str | list[str]
    time_slots: list[int]
    road_network: dict[str, dict[str, Any]] = Field(default_factory=dict)
    mobility: dict[str, float] = Field(default_factory=dict)
    interventions: list[dict[str, Any]] = Field(default_factory=list)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "city": "chandigarh"}


@app.get("/api/v1/chandigarh/scenarios")
async def scenarios() -> dict[str, Any]:
    return {
        "city": "chandigarh",
        "scenarios": [
            "bus_priority",
            "traffic_signal_coordination",
            "low_emission_zone",
            "road_closure",
        ],
    }


@app.post("/api/v1/chandigarh/simulate")
async def simulate(request: SimulationRequest) -> dict[str, Any]:
    if request.city.lower() != "chandigarh":
        raise HTTPException(status_code=400, detail="This endpoint is Chandigarh-specific.")

    base = request.model_dump(exclude={"interventions"})
    baseline = await adapter.run(base)

    intervention_scenario = engine.apply_interventions(
        base, request.interventions
    )
    intervention = await adapter.run(intervention_scenario)

    return {
        "city": "chandigarh",
        "baseline": baseline,
        "intervention": intervention,
        "comparison": engine.compare(baseline, intervention),
    }
