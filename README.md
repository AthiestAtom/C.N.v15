# Chandigarh CityNexus v15 – Genuine CITYNEXUS Model I/O Integration

**Status:** ✅ Ready to integrate | ⏳ Waiting on: `run_mobility_model` binary

---

## 📦 What's in This Package

### Core CITYNEXUS Modules (Ready to Use)

```
citynexus-model-core/
├── simulation/
│   ├── model_input.py          (84 lines)  ← Input adapter
│   ├── model_output.py         (153 lines) ← Result unpacker
│   ├── model_run.py            (175 lines) ← Reference runner
│   ├── xai_blackbox.py         (137 lines) ← XAI analysis (defer to v16)
│   └── xai_record.py           (55 lines)  ← XAI metadata (defer to v16)
├── model/
│   ├── generic.py              (43 lines)  ← Shared types (SimulationID)
│   └── mobility_model_input.py  (20 lines) ← Schema definitions
├── pyproject.toml              (49 lines)  ← Dependencies
└── MODEL_DOCS.md               (247 lines) ← Official CITYNEXUS reference
```

### Documentation & Guides

```
├── CITYNEXUS_INTEGRATION_GUIDE.md   (243 lines) ← Comprehensive integration manual
├── QUICK_CHECKLIST.md              (190 lines) ← Implementation checklist
├── v15_INTEGRATION_EXAMPLE.py       (355 lines) ← Complete code example
└── README.md                        (this file)
```

**Total:** ~1,750 lines of documentation + core Python modules (37 KB)

---

## 🚀 Get Started in 5 Steps

### 1. Read This First (2 min)
→ **QUICK_CHECKLIST.md** – Overview + immediate integration points

### 2. Understand the Architecture (10 min)
→ **CITYNEXUS_INTEGRATION_GUIDE.md** – Full context + contracts

### 3. See Working Code (5 min)
→ **v15_INTEGRATION_EXAMPLE.py** – Copy-paste skeleton for your runner

### 4. Check Official Docs (5 min)
→ **citynexus-model-core/MODEL_DOCS.md** – `run_mobility_model` CLI reference

### 5. Integrate Now (30 min)
1. Copy `citynexus-model-core/` into your project
2. Import + adapt the example code
3. Find the `run_mobility_model` binary
4. Wire up your Chandigarh road/grid data
5. Run the simulation

---

## 🎯 The Three Integration Points

### Point 1: INPUT (Chandigarh Data → JSON)
```python
from citynexus.adapters.mobility_model.simulation.model_input import (
    store_input_file, derive_input_file_path
)

# Your Chandigarh road modifications, grid, scenario
store_input_file(derive_input_file_path(sim_id), model_input)
```

**Input Contract:**
```json
{
  "road_network": { "road_id": { "speed": 50, "closed": false } },
  "grid": { "h3_cell": { "landuse": {...}, "pois": {...}, "population": {...} } },
  "scenario": { "day type": ["weekday"], "time slots": [9], "bicycle percentage": 0.05 }
}
```

### Point 2: EXECUTION (Model Binary)
```bash
/run_mobility_model \
  --json-path /model_input/user_123_pred_456.json \
  --output-path /model_output/user_123/predictions/pred_456/ \
  --file-name results_simulation \
  --fast-simulation true
```

**Status:** ❌ Binary not included – see section below

### Point 3: OUTPUT (Result ZIP → KPIs)
```python
from citynexus.adapters.mobility_model.simulation.model_output import (
    find_latest_file, load_result_zip, load_as_geodf, filter_time_slot
)

gdf = load_result_zip(result_zip, load_as_geodf)
gdf_filtered = filter_time_slot(gdf, "weekday", 9)
# → GeoDataFrame with occupancy, speed, no2, co2, geometry per road
```

**Output Contract:** GeoDataFrame (road segment features with KPIs)

---

## ❌ What's Still Missing

### The `run_mobility_model` Binary
- **Status:** Not included in this package (compiled executable)
- **Size:** ~50-200 MB
- **Location:** ESA/Solenix Docker image or compiled release
- **How to get:** 
  1. Check GitLab CI artifacts from CITYNEXUS project
  2. Extract from Docker image: `docker run --rm -v /tmp:/tmp <image> cp /run_mobility_model /tmp/`
  3. Contact ESA/Solenix directly
  4. Compile from source (if source available)

