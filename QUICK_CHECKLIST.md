# v15 Integration Checklist – Genuine CITYNEXUS Model I/O

## ✅ What You Have Now

| File | Status | Purpose |
|------|--------|---------|
| `simulation/model_input.py` | ✅ Ready | Serialize Chandigarh scenario → JSON input |
| `simulation/model_output.py` | ✅ Ready | Deserialize result ZIP → GeoDataFrame + KPIs |
| `simulation/model_run.py` | ✅ Reference | Example runner pattern (adapt your v15 runner) |
| `model/mobility_model_input.py` | ✅ Schema | Data model definitions |
| `simulation/xai_*.py` | 🟡 Defer | What-if analysis (v16+) |
| `MODEL_DOCS.md` | ✅ Reference | Official `run_mobility_model` command signatures |

---

## 🚀 Immediate Integration (Today)

### 1. Copy Files to Your Project
```bash
# From downloaded citynexus-model-core/
cp -r simulation/ model/ YOUR_CHANDIGARH_REPO/citynexus/adapters/mobility_model/
```

### 2. Update Your v15 Input Adapter
**Where:** Your existing Chandigarh scenario → model input function

**Use these functions:**
```python
from citynexus.adapters.mobility_model.simulation.model_input import (
    store_input_file,
    derive_input_file_path
)

# In your adapter:
simulation_id = SimulationID(user_id="user123", prediction_id="pred_456")
input_file = derive_input_file_path(simulation_id)
store_input_file(input_file, your_scenario_json)
# → Writes to /model_input/user123_pred_456.json (exact CITYNEXUS contract)
```

### 3. Update Your v15 Result Unpacker (NEW)
**Where:** After `run_mobility_model` completes

**Use these functions:**
```python
from citynexus.adapters.mobility_model.simulation.model_output import (
    find_latest_file,
    load_result_zip,
    load_as_geodf,
    filter_time_slot,
    derive_output_path
)

# In your result handler:
output_dir = derive_output_path(simulation_id)  # /model_output/user123/predictions/pred_456/
result_file = find_latest_file(output_dir, "results_simulation_weekday_timeslot_9_*.zip")
gdf = load_result_zip(result_file, load_as_geodf)
gdf_filtered = filter_time_slot(gdf, day_type="weekday", time_slot=9)

# Now gdf_filtered has columns:
# → occupancy, speed, no2, co2, time_window, geometry, road_id
# Map to your KPI dashboard
```

### 4. Adapt model_run.py Execution
**Where:** Your subprocess runner (currently v15)

**Key snippet from CITYNEXUS:**
```python
subprocess.run([
    "/run_mobility_model",  # ← Find this binary (ESA/Docker)
    "--json-path", str(input_file),
    "--output-path", str(output_dir),
    "--file-name", "results_simulation",
    "--fast-simulation", "true",  # ← Speed vs. accuracy
    "--cpu-to-use", "8"
])
```

---

## 🔍 Three Integration Points (Exact)

### Point 1: Input Serialization
```
Your Chandigarh Data
    ↓
(your adapter code)
    ↓
model_input.py::store_input_file()
    ↓
/model_input/{user_id}_{prediction_id}.json ✅
```

### Point 2: Model Execution
```
/model_input/{user_id}_{prediction_id}.json
    ↓
./run_mobility_model --json-path ... --output-path ...
    ↓
/model_output/{user_id}/predictions/{prediction_id}/results_simulation_*.zip ✅
```

### Point 3: Result Unpacking
```
results_simulation_*.zip
    ↓
model_output.py::load_result_zip()
    ↓
GeoDataFrame (occupancy, speed, NO₂, CO₂, time_window, geometry)
    ↓
Your KPI Dashboard ✅
```

---

## ❌ What's Still Missing

### 1. **`run_mobility_model` Binary**
   - **Where to find**: ESA repository, Docker image, or Solenix
   - **Size**: ~50-200 MB (compiled C++)
   - **Path**: Must be at `/run_mobility_model` (hardcoded in model_run.py)
   - **Action**: Contact ESA or extract from Docker image

### 2. **Chandigarh Road Network**
   - **Format**: GeoJSON with OSM IDs, geometries
   - **Mapping**: road_id (JSON) ↔ OSM ID
   - **Adapter**: Convert your road data to CITYNEXUS schema

### 3. **Chandigarh Grid & Demand**
   - **Format**: H3 cells (or similar) with landuse, POI, population
   - **Source**: OSM, census data, synthetic generation
   - **Adapter**: Populate `grid` section of JSON

---

## 📋 Key Paths & Contracts

| Concept | Type | Value | Notes |
|---------|------|-------|-------|
| Model Input | Path | `/model_input/{user_id}_{prediction_id}.json` | Deterministic |
| Model Binary | Path | `/run_mobility_model` | Hardcoded, must exist |
| Output Base | Path | `/model_output/{user_id}/predictions/{prediction_id}/` | Created by binary |
| Result File | Pattern | `results_simulation_{day}_{slot}_TIMESTAMP.zip` | Find latest |
| Time Window | Format | `"weekday_9"` or `"weekend_18"` | Filter results |
| Result Fields | GeoJSON | occupancy, speed, no2, co2, time_window | Per road segment |

---

## 🎯 Success Criteria

- [ ] Input JSON stored at correct path before subprocess call
- [ ] `run_mobility_model` returns code 0
- [ ] Result ZIP found in output directory
- [ ] Result ZIP unpacks to GeoDataFrame with road segments
- [ ] All 5 columns present: occupancy, speed, no2, co2, time_window
- [ ] Geometry matches your Chandigarh road network
- [ ] KPI dashboard receives and visualizes output

---

## 📞 Next Call

**Needed:** `run_mobility_model` binary  
**Source:** ESA/Solenix (ask directly or check Docker image)  
**Blocker:** Nothing else – rest is Python + your Chandigarh data

Once you have the binary → v15 goes live. 🚀

---

## File Sizes (Extracted)

```
simulation/model_input.py        3.6 KB  ← Input adapter
simulation/model_output.py       6.0 KB  ← Result unpacker
simulation/model_run.py          7.5 KB  ← Reference runner
simulation/xai_blackbox.py       6.9 KB  (defer)
simulation/xai_record.py         1.9 KB  (defer)
model/mobility_model_input.py    0.5 KB  ← Schema
model/generic.py                 1.1 KB  ← Types
pyproject.toml                   1.1 KB  ← Dependencies
MODEL_DOCS.md                    8.3 KB  ← Reference
---
Total: ~37 KB (minimal, pure Python I/O)
```

---

**Status: Ready for integration. Waiting on binary. 🔄**
