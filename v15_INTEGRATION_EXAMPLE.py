"""
Chandigarh CityNexus v15 Integration Example
============================================

Shows how to use the genuine CITYNEXUS I/O modules to:
1. Serialize Chandigarh scenario → model input JSON
2. Run the model binary
3. Deserialize result ZIP → KPI dashboard

This is the skeleton your v15 runner should follow.
"""

from pathlib import Path
import subprocess
import logging
from typing import Dict, Any

# Import genuine CITYNEXUS modules (relative to your project)
from citynexus.adapters.mobility_model.simulation.model_input import (
    store_input_file,
    derive_input_file_path,
)
from citynexus.adapters.mobility_model.simulation.model_output import (
    find_latest_file,
    load_result_zip,
    load_as_geodf,
    filter_time_slot,
    derive_output_path,
)
from citynexus.adapters.mobility_model.model.generic import SimulationID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# STEP 1: INPUT ADAPTER (Your Chandigarh scenario → CITYNEXUS JSON)
# ============================================================================

def chandigarh_scenario_to_citynexus(
    user_id: str,
    prediction_id: str,
    road_modifications: Dict[str, Any],
    grid_data: Dict[str, Any],
    scenario_params: Dict[str, Any],
) -> Path:
    """
    Converts Chandigarh input data to CITYNEXUS model input JSON.
    
    Args:
        user_id: User identifier (e.g., "user_123")
        prediction_id: Prediction identifier (e.g., "pred_456")
        road_modifications: Dict of road_id → {speed, closed, underground}
        grid_data: Dict of cell_id → {landuse, pois, population}
        scenario_params: {day_type, time_slots, bicycle%, evehicle%}
    
    Returns:
        Path to stored model input JSON
    """
    
    # Create unique identifier
    simulation_id = SimulationID(user_id=user_id, prediction_id=prediction_id)
    
    # Build CITYNEXUS input JSON structure
    model_input = {
        "road_network": road_modifications,  # Your Chandigarh roads
        "grid": grid_data,                   # Your H3 cells or grid
        "scenario": scenario_params,         # Day type, time slots, vehicle mix
    }
    
    # Serialize to /model_input/{user_id}_{prediction_id}.json
    input_file = derive_input_file_path(simulation_id)
    store_input_file(input_file, model_input)
    
    logger.info(f"✅ Model input stored: {input_file}")
    return input_file


# ============================================================================
# STEP 2: MODEL EXECUTION (subprocess call to run_mobility_model binary)
# ============================================================================

