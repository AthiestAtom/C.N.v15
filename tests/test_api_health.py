from pathlib import Path

from fastapi.testclient import TestClient

from mobility_model_api.api import app as api_app


def test_health_reports_degraded_when_binary_missing():
    client = TestClient(api_app.app)
    api_app.MODEL_BIN_PATH = Path("/definitely/missing/run_mobility_model")

    response = client.get("/health")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "degraded"
    assert payload["model_binary_available"] is False


def test_health_reports_ok_when_binary_exists(tmp_path):
    binary = tmp_path / "run_mobility_model"
    binary.write_text("#!/bin/sh\nexit 0\n")
    client = TestClient(api_app.app)
    api_app.MODEL_BIN_PATH = binary

    response = client.get("/health")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert payload["model_binary_available"] is True
