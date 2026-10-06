# CityNexus Mobility Model Integration Guide

## What You've Been Extracted

You now have the **genuine CITYNEXUS I/O contract and simulation pipeline** from the original repository. This is the exact interface that bridges your Chandigarh data → CITYNEXUS model → result unpacking.

---

## 📦 Package Contents

### 1. **simulation/model_input.py** 🔴 ESSENTIAL
   - **Purpose**: Serializes Chandigarh scenario data into CITYNEXUS JSON input format
   - **Key Functions**:
     - `store_input_file()` – writes JSON to `/model_input/{user_id}_{prediction_id}.json`
     - `get_road_ids()` – extracts road modifications from scenario
     - `derive_input_file_path()` – deterministic path for model input
     - `derive_flood_model_file_path()` – path for flood tiff (if integrated)
     - `create_model_input_modification()` – XAI variant (single road removed)
   - **Contract**:
     ```json
     {
       "road_network": { "road_id": { "speed": 50, "closed": false, "underground": false } },
       "grid": { "h3_id": { "landuse": {...}, "pois": {...}, "population": {...} } },
       "scenario": { "bicycle percentage": 0.1, "evehicle percentage": 0.05, "day type": ["weekday"], "time slots": [9] }
     }
     ```

### 2. **simulation/model_output.py** 🔴 ESSENTIAL
   - **Purpose**: Reads and unpacks CITYNEXUS result ZIP files
   - **Key Functions**:
     - `load_result_zip()` – opens `results_simulation_*.zip` and deserializes contained JSON/GeoJSON
     - `load_as_geodf()` – unpacks results into GeoDataFrame (road segment flows, occupancy, emissions)
     - `filter_time_slot()` – extracts single time window from multi-slot results
     - `find_latest_file()` – finds most recent result in `/model_output/{user_id}/predictions/{prediction_id}/`
     - `get_target_area()` – spatial filtering by bounding box or polygon
   - **Result ZIP Contract**:
     ```
     results_simulation_weekday_timeslot_9_TIMESTAMP.zip
     └── (GeoJSON)
         road_id | geometry | occupancy | speed | no2 | co2 | time_window
     ```

### 3. **simulation/model_run.py** 🟠 REFERENCE
   - **Purpose**: Shows how CITYNEXUS originally wraps the `run_mobility_model` executable
   - **Key Pattern**:
     ```python
     subprocess.run([
         "../run_mobility_model",
         "--json-path", str(model_input_path),
         "--flood-depth-map", str(flood_tiff_path),  # optional
         "--output-path", str(output_dir),
         "--file-name", "results_simulation",
         "--fast-simulation", "true",
         "--cpu-to-use", "8"
     ])
     ```
   - **Use this as your baseline** – adapt paths and parameters for your v15 runner

### 4. **model/mobility_model_input.py** 🟠 IMPORTANT
   - **Purpose**: Defines the top-level data model/schema
   - **What it Contains**: Pydantic or dataclass definitions for input validation

### 5. **model/generic.py** 🟡 USEFUL
   - **Purpose**: Shared types and enums
   - **Key Types**: `SimulationID` (user_id, prediction_id) – used throughout for deterministic path derivation

### 6. **simulation/xai_blackbox.py** 🟡 USEFUL (Later)
   - **Purpose**: What-if analysis explainability
   - **Use Case**: Run model for each road **without** its modifications to measure per-road impact
   - **Defer integration** until core model runs successfully

### 7. **simulation/xai_record.py** 🟡 USEFUL (Later)
   - **Purpose**: Metadata wrapper for XAI runs
   - **Use Case**: Tracks which road was removed, stores its modified input/output pair

### 8. **MODEL_DOCS.md**
   - Copy of the official mobility model README from CITYNEXUS
   - Command-line signatures for `run_mobility_model` binary
   - Input JSON structure specification (definitive reference)

### 9. **pyproject.toml**
   - CITYNEXUS dependency tree – consider aligning for compatibility
   - Key deps: `geopandas`, `shapely`, `rasterio` (flood model support)

---

## 🏗️ Integration Checklist

### Phase 1: **Input Adapter** (Your v15 currently covers this)
- [ ] Map Chandigarh roads → `road_network` JSON keys
- [ ] Map Chandigarh grid (H3 cells?) → `grid` JSON with landuse/POI/population
- [ ] Map user scenario → `scenario` JSON (day_type, time_slots, vehicle mix)
- [ ] Call `simulation.model_input.store_input_file()` to serialize

### Phase 2: **Model Execution** (Needs `run_mobility_model` binary)
- [ ] Locate or build the `run_mobility_model` executable (likely pre-compiled in Docker or from ESA)
- [ ] Pass input JSON path via `--json-path`
- [ ] Set `--output-path` to `/model_output/{user_id}/predictions/{prediction_id}/`
- [ ] Set `--file-name` to deterministic prefix (e.g., `results_simulation`)
- [ ] Subprocess call with timeout + error handling

