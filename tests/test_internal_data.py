import pytest
from server.internal_game_data import (
    update_internal_game_data,
    reset_internal_game_data,
    get_internal_game_data
)

def test_internal_game_data_cycle():
    reset_internal_game_data()
    status = {
        "O": 100,
        "S": 0,
        "Planta": 0,
        "numPantalla": 23,
        "Personajes": [{"nombre": "Abad", "posX": 136, "posY": 168}]
    }
    update_internal_game_data(status)
    data = get_internal_game_data()
    assert data["O"] == 100
    assert data["investigation_notes"]["Abad"] == "Met the Abbot."
    assert 23 in data["map_discovered"]
    
    reset_internal_game_data()
    assert len(get_internal_game_data()["map_discovered"]) == 0
