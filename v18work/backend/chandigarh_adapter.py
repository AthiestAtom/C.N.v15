from __future__ import annotations

import os
import uuid
from typing import Any

import jsonschema

import httpx


class ChandigarhModelAdapter:
    """Adapter between Chandigarh's canonical scenario format and a CITYNEXUS-compatible model API."""

    def __init__(self, mode: str | None = None, endpoint: str | None = None) -> None:
        self.mode = mode or os.getenv("CHANDIGARH_MODEL_MODE", "remote")
        self.endpoint = endpoint or os.getenv("CHANDIGARH_MODEL_URL", "").rstrip("/")

    def build_model_input(self, scenario: dict[str, Any]) -> dict[str, Any]:
        """Translate the Chandigarh scenario contract into the mobility model contract."""
        self._validate_road_network(scenario.get("road_network"))
        payload = {
            "simulation_id": {
                "user_id": self._execution_id(scenario, "user_id"),
                "prediction_id": self._execution_id(scenario, "prediction_id"),
            },
            "mobility_model_input": {
                "grid": scenario.get("grid", {}),
                "road_network": scenario.get("road_network", {}),
                "scenario": {
                    "bicycle percentage": self._required_mobility(scenario, "bicycle_percentage"),
                    "evehicle percentage": self._required_mobility(scenario, "evehicle_percentage"),
                    "day type": self._required_list(scenario, "day_type"),
                    "time slots": self._required_list(scenario, "time_slots"),
                },
            }
        }
        self._validate_model_input(payload)
        return payload


    @staticmethod
    def _execution_id(scenario: dict[str, Any], key: str) -> str:
        value = scenario.get(key)
        if value is not None and str(value).strip():
            return str(value)
        return f"chandigarh-{key}-{uuid.uuid4().hex}"

    @staticmethod
    def _validate_road_network(roads: Any) -> None:
        if not isinstance(roads, dict) or not roads:
            raise ValueError("scenario.road_network must contain acquired Chandigarh road features")
        missing = []
        for rid, road in roads.items():
            if not isinstance(road, dict):
                missing.append((rid, "road_object")); continue
            if "geometry" not in road:
                missing.append((rid, "geometry"))
        if missing:
            sample = ", ".join(f"{rid}:{field}" for rid, field in missing[:8])
            raise ValueError(f"road_network lacks source geometry required for downstream network construction: {sample}")

    @staticmethod
    def _required_mobility(scenario: dict[str, Any], key: str) -> Any:
        mobility = scenario.get("mobility")
        if not isinstance(mobility, dict) or key not in mobility:
            raise ValueError(f"scenario.mobility.{key} is required; no synthetic default is permitted")
        return mobility[key]

    @staticmethod
    def _required_list(scenario: dict[str, Any], key: str) -> list[Any]:
        value = scenario.get(key)
        if isinstance(value, list) and value:
            return value
        if key == "day_type" and isinstance(value, str) and value:
            return [value]
        raise ValueError(f"scenario.{key} must be supplied; no synthetic default is permitted")

    @staticmethod
    def _validate_model_input(payload: dict[str, Any]) -> None:
        schema = {
            "type": "object",
            "required": ["mobility_model_input"],
            "properties": {"mobility_model_input": {
                "type": "object",
                "required": ["grid", "road_network", "scenario"],
                "properties": {
                    "grid": {"type": "object"},
                    "road_network": {"type": "object"},
                    "scenario": {
                        "type": "object",
                        "required": ["bicycle percentage", "evehicle percentage", "day type", "time slots"],
                    },
                },
            }}
        }
        jsonschema.validate(payload, schema)

    async def run(self, scenario: dict[str, Any]) -> dict[str, Any]:
        payload = self.build_model_input(scenario)

        if self.mode == "mock":
            raise RuntimeError("Mock simulation is disabled: this project does not generate synthetic KPI observations")

        if self.mode not in {"remote", "local"}:
            raise ValueError(f"Unsupported CHANDIGARH_MODEL_MODE: {self.mode}")

        if self.mode == "local":
            from pathlib import Path
            from tempfile import TemporaryDirectory
            from .result_decoder import decode_result_zip
            from integrations.citynexus_upstream.binary_runner import CityNexusBinaryRunner

            with TemporaryDirectory(prefix="chandigarh-citynexus-") as work:
                root = Path(work)
                input_file = root / "model_input.json"
                output_dir = root / "output"
                # The API payload wraps the actual binary contract under
                # `mobility_model_input`. The genuine CITYNEXUS binary expects
                # that inner object directly, not the FastAPI wrapper.
                model_input = payload["mobility_model_input"]
                input_file.write_text(__import__("json").dumps(model_input), encoding="utf-8")
                result = CityNexusBinaryRunner().run(input_file, output_dir)
                zips = sorted(output_dir.glob("*.zip"), key=lambda x: x.stat().st_mtime, reverse=True)
                if not zips:
                    raise RuntimeError("CITYNEXUS binary completed without a result ZIP")
                result["decoded"] = decode_result_zip(zips[0].read_bytes())
                return result

        if not self.endpoint:
            raise RuntimeError("CHANDIGARH_MODEL_URL is required for remote mode")

        from .citynexus_client import CityNexusMobilityClient
        project = os.getenv("CITYNEXUS_MODEL_PROJECT")
        city = os.getenv("CITYNEXUS_MODEL_CITY")
        if not project or not city:
            raise RuntimeError("CITYNEXUS_MODEL_PROJECT and CITYNEXUS_MODEL_CITY must identify the deployed model; no city/model default is allowed")
        client = CityNexusMobilityClient(self.endpoint, project=project, city=city)
        return await client.run(payload)
