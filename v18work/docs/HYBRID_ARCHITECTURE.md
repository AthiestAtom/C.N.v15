# Hybrid architecture

```text
                  Chandigarh source data
                           |
             +-------------+-------------+
             |                           |
       road/network data          scenario inputs
             |                           |
             +------------+--------------+
                          |
                  Chandigarh Adapter
                          |
                  Canonical model input
                          |
             +------------+-------------+
             |                          |
       CITYNEXUS mobility        Chandigarh KPI layer
       model / compatible       + intervention logic
       model service                    |
             |                          |
             +-------------+------------+
                           |
                    Scenario results
                           |
                 Chandigarh API / UI
```

## What is reused

- Existing urban mobility model service interface
- Existing model execution concept
- Existing simulation output concepts

## What is new in this layer

- Chandigarh city identity/configuration
- Chandigarh data contract
- Chandigarh road/scenario normalization
- intervention schema
- scenario comparison
- KPI aggregation
- validation
- API boundary
- city-specific UI state

## Why this is preferable

There is no engineering value in rewriting a proven mobility simulation engine merely to
make the source tree look unrelated. The novelty is the Chandigarh digital-twin layer,
local data/model calibration, intervention design, and decision-support pipeline.
