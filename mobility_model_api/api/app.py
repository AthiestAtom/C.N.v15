import os
import subprocess
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException

from mobility_model_api.model.mobility_model_input import MobilityModelInput
from mobility_model_api.simulation.model_input import derive_input_file_path, store_input_file
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CITYNEXUS Mobility Model API", version="0.1.14")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
MODEL_BIN_PATH = Path(os.getenv("MODEL_BIN_PATH", "/run_mobility_model"))
MODEL_OUTPUT_BASE_PATH = Path(os.getenv("MODEL_OUTPUT_BASE_PATH", "/model_output"))


def _binary_available() -> bool:
    return MODEL_BIN_PATH.exists() and MODEL_BIN_PATH.is_file()


@app.get("/health")
def health() -> dict:
    binary_available = _binary_available()
    return {
        "service": "citynexus-mobility-model-api",
        "status": "ok" if binary_available else "degraded",
        "model_binary_path": str(MODEL_BIN_PATH),
        "model_binary_available": binary_available,
    }


@app.post("/simulate")
def simulate(payload: MobilityModelInput) -> dict:
    if not _binary_available():
        raise HTTPException(
            status_code=503,
            detail=(
                f"Mobility model binary not available at {MODEL_BIN_PATH}. "
                "Set MODEL_BIN_PATH to a valid run_mobility_model executable."
            ),
        )

    input_file = derive_input_file_path(payload.simulation_id)
    output_path = (
        MODEL_OUTPUT_BASE_PATH
        / payload.simulation_id.user_id
        / "predictions"
        / payload.simulation_id.prediction_id
    )
    store_input_file(input_file, payload.mobility_model_input)
    run_cmd = [
        str(MODEL_BIN_PATH.absolute()),
        "--json-path",
        str(input_file.absolute()),
        "--output-path",
        str(output_path.absolute()),
    ]
    if payload.create_trajectories:
        run_cmd += ["--return-od", "true"]
    output_path.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(run_cmd, capture_output=True)
    return_code = proc.returncode
    status = "completed" if return_code == 0 else "failed"
    return {
        "simulation_id": payload.simulation_id.model_dump(),
        "status": status,
        "return_code": return_code,
        "input_file": str(input_file),
        "output_path": str(output_path),
    }


def run() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("mobility_model_api.api.app:app", host=host, port=port, reload=False)
