import pytest
from server.game_data import (
    get_cell,
    set_cell,
    save_game_status,
    get_game_status,
    get_game_map,
    initialize_and_truncate_map,
    reset_game_data,
    update_map_from_game_state,
    load_game_map,
    initialize_map,
    _update_dynamic_entities
)
import os

@pytest.fixture
def clean_game_data():
    reset_game_data()
    yield
    reset_game_data()

def test_cell_operations(clean_game_data, mocker):
    m_map = [[[{"h": 0} for _ in range(10)] for _ in range(10)]]
    mocker.patch("server.game_data.game_map", m_map)
    set_cell(0, 5, 5, {"h": 5, "c": 0, "o": 0, "r": 0})
    assert get_cell(0, 5, 5)["h"] == 5
    assert get_cell(0, 9, 9)["h"] == 0
    assert get_cell(1, 0, 0)["h"] == 0

def test_save_get_status(clean_game_data, mocker):
    mocker.patch("server.game_data.update_internal_game_data")
    mocker.patch("server.game_data.update_map_from_game_state")
    status = {"Planta": 0}
    save_game_status(status)
    assert get_game_status() == status
    assert get_game_map() == []

def test_load_game_map(clean_game_data, mocker):
    mocker.patch("server.map_utils.load_map", return_value=[[[{"h": 1}]]])
    load_game_map("test")
    assert get_game_map()[0][0][0]["h"] == 1

def test_initialize_map(clean_game_data, mocker, tmp_path):
    mocker.patch("server.config.STORE_PATH", str(tmp_path))
    mocker.patch("server.game_data.load_game_map")
    m_map = [
        [[{"h": 0} for _ in range(300)] for _ in range(300)],
        [[{"h": 0} for _ in range(150)] for _ in range(150)],
        [[{"h": 0} for _ in range(150)] for _ in range(150)]
    ]
    mocker.patch("server.game_data.game_map", m_map)
    initialize_map()
    assert len(m_map[0]) == 256
    assert len(m_map[1]) == 100
    assert len(m_map[2]) == 100

def test_update_map_from_game_state_logic(clean_game_data, mocker):
    m_map = [[[{"h": 0, "r": 0} for _ in range(50)] for _ in range(50)]]
    mocker.patch("server.game_data.game_map", m_map)
    mocker.patch("server.map_utils.save_map")
    status = {
        "Planta": 0, "NumPantalla": 23,
        "Personajes": [{"nombre": "Guillermo", "posX": 10, "posY": 10, "id": 0}],
        "Rejilla": [[1]]
    }
    update_map_from_game_state(status)
    # Testing branch where map is saved on screen change
    m_map[0][10][10]["r"] = 1
    update_map_from_game_state(status)

def test_update_dynamic_entities(clean_game_data, mocker):
    m_map = [[[{"h": 0, "c": 0, "o": 0} for _ in range(50)] for _ in range(50)]]
    mocker.patch("server.game_data.game_map", m_map)
    status = {
        "Planta": 0,
        "Personajes": [{"id": 0, "posX": 10, "posY": 10, "nombre": "Guillermo"}],
        "Objetos": [{"id": 1, "posX": 11, "posY": 11}]
    }
    _update_dynamic_entities(status, 0, 0)
    assert get_cell(0, 10, 10)["c"] == 1
    assert get_cell(0, 11, 11)["o"] == 1
