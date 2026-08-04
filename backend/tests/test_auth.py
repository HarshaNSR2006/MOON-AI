import uuid

from fastapi.testclient import TestClient

from app.main import app


def test_register_login_and_me_flow() -> None:
    client = TestClient(app)
    unique_id = uuid.uuid4().hex[:8]
    username = f"moonuser_{unique_id}"
    email = f"{username}@example.com"

    register_payload = {
        "username": username,
        "email": email,
        "password": "StrongPass123!",
    }

    register_response = client.post("/auth/register", json=register_payload)
    assert register_response.status_code == 201
    user_data = register_response.json()
    assert user_data["username"] == username
    assert user_data["email"] == email

    login_response = client.post(
        "/auth/login",
        data={"username": username, "password": "StrongPass123!"},
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert token_data["token_type"] == "bearer"
    access_token = token_data["access_token"]
    assert access_token

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["username"] == username
    assert me_data["email"] == email
