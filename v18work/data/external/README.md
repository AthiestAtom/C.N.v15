# External Chandigarh sources

The project uses direct first-party/public URLs where machine-readable endpoints are available. The application may fetch these at runtime; it does not replace failed requests with synthetic observations.

## Direct sources

- NIC Chandigarh road layer: `data/external/REMOTE_URLS.yaml`
- BBMB Chandigarh rainfall telemetry 2021-2025: direct CSV URL in `REMOTE_URLS.yaml`
- BBMB Chandigarh rainfall telemetry 2026-2030: direct CSV URL in `REMOTE_URLS.yaml`

The National Water Data Portal identifies the BBMB Chandigarh rainfall resources as CSV/API datasets and records their update dates and open licensing metadata. The NIC road layer supports GeoJSON queries and exposes road attributes including road type, lane, one-way and elevation fields.

## v18 data-acceptance rule

A source is considered **registered** when its URL, provenance and intended use are documented. It is considered **acquired** only after the runtime successfully retrieves it and records a checksum/provenance entry. These states must not be conflated.

For competition use, every current-data adapter must expose the source timestamp and coverage alongside the data. Historical calibration datasets must retain their study year.
