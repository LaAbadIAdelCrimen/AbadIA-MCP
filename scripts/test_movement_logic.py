
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
                "posX": 137,
                "posY": 168, # Blocks East
                "altura": 0
            }
        ]
    }

    # Mock game map (256x256)
    # All height 0, except for some walls
    m_floor = [[{'h': 0, 'c': 0, 'o': 0, 'r': 23} for _ in range(256)] for _ in range(256)]
    
    # Guillermo is at 136, 168. To move North, he moves to 136, 167.
    # His 2x2 volume includes (136, 167), (135, 167), (135, 168), (136, 168).
    # Let's put a wall at (135, 167) to block his volume.
    m_floor[167][135]['h'] = 10 

    with patch('server.logic.get_full_game_state_internal', return_value=mock_status), \
         patch('server.logic.get_game_map', return_value=[m_floor]):
        
        result = get_possible_moves_internal()
        print("Possible Moves result:", result)
        
        if result['status'] == 'OK':
            print("Basic Moves:", result['data']['basic_moves'])
            print("Cardinal Moves:", result['data']['cardinal_moves'])
            
            # Check if North is blocked by Wall at (135, 167)
            if 'N' in result['data']['cardinal_moves']:
                print("FAIL: North should be blocked by Wall")
            else:
                print("SUCCESS: North is blocked by Wall")
            
            # Check if East is blocked by Abbot at (137, 168)
            if 'E' in result['data']['cardinal_moves']:
                print("FAIL: East should be blocked by Abbot")
            else:
                print("SUCCESS: East is blocked by Abbot")

if __name__ == "__main__":
    test_movement_validation()
