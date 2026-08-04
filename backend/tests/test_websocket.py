import json

from fastapi.testclient import TestClient

from app.main import app


def test_websocket_invalid_payload() -> None:
    client = TestClient(app)
    with client.websocket_connect("/ws/chat") as websocket:
        websocket.send_text("not a json payload")
        response = websocket.receive_text()
        message = json.loads(response)
        assert "error" in message
