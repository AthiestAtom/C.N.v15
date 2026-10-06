# Hybrid assembly

## What is actually being assembled

1. **CITYNEXUS** supplies the main urban digital-twin / mobility / environmental
   simulation capability.
2. **SUMO** supplies mature microscopic traffic simulation where the CITYNEXUS
   deployment exposes or needs a direct traffic-simulation path.
3. **Chandigarh data adapters** supply local road geometry, traffic observations,
   air-quality observations and scenario parameters.
4. **UrbanSync patterns** inform live-feed adapters, routing and operational dashboard
   behaviour; its source is not copied because the repository has no declared license.
5. **MARGDARSHAK patterns** inform future cross-domain cascade handling; its trained
   Chennai models are not used as Chandigarh predictions.

## Runtime path

```text
Chandigarh OSM/GIS + traffic + AQ observations
                    |
                    v
          Chandigarh scenario contract
                    |
          +---------+---------+
          |                   |
          v                   v
      CITYNEXUS             SUMO bridge
      production            validation /
      simulation            traffic-only runs
          |                   |
          +---------+---------+
                    v
          baseline vs intervention
                    |
                    v
       normalized Chandigarh KPIs
```

The goal is to **reuse mature engines**, not to recreate their internals.

## v18 completion boundary

The assembly is considered architecturally complete. Remaining implementation is dependency-driven: obtain/verify the genuine CITYNEXUS mobility runtime, acquire current Chandigarh inputs, calibrate/validate, and connect production visualizations. See `REQUIREMENTS.md`, `COMPLETION_MATRIX.md`, and `DEMO_READINESS.md`.

v18 deliberately does not integrate an unverified registry image during the competition crunch. The existing runner remains ready for later connection.
