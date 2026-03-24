"""
Tests for authentication endpoints: /api/v1/auth/signup, /api/v1/auth/login, /api/v1/auth/me
"""


SIGNUP_URL = "/api/v1/auth/signup"
LOGIN_URL = "/api/v1/auth/login"
ME_URL = "/api/v1/auth/me"

VALID_PLAYER = {
    "name": "Auth Tester",
    "email": "authtest@example.com",
    "zip": "12345",
    "password": "securepass1",
}


def _signup_and_login(client, email="authtest@example.com", password="securepass1"):
    resp = client.post(SIGNUP_URL, json={
        "name": "Auth Tester",
        "email": email,
        "zip": "12345",
        "password": password,
    })
    return resp.json()["access_token"]


# ---------------------------------------------------------------------------
# Signup tests
# ---------------------------------------------------------------------------

def test_signup_valid_data_returns_201(client):
    resp = client.post(SIGNUP_URL, json=VALID_PLAYER)
    assert resp.status_code == 201
    data = resp.json()
    # Signup now returns SignupResponse: { player, access_token, token_type }
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    player = data["player"]
    assert player["email"] == VALID_PLAYER["email"]
    assert player["name"] == VALID_PLAYER["name"]
    assert "id" in player
    assert "password" not in player
    assert "hashed_password" not in player


def test_signup_duplicate_email_returns_422(client):
    client.post(SIGNUP_URL, json=VALID_PLAYER)
    # Second signup with same email
    resp = client.post(SIGNUP_URL, json=VALID_PLAYER)
    assert resp.status_code == 422


def test_signup_without_password_returns_422(client):
    payload = {
        "name": "No Pass Player",
        "email": "nopass@example.com",
        "zip": "12345",
        # password intentionally omitted
    }
    resp = client.post(SIGNUP_URL, json=payload)
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Login tests
# ---------------------------------------------------------------------------

def test_login_valid_credentials_returns_token(client):
    client.post(SIGNUP_URL, json=VALID_PLAYER)
    resp = client.post(
        LOGIN_URL,
        data={"username": VALID_PLAYER["email"], "password": VALID_PLAYER["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password_returns_401(client):
    client.post(SIGNUP_URL, json=VALID_PLAYER)
    resp = client.post(
        LOGIN_URL,
        data={"username": VALID_PLAYER["email"], "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# /me tests
# ---------------------------------------------------------------------------

def test_get_me_with_valid_token_returns_current_user(client):
    token = _signup_and_login(client)
    resp = client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == VALID_PLAYER["email"]
    assert data["name"] == VALID_PLAYER["name"]
    assert "id" in data


def test_get_me_without_token_returns_401(client):
    resp = client.get(ME_URL)
    assert resp.status_code == 401
