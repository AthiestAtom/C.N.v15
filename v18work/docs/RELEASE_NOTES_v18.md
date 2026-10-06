# v18 Release Notes

## Purpose

v18 is the documentation and requirements completion release following the CITYNEXUS container discovery. No new external model is integrated in this release.

## Changes

- Consolidated functional, data, model, calibration, scenario, security and release requirements in `docs/REQUIREMENTS.md`.
- Added `docs/COMPLETION_MATRIX.md` as the single workstream status ledger.
- Added `docs/DEMO_READINESS.md` with a competition-facing acceptance checklist.
- Updated the implementation status to distinguish architecture completion from external-runtime blockers.
- Updated the data pipeline documentation to state the exact requirements for a real Chandigarh run.
- Updated model-output documentation to distinguish decoder readiness from verified real-model output semantics.
- Updated container-hunt documentation to make registry access/inspection the remaining model-runtime gate.
- Preserved the v17 architecture and source-derived CITYNEXUS components; no wholesale upstream merge was performed.

## Explicitly not done in v18

- No CITYNEXUS binary was fabricated.
- No European demonstration-city output was relabelled as Chandigarh.
- No private registry credential was added.
- No unverified container was copied into the repository.
- No synthetic Chandigarh KPI result was added.
- No risky last-minute model integration was performed.
