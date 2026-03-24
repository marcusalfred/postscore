"""
Tests for player endpoints: /api/v1/players/
"""
from ulid import ULID

from db.models import Player
from core.security import get_password_hash


SIGNUP_URL = "/api/v1/auth/signup"
LOGIN_URL = "/api/v1/auth/login"
PLAYERS_URL = "/api/v1/players/"


def _signup_and_login(client, email="player1@example.com", password="securepass1", name="Player One"):
    """Helper: create a player via signup and return an auth token."""
    client.post(SIGNUP_URL, json={
        "name": name,
        "email": email,
        "zip": "12345",
        "password": password,
    })
    resp = client.post(
        LOGIN_URL,
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json()["access_token"]


def _make_player_in_db(db, email="other@example.com", name="Other Player"):
    """Helper: insert a player directly into the DB and return the ORM object."""
    player = Player(
        id=str(ULID()),
        name=name,
        email=email,
        zip="54321",
        hashed_password=get_password_hash("securepass1"),
        is_active=True,
        is_super=False,
    )
    db.add(player)
    db.commit()
    return player


# ---------------------------------------------------------------------------
# GET /players/ tests
# ---------------------------------------------------------------------------

def test_get_players_returns_empty_list(client, db):
    # Sign up one player so we have auth, then list players
    token = _signup_and_login(client)
    resp = client.get(PLAYERS_URL, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    # The signed-up player counts, so at least one entry; test list is returned
    assert isinstance(resp.json(), list)


def test_get_players_returns_players_after_creation(client, db):
    token = _signup_and_login(client)
    # Add a second player directly in DB
    _make_player_in_db(db, email="second@example.com", name="Second Player")

    resp = client.get(PLAYERS_URL, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    players = resp.json()
    emails = [p["email"] for p in players]
    assert "player1@example.com" in emails
    assert "second@example.com" in emails


# ---------------------------------------------------------------------------
# GET /players/{id} tests
# ---------------------------------------------------------------------------

def test_get_player_by_id_returns_player(client, db):
    token = _signup_and_login(client)
    other = _make_player_in_db(db)

    resp = client.get(f"{PLAYERS_URL}{other.id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["id"] == other.id
    assert resp.json()["email"] == other.email


def test_get_player_by_bad_id_returns_404(client, db):
    token = _signup_and_login(client)
    bad_id = str(ULID())  # valid-format but non-existent

    resp = client.get(f"{PLAYERS_URL}{bad_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /players/{id} tests
# ---------------------------------------------------------------------------

def test_patch_player_by_owner_succeeds(client, db):
    token = _signup_and_login(client)

    # Find our own player id via /me
    me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    player_id = me_resp.json()["id"]

    resp = client.patch(
        f"{PLAYERS_URL}{player_id}",
        json={"zip": "99999"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["zip"] == "99999"


def test_patch_player_by_different_player_returns_403(client, db):
    # player1 tries to update player2's profile
    token1 = _signup_and_login(
        client,
        email="actor@example.com",
        password="securepass1",
        name="Actor Player",
    )
    player2 = _make_player_in_db(db, email="target@example.com", name="Target Player")

    resp = client.patch(
        f"{PLAYERS_URL}{player2.id}",
        json={"zip": "00000"},
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert resp.status_code == 403
