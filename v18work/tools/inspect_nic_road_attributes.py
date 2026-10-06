#!/usr/bin/env python3
"""Inspect live NIC Chandigarh road attributes without interpreting undocumented fields."""
from __future__ import annotations
import argparse, json
from collections import Counter
from urllib.parse import urlencode
import requests

DEFAULT_URL="https://webgis1.nic.in/nicstreet/rest/services/roadnetwork/MapServer/6/query"
FIELDS=["OBJECTID","Name","Road_Type","Class_Code","Lane","Oneway","T_Elevatio","F_Elevatio","Minute","Meter","SL","Remarks","Bridge_Fly","Shape_Length"]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--where", default="1=1")
    ap.add_argument("--limit", type=int, default=2000)
    ap.add_argument("--output")
    args=ap.parse_args()
    params={"where":args.where,"outFields":",".join(FIELDS),"returnGeometry":"false","f":"json","resultRecordCount":args.limit}
    r=requests.get(args.url,params=params,timeout=60); r.raise_for_status()
    payload=r.json()
    if "error" in payload: raise RuntimeError(payload["error"])
    features=payload.get("features",[])
    report={"source_url":r.url,"feature_count":len(features),"fields":{}}
    for field in FIELDS:
        vals=[f.get("attributes",{}).get(field) for f in features]
        present=[v for v in vals if v not in (None,"")]
        report["fields"][field]={"present":len(present),"missing":len(vals)-len(present),"distinct":len({str(v) for v in present}),"sample_values":list(dict.fromkeys(str(v) for v in present))[:20]}
    print(json.dumps(report,indent=2))
    if args.output:
        with open(args.output,"w",encoding="utf-8") as fh: json.dump(report,fh,indent=2)

if __name__=="__main__": main()
