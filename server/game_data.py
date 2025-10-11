from server.internal_game_data import update_internal_game_data, reset_internal_game_data

game_status = None

def save_game_status(response: dict):
    """Saves the game status response and updates internal game data."""
    global game_status
    game_status = response
    if game_status:
        update_internal_game_data(game_status)

def get_game_status():
    """Returns the current game status."""
    return game_status

def reset_game_data():
    """Resets all game-related data."""
    global game_status
    game_status = None
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


location_paths = {
    "library": "UP:UP:LEFT:UP",
    "church": "RIGHT:RIGHT:UP",
    "cell": "DOWN:DOWN:LEFT"
}

character_locations = {
    "abbot": "church",
    "jorge": "library"
}