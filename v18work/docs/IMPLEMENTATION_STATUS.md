# Implementation status

## Completed in this hybrid layer

- Chandigarh identity/configuration
- Chandigarh scenario contract
- CITYNEXUS-compatible mobility adapter
- local/remote real-model modes; synthetic KPI/mock execution disabled
- original intervention engine
- baseline-vs-intervention comparison
- Chandigarh API
- frontend city configuration
- attribution boundary

## Added in this assembly pass

- Thin SUMO execution bridge for optional traffic-simulation validation
- Explicit upstream-component boundary and provenance documentation
- Live-data adapter boundary with source/license/retrieval metadata requirements

## Still required before a competition-grade submission

1. Deploy/connect the actual CITYNEXUS mobility service configured for Chandigarh.
2. Build Chandigarh road-network input from authoritative/open Chandigarh GIS/OSM data.
3. Validate road IDs and attributes against the model's expected schema.
4. Calibrate mobility assumptions using Chandigarh-relevant observations.
5. Add real emissions/environmental coupling where the selected CITYNEXUS pipeline supports it.
6. Add scenario visualisation and KPI charts.
7. Run baseline validation against observed traffic indicators.
8. Preserve upstream Apache-2.0 notices for any redistributed upstream code.


### Verified upstream contract
The inspected CITYNEXUS mobility example uses `mobility_model_input.grid`,
`mobility_model_input.road_network`, and `mobility_model_input.scenario`, with
`bicycle percentage`, `evehicle percentage`, `day type`, and `time slots`.
The adapter now validates that contract before sending a request.

### Chandigarh road ingestion

`tools/build_chandigarh_road_network.py` can generate the road-network JSON
from OpenStreetMap/Overpass data. The generated network is input data, not
a trained model and must be reviewed/licensed/attributed under the applicable
OSM terms before redistribution.

### Not claimed as complete
The upstream Mobility Model README documents an S3/model-output setup. Until
that upstream model/data environment is actually installed and exercised, this
package does **not** claim that the trained CITYNEXUS mobility model is locally
runnable. `mock` mode is disabled and is not an execution path; the package never emits synthetic KPI observations.

## Latest implementation update

- Verified the upstream CITYNEXUS mobility API lifecycle from its source code.
- Added `backend/citynexus_client.py` implementing submit → status polling → ZIP retrieval.
- Updated `ChandigarhModelAdapter` to emit the upstream `simulation_id` contract.
- Added an executable upstream-contract test.
- Added `.env.example` for real-model configuration.
- Added `docs/REAL_MODEL_CONNECTION.md` documenting the real service boundary.

Remaining for a genuinely Chandigarh-calibrated deployment:

1. Obtain/build the CITYNEXUS model/data runtime required by the selected city/model configuration.
2. Produce authoritative Chandigarh road-network inputs and map their OSM IDs/attributes to the model schema.
3. Calibrate baseline mobility against Chandigarh observations.
4. Decode the actual model-output files into Chandigarh KPI definitions after inspecting the deployed model result properties; no unverified property is treated as a KPI.
5. Couple environmental/flood outputs where the deployed CITYNEXUS pipeline exposes those services.
6. Add the production dashboard and scenario-result visualization.


## v6 data acquisition update

Published Chandigarh observations have now been populated instead of leaving the calibration layer empty. Historical RITES 2011 traffic counts, a 2018 MetroCount/Radar-Gun traffic study, and CPCB 2017 NO2 observations are included under `data/calibration/` and `data/air_quality/`. These are explicitly time-stamped historical calibration targets, not live 2026 measurements.


## Open-data expansion (v9)
- Added public-dataset source registry at `data/external/SOURCES.yaml`.
- Added acquisition script with provenance and explicit no-fabrication behavior: `tools/acquire_open_datasets.py`.
- Added CHETNA-Road NetCDF reader: `backend/chetna_road.py`.
- Added exact NWIC Chandigarh rainfall resource URLs for 2021-2025 and 2026-2030.
- Added Chandigarh sector/ward/boundary and NIC HealthGIS acquisition targets.
- Runtime verification in this environment: public internet/DNS is unavailable, so downloads were not falsely marked successful.
- Contract tests remain passing.


## v11 engineering hardening

