import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from server.main import app
import json

client = TestClient(app)

@pytest.fixture
def mock_game_response():
    return {
        "status": "OK",
        "Personajes": [
            {
                "altura": 0,
                "id": 0,
                "nombre": "Guillermo",
                "objetos": 32,
                "orientacion": 1,
                "posX": 136,
                "posY": 168
            }
        ],
        "Rejilla": [[0 for _ in range(24)] for _ in range(24)],
        "Planta": 0,
        "NumPantalla": 23,
        "dia": 1,
        "momentoDia": 4
    }

@patch("server.common.requests.get")
@patch("server.common.requests.post")
def test_get_status_functional(mock_post, mock_get, mock_game_response):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_game_response
    
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["data"]["Personajes"][0]["nombre"] == "Guillermo"

@patch("server.common.requests.get")
@patch("server.common.requests.post")
@patch("server.main.time.sleep", return_value=None)
def test_reset_game_functional(mock_sleep, mock_post, mock_get, mock_game_response):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_game_response
    
    response = client.get("/reset")
    assert response.status_code == 200
    assert response.json()["message"] == "Game reset successfully"

@patch("server.common.requests.get")
@patch("server.common.requests.post")
def test_send_game_cmd_functional(mock_post, mock_get, mock_game_response):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "OK"}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_game_response
    
    response = client.get("/game/cmd/UP")
    assert response.status_code == 200
    assert response.json()["message"] == "Command UP execution attempted"

@patch("server.common.requests.get")
@patch("server.common.requests.post")
@patch("server.main.get_game_status")
def test_send_move_cmd_functional(mock_get_status, mock_post, mock_get, mock_game_response):
    mock_get_status.return_value = mock_game_response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "OK"}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_game_response
    
    # Orientation 1 (North), move North (N) -> UP:UP
    response = client.get("/game/move/N")
    assert response.status_code == 200
    assert response.json()["message"] == "Moved N"
    # send_game_command_internal uses mode='GET' by default
    assert mock_get.call_count >= 3 # 1 for status check (if any) + 2 for moves. 
    # Actually main.py:127 calls get_game_status() (no network call if cached)
    # Then main.py:133 calls send_game_command_internal (network GET)
    # Then main.py:136 calls get_full_game_state_internal (network GET)
    # So 2 for moves + 1 for final status = 3

def test_get_internal_status_functional():
    response = client.get("/internal_status")
    assert response.status_code == 200
    assert "current_day" in response.json()

@patch("server.main.get_game_map")
@patch("server.main.get_game_status")
def test_get_map_ascii_functional(mock_get_status, mock_get_map, mock_game_response):
    # Mock a minimal map: 1 floor, 2x2
    mock_get_map.return_value = [[[None, None], [None, None]]]
    mock_get_status.return_value = mock_game_response
    
    response = client.get("/map/ascii?cells=2&center_on_guillermo=false&center_x=0&center_y=0")
    assert response.status_code == 200
    assert isinstance(response.text, str)

@patch("server.main.save_map")
def test_save_map_functional(mock_save_map):
    response = client.post("/map/save/test_map")
    assert response.status_code == 200
    assert "test_map" in response.json()["message"]
    mock_save_map.assert_called_once()

@patch("server.main.load_game_map")
def test_load_map_functional(mock_load_map):
    response = client.post("/map/load/test_map")
    assert response.status_code == 200
    assert "test_map" in response.json()["message"]
    mock_load_map.assert_called_once()

@patch("server.logic.send_game_command_internal")
@patch("server.logic.get_full_game_state_internal")
def test_move_to_location_tool_functional(mock_get_state, mock_send_cmd):
    mock_get_state.return_value = {"status": "OK"}
    response = client.post("/tools/move_to_location?location=library")
    assert response.status_code == 200
    assert "Successfully moved to library" in response.json()["message"]

@patch("server.logic.get_game_map")
@patch("server.logic.get_game_status")
def test_find_path_to_location_functional(mock_get_status, mock_get_map, mock_game_response):
    # Mock a navigable map
    # A floor of 200x200
    m_floor = [[None for _ in range(200)] for _ in range(200)]
    mock_get_map.return_value = [m_floor]
    mock_get_status.return_value = mock_game_response
    
    # Target is (137, 168) from (136, 168) -> one step Right
    response = client.post("/tools/find_path_to_location?dest_x=137&dest_y=168&floor=0")
    assert response.status_code == 200
    assert response.json()["data"] == ["RIGHT"]
