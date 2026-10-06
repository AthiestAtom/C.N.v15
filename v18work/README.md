# Chandigarh Urban Digital Twin — Hybrid CITYNEXUS Implementation

This package is the Chandigarh-specific layer for a hybrid implementation based on the
open-source CITYNEXUS architecture.

## Design principle

We reuse the mature CITYNEXUS mobility/model integration where appropriate instead of
reimplementing an existing urban simulation stack. The Chandigarh layer is responsible for:

- Chandigarh-specific input data
- validation and normalization
- scenario definitions
- intervention parameters
- scenario orchestration
- KPI calculation
- Chandigarh-specific output handling
- API contracts
- frontend city defaults

The European demonstration data/model outputs are NOT relabelled as Chandigarh data.

## Upstream relationship

CITYNEXUS:
https://github.com/destination-earth/DestinE_ESA_CityNexus

Its repository is Apache-2.0 licensed. Preserve the upstream LICENSE and required notices
when redistributing upstream-derived source.

This project adds original Chandigarh-specific code under `backend/`, `config/`, `data/`,
`frontend/`, and `docs/`.

## Runtime modes

1. `remote`: call a compatible CITYNEXUS mobility-model endpoint.
2. `local`: connect this layer to a locally deployed CITYNEXUS mobility model.
3. `mock`: disabled. This package does not generate synthetic KPI observations.

Set `CHANDIGARH_MODEL_MODE` to one of these values.

## Quick start

```bash
pip install -r backend/requirements.txt
uvicorn backend.api:app --reload
```

Then:

```text
GET  /health
GET  /api/v1/chandigarh/scenarios
POST /api/v1/chandigarh/simulate
```

## Real CITYNEXUS model connection

The adapter now supports the actual CITYNEXUS mobility API lifecycle rather than assuming a synchronous `/predict` endpoint. See `docs/REAL_MODEL_CONNECTION.md` and `.env.example`.

There is no synthetic KPI fallback. Production/demo execution uses the real model path; missing external inputs cause an explicit failure rather than fabricated data.


## v4 data pipeline
Added NIC Chandigarh road-layer ingestion and conversion into the verified CITYNEXUS mobility contract. The pipeline deliberately does not fabricate traffic or emissions observations.


### Public open-data expansion
The project now registers and can acquire Chandigarh-specific public datasets including DataMeet/India-Geodata municipal boundaries, NIC HealthGIS facilities, NWIC Chandigarh telemetry rainfall, CPCB OGD AQI, and CHETNA-Road 2021 road-emission grids. Acquisition failures are recorded rather than replaced with synthetic data.

## v18 release boundary

v18 freezes the working architecture and completes the project requirements documentation without attempting an urgent last-minute integration of the inaccessible CITYNEXUS mobility container.

Read these files for the authoritative status:

- `docs/REQUIREMENTS.md` — functional/data/model/calibration/security requirements.
- `docs/COMPLETION_MATRIX.md` — workstream-by-workstream completion state.
- `docs/DEMO_READINESS.md` — competition acceptance checklist.
- `docs/RELEASE_NOTES_v18.md` — v18 changes and explicit non-changes.

The project remains honest about its primary external blocker: genuine CITYNEXUS mobility-model execution requires authorized access to the model runtime/artifact. No synthetic Chandigarh KPI fallback is permitted.
