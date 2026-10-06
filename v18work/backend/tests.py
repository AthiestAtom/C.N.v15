import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.chandigarh_adapter import ChandigarhModelAdapter


def test_upstream_contract():
    scenario = {
        "user_id": "chandigarh_demo",
        "prediction_id": "scenario_001",
        "road_network": {"123": {"maxspeed": 50, "geometry": {"type": "LineString", "coordinates": [[76.7,30.7],[76.71,30.71]]}}},
        "mobility": {"bicycle_percentage": 8, "evehicle_percentage": 12},
        "day_type": ["weekday"],
        "time_slots": [3],
    }
    payload = ChandigarhModelAdapter(mode="remote").build_model_input(scenario)
    assert payload["simulation_id"]["user_id"] == "chandigarh_demo"
    assert payload["mobility_model_input"]["scenario"]["evehicle percentage"] == 12
    assert payload["mobility_model_input"]["road_network"]["123"]["maxspeed"] == 50


def test_missing_scenario_input_is_rejected():
    scenario = {
        "road_network": {},
        "mobility": {"bicycle_percentage": 8},
        "day_type": ["weekday"],
        "time_slots": [3],
    }
    scenario["road_network"] = {"123": {"maxspeed": 50, "geometry": {"type": "LineString", "coordinates": [[76.7,30.7],[76.71,30.71]]}}}
    try:
        ChandigarhModelAdapter(mode="remote").build_model_input(scenario)
    except ValueError as exc:
        assert "evehicle_percentage" in str(exc)
    else:
        raise AssertionError("missing scenario input was silently defaulted")


def test_mock_execution_is_disabled():
    scenario = {
        "road_network": {"123": {"maxspeed": 50, "geometry": {"type": "LineString", "coordinates": [[76.7,30.7],[76.71,30.71]]}}},
        "mobility": {"bicycle_percentage": 8, "evehicle_percentage": 12},
        "day_type": ["weekday"],
        "time_slots": [3],
    }
    import asyncio
    try:
        asyncio.run(ChandigarhModelAdapter(mode="mock").run(scenario))
    except RuntimeError as exc:
        assert "synthetic KPI" in str(exc)
    else:
        raise AssertionError("synthetic simulation unexpectedly executed")




def test_local_runner_receives_inner_citynexus_contract(tmp_path, monkeypatch):
    import asyncio, json
    import integrations.citynexus_upstream.binary_runner as runner_module

    captured = {}

    class FakeRunner:
        def run(self, input_file, output_path, *args, **kwargs):
            captured["payload"] = json.loads(Path(input_file).read_text())
            captured["output_path"] = str(output_path)
            # The adapter expects a ZIP after successful execution.
            Path(output_path).mkdir(parents=True, exist_ok=True)
            import zipfile
            zip_path = Path(output_path) / "results_simulation_weekday_timeslot_3_test.zip"
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("result.json", json.dumps({"type": "FeatureCollection", "features": []}))
            return {"returncode": 0, "ok": True}

    monkeypatch.setattr(runner_module, "CityNexusBinaryRunner", FakeRunner)
    scenario = {
        "user_id": "chandigarh_demo",
        "prediction_id": "scenario_002",
        "road_network": {"123": {"geometry": {"type": "LineString", "coordinates": [[76.7,30.7],[76.71,30.71]]}}},
        "grid": {},
        "mobility": {"bicycle_percentage": 8, "evehicle_percentage": 12},
        "day_type": ["weekday"],
        "time_slots": [3],
    }
    result = asyncio.run(ChandigarhModelAdapter(mode="local").run(scenario))
    assert result["returncode"] == 0
    assert "simulation_id" not in captured["payload"]
    assert set(captured["payload"]) == {"grid", "road_network", "scenario"}
    assert captured["payload"]["scenario"]["time slots"] == [3]

def test_intervention_parameters_are_explicit():
    from backend.scenario_engine import ScenarioEngine
    engine = ScenarioEngine()
    base = {"road_network": {"r1": {}}}
    try:
        engine.apply_interventions(base, [{"type": "traffic_signal_coordination", "junctions": ["j1"]}])
    except ValueError as exc:
        assert "cycle_seconds" in str(exc)
    else:
        raise AssertionError("signal cycle was silently defaulted")


def test_nic_source_attributes_are_preserved_without_semantic_guessing(tmp_path):
    import json, subprocess, sys
    src = tmp_path / "roads.geojson"
    src.write_text(json.dumps({"features": [{"properties": {"OBJECTID": 1, "SL": 40, "Name": "Example"}, "geometry": {"type": "LineString", "coordinates": [[76.7,30.7],[76.71,30.71]]}}]}))
    out = tmp_path / "citynexus.json"
    subprocess.run([sys.executable, "tools/convert_nic_roads_to_citynexus.py", str(src), str(out)], check=True)
    result=json.loads(out.read_text())
    road=result["road_network"]["1"]
    assert road["source_SL"] == 40
    assert road["geometry"]["type"] == "LineString"
    assert "speed" not in road


if __name__ == "__main__":
    import tempfile
    from pathlib import Path
    test_upstream_contract()
    test_missing_scenario_input_is_rejected()
    test_mock_execution_is_disabled()
    test_intervention_parameters_are_explicit()
    with tempfile.TemporaryDirectory() as d:
        test_nic_source_attributes_are_preserved_without_semantic_guessing(Path(d))
    print("contract tests: PASS")
