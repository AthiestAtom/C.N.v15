# v18 Completion Matrix

## Status legend

- **DONE** — implemented and locally verifiable.
- **WIRED** — implementation exists, but requires an external service/data source for execution.
- **PARTIAL** — some required pieces exist; production completion remains.
- **BLOCKED** — dependency is unavailable or access-controlled.
- **VERIFY** — implementation exists but must be validated against the real upstream artifact/data before being declared production-ready.

| Workstream | Status | What exists | What remains |
|---|---|---|---|
| Project architecture | DONE | Hybrid CITYNEXUS + Chandigarh adapter architecture | None at architecture level |
| CITYNEXUS input contract | DONE | Upstream-derived contract and validation | Revalidate against acquired runtime if interface changes |
| CITYNEXUS local runner | WIRED | Real `/run_mobility_model` invocation path | Obtain runtime and execute |
| CITYNEXUS remote client | WIRED | Submit → poll → retrieve lifecycle | Accessible compatible deployment/project/city |
| Genuine mobility binary | BLOCKED | Exact upstream reference and registry image locations documented | Authorized registry/artifact access |
| Model portability | VERIFY | Decision criteria documented | Inspect image/binary/assets |
| Chandigarh roads | WIRED | NIC direct endpoint + conversion/inspection tools | Acquire data in execution environment and validate attributes |
| Traffic calibration | PARTIAL | 2011/2018 published observations | Current data + fitted/held-out validation |
| Air-quality calibration | PARTIAL | CPCB 2017 NO2 observations | Current feed + temporal/spatial validation |
| Rainfall/weather | WIRED | NWDP direct URLs and acquisition boundary | Runtime fetch/API validation |
| Current traffic feed | PARTIAL | Adapter boundary and source research | Authorized/raw endpoint |
| Transit | PARTIAL | Configurable integration boundary | Actual GTFS-RT/public feed |
| Health/emergency | PARTIAL | Facility source identified | Production ingestion/state model |
| SUMO bridge | DONE/WIRED | Thin execution bridge | Actual SUMO run on acquired network |
| Scenario engine | DONE | Baseline/intervention orchestration | Validate with genuine model outputs |
| Result decoder | DONE/VERIFY | Normalization and aggregation layer | Confirm exact properties from real result ZIP |
| KPI validation | PARTIAL | Historical target datasets and metrics plan | Real model + Chandigarh calibration |
| Frontend city shell | DONE | Chandigarh city configuration | Live result charts/maps |
| Live dashboard | PARTIAL | Data/model boundaries documented | Connect validated live/model feeds |
| XAI | DEFERRED | Upstream reference only | Enable only after genuine model execution |
| Provenance/licensing | DONE | Notices, source registry and provenance requirements | Update after every newly acquired artifact |
| Tests | DONE | Contract/compile/package checks | Add runtime integration tests after model access |
| Competition demo | BLOCKED | Architecture and requirements are documented | Genuine model execution + validation + visualization |

## v18 conclusion

The project is **not** 100% simulation-complete. The remaining work is concentrated around external dependencies rather than missing architectural design: genuine CITYNEXUS runtime access, Chandigarh data acquisition, calibration, validation and live-result presentation.
