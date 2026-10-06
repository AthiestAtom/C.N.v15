# Model output and Chandigarh calibration

## What CITYNEXUS actually produces

The CITYNEXUS technical documentation describes road-segment outputs for pollutants and mobility statistics. The documented KPI families include NO2, CO2, NOx, PMx, HC, CO, fuel consumption, traffic speed and occupancy.

The repository's mobility API stores model result ZIPs under `/model_output/<user>/predictions/<prediction>/` and the model runner identifies result files using the `results_simulation_<day>_timeslot_<hour>_*.zip` pattern.

This hybrid does **not** fabricate Chandigarh KPI values. The result decoder only emits a KPI when that property is present in an actual model result.

## Normalization

`backend/result_decoder.py` accepts common property-name variants and normalizes them to:

- `no2_g`
- `co2_g`
- `nox_g`
- `pmx_g`
- `hc_g`
- `co_g`
- `fuel_g`
- `speed_kmh`
- `occupancy`

For emissions/fuel, the current aggregate is a sum across returned road records. For speed and occupancy it is an unweighted mean. These aggregation choices are application-level summaries, not claims about the upstream model's own KPI methodology.

## Calibration

`data/examples/chandigarh_calibration_template.json` is deliberately empty of invented observations. Fill it with measured Chandigarh counts/speeds and source references.

Recommended calibration sequence:

1. Align road IDs/geometry.
2. Align observation windows with CITYNEXUS's 3-hour simulation slots.
3. Compare observed vehicle counts and mean speeds with model outputs.
4. Calibrate demand/road attributes.
5. Hold out a separate set of junctions/time windows for validation.
6. Report MAE/RMSE for speed and count where observations exist.

Planning documents may provide useful context or projected demand, but they must not silently become ground-truth observations.

## v18 acceptance boundary

The decoder is application-ready, but KPI semantics are not considered finally validated until an actual CITYNEXUS result ZIP is inspected. In particular, the project must verify the exact meaning, units, aggregation level and temporal scope of each returned property before presenting it as a Chandigarh KPI.

### Required validation evidence

A completed Chandigarh model run should retain:

1. model image/service identifier and version;
2. input-contract version;
3. source-data manifest/checksums;
4. scenario definition;
5. raw model result archive or permitted reference to it;
6. normalized KPI output;
7. calibration/holdout dataset identifiers;
8. error metrics and validation notes.

Until these exist, historical datasets can demonstrate **calibration readiness**, not model accuracy.
