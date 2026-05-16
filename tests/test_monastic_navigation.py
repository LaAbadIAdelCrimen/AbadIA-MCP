import pytest
from server.logic import check_volume_walkable, is_cell_occupied_by_any_character

# Mocking the game_map and game_status
@pytest.fixture
def mock_game_map():
    # 3 floors, 50x50 grid
    return [[[{"h": 0} for _ in range(50)] for _ in range(50)] for _ in range(3)]

@pytest.fixture
def mock_game_status():
    return {
        "Planta": 0,
        "Personajes": [
            {"id": 0, "nombre": "Guillermo", "posX": 10, "posY": 10, "altura": 0},
            {"id": 1, "nombre": "Adso", "posX": 12, "posY": 12, "altura": 0}
        ]
    }

def test_volume_walkable_success(mock_game_map, mock_game_status):
    # Guillermo is at 10,10. Move to 15,15 (empty and flat)
    assert check_volume_walkable(mock_game_map, 0, 15, 15, 0, 0, mock_game_status) is True

def test_volume_walkable_blocked_by_height(mock_game_map, mock_game_status):
    # Set a wall at 15,15 (height 5, Guillermo is at 0)
    mock_game_map[0][15][15]["h"] = 5
    assert check_volume_walkable(mock_game_map, 0, 15, 15, 0, 0, mock_game_status) is False

def test_volume_walkable_blocked_by_npc(mock_game_map, mock_game_status):
    # Adso is at 12,12. 
    # Adso's volume: (12,12), (11,12), (11,13), (12,13)
    # Trying to move Guillermo to 12,12 should fail
    assert check_volume_walkable(mock_game_map, 0, 12, 12, 0, 0, mock_game_status) is False

def test_volume_walkable_boundary_check(mock_game_map, mock_game_status):
    # Edge of map (0,0) - volume (0,0), (-1,0), etc. should fail
    assert check_volume_walkable(mock_game_map, 0, 0, 0, 0, 0, mock_game_status) is False
