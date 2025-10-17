from server.internal_game_data import update_internal_game_data, reset_internal_game_data
from server.map_utils import load_map

game_status = None
game_map = []

def save_game_status(response: dict):
    """Saves the game status response and updates internal game data."""
    global game_status
    game_status = response
    if game_status:
        update_internal_game_data(game_status)

def get_game_status():
    """Returns the current game status."""
    return game_status

def load_game_map(map_name: str):
    """Loads the game map from the storage directory."""
    global game_map
    game_map = load_map(map_name)

def get_game_map():
    """Returns the current game map."""
    return game_map

def update_map_from_game_state(game_status: dict):
    """
    Updates the absolute game_map with data from the latest game_status.
    This is the main orchestrator for translating relative game data to the absolute map.
    """
    # This function will be implemented in the next subtasks.
    pass

def reset_game_data():
    """Resets all game-related data."""
    global game_status, game_map
    game_status = None
    game_map = []
    reset_internal_game_data()

location_paths = {
    "library": "UP:UP:LEFT:UP",
    "church": "RIGHT:RIGHT:UP",
    "cell": "DOWN:DOWN:LEFT"
}

character_locations = {
    "abbot": "church",
    "jorge": "library"
}
