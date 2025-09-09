import pytest
from fastapi.testclient import TestClient
from server.main import app  # Import the FastAPI app from your server code

# Create a TestClient instance
client = TestClient(app)

def test_status_endpoint():
    """Tests the /status endpoint."""
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_move_to_location_success(mocker):
    """Tests the /move_to/{location} endpoint for a successful case."""
    # Mock the sendCmd function to avoid real network calls
    mocker.patch("server.main.sendCmd", return_value={"game_state": "mocked"})

    response = client.post("/move_to/library")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "OK"
    assert json_response["message"] == "Successfully moved to library"

def test_move_to_location_not_found():
    """Tests the /move_to/{location} endpoint for a location that doesn't exist."""
    response = client.post("/move_to/non_existent_place")
    assert response.status_code == 404
    assert response.json() == {"detail": "Location 'non_existent_place' not found."}

def test_investigate_location_success(mocker):
    """Tests the /investigate/{location} endpoint for a successful case."""
    # Mock the sendCmd function
    mocker.patch("server.main.sendCmd", return_value={"game_state": "mocked"})
    
    # We also need to mock the move_to function within the investigate function
    # Since it's an async function, we'll mock it with an async mock
    mocker.patch("server.main.move_to", new_callable=mocker.AsyncMock)

    response = client.post("/investigate/church")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "OK"
    assert json_response["message"] == "Successfully investigated church"

def test_investigate_location_not_found(mocker):
    """Tests the /investigate/{location} endpoint for a location that doesn't exist."""
    # Mock the sendCmd function
    mocker.patch("server.main.sendCmd", return_value={"game_state": "mocked"})
    
    response = client.post("/investigate/non_existent_place")
    assert response.status_code == 404
