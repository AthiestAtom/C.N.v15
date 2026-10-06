# Chandigarh data pipeline

## Road geometry
The package uses the NIC Chandigarh roadnetwork Feature Layer:
`https://webgis1.nic.in/nicstreet/rest/services/roadnetwork/MapServer/6`

Run:
```bash
python tools/download_chandigarh_roads_nic.py --out data/raw/chandigarh_roads.geojson
python tools/convert_nic_roads_to_citynexus.py data/raw/chandigarh_roads.geojson data/processed/chandigarh_mobility_input.json
```

The layer exposes Chandigarh polylines with fields including OBJECTID, Name,
Road_Type, Class_Code, Lane, Oneway, elevation fields and Shape_Length.

## No fabricated calibration data
The converter deliberately does not invent traffic volume, capacity, speed,
or emissions measurements. A default speed is used only where the CITYNEXUS
input contract requires a speed and the source has no usable speed field; this
must be replaced by authoritative speed-limit/observed-speed data before
calibration claims.

## Calibration targets
Chandigarh Master Plan 2031 reports RITES mobility surveys and identifies
Madhya Marg, Udyog Path, Dakshin Marg and other corridors/junctions as
congestion/capacity concerns. Current measurements should be supplied
separately for quantitative validation.

Chandigarh Smart City ITMS is another integration target: its documented
deployment covers major junctions and traffic-monitoring infrastructure.

## Provenance
Store retrieval timestamp, source URL, query/filter, license/terms,
transformation version and checksum with every imported dataset.


## NIC road-field semantics guardrail

The public Chandigarh NIC Feature Layer documents the fields `Road_Type`, `Class_Code`, `Lane`, `Oneway`, `T_Elevatio`, `F_Elevatio`, `Minute`, `Meter`, `SL`, `Remarks`, and `Bridge_Fly`, but its field metadata does not define an expanded meaning for `SL` or the elevation abbreviations. The ingestion layer therefore preserves these values under their source names and does not convert them into speed, tunnel, capacity, or other model semantics. Use `tools/inspect_nic_road_attributes.py` to obtain an empirical attribute report from the live endpoint.

## v18 production-data requirements

Before a result can be labelled a Chandigarh digital-twin simulation, the run must record:

- source URL or dataset identifier;
- retrieval timestamp;
- spatial coverage;
- temporal coverage and study year;
- license/terms;
- transformation script/version;
- checksum where a file is imported;
- mapping from source attributes to CITYNEXUS attributes;
- missing-value treatment.

Historical RITES/MetroCount/CPCB observations remain calibration/validation targets. They are not current live measurements.

## Current completion boundary

Road acquisition is **wired**, not falsely marked as downloaded. The current runtime previously failed public DNS resolution. A future execution environment can run the direct NIC acquisition command. Failure must remain explicit rather than triggering generated replacement data.
