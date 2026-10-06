from __future__ import annotations

from copy import deepcopy
from typing import Any


class ScenarioEngine:
    """Original Chandigarh intervention layer.

    CITYNEXUS supplies the reusable simulation capability; this class owns the
    Chandigarh-side intervention semantics and scenario comparison.
    """

    def apply_interventions(
        self, base: dict[str, Any], interventions: list[dict[str, Any]]
    ) -> dict[str, Any]:
        scenario = deepcopy(base)

        for intervention in interventions:
            kind = intervention["type"]

            if kind == "bus_priority":
                self._bus_priority(scenario, intervention)
            elif kind == "traffic_signal_coordination":
                self._signal_coordination(scenario, intervention)
            elif kind == "low_emission_zone":
                self._low_emission_zone(scenario, intervention)
            elif kind == "road_closure":
                self._road_closure(scenario, intervention)
            else:
                raise ValueError(f"Unknown intervention type: {kind}")

        return scenario

    def _bus_priority(self, scenario: dict[str, Any], item: dict[str, Any]) -> None:
        for road_id in item.get("corridor", []):
            road = scenario.setdefault("road_network", {}).get(road_id)
            if road:
                road["bus_priority"] = self._required_value(item, "priority")

    def _signal_coordination(
        self, scenario: dict[str, Any], item: dict[str, Any]
    ) -> None:
        scenario.setdefault("traffic_controls", []).append(
            {
                "type": "signal_coordination",
                "junctions": item.get("junctions", []),
                "cycle_seconds": self._required_value(item, "cycle_seconds"),
            }
        )

    def _low_emission_zone(
        self, scenario: dict[str, Any], item: dict[str, Any]
    ) -> None:
        for road_id in item.get("roads", []):
            road = scenario.setdefault("road_network", {}).get(road_id)
            if road:
                road["low_emission_zone"] = True

    def _road_closure(self, scenario: dict[str, Any], item: dict[str, Any]) -> None:
        for road_id in item.get("roads", []):
            road = scenario.setdefault("road_network", {}).get(road_id)
            if road:
                road["road_open"] = self._required_value(item, "road_open")

    @staticmethod
    def _required_value(item: dict[str, Any], key: str) -> Any:
        if key not in item:
            raise ValueError(f"intervention.{key} is required; no synthetic default is permitted")
        return item[key]

    @staticmethod
    def compare(base: dict[str, Any], intervention: dict[str, Any]) -> dict[str, Any]:
        base_m = base.get("metrics", {})
        intervention_m = intervention.get("metrics", {})
        keys = sorted(set(base_m) | set(intervention_m))

        delta = {}
        for key in keys:
            a = base_m.get(key)
            b = intervention_m.get(key)
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                delta[key] = round(b - a, 4)

        return {
            "baseline": base_m,
            "intervention": intervention_m,
            "delta": delta,
        }
