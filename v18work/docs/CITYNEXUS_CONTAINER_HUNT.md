# CITYNEXUS Mobility-Model Container Hunt

## Finding

The public CITYNEXUS repository does **not** contain the `/run_mobility_model`
executable. The repository's deployment configuration does, however, expose the
actual container registry host and image path used by the deployed service.

### Verified production images

| City | Registry | Tag |
|---|---|---|
| Copenhagen | `registry-ct.prod.desp.space/citynexus/mobility-model-api` | `0.0.10-cph` |
| Bologna | `registry-ct.prod.desp.space/citynexus/mobility-model-api` | `0.0.10-blq` |
| Seville | `registry-ct.prod.desp.space/citynexus/mobility-model-api` | `0.0.10-svq` |
| Aarhus | `registry-ct.prod.desp.space/citynexus/mobility-model-api` | `0.0.10-aar` |

These values come directly from the public CITYNEXUS Helm deployment values.
The same repository also exposes newer `0.0.11-*` development/IVV tags.

## Why this is the missing piece

The upstream mobility API Dockerfile begins with:

```dockerfile
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
```

and then copies only the Python mobility API into that base image. The public
repository therefore does not build `/run_mobility_model` itself. The executable
must already exist in the base image used by the CI build.

The upstream model runner explicitly expects:

```text
/run_mobility_model
```

and the model documentation says the container also contains the road and grid
assets used by the model.

The CI file passes city/model-related variables such as
`MOBILITY_MODEL_COPENHAGEN` and `MOBILITY_MODEL_IMAGE_REPO`, but their values are
not present in the public repository. The external DevSecOps CI template is also
not included publicly; its variables are referenced through
`$DEVSECOPS_TEMPLATES_REPOSITORY` and `$DEVSECOPS_TEMPLATES_REF`.

## Access result from this development environment

The registry hosts could not be resolved from the current runtime:

- `registry-ct.prod.desp.space`
- `registry-ct.dev.desp.space`
- `registry-ct.ivv.desp.space`

The failure is DNS/network access (`Could not resolve host`), not evidence that
the images do not exist. No image was marked as downloaded and no binary was
fabricated or substituted.

## City-specificity assessment

The image tags are explicitly city-specific (`cph`, `blq`, `svq`, `aar`), and the
upstream build sets `MOBILITY_MODEL_CITY_NAME` to the corresponding city. The
model README also states that the container contains the model's road/grid
assets.

Therefore we must **not** assume that a Copenhagen image can simply be fed
Chandigarh data. Before using any demonstration-city image, inspect the image
contents and runtime configuration to determine whether it contains embedded
city-specific model/data assets or a city-generic executable with external
assets.

## Next verification when registry access is available

```bash
# Authenticate only if the DESP/Harbor registry requires credentials.
docker login registry-ct.prod.desp.space

# Pull one known production image.
docker pull registry-ct.prod.desp.space/citynexus/mobility-model-api:0.0.10-cph

# Inspect the image without modifying the source project.
docker run --rm --entrypoint /bin/sh \
  registry-ct.prod.desp.space/citynexus/mobility-model-api:0.0.10-cph \
  -lc 'ls -lh /run_mobility_model; file /run_mobility_model; find / -maxdepth 3 \
  \( -name "roads.geojson" -o -name "grid.geojson" \) -print 2>/dev/null'

# Inspect executable help and dependencies.
docker run --rm --entrypoint /run_mobility_model \
  registry-ct.prod.desp.space/citynexus/mobility-model-api:0.0.10-cph --help
```

Do not copy the executable into the Chandigarh package until its license,
redistribution permission, embedded assets, and city-generic/city-specific
behavior are verified.

## Sources inspected

- `destination-earth/DestinE_ESA_CityNexus/.gitlab-ci.yml`
- `destination-earth/DestinE_ESA_CityNexus/images/mobility-model-api/Dockerfile`
- `destination-earth/DestinE_ESA_CityNexus/model/README.md`
- `destination-earth/DestinE_ESA_CityNexus/deployment/mobility-model-api-*/values.desp-prod.yaml`
- `destination-earth/DestinE_ESA_CityNexus/deployment/mobility-model-api-*/values.desp-dev.yaml`
- `destination-earth/DestinE_ESA_CityNexus/deployment/mobility-model-api-*/values.desp-ivv.yaml`

## v18 access decision

The container hunt is now an **external-access task**, not a reason to rebuild the mobility model. The exact production image references remain recorded in `data/external/CITYNEXUS_IMAGES.yaml`.

The preferred access request is read-only academic access or an approved downloadable artifact. Credentials, tokens and private image layers must never be committed to this repository.

Once access is granted, inspection must precede integration. In particular, a `cph` image must not be used to generate Chandigarh claims merely because its executable accepts the CITYNEXUS input contract.
