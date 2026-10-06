# Connecting the real CITYNEXUS mobility model

The upstream CITYNEXUS mobility API uses an asynchronous lifecycle:

1. `POST /api/v1/mobility-model-{project}-{city}/analysis`
2. poll `GET /api/v1/mobility-model-{project}-{city}/analysis/status`
3. retrieve `GET /api/v1/mobility-model-{project}-{city}/analysis`

The Chandigarh adapter now implements this lifecycle. It sends the upstream
`simulation_id` plus `mobility_model_input` contract and does not assume that
`POST` returns final KPIs.

The upstream API's README also documents model-output storage requirements,
including S3 mounting. Therefore the real-model mode requires the corresponding
CITYNEXUS model/data environment; this repository does not package or relabel
European model outputs as Chandigarh data.

Environment variables are in `.env.example`.

## v18 runtime gate

No new runtime integration is required for v18. The existing local and remote paths remain the implementation target for a later controlled connection.

The next runtime acceptance sequence is:

1. obtain authorized access to a CITYNEXUS mobility-model image/artifact;
2. inspect license and image provenance;
3. verify `/run_mobility_model` and `--help`;
4. identify embedded road/grid/model assets;
5. determine city-specificity;
6. execute a known-valid upstream contract test;
7. only then connect Chandigarh inputs;
8. compare returned properties with `result_decoder.py`;
9. calibrate and validate against Chandigarh observations.

A failure at any step must stop the chain rather than trigger a substitute model or synthetic KPI path.
