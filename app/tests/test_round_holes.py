"""
Tests for round hole endpoints.

Round hole routes (all under /api/v1/rounds/):
  POST   /holes                    -> create a round hole
  GET    /holes/{round_hole_id}    -> get round hole detail
  PATCH  /holes/{round_hole_id}    -> update a round hole
  DELETE /holes/{round_hole_id}    -> delete a round hole

Duplicate hole for the same round returns 422.
"""
from ulid import ULID

from db.models import Course, TeeBox, TeeBoxHole, Player, Round
from core.security import get_password_hash


SIGNUP_URL = "/api/v1/auth/signup"
LOGIN_URL = "/api/v1/auth/login"
ROUNDS_URL = "/api/v1/rounds/"
HOLES_URL = "/api/v1/rounds/holes"


# ---------------------------------------------------------------------------
# DB helpers (direct inserts – same pattern as test_rounds.py)
# ---------------------------------------------------------------------------

def _make_course(db):
    course = Course(
        id=str(ULID()),
        name="Hole Test Course",
        address="1 Hole Rd",
        city="Holetown",
        state="TX",
        zip="77001",
        website="https://holecourse.example.com",
    )
    db.add(course)
    db.commit()
    return course


def _make_tee_box(db, course_id):
    tee_box = TeeBox(
        id=str(ULID()),
        name="Blue",
        course_id=course_id,
        rating=71.0,
        slope=128,
        yardage=6500,
    )
    db.add(tee_box)
    db.commit()
    return tee_box


def _make_tee_box_hole(db, tee_box_id, hole_number=1):
    hole = TeeBoxHole(
        id=str(ULID()),
        tee_box_id=tee_box_id,
        hole_number=hole_number,
        par=4,
        yardage=420,
        handicap=7,
    )
    db.add(hole)
    db.commit()
    return hole


def _make_player(db):
    player = Player(
        id=str(ULID()),
        name="Hole Tester",
        email="holetester@example.com",
        zip="77001",
        hashed_password=get_password_hash("securepass1"),
        is_active=True,
        is_super=False,
    )
    db.add(player)
    db.commit()
    return player


def _get_token(client, email="holetester@example.com", password="securepass1"):
    resp = client.post(
        LOGIN_URL,
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json()["access_token"]


def _setup(db, client):
    """Create course, tee box, tee box hole, player and return everything plus a token."""
    course = _make_course(db)
    tee_box = _make_tee_box(db, course.id)
    tbh = _make_tee_box_hole(db, tee_box.id, hole_number=1)
    player = _make_player(db)
    token = _get_token(client)
    return course, tee_box, tbh, player, token


def _create_round(client, course_id, tee_box_id, player_id, token):
    resp = client.post(
        ROUNDS_URL,
        json={
            "course_id": course_id,
            "tee_box_id": tee_box_id,
            "player_id": player_id,
            "holes": 18,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_round_hole(client, round_id, tee_box_hole_id, token, score=4):
    return client.post(
        HOLES_URL,
        json={
            "round_id": round_id,
            "tee_box_hole_id": tee_box_hole_id,
            "score": score,
        },
        headers={"Authorization": f"Bearer {token}"},
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_create_round_hole(client, db):
    course, tee_box, tbh, player, token = _setup(db, client)
    round_id = _create_round(client, course.id, tee_box.id, player.id, token)

    resp = _create_round_hole(client, round_id, tbh.id, token)
    assert resp.status_code == 201
    data = resp.json()
    assert data["round_id"] == round_id
    assert data["tee_box_hole_id"] == tbh.id
    assert data["score"] == 4
    assert "id" in data


def test_get_round_hole_detail(client, db):
    course, tee_box, tbh, player, token = _setup(db, client)
    round_id = _create_round(client, course.id, tee_box.id, player.id, token)

    create_resp = _create_round_hole(client, round_id, tbh.id, token)
    round_hole_id = create_resp.json()["id"]

    resp = client.get(
        f"{HOLES_URL}/{round_hole_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == round_hole_id
    assert data["round_id"] == round_id
    assert data["score"] == 4


def test_create_duplicate_hole_for_same_round_returns_422(client, db):
    course, tee_box, tbh, player, token = _setup(db, client)
    round_id = _create_round(client, course.id, tee_box.id, player.id, token)

    # First insert should succeed
    first = _create_round_hole(client, round_id, tbh.id, token)
    assert first.status_code == 201

    # Second insert of the same hole in the same round should fail
    second = _create_round_hole(client, round_id, tbh.id, token)
    assert second.status_code == 422


def test_patch_round_hole(client, db):
    course, tee_box, tbh, player, token = _setup(db, client)
    round_id = _create_round(client, course.id, tee_box.id, player.id, token)

    create_resp = _create_round_hole(client, round_id, tbh.id, token, score=4)
    round_hole_id = create_resp.json()["id"]

    resp = client.patch(
        f"{HOLES_URL}/{round_hole_id}",
        json={"score": 6, "putts": 3},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["score"] == 6
    assert data["putts"] == 3


def test_delete_round_hole(client, db):
    course, tee_box, tbh, player, token = _setup(db, client)
    round_id = _create_round(client, course.id, tee_box.id, player.id, token)

    create_resp = _create_round_hole(client, round_id, tbh.id, token)
    round_hole_id = create_resp.json()["id"]

    del_resp = client.delete(
        f"{HOLES_URL}/{round_hole_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert del_resp.status_code == 204

    # Confirm it's gone
    get_resp = client.get(
        f"{HOLES_URL}/{round_hole_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_resp.status_code == 404
