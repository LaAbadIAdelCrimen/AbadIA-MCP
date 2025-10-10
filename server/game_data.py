game_status = None

def save_game_status(response: dict):
    """Saves the game status response to a global variable."""
    global game_status
    game_status = response

def get_game_status():
    """Returns the current game status."""
    return game_status

location_paths = {
    "library": "UP:UP:LEFT:UP",
    "church": "RIGHT:RIGHT:UP",
    "cell": "DOWN:DOWN:LEFT"
}

character_locations = {
    "abbot": "church",
    "jorge": "library"
}