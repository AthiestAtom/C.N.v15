# Selected CITYNEXUS upstream components

This directory contains only two selectively reused components from the upstream
CITYNEXUS repository, rather than a wholesale repository merge:

- `mobility_model_input.py`: upstream mobility API contract.
- `binary_runner.py`: the reusable local process-execution portion of upstream
  `model_run.py`, adapted only to remove dependencies on upstream XAI modules.

Upstream project: `destination-earth/DestinE_ESA_CityNexus`
License: Apache-2.0.

The Chandigarh application remains responsible for acquiring and validating
Chandigarh-specific data. No upstream demonstration-city observations are
relabelled as Chandigarh data.
