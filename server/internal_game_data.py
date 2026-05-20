from typing import Dict, Any, List
import time
import os

# Initialize the internal game data structure with AKI (ADR-011)
internal_game_data: Dict[str, Any] = {
    "current_day": 1,
    "current_horarium": "Prima",
    "max_progress_observed": 0.0,
    "obsequium_history": [],  # List of (time, value)
    "rules_induced": [],  # List of {trigger, context, action, result, confidence}
    "death_zones": [],    # List of (day, time, location, cause)
    "golden_paths": [],   # Successful trajectories
    "investigation_notes": {},
    "map_discovered": [],
}

def get_internal_game_data() -> Dict[str, Any]:
    """Returns the current internal game data."""
    return internal_game_data

def update_internal_game_data(game_state: Dict[str, Any]):
    """
    Updates internal game data using AKI logic (ADR-011).
    Detects patterns, progress jumps, and death zones.
    """
    global internal_game_data

    if not isinstance(game_state, dict):
        return

    # 1. Update Core State
    prev_progress = internal_game_data.get("max_progress_observed", 0.0)
    current_progress = game_state.get("P", 0.0)
    current_obsequium = game_state.get("O", 31)
    current_day = game_state.get("dia", 1)
    
    # Simple mapping of moments (mock logic until real triggers are mapped)
    # In a real scenario, this would come from the 'moment' or 'bells' field
    current_time = game_state.get("momento", "Unknown")

    # 2. Progress Tracking (Golden Path Induction)
    if current_progress > prev_progress:
        internal_game_data["max_progress_observed"] = current_progress
        # Mark current trajectory as high potential
        internal_game_data["golden_paths"].append({
            "day": current_day,
            "time": current_time,
            "progress": current_progress,
            "location": game_state.get("numPantalla", 0)
        })

    # 3. Obsequium Monitoring (Death Zone Detection)
    if len(internal_game_data["obsequium_history"]) > 0:
        prev_o = internal_game_data["obsequium_history"][-1][1]
        if current_obsequium < prev_o:
            # We lost honor! Induce a risk rule
            drop_amount = prev_o - current_obsequium
            context_log = f"Día {current_day}, {current_time}. Pantalla {game_state.get('numPantalla', 0)}. Obsequium: {prev_o} -> {current_obsequium} (Pérdida: {drop_amount})"
            
            risk_entry = {
                "day": current_day,
                "time": current_time,
                "location": game_state.get("numPantalla", 0),
                "drop": drop_amount
            }
            if risk_entry not in internal_game_data["death_zones"]:
                internal_game_data["death_zones"].append(risk_entry)
                
                # Trigger DeepSeek Analysis (Agentic Automation)
                import subprocess
                script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts/analyze_sin.py")
                subprocess.Popen(["python3", script_path, context_log])

    internal_game_data["obsequium_history"].append((time.time(), current_obsequium))
    # Keep history manageable
    if len(internal_game_data["obsequium_history"]) > 100:
        internal_game_data["obsequium_history"].pop(0)

    # 4. Map & Character Discovery
    if "numPantalla" in game_state:
        screen = game_state["numPantalla"]
        if screen not in internal_game_data["map_discovered"]:
            internal_game_data["map_discovered"].append(screen)

    if "Personajes" in game_state:
        for char in game_state["Personajes"]:
            name = char.get("nombre")
            if name and name not in internal_game_data["investigation_notes"]:
                internal_game_data["investigation_notes"][name] = f"Discovery: {name} found at Day {current_day}."

def reset_internal_game_data():
    """Resets the internal game data to its initial state."""
    global internal_game_data
    internal_game_data = {
        "current_day": 1,
        "current_horarium": "Prima",
        "max_progress_observed": 0.0,
        "obsequium_history": [],
        "rules_induced": [],
        "death_zones": [],
        "golden_paths": [],
        "investigation_notes": {},
        "map_discovered": [],
    }
