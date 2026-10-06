"""Small local runner adapted from CITYNEXUS's model_run.py.

Source: destination-earth/DestinE_ESA_CityNexus
Path: images/mobility-model-api/mobility_model_api/simulation/model_run.py
License: Apache-2.0

Only the reusable process-execution portion is retained. XAI orchestration is
left to the upstream service because its supporting modules are not part of
this selective integration.
"""
from __future__ import annotations
import logging
import os
import subprocess
from pathlib import Path


class CityNexusBinaryRunner:
    """Execute the genuine CITYNEXUS mobility binary when it is installed."""

    def __init__(self, binary: str | None = None):
        self.binary = binary or os.getenv("CITYNEXUS_MODEL_BINARY", "/run_mobility_model")

    def run(self, input_file: str | Path, output_path: str | Path,
            create_trajectories: bool = False, flood_model_input: str | Path | None = None,
            timeout: int = 1800) -> dict:
        input_file = Path(input_file).resolve()
        output_path = Path(output_path).resolve()
        if not input_file.exists():
            raise FileNotFoundError(f"CITYNEXUS model input not found: {input_file}")
        output_path.mkdir(parents=True, exist_ok=True)
        binary = Path(self.binary)
        if not binary.exists() and os.path.sep in self.binary:
            raise FileNotFoundError(
                f"CITYNEXUS mobility binary not found: {self.binary}. "
                "Install/provide the genuine CITYNEXUS model binary; no fallback model is used."
            )
        cmd = [self.binary, "--json-path", str(input_file), "--output-path", str(output_path)]
        if flood_model_input is not None:
            flood = Path(flood_model_input).resolve()
            if not flood.exists():
                raise FileNotFoundError(f"Flood model input not found: {flood}")
            cmd += ["--flood-depth-map", str(flood)]
        if create_trajectories:
            cmd += ["--return-od", "true"]
        logging.info("Executing CITYNEXUS mobility binary")
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if proc.returncode:
            raise RuntimeError(f"CITYNEXUS mobility binary failed ({proc.returncode}): {proc.stderr[-4000:]}")
        return {"returncode": 0, "ok": True, "stdout": proc.stdout[-10000:], "stderr": proc.stderr[-10000:], "command": cmd, "output_path": str(output_path)}
