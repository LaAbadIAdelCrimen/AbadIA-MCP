from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_execute_command():
    response = client.post(
        "/api/command",
        json={"command": "test", "parameters": {}}
    )
    assert response.status_code == 200
    assert "status" in response.json() 