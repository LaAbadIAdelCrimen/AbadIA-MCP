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
    
    planta = game_status.get('Planta', 0)
    personajes = game_status.get('Personajes', [])
    objetos = game_status.get('Objetos', [])

    logger.info(f"--- DYNAMIC ENTITY UPDATE (Floor {planta}) ---")
    logger.info(f"Clearing entities for screen area starting at ({offset_x}, {offset_y}).")
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
    logger.info(f"Placing {len(personajes)} characters on the map.")
    for personaje in personajes:
        p_x = personaje['posX']
        p_y = personaje['posY']
        p_id = personaje['id']
        p_nombre = personaje['nombre']
        logger.info(f"  - Placing '{p_nombre}' (ID: {p_id}) at absolute map coordinates ({p_x}, {p_y}).")
        if (planta < len(game_map) and
            p_y < len(game_map[planta]) and
            p_x < len(game_map[planta][p_y])):
            game_map[planta][p_y][p_x]['character'] = p_id

    # Place current objects on the map
    logger.info(f"Placing {len(objetos)} objects on the map.")
    for objeto in objetos:
        o_x = objeto['posX']
        o_y = objeto['posY']
        o_id = objeto['id']
        o_nombre = objeto.get('nombre', 'Unknown') # Use .get for safety
        logger.info(f"  - Placing '{o_nombre}' (ID: {o_id}) at absolute map coordinates ({o_x}, {o_y}).")
        if (planta < len(game_map) and
            o_y < len(game_map[planta]) and
            o_x < len(game_map[planta][o_y])):
            game_map[planta][o_y][o_x]['object'] = o_id
    logger.info("--- DYNAMIC ENTITY UPDATE COMPLETE ---")


def update_map_from_game_state(game_status: dict):
    """
    Updates the absolute game_map with data from the latest game_status.
    This is the main orchestrator for translating relative game data to the absolute map.
    """
    global game_map
    logger.info("========== MAP UPDATE CYCLE START ==========")
    if not game_status or 'Rejilla' not in game_status or 'Personajes' not in game_status:
        logger.warning("MAP UPDATE SKIPPED: game_status is missing required keys ('Rejilla' or 'Personajes').")
        logger.info("========== MAP UPDATE CYCLE END ==========")
        return

    # Extract key data
    rejilla = game_status['Rejilla']
    personajes = game_status['Personajes']
    planta = game_status.get('Planta', 0)
    num_pantalla = game_status.get('NumPantalla', 0)
    logger.info(f"Received data for Floor: {planta}, Screen: {num_pantalla}.")

    # Find Guillermo to get the reference position
    guillermo = next((p for p in personajes if p['nombre'] == 'Guillermo'), None)
    if not guillermo:
        logger.warning("MAP UPDATE SKIPPED: Guillermo not found in 'Personajes' list.")
        logger.info("========== MAP UPDATE CYCLE END ==========")
        return

    pos_x = guillermo['posX']
    pos_y = guillermo['posY']
    logger.info(f"Guillermo's absolute position: ({pos_x}, {pos_y}).")

    # Calculate the top-left corner of the current screen on the absolute map
    offset_x = (pos_x // 24) * 24
    offset_y = (pos_y // 24) * 24
    logger.info(f"Calculated screen offset on absolute map: ({offset_x}, {offset_y}).")

    # Ensure the map is large enough for the current floor
    if planta >= len(game_map):
        logger.error(f"MAP UPDATE FAILED: Floor {planta} is out of bounds for the current map (size: {len(game_map)} floors).")
        logger.info("========== MAP UPDATE CYCLE END ==========")
        return

    # Loop through the 24x24 rejilla and update the game_map
    logger.info("Starting to process 24x24 Rejilla to update terrain and room data...")
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
    logger.info("Rejilla data (height and room) successfully updated on the map.")
    
    # Update characters and objects
    _update_dynamic_entities(game_status, offset_x, offset_y)
    logger.info("========== MAP UPDATE CYCLE END ==========")

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