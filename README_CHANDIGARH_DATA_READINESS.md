# CITYNEXUS Chandigarh: data-readiness work

This small companion bundle advances the Chandigarh-specific data pipeline while
the genuine `run_mobility_model` executable remains unavailable.

## Fetch a real road-network snapshot
Run from the repository root:
```bash
python scripts/fetch_chandigarh_roads.py
```
It queries OpenStreetMap's Overpass API for administrative areas named Chandigarh
and their highway ways, then saves the raw response and retrieval metadata under
`data/chandigarh_osm/`. Internet access is required. Check the matched boundary and
inspect the snapshot before using it.

## Important limitations
- This is raw OSM source data, not a finished CITYNEXUS `road_network`/`grid` input.
- OSM road classes are not observed traffic speeds. No traffic volumes, OD matrix,
  population, pollution, or emissions are fabricated.
- No simulation is run and no impact KPI is claimed.
- Next data tasks: verify boundary selection; construct line geometries keyed by OSM
  way ID; obtain defensible speed/demand/population sources; document each source,
  timestamp, units, coverage and limitations; only then implement the model adapter.
