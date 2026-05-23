import pytest
from unittest.mock import patch, MagicMock
from server.logic import move_cardinal_internal, wait_internal

@pytest.fixture
def mock_game_status():
    with patch('server.logic.get_game_status') as mock:
        mock.return_value = {
            "Personajes": [
                {"nombre": "Guillermo", "posX": 100, "posY": 100, "orientacion": 1, "altura": 0, "id": 0}
            ],
            "Planta": 0
        }
        yield mock

@pytest.fixture
def mock_send_command():
    with patch('server.logic.send_game_command_internal') as mock:
        yield mock

def test_move_cardinal_n_facing_n(mock_game_status, mock_send_command):
    # Orientation 1 is North. Moving N should just be UP:UP.
    res = move_cardinal_internal("N")
    assert res["status"] == "OK"
    assert mock_send_command.call_count == 2
    mock_send_command.assert_any_call("UP")

def test_move_cardinal_e_facing_n(mock_game_status, mock_send_command):
    # Orientation 1 is North. Moving E should be RIGHT:UP:UP.
    res = move_cardinal_internal("E")
    assert res["status"] == "OK"
    # Mapping for 1E is RIGHT:UP:UP
    assert mock_send_command.call_count == 3
    calls = [call.args[0] for call in mock_send_command.call_args_list]
    assert calls == ["RIGHT", "UP", "UP"]

def test_wait_nop():
    with patch('server.logic.get_full_game_state_internal') as mock_state:
        mock_state.return_value = {"status": "mocked"}
        res = wait_internal()
        assert res["status"] == "OK"
        assert "NOP executed" in res["message"]
        mock_state.assert_called_once()
