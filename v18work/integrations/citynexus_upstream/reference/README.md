# Selective CITYNEXUS upstream reference

These files are retained as source-derived reference material from
`destination-earth/DestinE_ESA_CityNexus` under its Apache-2.0 license.

They are **not** a wholesale copy of the CITYNEXUS repository. The Chandigarh
application uses a thin local adapter and keeps Chandigarh-specific validation,
data acquisition, and KPI logic separate.

The reference modules document the genuine contracts used by the mobility model:
- `simulation/model_input.py`: input path/serialization helpers
- `simulation/model_output.py`: result ZIP loading/filtering helpers
- `model/generic.py`: `SimulationID` and status types
- `model/mobility_model_input.py`: API input schema