### Chandigarh-Specific Data
You need to provide:
- **Road network** (GeoJSON): Chandigarh roads with OSM IDs, geometries, speeds
- **Grid/H3 cells** (GeoJSON): Cell IDs with landuse, POI counts, population
- **Demand patterns**: Origin-destination matrices or population-based generation

---

## 📋 File Summary

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| **QUICK_CHECKLIST.md** | 190 | Start here – 3 integration points + missing items | ✅ Read first |
| **CITYNEXUS_INTEGRATION_GUIDE.md** | 243 | Comprehensive manual + contracts + phases | ✅ Reference |
| **v15_INTEGRATION_EXAMPLE.py** | 355 | Full working code example (copy-paste) | ✅ Adapt this |
| **citynexus-model-core/simulation/model_input.py** | 84 | Input adapter (serialize → JSON) | ✅ Use this |
| **citynexus-model-core/simulation/model_output.py** | 153 | Result unpacker (ZIP → GeoDataFrame) | ✅ Use this |
| **citynexus-model-core/simulation/model_run.py** | 175 | Reference subprocess runner | ✅ Reference only |
| **citynexus-model-core/simulation/xai_blackbox.py** | 137 | XAI analysis (what-if) | 🟡 Defer to v16 |
| **citynexus-model-core/simulation/xai_record.py** | 55 | XAI metadata | 🟡 Defer to v16 |
| **citynexus-model-core/model/generic.py** | 43 | Shared types (SimulationID, etc.) | ✅ Use as-is |
| **citynexus-model-core/model/mobility_model_input.py** | 20 | Schema definitions | ✅ Use as-is |
| **citynexus-model-core/MODEL_DOCS.md** | 247 | Official CITYNEXUS reference | ✅ Keep for reference |
| **citynexus-model-core/pyproject.toml** | 49 | Python dependencies | ✅ Check deps |

---

## 🔗 Integration Flow (v15)

```
Your Chandigarh Data
    ↓
[Your Adapter Code]
    ↓
simulation.model_input.store_input_file() ←─ use this
    ↓
/model_input/{user_id}_{prediction_id}.json
    ↓
./run_mobility_model --json-path ... --output-path ... ←─ need binary!
    ↓
/model_output/{user_id}/predictions/{prediction_id}/results_simulation_*.zip
    ↓
simulation.model_output.load_result_zip() ←─ use this
    ↓
GeoDataFrame (occupancy, speed, no2, co2, geometry)
    ↓
Your KPI Dashboard
```

---

## ⚡ Quick Start (TL;DR)

1. **Copy code:**
   ```bash
   cp -r citynexus-model-core/simulation citynexus-model-core/model YOUR_PROJECT/
   ```

2. **Adapt example:**
   Open `v15_INTEGRATION_EXAMPLE.py`, replace:
   - `road_modifications` with your Chandigarh roads
   - `grid_data` with your H3 cells
   - `scenario_params` with user input

3. **Run it:**
   ```bash
   python v15_INTEGRATION_EXAMPLE.py
   ```

4. **Get binary:**
   - Ask ESA/Solenix or check Docker image
   - Place at `/run_mobility_model`

5. **Done!** Results flow to your dashboard.

---

## 🎓 Key Concepts

### SimulationID
Deterministic identifier for reproducibility:
```python
SimulationID(user_id="user_123", prediction_id="pred_456")
# → Paths: /model_input/user_123_pred_456.json
#           /model_output/user_123/predictions/pred_456/
```

### Time Windows
Model results tagged by day type + time slot:
```
time_window: "weekday_9"  (weekday, 9:00-10:00)
time_window: "weekend_18" (weekend, 18:00-19:00)
```

### Result Columns
Each road segment in result:
- `road_id`: Road identifier
- `occupancy`: Ratio of vehicles to capacity (0.0-1.0)
- `speed`: Average speed (km/h)
- `no2`: Nitrogen dioxide concentration (µg/m³)
- `co2`: Carbon dioxide emissions (g/km)
- `time_window`: "weekday_9", "weekend_18", etc.
- `geometry`: LineString (road shape)

---

## 🔄 Version Tracking

