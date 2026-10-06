# Live-data boundary

This folder is intentionally empty of fabricated live observations.

Expected adapters can populate:

- traffic incidents / road closures
- weather and rainfall
- current AQ observations
- public transit state
- emergency-facility state

Each adapter should record `source`, `retrieved_at`, `coverage`, and `license` before
its data are allowed into a simulation run.
