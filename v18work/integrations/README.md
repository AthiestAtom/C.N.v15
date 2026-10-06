# Reused simulation/data boundaries

This directory deliberately contains **adapters**, not a reimplementation of the
upstream projects.

## CITYNEXUS
The main production mobility/environmental simulation remains the CITYNEXUS service
connected through `backend/citynexus_client.py`.

## SUMO
`sumo_runner.py` is a thin execution bridge around the existing SUMO simulator. SUMO
is the mature traffic simulator used by CITYNEXUS and is also the simulation engine
behind the MIT-licensed `SUMO_LLM_Agent` project.

Upstream project: https://github.com/xuyimingxym/SUMO_LLM_Agent
License: MIT for that repository's own source. SUMO has its own licensing/attribution.

## UrbanSync
UrbanSync was inspected as an implementation reference for live traffic, weather,
hospital, transit and what-if ingestion patterns. Its GitHub repository currently has
no declared repository license, so its source code is **not copied** here.

Upstream: https://github.com/RahulBansal-24/Urbansync

## MARGDARSHAK
MARGDARSHAK was inspected as an architecture reference for coupled flood → traffic →
air-quality risk propagation. Its trained Chennai outputs are not relabelled as
Chandigarh outputs.

Upstream: https://github.com/yashaswi15/PROJECT---MARGDARSHAK
