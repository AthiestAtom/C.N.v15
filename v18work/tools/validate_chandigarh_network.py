#!/usr/bin/env python3
"""Audit a Chandigarh road network without filling missing attributes.

This validator deliberately reports source coverage rather than inventing
CITYNEXUS/SUMO values. Model readiness is only asserted when the caller has
provided an explicit required-attribute contract.
"""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path

def audit(path: Path) -> int:
    data=json.loads(path.read_text())
    roads=data.get("road_network", {})
    if not isinstance(roads, dict) or not roads:
        print("BLOCKED: road_network is empty")
        return 2
    keys=Counter()
    for road in roads.values():
        if isinstance(road, dict):
            keys.update(road.keys())
    print(f"roads={len(roads)}")
    for key, count in sorted(keys.items()):
        print(f"present_{key}={count}")
    print("status=SOURCE_AUDIT_ONLY")
    print("note=No missing road attribute was synthesized by this audit.")
    return 0

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("network")
    raise SystemExit(audit(Path(ap.parse_args().network)))
