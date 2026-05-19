import pytest
from server.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

client = TestClient(app)

@patch("server.main.get_full_game_state_internal")
def test_all_mcp_tools_and_rest(mock_get_state):
    mock_get_state.return_value = {
        "Planta": 0, "NumPantalla": 1, "dia": 1, "numPantalla": 1,
        "Personajes": [{"nombre": "Guillermo", "posX": 10, "posY": 10, "orientacion": 0, "id": 0}],
        "Rejilla": [[1]]
    }
    
    # 1. toggle_adso
    with patch("server.main.send_game_command_internal") as m:
        client.post("/tools/toggle_adso")
        client.post("/tools/send_game_command?command=S")
        
    # 2. movement
    with patch("server.main.move_to_location_internal", return_value={"status": "OK", "message": "ok"}):
        client.post("/tools/move_to_location?location=library")
        client.get("/game/move/N")
        
    # 3. investigation & talk
    with patch("server.main.investigate_location_internal", return_value={"status": "OK", "message": "ok"}):
        client.post("/tools/investigate_location?location=library")
    with patch("server.main.talk_to_character_internal", return_value={"status": "OK", "message": "ok"}):
        client.post("/tools/talk_to_character?character=abbot")

    # 4. find_path
    with patch("server.main.find_path_to_location_internal", return_value={"status": "OK", "data": ["UP"]}):
        client.post("/tools/find_path_to_location?dest_x=11&dest_y=11")
    with patch("server.main.find_path_to_location_internal", return_value={"status": "ERROR", "message": "fail"}):
        client.post("/tools/find_path_to_location?dest_x=11&dest_y=11")
        
    # 5. possible_moves
    with patch("server.main.get_possible_moves_internal", return_value={"status": "OK", "data": {"basic_moves": ["UP"]}}):
        client.get("/game/possible_moves")
        client.get("/tools/get_possible_moves")
    with patch("server.main.get_possible_moves_internal", return_value={"status": "ERROR", "message": "fail"}):
        client.get("/game/possible_moves")
        
    # 6. map
    with patch("server.main.draw_map_ascii", return_value="map"):
        client.get("/map/ascii")
        client.get("/map/ascii?center_on_guillermo=false&floor=0&center_x=10&center_y=10&cells=5")
        
    # 7. status variants
    client.get("/status")
    client.get("/tools/get_full_game_state")
    client.get("/internal_status")
    
    # 8. reset
    with patch("server.main.sendCmd", return_value={"NumPantalla": 1}):
        client.get("/reset")
        
    # 9. map save/load
    with patch("server.main.save_map") as ms, patch("server.main.load_game_map") as ml:
        client.post("/map/save/test")
        client.post("/map/load/test")
    
    # 10. game cmd and rest tools
    with patch("server.main.send_game_command_internal", return_value={"status": "OK"}):
        client.get("/game/cmd/UP")
        client.post("/tools/send_game_command?command=UP")

    # 11. startup call (to cover @app.on_event("startup"))
    with patch("server.main.initialize_map"):
         # Triggering startup event manually for coverage if possible, 
         # but TestClient does it on initialization usually.
         pass

def test_error_branches():
    with patch("server.main.get_full_game_state_internal", return_value=None):
        response = client.get("/status")
        assert response.status_code == 502
    
    with patch("server.main.send_game_command_internal", return_value=None):
        response = client.get("/game/cmd/UP")
        assert response.status_code == 502

    # Tool errors
    with patch("server.main.move_to_location_internal", return_value={"status": "ERROR", "message": "err"}):
        res = client.post("/tools/move_to_location?location=library")
        assert res.status_code == 400
    with patch("server.main.investigate_location_internal", return_value={"status": "ERROR", "message": "err"}):
        res = client.post("/tools/investigate_location?location=library")
        assert res.status_code == 400
    with patch("server.main.talk_to_character_internal", return_value={"status": "ERROR", "message": "err"}):
        res = client.post("/tools/talk_to_character?character=abbot")
        assert res.status_code == 400

@pytest.mark.asyncio
async def test_mcp_direct_calls():
    from server.main import toggle_adso, move_to_location, investigate_location, talk_to_character, find_path, get_possible_moves, send_game_command, list_mcp_tools, get_full_game_state, startup_event
    with patch("server.main.send_game_command_internal"):
        await toggle_adso()
        await send_game_command("UP")
    with patch("server.main.move_to_location_internal", return_value={"message": "ok"}):
        await move_to_location("library")
    with patch("server.main.investigate_location_internal", return_value={"message": "ok"}):
        await investigate_location("library")
    with patch("server.main.talk_to_character_internal", return_value={"message": "ok"}):
        await talk_to_character("abbot")
    with patch("server.main.find_path_to_location_internal", return_value={"status": "OK", "data": ["UP"]}):
        await find_path(10, 10)
    with patch("server.main.find_path_to_location_internal", return_value={"status": "ERROR", "message": "err"}):
        await find_path(10, 10)
    with patch("server.main.get_possible_moves_internal", return_value={"data": {}}):
        await get_possible_moves()
    with patch("server.main.get_full_game_state_internal", return_value={}):
        await get_full_game_state()
    
    res = await list_mcp_tools()
    assert "tools" in res
    
    with patch("server.main.initialize_map"):
        await startup_event()
