#!/usr/bin/env python3
"""Convert authoritative NIC Chandigarh road GeoJSON without inventing attributes."""
import argparse, json
from pathlib import Path

def main(src, out):
    payload=json.loads(Path(src).read_text())
    roads={}; sidecar=[]
    for f in payload.get("features", []):
        props=f.get("properties") or {}
        rid=props.get("OBJECTID")
        if rid is None:
            continue
        road={"source_object_id": rid}
        # Preserve only source-provided values. Do not invent speed, capacity,
        # lane count, or traffic volume when NIC has not supplied them.
        # Preserve NIC elevation fields verbatim. Their semantics are not documented
        # by the public layer metadata, so they must not be converted into a tunnel
        # flag or any other model attribute here.
        for field in ("T_Elevatio", "F_Elevatio", "Minute", "Meter", "Remarks", "Bridge_Fly"):
            if props.get(field) not in (None, ""):
                road[field] = props[field]
        if props.get("Lane") not in (None, ""):
            road["lane"] = props["Lane"]
        if props.get("Oneway") not in (None, ""):
            road["oneway"] = props["Oneway"]
        if props.get("Road_Type") not in (None, ""):
            road["road_type"] = props["Road_Type"]
        if props.get("Class_Code") not in (None, ""):
            road["class_code"] = props["Class_Code"]
        if props.get("Shape_Length") not in (None, ""):
            road["shape_length"] = props["Shape_Length"]
        if props.get("SL") not in (None, ""):
            road["source_SL"] = props["SL"]
        if props.get("Name") not in (None, ""):
            road["name"] = props["Name"]
        if f.get("geometry") is not None:
            road["geometry"] = f["geometry"]
        roads[str(rid)] = road
        sidecar.append({"road_id":str(rid), **props})
    result={"grid":{},"road_network":roads,"source":{"type":"NIC Feature Layer GeoJSON","input":str(src)}}
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).write_text(json.dumps(result,indent=2))
    Path(str(out)+".metadata.json").write_text(json.dumps(sidecar,indent=2))
    print(f"converted {len(roads)} source road features -> {out}")

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out"); a=ap.parse_args(); main(a.src,a.out)
