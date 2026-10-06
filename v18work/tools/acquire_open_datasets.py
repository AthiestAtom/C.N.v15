#!/usr/bin/env python3
"""Acquire Chandigarh public datasets with provenance; never synthesizes missing data."""
from __future__ import annotations
import argparse, json, os
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data'/'raw'
RAW.mkdir(parents=True,exist_ok=True)
TIMEOUT=120

URLS={
 'sectors.geojson':'https://raw.githubusercontent.com/datameet/Municipal_Spatial_Data/master/Chandigarh/Chandigarh_Sectors.geojson',
 'wards.geojson':'https://raw.githubusercontent.com/datameet/Municipal_Spatial_Data/master/Chandigarh/Chandigarh_Wards.geojson',
 'boundary.geojson':'https://raw.githubusercontent.com/datameet/Municipal_Spatial_Data/master/Chandigarh/Chandigarh_Boundary.geojson',
 'rainfall_2021_2025.csv':'https://nwdp.nwic.gov.in/dataset/83507a8e-ffc0-46d9-b041-f109248a1f79/resource/8964fc68-3716-4422-a031-14ad16e21f91/download/rainfall_tel_hr_punjab_sw_ch_2021_2025.csv',
 'rainfall_2026_2030.csv':'https://nwdp.nwic.gov.in/dataset/83507a8e-ffc0-46d9-b041-f109248a1f79/resource/033c0be0-e8a6-44cc-ba6e-e927d6184e47/download/rainfall_tel_hr_punjab_sw_ch_2026_2030.csv',
 'healthcare_facilities.geojson':'https://github.com/yashveeeeeer/india-geodata/releases/download/healthcare%2Ffacilities/INDIA_HEALTH_FACILITIES_NIC.geojson',
}

def fetch(name,url):
    out=RAW/name
    if out.exists() and out.stat().st_size>0:
        return {'name':name,'status':'already_present','path':str(out)}
    try:
        with requests.get(url,stream=True,timeout=TIMEOUT,headers={'User-Agent':'CITYNEXUS-Chandigarh/1.0'}) as r:
            r.raise_for_status()
            with out.open('wb') as f:
                for chunk in r.iter_content(1024*1024):
                    if chunk: f.write(chunk)
        return {'name':name,'status':'downloaded','path':str(out),'bytes':out.stat().st_size,'url':url}
    except Exception as e:
        if out.exists() and out.stat().st_size==0: out.unlink()
        return {'name':name,'status':'unavailable','url':url,'error':str(e)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--only',action='append',choices=list(URLS)); args=ap.parse_args()
    selected=args.only or list(URLS)
    results=[fetch(k,URLS[k]) for k in selected]
    stamp=ROOT/'data'/'raw'/'acquisition_manifest.json'
    stamp.write_text(json.dumps({'sources':results},indent=2))
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
