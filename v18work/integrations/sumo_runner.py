from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any


class SumoRunner:
    """Optional SUMO execution bridge.

    SUMO itself is not bundled. Install SUMO separately and point SUMO_BINARY at
    sumo or sumo-gui. This bridge keeps the Chandigarh layer independent of the
    SUMO web/LLM application while allowing us to reuse SUMO as the mature traffic
    simulation engine used by CITYNEXUS.
    """

    def __init__(self, config_file: str | Path, binary: str | None = None):
        self.config_file = Path(config_file)
        self.binary = binary or os.getenv("SUMO_BINARY", "sumo")

    def run(self, extra_args: list[str] | None = None, timeout: int = 300) -> dict[str, Any]:
        if not self.config_file.exists():
            raise FileNotFoundError(f"SUMO config not found: {self.config_file}")
        command = [self.binary, "-c", str(self.config_file), "--quit-on-end"]
        command.extend(extra_args or [])
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return {
            "returncode": proc.returncode,
            "ok": proc.returncode == 0,
            "stdout": proc.stdout[-10000:],
            "stderr": proc.stderr[-10000:],
            "command": command,
        }