- Production model mode now defaults to `remote`; there is no synthetic KPI fallback.
- CITYNEXUS project/city identifiers are required at runtime instead of defaulting to a demonstration city.
- Scenario mobility percentages, day type and time slots must be supplied; no synthetic scenario defaults are inserted.
- NIC road conversion no longer inserts a fabricated speed or other traffic attributes when the source omits them. Source `SL` is preserved as `source_SL` without assuming what the undocumented field means.
- OSM road acquisition now preserves source geometry and source-provided `maxspeed`, `lanes`, and `oneway` values; missing values remain missing.
- Remote acquisition now reads URLs from the source registry and writes SHA-256/provenance records. Failed downloads remain unavailable and cause a non-zero acquisition command result.
- Current execution environment cannot resolve public DNS, so no remote source is falsely marked as downloaded.


## v14 selective CITYNEXUS integration

- Added the upstream CITYNEXUS mobility-input contract and a thin local binary runner, rather than merging the upstream repository wholesale.
- Verified the runner flags against the upstream `model_run.py`: `--json-path`, `--output-path`, optional `--flood-depth-map`, and `--return-od true`.
- The local runner fails when the genuine `/run_mobility_model` binary is unavailable; there is no synthetic fallback.
- Tightened result decoding so a generic `vehicle_count` field is not silently interpreted as occupancy.


- Corrected NIC ingestion: `T_Elevatio` is no longer interpreted as a tunnel flag.
- `T_Elevatio`, `F_Elevatio`, `Minute`, `Meter`, `SL`, `Remarks`, and `Bridge_Fly` are preserved as source attributes until their semantics are established.
- Removed the adapter's artificial `tunnel` requirement from source ingestion.
- Added `tools/inspect_nic_road_attributes.py` to query the authoritative NIC Chandigarh layer and produce an empirical field-coverage/value report without transforming undocumented fields.
- Network auditing is now a source-coverage audit; it does not claim model readiness merely because missing fields were filled.
- No existing CITYNEXUS architecture or source component was removed.


## v16 selective upstream extraction integration

- The C.N.v15 repository was inspected against the extracted CITYNEXUS modules.
- Source-derived reference copies of the upstream input/output contracts and shared types are retained under `integrations/citynexus_upstream/reference/`.
- The local Chandigarh adapter now writes only the inner `mobility_model_input` object to the genuine `run_mobility_model` binary. The API envelope is not passed to the binary.
- The existing Chandigarh result decoder remains the application KPI layer; it was not replaced by the upstream unpacker.
- XAI source remains reference-only and is not enabled until genuine model execution is available.
- No Chandigarh observations, roads, grid cells, demand values, or model outputs were fabricated during this integration.

## v17 CITYNEXUS container-hunt update

- Traced the public deployment manifests to the actual DESP Harbor registry host:
  `registry-ct.prod.desp.space`.
- Verified production mobility-model-api image references for Copenhagen, Bologna,
  Seville, and Aarhus, including their `0.0.10-*` tags.
- Verified development/IVV manifests expose corresponding `0.0.11-*` image tags.
- Confirmed the public Dockerfile uses an external `BASE_IMAGE`, while the public
  repository itself contains no `/run_mobility_model` binary.
- Confirmed the model README says the container also contains road/grid assets.
- Registry access from this runtime failed at DNS resolution; no image or executable
  was falsely claimed as acquired.
- Added `docs/CITYNEXUS_CONTAINER_HUNT.md` and
  `data/external/CITYNEXUS_IMAGES.yaml` with the verified image references.
- City-specificity remains an explicit verification gate before any demonstration
  image is used for Chandigarh.

## v18 documentation/completion freeze

v18 does not introduce a new simulation engine or attempt an unverified registry integration. The purpose of this release is to close the requirements/documentation gap and make the remaining work explicit.

### Documentation now authoritative

- `docs/REQUIREMENTS.md` — complete requirement and acceptance matrix.
- `docs/COMPLETION_MATRIX.md` — current workstream status.
- `docs/DEMO_READINESS.md` — competition/demo acceptance checklist.
- `docs/RELEASE_NOTES_v18.md` — release boundary and explicit non-changes.

### Remaining hard dependencies

1. Authorized access to the genuine CITYNEXUS mobility runtime/artifact.
2. Inspection of city-specific assets and executable interface.
3. Acquisition/validation of Chandigarh road and current observational data.
4. Chandigarh calibration and holdout validation.
5. Genuine model-result visualization.

The architecture and integration boundaries remain intact. No existing working component is intentionally removed or replaced merely to increase the version number.
