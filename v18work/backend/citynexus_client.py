from __future__ import annotations

import io
import os
import time
import zipfile
from typing import Any

import httpx

from .result_decoder import decode_result_zip


class CityNexusMobilityClient:
    """Client for the real CITYNEXUS mobility-model API lifecycle.

    CITYNEXUS does not return simulation metrics directly from POST /analysis.
    It queues a simulation, exposes status, then exposes a ZIP result.
    """

    def __init__(self, base_url: str, project: str, city: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.project = project
        self.city = city
        self.api_prefix = f"/api/v1/mobility-model-{project}-{city}"

    async def run(self, model_input: dict[str, Any]) -> dict[str, Any]:
        simulation_id = model_input.get("simulation_id")
        if not simulation_id:
            raise ValueError("model_input must contain simulation_id")

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{self.base_url}{self.api_prefix}/analysis",
                json=model_input,
            )
            response.raise_for_status()

            timeout_s = int(os.getenv("CHANDIGARH_MODEL_POLL_TIMEOUT", "300"))
            interval_s = float(os.getenv("CHANDIGARH_MODEL_POLL_INTERVAL", "2"))
            deadline = time.monotonic() + timeout_s

            status = None
            while time.monotonic() < deadline:
                status_response = await client.get(
                    f"{self.base_url}{self.api_prefix}/analysis/status",
                    params=simulation_id,
                )
                status_response.raise_for_status()
                status = status_response.json()
                state = status.get("status")
                if state == "Completed":
                    break
                if state in {"Failed", "Not Available"}:
                    raise RuntimeError(f"CITYNEXUS simulation ended with status: {state}")
                await self._sleep(interval_s)
            else:
                raise TimeoutError("CITYNEXUS mobility simulation timed out")

            result_response = await client.get(
                f"{self.base_url}{self.api_prefix}/analysis",
                params=simulation_id,
            )
            result_response.raise_for_status()
            return self._decode_result_zip(result_response.content)

    @staticmethod
    async def _sleep(seconds: float) -> None:
        import asyncio
        await asyncio.sleep(seconds)

    @staticmethod
    def _decode_result_zip(content: bytes) -> dict[str, Any]:
        """Return JSON members when available; preserve other files as metadata.

        The exact model-output schema is version-dependent, so this adapter does
        not invent KPI names. JSON members are surfaced verbatim for the KPI layer.
        """
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            members = archive.namelist()
            json_files: dict[str, Any] = {}
            for name in members:
                if name.lower().endswith(".json"):
                    try:
                        import json
                        json_files[name] = json.loads(archive.read(name).decode("utf-8"))
                    except Exception:
                        continue
            decoded = decode_result_zip(content)
        decoded["files"] = members
        # Keep JSON members available for debugging/version inspection while
        # exposing normalized KPIs to the Chandigarh decision layer.
        decoded["json"] = json_files
        return decoded
