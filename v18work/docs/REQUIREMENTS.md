# CITYNEXUS Chandigarh v18 Requirements and Completion Matrix

**Release:** v18 documentation/completion freeze  
**Scope:** documentation, requirements, acceptance criteria and project-readiness bookkeeping.  
**Important:** v18 does **not** attempt to obtain, integrate, or execute the unavailable CITYNEXUS mobility binary.

## 1. Functional requirements

| ID | Requirement | Status | Acceptance condition |
|---|---|---|---|
| FR-01 | Represent Chandigarh as the target city | COMPLETE | Chandigarh configuration and API require explicit city context. |
| FR-02 | Accept Chandigarh road/network inputs | COMPLETE/VERIFY | NIC/OSM acquisition and conversion tooling exists; source attributes are preserved. |
| FR-03 | Validate CITYNEXUS mobility input contract | COMPLETE | Inner `mobility_model_input` contract is validated before real-model execution. |
| FR-04 | Submit a real CITYNEXUS simulation | INTEGRATED, NOT EXECUTED | Local runner and remote lifecycle are implemented; genuine model runtime remains unavailable. |
| FR-05 | Prevent synthetic KPI fallback | COMPLETE | Mock execution is disabled and missing real model results fail explicitly. |
| FR-06 | Run baseline vs intervention scenarios | COMPLETE | Scenario engine produces a comparison from actual returned model results. |
| FR-07 | Normalize returned mobility/emissions KPIs | COMPLETE/VERIFY AGAINST MODEL | Decoder accepts documented result-property variants; final KPI mapping must be checked against the acquired model output. |
| FR-08 | Use Chandigarh calibration observations | PARTIAL | Historical traffic/AQ datasets are present; current observations and final calibration remain outstanding. |
| FR-09 | Ingest weather/rainfall | PARTIAL | Direct NWDP resources are registered; runtime acquisition depends on network/API availability. |
| FR-10 | Ingest current air quality | PARTIAL | Source/adaptor boundary exists; production current-feed credentials/access still need verification. |
| FR-11 | Ingest current traffic/ITMS data | PARTIAL | Integration target identified; no public raw feed is claimed without evidence. |
| FR-12 | Support transit state | PARTIAL | Endpoint-configurable boundary is planned; no live endpoint is fabricated. |
| FR-13 | Support emergency/health facilities | PARTIAL | Public facility source identified; production live-state integration remains. |
| FR-14 | Provide scenario-result visualization | PARTIAL | Frontend city shell exists; live model-result visualization remains to be completed. |
| FR-15 | Preserve provenance and licenses | COMPLETE | Source registries, notices and acquisition provenance requirements are documented. |

## 2. Data requirements

A competition-grade Chandigarh run requires, at minimum:

1. authoritative or appropriately licensed road geometry;
2. road attributes required by the selected CITYNEXUS model;
3. observed traffic counts/speeds for calibration and holdout validation;
4. an explicitly defined simulation day type and time window;
5. current or appropriately time-aligned air-quality observations for environmental validation;
6. meteorological/rainfall inputs when required by the selected scenario/model path;
7. population/grid/service data when the selected CITYNEXUS deployment exposes those KPIs;
8. documented provenance, retrieval time and license/terms for every external dataset.

Missing values must remain missing or cause a controlled failure. They must not be filled with invented Chandigarh observations.

## 3. Model requirements

The selected mobility runtime must provide or expose:

- the documented CITYNEXUS mobility input contract;
- `/run_mobility_model` or an equivalent supported service interface;
- model output ZIP/results compatible with the decoder after contract verification;
- the required model/grid/road assets;
- a license or usage permission permitting the intended academic use;
- enough configuration information to determine whether the model is generic or city-specific.

A demonstration-city model is **not automatically a Chandigarh model**. Portability must be established before Chandigarh results are claimed.

## 4. Calibration requirements

Calibration is accepted only when:

- road identifiers/geometries are aligned;
- observation and simulation windows are comparable;
- calibration data are identified by source and study year;
- a holdout set is kept separate from fitted observations;
- speed/count errors are reported using MAE/RMSE or another explicitly stated metric;
- the final model configuration and calibration parameters are recorded.

Historical 2011/2018 traffic and 2017 NO2 data are calibration/validation evidence, not 2026 live observations.

## 5. Scenario requirements

Each submitted scenario must explicitly identify:

- city;
- day type;
- simulation time slots;
- mobility assumptions;
- road/intervention changes;
- environmental/flood inputs where applicable;
- baseline/reference scenario;
- intervention scenario;
- output provenance.

No scenario may silently inherit a demonstration city's defaults.

## 6. Security and integrity requirements

- No credentials are committed to the repository.
- Private registry access must be supplied externally through approved authentication.
- Registry artifacts must be inspected before redistribution.
- Third-party licenses/notices must remain intact.
- Failed network acquisition must not trigger synthetic data generation.

## 7. v18 release gate

v18 is considered **documentation-complete**, not simulation-complete.

The remaining hard gate for a genuine end-to-end Chandigarh simulation is access to and verification of the actual CITYNEXUS mobility runtime/model assets. The project must not claim a completed digital-twin simulation until that gate is passed and Chandigarh calibration/validation has been performed.
