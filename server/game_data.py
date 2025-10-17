import logging
from server.internal_game_data import update_internal_game_data, reset_internal_game_data
from server.map_utils import load_map

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

game_status = None
game_map = []

def save_game_status(response: dict):
    """
    Saves the game status response, updates the internal game data,
    and updates the master game map.
    """
    global game_status
    game_status = response
    if game_status:
        update_internal_game_data(game_status)
        update_map_from_game_state(game_status)

def get_game_status():
    """Returns the current game status."""
    return game_status

def load_game_map(map_name: str):
    """Loads the game map from the storage directory."""
    global game_map
    game_map = load_map(map_name)
    logger.info(f"Loaded map '{map_name}' with {len(game_map)} floors.")

def get_game_map():
    """Returns the current game map."""
    return game_map

def _update_dynamic_entities(game_status: dict, offset_x: int, offset_y: int):
    """
    Clears old entity positions and places new characters and objects on the map.
    """
    global game_map
    
    planta = game_status.get('planta', 0)
    personajes = game_status.get('personajes', [])
    objetos = game_status.get('objetos', [])

    logger.info(f"Clearing entities for screen at offset ({offset_x}, {offset_y}) on floor {planta}.")
    # Clear all character and object data from the current screen
    for y_rejilla in range(24):
        for x_rejilla in range(24):
            map_x = offset_x + x_rejilla
            map_y = offset_y + y_rejilla
            if (planta < len(game_map) and
                map_y < len(game_map[planta]) and
                map_x < len(game_map[planta][map_y])):
                game_map[planta][map_y][map_x]['character'] = 0
                game_map[planta][map_y][map_x]['object'] = 0

    # Place current characters on the map
    logger.info(f"Updating {len(personajes)} characters on the map.")
    for personaje in personajes:
        p_x = personaje['posX']
        p_y = personaje['posY']
        p_id = personaje['id']
        logger.debug(f"Placing character {p_id} at ({p_x}, {p_y}) on floor {planta}.")
        if (planta < len(game_map) and
            p_y < len(game_map[planta]) and
            p_x < len(game_map[planta][p_y])):
            game_map[planta][p_y][p_x]['character'] = p_id

    # Place current objects on the map
    logger.info(f"Updating {len(objetos)} objects on the map.")
    for objeto in objetos:
        o_x = objeto['posX']
        o_y = objeto['posY']
        o_id = objeto['id']
        logger.debug(f"Placing object {o_id} at ({o_x}, {o_y}) on floor {planta}.")
        if (planta < len(game_map) and
            o_y < len(game_map[planta]) and
            o_x < len(game_map[planta][o_y])):
            game_map[planta][o_y][o_x]['object'] = o_id


def update_map_from_game_state(game_status: dict):
    """
    Updates the absolute game_map with data from the latest game_status.
    This is the main orchestrator for translating relative game data to the absolute map.
    """
    global game_map
    logger.info("Attempting to update map from game state...")
    if not game_status or 'rejilla' not in game_status or 'personajes' not in game_status:
        logger.warning("Map update skipped: game_status is missing required keys ('rejilla' or 'personajes').")
        return

    # Extract key data
    rejilla = game_status['rejilla']
    personajes = game_status['personajes']
    planta = game_status.get('planta', 0)
    num_pantalla = game_status.get('numPantalla', 0)

    # Find Guillermo to get the reference position
    guillermo = next((p for p in personajes if p['nombre'] == 'Guillermo'), None)
    if not guillermo:
        logger.warning("Map update skipped: Guillermo not found in 'personajes' list.")
        return

    pos_x = guillermo['posX']
    pos_y = guillermo['posY']

    # Calculate the top-left corner of the current screen on the absolute map
    offset_x = (pos_x // 24) * 24
    offset_y = (pos_y // 24) * 24
    logger.info(f"Updating map for screen {num_pantalla} at offset ({offset_x}, {offset_y}) on floor {planta}.")

    # Ensure the map is large enough for the current floor
    if planta >= len(game_map):
        logger.error(f"Map update failed: Floor {planta} is out of bounds for the current map (size: {len(game_map)} floors).")
        return

    # Loop through the 24x24 rejilla and update the game_map
    for y_rejilla, row in enumerate(rejilla):
        for x_rejilla, cell_value in enumerate(row):
            map_x = offset_x + x_rejilla
            map_y = offset_y + y_rejilla

            # Ensure the coordinates are within the map boundaries
            if (planta < len(game_map) and
                map_y < len(game_map[planta]) and
                map_x < len(game_map[planta][map_y])):
                
                # Update height and room number
                game_map[planta][map_y][map_x]['height'] = cell_value
                game_map[planta][map_y][map_x]['room'] = num_pantalla
            else:
                # This would be the place to dynamically expand the map if we wanted to
                pass
    logger.info("Rejilla data (height and room) updated on the map.")
    
    # Update characters and objects
    _update_dynamic_entities(game_status, offset_x, offset_y)
    logger.info("Dynamic entities (characters and objects) updated on the map.")

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