
import sys
import os
from unittest.mock import patch, MagicMock

# Ensure the root directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.logic import get_possible_moves_internal

def test_movement_validation():
    # Mock game state
    mock_status = {
        "status": "OK",
        "Planta": 0,
        "Personajes": [
            {
                "nombre": "Guillermo",
                "id": 0,
                "posX": 136,
                "posY": 168,
                "altura": 0,
                "orientacion": 1 # North
            },
            {
                "nombre": "Abbot",
                "id": 1,
                "posX": 136,
                "posY": 165, # A few steps north
                "altura": 0
            }
        ]
    }

    # Mock game map (256x256)
    # All height 0, except for some walls
    m_floor = [[{'h': 0, 'c': 0, 'o': 0, 'r': 23} for _ in range(256)] for _ in range(256)]
    
    # Put a wall (height 5) at North (136, 167)
    # Guillermo is at 136, 168. To move North, he moves to 136, 167.
    # His volume includes (136, 167), (137, 168), (135, 166), etc. (3x3 corners)
    # Let's just make it simple: make a block of high height north of him.
    for y in range(160, 165):
        for x in range(130, 140):
            m_floor[y][x]['h'] = 10 

    with patch('server.logic.get_full_game_state_internal', return_value=mock_status), \
         patch('server.logic.get_game_map', return_value=[m_floor]):
        
        result = get_possible_moves_internal()
        print("Possible Moves result:", result)
        
        if result['status'] == 'OK':
            print("Basic Moves:", result['data']['basic_moves'])
            print("Cardinal Moves:", result['data']['cardinal_moves'])
            
            # Since North has characters and high height, check if North is excluded
            if 'N' in result['data']['cardinal_moves']:
                print("FAIL: North should be blocked by Abbot or Wall")
            else:
                print("SUCCESS: North is blocked as expected")

if __name__ == "__main__":
    test_movement_validation()
