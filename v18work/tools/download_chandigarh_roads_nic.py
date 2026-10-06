#!/usr/bin/env python3
"""Download Chandigarh road polylines from the NIC roadnetwork Feature Layer."""
import argparse, json, time
from pathlib import Path
import requests
SERVICE="https://webgis1.nic.in/nicstreet/rest/services/roadnetwork/MapServer/6/query"
FIELDS="OBJECTID,Name,Road_Type,Class_Code,Lane,Oneway,T_Elevatio,F_Elevatio,Minute,Meter,SL,Remarks,Bridge_Fly,Shape_Length"
def fetch_all(out: Path, page_size=1000):
    features=[]; offset=0
    while True:
        params={"where":"1=1","outFields":FIELDS,"returnGeometry":"true","f":"geojson",
                "resultOffset":offset,"resultRecordCount":page_size}
        r=requests.get(SERVICE,params=params,timeout=60); r.raise_for_status()
        batch=r.json().get("features",[]); features.extend(batch)
        if len(batch)<page_size: break
        offset += len(batch); time.sleep(.2)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"type":"FeatureCollection","features":features,"source":SERVICE},indent=2))
    print(f"saved {len(features)} road features -> {out}")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="data/raw/chandigarh_roads.geojson")
    fetch_all(Path(ap.parse_args().out))
