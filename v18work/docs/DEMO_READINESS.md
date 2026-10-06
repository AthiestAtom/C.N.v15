# Competition Demo Readiness

## Current release: v18

v18 is a **documentation-complete engineering baseline**. It is intentionally frozen before the urgent competition period rather than introducing an unverified CITYNEXUS binary or fabricated Chandigarh results.

## Demo acceptance checklist

### A. Core software

- [x] Chandigarh API starts.
- [x] Scenario contract requires explicit city/day/time context.
- [x] CITYNEXUS-compatible input validation exists.
- [x] Real local and remote model paths exist.
- [x] Synthetic/mock KPI execution is disabled.
- [x] Baseline/intervention comparison exists.
- [x] Third-party attribution boundary exists.

### B. Real data

- [x] Chandigarh historical traffic evidence is packaged.
- [x] Chandigarh historical NO2 evidence is packaged.
- [x] Authoritative NIC road source is registered.
- [x] NWDP rainfall resources are registered.
- [ ] Current road data acquired in the execution environment.
- [ ] Current traffic observations connected.
- [ ] Current AQ observations connected.
- [ ] Required weather/environmental inputs connected.

### C. Genuine CITYNEXUS execution

- [x] Missing binary is explicitly documented.
- [x] Production image references are documented.
- [x] Local runner points at the genuine binary path.
- [ ] Authorized registry/artifact access obtained.
- [ ] Image inspected for city-specific assets.
- [ ] `/run_mobility_model --help` verified.
- [ ] One genuine run completed.
- [ ] Result ZIP contract verified.

### D. Chandigarh validation

- [ ] Road IDs/attributes mapped to model expectations.
- [ ] Calibration parameters fitted from Chandigarh observations.
- [ ] Holdout validation completed.
- [ ] Error metrics reported.
- [ ] No demonstration-city output presented as Chandigarh output.

### E. Presentation

- [x] Architecture and provenance can be explained.
- [ ] Live/real baseline map populated.
- [ ] Intervention controls connected to real model.
- [ ] KPI charts populated from genuine outputs.
- [ ] Before/after comparison shown with source/model provenance.
- [ ] Limitations shown explicitly.

## Hard rule

A demo may show architecture, contracts, source data, historical calibration evidence and a clearly labelled integration state. It must **not** show invented Chandigarh simulation KPIs merely to make the demo appear complete.
