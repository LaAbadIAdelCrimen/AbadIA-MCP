from typing import Dict, Any

# Initialize the internal game data structure
internal_game_data: Dict[str, Any] = {
    "current_day": 1,
    "goals_completed": {
        "day1": [],
        "day2": [],
        "day3": [],
        "day4": [],
        "day5": [],
        "day6": [],
        "day7": [],
    },
    "investigation_notes": {},
    "map_discovered": [],
}

def get_internal_game_data() -> Dict[str, Any]:
    """Returns the current internal game data."""
    return internal_game_data

def update_internal_game_data(game_state: Dict[str, Any]):
    """
    Updates the internal game data based on the current game state.
    This function can be expanded to include more complex logic for tracking progress.
    """
    global internal_game_data

    # Example logic: Update current day based on game state
    if "dia" in game_state:
        internal_game_data["current_day"] = game_state["dia"]

    # Example logic: Add a simple note if a character is met
    if "Personajes" in game_state:
        for character in game_state["Personajes"]:
            if character["nombre"] == "Abad" and "Abad" not in internal_game_data["investigation_notes"]:
                internal_game_data["investigation_notes"]["Abad"] = "Met the Abbot."

    # Example logic: Update map based on current screen
    if "numPantalla" in game_state:
        screen = game_state["numPantalla"]
        if screen not in internal_game_data["map_discovered"]:
            internal_game_data["map_discovered"].append(screen)

    # Add any new keys from game_state to internal_game_data
    for key, value in game_state.items():
        if key not in internal_game_data:
            internal_game_data[key] = value

    # TODO: Add more sophisticated logic to track goals based on game events.
    # For example, check inventory, character interactions, or specific locations.

def reset_internal_game_data():
    """Resets the internal game data to its initial state."""
    global internal_game_data
    internal_game_data = {
        "current_day": 1,
        "goals_completed": {
            "day1": [], "day2": [], "day3": [], "day4": [], "day5": [], "day6": [], "day7": [],
        },
        "investigation_notes": {},
        "map_discovered": [],
    }