- **v15 (Current):** Genuine CITYNEXUS I/O adapters ready
- **v15.1:** Result unpacking integrated → dashboard receives KPIs
- **v15.2:** Binary execution working → end-to-end simulation
- **v16:** XAI framework (what-if analysis) + Chandigarh tuning

---

## 📞 Support

### I have the binary, now what?
→ See `v15_INTEGRATION_EXAMPLE.py` (copy-paste + adapt)

### I don't have Chandigarh road data yet
→ Start with mock data in the example, wire up real data later

### Results don't look right
→ Check:
1. Is `run_mobility_model` returning code 0?
2. Is result ZIP in expected path?
3. Do road IDs match between input JSON and results?
4. Are time_window values correct (e.g., "weekday_9")?

### I want to add XAI (what-if analysis)
→ See `simulation/xai_blackbox.py` and `v16+` (not v15)

---

## 📂 Directory After Integration

```
your-project/
├── citynexus/
│   ├── adapters/
│   │   └── mobility_model/
│   │       ├── simulation/
│   │       │   ├── model_input.py      (from citynexus-model-core/)
│   │       │   ├── model_output.py
│   │       │   ├── model_run.py
│   │       │   └── xai_*.py
│   │       └── model/
│   │           ├── generic.py
│   │           └── mobility_model_input.py
│   ├── runners/
│   │   └── v15_mobility_runner.py      (your adapter, based on example)
│   └── dashboard/
│       └── kpi_layer.py                (connects to output)
├── data/
│   ├── chandigarh_roads.geojson
│   ├── chandigarh_grid.geojson
│   └── scenarios.json
└── README.md
```

---

**Status: Ready to integrate. Missing: binary. Timeline: 1-2 days once binary is sourced. 🚀**

---

*Questions? Check CITYNEXUS_INTEGRATION_GUIDE.md for detailed context, or reference the official MODEL_DOCS.md for the mobility model's command-line interface.*

---

## Deployment setup (frontend + backend)

### Frontend (GitHub Pages)

- Static dashboard files live in `/web`.
- Pages deployment workflow: `.github/workflows/pages.yml`
- Expected project-site URL after Pages is enabled:
  - `https://athiestatom.github.io/C.N.v15/`
- The frontend uses relative asset paths (`./...`) so it works under the `/C.N.v15/` base path.

#### Frontend API base URL configuration

Set the backend URL in `web/config.js`:

```js
window.CITYNEXUS_CONFIG = {
  apiBaseUrl: "https://your-backend.example.com"
};
```

- Leave empty to disable API calls until backend is configured.
- Do not hard-code localhost in production Pages deployments.

### Backend (containerized API)

- FastAPI entry point: `mobility_model_api/api/app.py`
- Health endpoint: `GET /health`
  - Returns `status: "degraded"` when `run_mobility_model` is missing.
- Simulation endpoint: `POST /simulate`
  - Preserves existing model input/output flow using existing adapters.

Environment variables:

- `MODEL_INPUT_BASE_PATH` (default `/model_input`)
- `MODEL_OUTPUT_BASE_PATH` (default `/model_output`)
- `MODEL_BIN_PATH` (default `/run_mobility_model`)
- `HOST` (default `0.0.0.0`)
- `PORT` (default `8000`)

Container assets:

- `Dockerfile`
- `.dockerignore`
- `requirements.txt`

Workflow for build/test/publish to GHCR:

- `.github/workflows/backend-container.yml`
- On pull requests: validates and builds image without push.
- On pushes to `main`: pushes to `ghcr.io/<owner>/<repo>/backend` when package permissions allow.

### Live vs deployment-ready

- **Live automatically after merge + repo settings**:
  - Frontend on GitHub Pages (once Pages is enabled for GitHub Actions in repository settings).
- **Deployment-ready but not guaranteed live yet**:
  - Backend container build/publish workflow.
  - Runtime hosting target for persistent API (e.g., Azure, AWS, Render, Fly.io, VPS) still requires one-time platform setup.

### One-time manual setup still required

1. Enable GitHub Pages source as **GitHub Actions** in repository settings.
2. Choose and configure a persistent backend host.
3. Provide `run_mobility_model` executable on that host/container image path and set `MODEL_BIN_PATH` if different.
4. Set `web/config.js` `apiBaseUrl` to the deployed backend URL.
