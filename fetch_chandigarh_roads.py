#!/usr/bin/env python3
"""
Fetch real OpenStreetMap road features for Chandigarh through Overpass API.

This produces a source snapshot for inspection and mapping; it does NOT fabricate
traffic speeds, demand, population, emissions, or CITYNEXUS model outputs.
Usage: python scripts/fetch_chandigarh_roads.py
"""
from __future__ import annotations
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
OUT = Path("data/chandigarh_osm")
QUERY = r"""
[out:json][timeout:90];
area["name"="Chandigarh"]["boundary"="administrative"]["admin_level"~"4|6|8"]->.a;
(
  way(area.a)["highway"];
);
out body;
>;
out skel qt;
"""

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    payload = urllib.parse.urlencode({"data": QUERY}).encode()
    last_error = None
    for endpoint in ENDPOINTS:
        req = urllib.request.Request(
            endpoint, data=payload,
            headers={"User-Agent": "CITYNEXUS-Chandigarh-research/1.0 (open-data prototype)"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                raw = response.read()
                source_url = endpoint
            data = json.loads(raw)
            if not isinstance(data.get("elements"), list):
                raise ValueError("Overpass response has no elements array")
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            raw_path = OUT / f"overpass_roads_{stamp}.json"
            raw_path.write_bytes(raw)
            metadata = {
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "source": source_url,
                "query": QUERY.strip(),
                "raw_file": str(raw_path),
                "element_count": len(data["elements"]),
                "note": (
                    "Raw OSM response only. Not a validated CITYNEXUS road_network/grid "
                    "input. No traffic observations or model outputs are inferred."
                ),
            }
            (OUT / "latest_metadata.json").write_text(
                json.dumps(metadata, indent=2), encoding="utf-8"
            )
            print(json.dumps(metadata, indent=2))
            print("Next: inspect boundary matches and convert way/node elements into "
                  "road geometries with stable OSM way IDs; do not invent speed/demand values.")
            return 0
        except Exception as exc:
            last_error = f"{endpoint}: {type(exc).__name__}: {exc}"
            print(last_error, file=sys.stderr)
            time.sleep(2)
    print("All Overpass endpoints failed. No dataset was created.", file=sys.stderr)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
