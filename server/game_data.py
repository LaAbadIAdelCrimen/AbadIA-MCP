import os
from server.internal_game_data import update_internal_game_data, reset_internal_game_data
from server.logger_config import log

game_status = None
game_map = []

# Default empty cell structure. Used when a map cell is None.
EMPTY_CELL = {"h": 0, "c": 0, "o": 0, "r": 0}

def get_cell(floor, x, y):
    """
    Safely gets a cell from the game map.
    If the cell is None, it returns a default empty cell structure.
    """
    if (floor < len(game_map) and
        y < len(game_map[floor]) and
        x < len(game_map[floor][y])):
        
        cell = game_map[floor][y][x]
        return cell if cell is not None else EMPTY_CELL.copy()
    
    # Return a copy to prevent modification of the global EMPTY_CELL
    return EMPTY_CELL.copy()

def set_cell(floor, x, y, cell_data):
    """
    Sets a cell in the game map.
    If the cell data matches the default empty state, it stores None instead.
    """
    if (floor < len(game_map) and
        y < len(game_map[floor]) and
        x < len(game_map[floor][y])):
        
        # if cell_data == EMPTY_CELL:
        #    game_map[floor][y][x] = None
        #else:
        game_map[floor][y][x] = cell_data

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
    from server.map_utils import load_map
    global game_map
    game_map = load_map(map_name)
    log.info(f"Loaded map '{map_name}' with {len(game_map)} floors.")

def get_game_map():
    """Returns the current game map."""
    if game_map:
        num_floors = len(game_map)
        first_floor = game_map[0] if num_floors > 0 else []
        y_dim = len(first_floor)
        x_dim = len(first_floor[0]) if y_dim > 0 else 0
        log.info(f"Accessing game_map. Dimensions: Floors={num_floors}, Y={y_dim}, X={x_dim}.")
    else:
        log.info("Accessing game_map, but it is currently empty.")
    return game_map

def initialize_map():
    """
    Initializes the game map, loading 'current_map.json' if it exists,
    otherwise falling back to 'default_map.json'.
    """
    from server.map_utils import STORE_PATH
    current_map_path = os.path.join(STORE_PATH, "current_map.json")
    
    if os.path.exists(current_map_path):
        log.info("Found 'current_map.json'. Loading persistent map state.")
        load_game_map("current_map")
    else:
        log.info("'current_map.json' not found. Loading 'default_map.json'.")
        load_game_map("default_map")

def _update_dynamic_entities(game_status: dict, offset_x: int, offset_y: int):
    """
    Clears old entity positions and places new characters and objects on the map.
    """
    planta = game_status.get('Planta', 0)
    personajes = game_status.get('Personajes', [])
    objetos = game_status.get('Objetos', [])

    log.info(f"--- DYNAMIC ENTITY UPDATE (Floor {planta}) ---")
    log.info(f"Clearing entities for screen area starting at ({offset_x}, {offset_y}).")
    
    for y_rejilla in range(24):
        for x_rejilla in range(24):
            map_x = offset_x + x_rejilla
            map_y = offset_y + y_rejilla
            cell = get_cell(planta, map_x, map_y)
            cell['c'] = 0
            cell['o'] = 0
            set_cell(planta, map_x, map_y, cell)

    log.info(f"Placing {len(personajes)} characters on the map.")
    for personaje in personajes:
        p_x, p_y, p_id = personaje['posX'], personaje['posY'], personaje['id']
        cell = get_cell(planta, p_x, p_y)
        cell['c'] = p_id + 1
        log.info(f"personaje {personaje}")
        set_cell(planta, p_x, p_y, cell)

    log.info(f"Placing {len(objetos)} objects on the map.")
    for objeto in objetos:
        o_x, o_y, o_id = objeto['posX'], objeto['posY'], objeto['id']
        cell = get_cell(planta, o_x, o_y)
        cell['o'] = o_id
        set_cell(planta, o_x, o_y, cell)
        
    log.info("--- DYNAMIC ENTITY UPDATE COMPLETE ---")

def update_map_from_game_state(game_status: dict):
    """
    Updates the absolute game_map with data from the latest game_status.
    """
    from server.map_utils import save_map
    global game_map
    log.info("========== MAP UPDATE CYCLE START ==========")
    if not game_status or 'Rejilla' not in game_status or 'Personajes' not in game_status:
        log.warning("MAP UPDATE SKIPPED: Missing required keys.")
        return

    planta = game_status.get('Planta', 0)
    num_pantalla = game_status.get('NumPantalla', 0)
    guillermo = next((p for p in game_status['Personajes'] if p['nombre'] == 'Guillermo'), None)

    if not guillermo:
        log.warning("MAP UPDATE SKIPPED: Guillermo not found.")
        return

    pos_x, pos_y = guillermo['posX'], guillermo['posY']
    
    current_cell = get_cell(planta, pos_x, pos_y)
    if current_cell['r'] != 0 and current_cell['r'] != num_pantalla:
        log.info(f"Screen change detected. Auto-saving map.")
        save_map("current_map", game_map)

    offset_x = (pos_x // 16) * 16 - 4
    offset_y = (pos_y // 16) * 16 - 4

    for y_rejilla, row in enumerate(game_status['Rejilla']):
        for x_rejilla, cell_value in enumerate(row):
            map_x, map_y = offset_x + x_rejilla, offset_y + y_rejilla
            cell = get_cell(planta, map_x, map_y)
            cell['h'] = cell_value % 16
            if (cell_value >> 4)  > 0:
                cell['c'] = (cell_value >> 4)
            else: 
                cell['c'] = None
            cell['r'] = num_pantalla
            set_cell(planta, map_x, map_y, cell)
            
    _update_dynamic_entities(game_status, offset_x, offset_y)
    log.info("========== MAP UPDATE CYCLE END ==========")

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
