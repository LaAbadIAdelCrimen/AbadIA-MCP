import pytest
from server.logic import (
    a_star_search, 
    check_volume_walkable, 
    is_cell_occupied_by_any_character,
    heuristic,
    get_neighbors,
    get_possible_moves_internal,
    move_to_location_internal,
    investigate_location_internal,
    talk_to_character_internal,
    send_game_command_internal,
    get_full_game_state_internal,
    reconstruct_path,
    path_to_commands
)
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_game_map():
    # 1 floor, 10x10 empty map (height 10)
    return [[
        [{"h": 10} for _ in range(10)] for _ in range(10)
    ]]

@pytest.fixture
def mock_game_status():
    return {
        "Planta": 0,
        "Personajes": [
            {"nombre": "Guillermo", "id": 0, "posX": 5, "posY": 5, "altura": 10, "orientacion": 0}
        ],
        "Objetos": []
    }

def test_heuristic():
    assert heuristic((0, 0), (3, 4)) == 7

def test_is_cell_occupied(mock_game_status):
    status = {
        "Planta": 0,
        "Personajes": [{"id": 1, "posX": 2, "posY": 2}]
    }
    assert is_cell_occupied_by_any_character(2, 2, 0, 0, status) == True
    assert is_cell_occupied_by_any_character(2, 2, 1, 0, status) == False # Wrong floor
    assert is_cell_occupied_by_any_character(5, 5, 0, 0, status) == False
    assert is_cell_occupied_by_any_character(0, 0, 0, 0, None) == False

def test_check_volume_walkable(mock_game_map, mock_game_status):
    # Success
    assert check_volume_walkable(mock_game_map, 0, 6, 5, 10, 0, mock_game_status) == True
    # Blocked height
    mock_game_map[0][5][6]["h"] = 20
    assert check_volume_walkable(mock_game_map, 0, 6, 5, 10, 0, mock_game_status) == False
    # Out of bounds
    assert check_volume_walkable(mock_game_map, 0, 0, 0, 10, 0, mock_game_status) == False
    assert check_volume_walkable(mock_game_map, 1, 5, 5, 10, 0, mock_game_status) == False # floor 1 not in map
    # Character collision
    mock_game_map[0][5][6]["h"] = 10
    colliding_status = {"Planta": 0, "Personajes": [{"id": 1, "posX": 6, "posY": 5}]}
    assert check_volume_walkable(mock_game_map, 0, 6, 5, 10, 0, colliding_status) == False

def test_get_neighbors(mock_game_map, mock_game_status):
    n = get_neighbors(mock_game_map, 0, (5,5), mock_game_status, 0, 10)
    assert len(n) == 8

def test_a_star_logic(mock_game_map, mock_game_status):
    with patch("server.logic.get_game_status", return_value=mock_game_status):
        # Found
        path = a_star_search(mock_game_map, 0, (5, 5), (6, 5))
        assert path == [(5, 5), (6, 5)]
        
        # No path (blocked)
        blocked_map = [[ [{"h": 20} for _ in range(10)] for _ in range(10) ]]
        blocked_map[0][5][5]["h"] = 10
        path = a_star_search(blocked_map, 0, (5, 5), (9, 9))
        assert path is None

def test_path_utils():
    came_from = {(1,1): (0,0), (2,1): (1,1)}
    assert reconstruct_path(came_from, (2,1)) == [(0,0), (1,1), (2,1)]
    assert path_to_commands([(0,0), (1,0), (1,1), (0,1), (0,0)]) == ["RIGHT", "DOWN", "LEFT", "UP"]

def test_internal_service_functions(mocker, mock_game_status, mock_game_map):
    mocker.patch("server.logic.get_full_game_state_internal", return_value=mock_game_status)
    mocker.patch("server.logic.get_game_map", return_value=mock_game_map)
    mocker.patch("server.logic.send_game_command_internal")
    mocker.patch("server.logic.sendCmd", return_value={"status": "ok"})
    mocker.patch("server.logic.save_game_status")
    mocker.patch("server.logic.get_game_status", return_value=mock_game_status)

    assert get_possible_moves_internal()["status"] == "OK"
    assert move_to_location_internal("library")["status"] == "OK"
    assert investigate_location_internal("library")["status"] == "OK"
    assert talk_to_character_internal("abbot")["status"] == "OK"
    assert send_game_command_internal("UP") == {"status": "ok"}
    assert get_full_game_state_internal() == {"status": "ok"}

def test_error_handling_logic(mocker):
    mocker.patch("server.logic.sendCmd", side_effect=Exception("network error"))
    assert get_full_game_state_internal() is None
    assert send_game_command_internal("UP") is None
    
    # Missing location in move_to_location_internal
    from server.logic import move_to_location_internal
    assert move_to_location_internal("hell")["status"] == "ERROR"
    
    # Missing character in talk_to_character_internal
    from server.logic import talk_to_character_internal
    assert talk_to_character_internal("ghost")["status"] == "ERROR"

def test_a_star_edge_cases(mock_game_map, mock_game_status):
    # No game status
    with patch("server.logic.get_game_status", return_value=None):
        assert a_star_search(mock_game_map, 0, (0,0), (1,1)) is None
    # No Guillermo
    with patch("server.logic.get_game_status", return_value={"Personajes": []}):
        assert a_star_search(mock_game_map, 0, (0,0), (1,1)) is None
    
    # Pathfinding hit a blocked node in loop
    with patch("server.logic.get_game_status", return_value=mock_game_status):
        blocked_map = [[ [{"h": 10} for _ in range(3)] for _ in range(3) ]]
        blocked_map[0][0][1]["h"] = 20 # Block east
        blocked_map[0][1][0]["h"] = 20 # Block south
        # etc
        assert a_star_search(blocked_map, 0, (0,0), (2,2)) is None

def test_possible_moves_edge_cases(mocker, mock_game_map, mock_game_status):
    mocker.patch("server.logic.get_full_game_state_internal", return_value=None)
    assert get_possible_moves_internal()["status"] == "ERROR"
    
    mocker.patch("server.logic.get_full_game_state_internal", return_value=mock_game_status)
    mocker.patch("server.logic.get_game_map", return_value=None)
    assert get_possible_moves_internal()["status"] == "ERROR"
    
    mocker.patch("server.logic.get_game_map", return_value=mock_game_map)
    mocker.patch("server.logic.get_full_game_state_internal", return_value={"Personajes": []})
    assert get_possible_moves_internal()["status"] == "ERROR"