def run_mobility_model_binary(
    input_file: Path,
    user_id: str,
    prediction_id: str,
    timeout_seconds: int = 600,
) -> bool:
    """
    Executes the genuine CITYNEXUS mobility model binary.
    
    Args:
        input_file: Path to model input JSON (from Step 1)
        user_id: User identifier
        prediction_id: Prediction identifier
        timeout_seconds: Maximum execution time
    
    Returns:
        True if successful, False otherwise
    """
    
    simulation_id = SimulationID(user_id=user_id, prediction_id=prediction_id)
    output_path = derive_output_path(simulation_id)  # /model_output/{user_id}/predictions/{prediction_id}/
    
    # Build subprocess command for run_mobility_model binary
    cmd = [
        "/run_mobility_model",              # Binary path (must be available!)
        "--json-path", str(input_file),    # Input JSON from Step 1
        "--output-path", str(output_path), # Output directory
        "--file-name", "results_simulation",  # Result file prefix
        "--fast-simulation", "true",        # Speed up by filtering unlikely trips
        "--cpu-to-use", "8",                # Parallel CPU cores
        # Optional flood model integration (if needed later):
        # "--flood-depth-map", "/path/to/flood.tiff",
    ]
    
    logger.info(f"Running: {' '.join(cmd)}")
    
    try:
        # Execute model binary with timeout and output capture
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,  # Don't raise on non-zero exit
        )
        
        # Log output
        if result.stdout:
            logger.info(f"Model stdout:\n{result.stdout}")
        if result.stderr:
            logger.warning(f"Model stderr:\n{result.stderr}")
        
        if result.returncode == 0:
            logger.info(f"✅ Model execution successful (code {result.returncode})")
            return True
        else:
            logger.error(f"❌ Model execution failed (code {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"❌ Model execution timed out after {timeout_seconds}s")
        return False
    except FileNotFoundError:
        logger.error("❌ run_mobility_model binary not found at /run_mobility_model")
        return False
    except Exception as e:
        logger.error(f"❌ Model execution error: {e}")
        return False


# ============================================================================
# STEP 3: RESULT UNPACKING (result ZIP → GeoDataFrame → KPI Dashboard)
# ============================================================================

def unpack_model_results(
    user_id: str,
    prediction_id: str,
    day_type: str = "weekday",
    time_slot: int = 9,
    target_area: list = None,
) -> Dict[str, Any]:
    """
    Unpacks CITYNEXUS model result ZIP and extracts KPIs.
    
    Args:
        user_id: User identifier
        prediction_id: Prediction identifier
        day_type: "weekday" or "weekend"
        time_slot: Hour (0-23)
        target_area: Optional spatial filter as list of coordinates
    
    Returns:
        Dict with extracted KPIs ready for dashboard
    """
    
    simulation_id = SimulationID(user_id=user_id, prediction_id=prediction_id)
    
    # Find result ZIP (latest file matching pattern)
    output_path = derive_output_path(simulation_id)
    file_pattern = f"results_simulation_{day_type.lower()}_timeslot_{time_slot}_*.zip"
    
    logger.info(f"Looking for result file: {output_path / file_pattern}")
    
    try:
        result_zip = find_latest_file(output_path, file_pattern)
        logger.info(f"✅ Found result ZIP: {result_zip}")
    except Exception as e:
        logger.error(f"❌ Result ZIP not found: {e}")
        return {"error": "Result ZIP not found"}
    
    # Unzip and load as GeoDataFrame
    try:
        gdf_full = load_result_zip(result_zip, load_as_geodf)
        logger.info(f"✅ Loaded GeoDataFrame with {len(gdf_full)} features")
        
        # Filter to specific time slot
        gdf = filter_time_slot(gdf_full, day_type, time_slot)
        logger.info(f"✅ Filtered to time window {day_type}_{time_slot}: {len(gdf)} segments")
        
    except Exception as e:
        logger.error(f"❌ Failed to load results: {e}")
        return {"error": "Failed to load results"}
    
    # Extract KPI columns and statistics
    kpis = {
        "total_road_segments": len(gdf),
        "avg_occupancy": float(gdf["occupancy"].mean()) if "occupancy" in gdf else None,
        "avg_speed": float(gdf["speed"].mean()) if "speed" in gdf else None,
        "total_no2": float(gdf["no2"].sum()) if "no2" in gdf else None,
        "total_co2": float(gdf["co2"].sum()) if "co2" in gdf else None,
        "congested_segments": int((gdf["occupancy"] > 0.8).sum()) if "occupancy" in gdf else None,
        "road_segments": [
            {
                "road_id": row["road_id"],
                "occupancy": float(row["occupancy"]) if "occupancy" in row else None,
                "speed": float(row["speed"]) if "speed" in row else None,
                "no2": float(row["no2"]) if "no2" in row else None,
                "co2": float(row["co2"]) if "co2" in row else None,
                "geometry": row["geometry"].wkt if hasattr(row["geometry"], "wkt") else str(row["geometry"]),
            }
            for idx, row in gdf.iterrows()
        ],
    }
    
    logger.info(f"✅ Extracted KPIs: {len(kdf['road_segments'])} segments")
    return kpis


# ============================================================================
# MAIN INTEGRATION FLOW
# ============================================================================

def run_chandigarh_simulation(
    user_id: str,
    prediction_id: str,
    road_mods: Dict[str, Any],
    grid: Dict[str, Any],
    scenario: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Complete end-to-end simulation flow: Chandigarh data → Model → KPIs.
    
    Args:
        user_id: User identifier
        prediction_id: Prediction identifier
        road_mods: Chandigarh road modifications
        grid: Chandigarh grid data (H3 cells)
        scenario: Simulation scenario (day_type, time_slots, etc.)
    
    Returns:
        Dict with KPI results ready for dashboard
    """
    
    logger.info("=" * 70)
    logger.info(f"Starting simulation: user={user_id}, prediction={prediction_id}")
    logger.info("=" * 70)
    
    # Step 1: Serialize input
    logger.info("\n[STEP 1] Preparing model input...")
    input_file = chandigarh_scenario_to_citynexus(
        user_id, prediction_id, road_mods, grid, scenario
    )
    
    # Step 2: Execute model
    logger.info("\n[STEP 2] Running model binary...")
    success = run_mobility_model_binary(input_file, user_id, prediction_id, timeout_seconds=600)
    
    if not success:
        logger.error("❌ Model execution failed. Aborting.")
        return {"error": "Model execution failed"}
    
    # Step 3: Extract results
    logger.info("\n[STEP 3] Unpacking results...")
    day_type = scenario.get("day type", ["weekday"])[0]
    time_slot = scenario.get("time slots", [9])[0]
    
    kpis = unpack_model_results(user_id, prediction_id, day_type, time_slot)
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ SIMULATION COMPLETE")
    logger.info("=" * 70)
    
    return kpis


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    # Example Chandigarh data (you'll replace with real data)
    road_modifications = {
        "chandigarh_road_123": {
            "speed": 50,
            "closed": False,
            "underground": False,
        },
        "chandigarh_road_456": {
            "speed": 40,
            "closed": False,
            "underground": True,  # Underground metro
        },
    }
    
    grid_data = {
        "h3_cell_abc": {
            "landuse": {
                "residential": 0.5,
                "commercial": 0.3,
                "agricultural": 0.1,
                "industrial": 0.1,
            },
            "pois": {
                "food": 10,
                "school": 2,
                "health": 3,
                "infrastructure": 1,
                "shop": 8,
                "sport": 1,
                "tourism": 0,
                "fun": 2,
                "services": 5,
            },
            "population": {
                "static": 25000,
            },
        },
    }
    
    scenario_params = {
        "bicycle percentage": 0.05,
        "evehicle percentage": 0.1,
        "day type": ["weekday"],
        "time slots": [9],  # Morning rush hour
    }
    
    # Run the simulation
    results = run_chandigarh_simulation(
        user_id="user_chandigarh_001",
        prediction_id="pred_sept_2026_v15",
        road_mods=road_modifications,
        grid=grid_data,
        scenario=scenario_params,
    )
    
    # Print results
    print("\n📊 RESULTS FOR DASHBOARD:")
    print(f"Total segments: {results.get('total_road_segments')}")
    print(f"Avg occupancy: {results.get('avg_occupancy'):.1%}")
    print(f"Avg speed: {results.get('avg_speed'):.1f} km/h")
    print(f"Total NO₂: {results.get('total_no2'):.0f} µg/m³")
    print(f"Total CO₂: {results.get('total_co2'):.0f} g")
    print(f"Congested segments: {results.get('congested_segments')}")
