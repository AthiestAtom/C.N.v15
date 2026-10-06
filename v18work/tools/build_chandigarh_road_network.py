"""Build a Chandigarh road-network input from an authoritative OSM/Overpass query.

No traffic counts, capacities, speeds, or emissions are fabricated. OSM attributes
are copied when present; missing attributes remain missing and are reported.
"""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
import requests

OVERPASS = "https://overpass-api.de/api/interpreter"
BBOX = (30.64, 76.70, 30.80, 76.90)
QUERY = """[out:json][timeout:120];way[\"highway\"]({s},{w},{n},{e});out tags geom;"""


def parse_speed(tags: dict):
    raw = str(tags.get("maxspeed", "")).split(";")[0].strip()
    if not raw:
        return None
    try:
        value = float(raw.split()[0])
    except (ValueError, IndexError):
        return None
    unit = raw.split()[1].lower() if len(raw.split()) > 1 else "km/h"
    if unit in {"mph", "mi/h"}:
        value *= 1.609344
    return value


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--bbox", nargs=4, type=float, default=BBOX, metavar=("S", "W", "N", "E"))
    args = ap.parse_args()
    s, w, n, e = args.bbox
    response = requests.post(OVERPASS, data=QUERY.format(s=s, w=w, n=n, e=e), timeout=180)
    response.raise_for_status()
    elements = response.json()["elements"]

    roads = {}
    missing_speed = 0
    for element in elements:
        tags = element.get("tags", {})
        speed = parse_speed(tags)
        road = {
            "source": "OpenStreetMap",
            "osm_id": str(element["id"]),
            "highway": tags.get("highway"),
            "oneway": tags.get("oneway"),
            "lanes": tags.get("lanes"),
            "maxspeed": speed,
            "geometry": element.get("geometry", []),
        }
        if speed is None:
            missing_speed += 1
        roads[str(element["id"])] = road

    out = {
        "source": "OpenStreetMap via Overpass",
        "generated_at_unix": int(time.time()),
        "road_network": roads,
        "quality": {
            "road_count": len(roads),
            "missing_maxspeed_count": missing_speed,
            "missing_maxspeed_fraction": missing_speed / len(roads) if roads else None,
        },
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {len(roads)} roads to {path}; missing OSM maxspeed: {missing_speed}")


if __name__ == "__main__":
    main()