### Phase 3: **Result Unpacking** (Ready to integrate now)
- [ ] Call `simulation.model_output.find_latest_file()` to locate result ZIP
- [ ] Call `simulation.model_output.load_result_zip()` to deserialize
- [ ] Filter by time window: `simulation.model_output.filter_time_slot(gdf, "weekday", 9)`
- [ ] Extract KPIs: occupancy, speed, NO₂, CO₂ per road segment
- [ ] Join with your Chandigarh road/grid reference data
- [ ] Return to your dashboard/KPI layer

### Phase 4: **Explainability** (Defer for now)
- [ ] Generate XAI inputs via `simulation.model_input.create_xai_records()`
- [ ] Run model for each: `{scenario with road_i's mods removed}`
- [ ] Compare results to baseline
- [ ] Surface per-road impact in UI

---

## 🎯 The Missing Piece: `run_mobility_model` Binary

**What you need next:**
- The compiled mobility model executable (`run_mobility_model`)
- Likely location: ESA/Solenix Docker image or GitLab CI artifacts
- **Do NOT try to run the Python files directly** – they're input/output wrappers only
- The binary is C++ or similar (fast, GPU-accelerated for OD matrix generation)

**Fallback approach:**
- If binary unavailable, check CITYNEXUS documentation for Docker image
- Pull image, extract binary, include in your deployment
- Or contact ESA/Solenix for standalone binary release

---

## 📋 Key Contracts at a Glance

### Input JSON (To Chandigarh Adapter)
```json
{
  "road_network": {
    "road_123": {
      "speed": 50,           // km/h (optional, default varies)
      "closed": false,       // boolean (optional)
      "underground": false   // boolean (optional)
    }
  },
  "grid": {
    "h3_cell_abc": {
      "landuse": {
        "residential": 0.5,
        "commercial": 0.3,
        "agricultural": 0.1,
        "industrial": 0.1
      },
      "pois": {
        "food": 5,
        "school": 1,
        "health": 2,
        ...
      },
      "population": {
        "static": 10000
      }
    }
  },
  "scenario": {
    "bicycle percentage": 0.1,
    "evehicle percentage": 0.05,
    "day type": ["weekday"],
    "time slots": [9, 12, 18]
  }
}
```

### Output ZIP (From Model)
```
results_simulation_weekday_timeslot_9_2025-10-06_12-34-56.zip
└── (GeoJSON FeatureCollection)
    {
      "features": [
        {
          "id": "road_123",
          "geometry": { "type": "LineString", "coordinates": [...] },
          "properties": {
            "occupancy": 0.75,        // vehicles / capacity
            "speed": 40,              // actual km/h
            "no2": 125.5,             // µg/m³
            "co2": 450.2,             // g/km
            "time_window": "weekday_9"
          }
        }
      ]
    }
```

---

## 🚀 Next Steps

1. **v15.1**: Integrate `simulation/model_output.py` → unpack results into KPI dashboard
2. **v15.2**: Source `run_mobility_model` binary → subprocess runner
3. **v15.3**: XAI framework (optional but valuable for what-if UI)
4. **v16**: Full Chandigarh-specific model tuning (road networks, demand patterns, POI density)

---

## 📚 Files Included

```
citynexus-model-core/
├── simulation/
│   ├── __init__.py
│   ├── model_input.py           ← INPUT ADAPTER
│   ├── model_output.py          ← RESULT UNPACKER
│   ├── model_run.py             ← REFERENCE RUNNER
│   ├── xai_blackbox.py          ← XAI (defer)
│   └── xai_record.py            ← XAI metadata
├── model/
│   ├── __init__.py
│   ├── mobility_model_input.py  ← DATA SCHEMA
│   └── generic.py               ← SHARED TYPES
├── MODEL_DOCS.md                ← OFFICIAL REFERENCE
└── pyproject.toml               ← DEPENDENCIES
```

---

## ⚠️ Important Notes

- **This is not executable code alone** – it's the adapter layer between your Chandigarh data and the genuine CITYNEXUS binary
- **Paths are hardcoded** for Docker (`/model_input`, `/model_output`) – adapt to your file system
- **SimulationID** determinism is critical – same user+prediction must yield same paths and results
- **No Copenhagen/Bologna data included** – you bring Chandigarh-specific road networks and demand
- **XAI requires multiple model runs** – plan for 5-10x longer execution with explainability enabled

---

**Integration Status:**  
✅ I/O contracts (exact)  
✅ Data schema (reference)  
❌ Binary executable (next step)  
❌ Chandigarh data adapter (yours to build)  
❌ KPI dashboarding (yours to connect)

Go build it. 🚀
