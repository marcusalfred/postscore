import pytest
from ulid import ULID

from db.models import Course, TeeBox, TeeBoxHole, Player, Round, RoundHole
from core.security import get_password_hash


def make_course(db):
    course = Course(
        id=str(ULID()),
        name="Test Course",
        address="100 Golf Rd",
        city="Golftown",
        state="TX",
        zip="77001",
        website="https://testcourse.example.com",
    )
    db.add(course)
    db.commit()
    return course


def make_tee_box(db, course_id):
    tee_box = TeeBox(
        id=str(ULID()),
        name="White",
        course_id=course_id,
        rating=70.0,
        slope=125,
        yardage=6200,
    )
    db.add(tee_box)
    db.commit()
    return tee_box


def make_tee_box_hole(db, tee_box_id, hole_number=1):
    hole = TeeBoxHole(
        id=str(ULID()),
        tee_box_id=tee_box_id,
        hole_number=hole_number,
        par=4,
        yardage=400,
        handicap=5,
    )
    db.add(hole)
    db.commit()
    return hole


def make_player(db):
    player = Player(
        id=str(ULID()),
        name="Round Tester",
        email="roundtester@example.com",
        zip="77001",
        hashed_password=get_password_hash("testpass123"),
        is_active=True,
        is_super=False,
    )
    db.add(player)
    db.commit()
    return player


def get_token_for_player(client, email="roundtester@example.com", password="testpass123"):
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json()["access_token"]


def test_create_round(client, db):
    course = make_course(db)
    tee_box = make_tee_box(db, course.id)
    player = make_player(db)
    token = get_token_for_player(client)

    resp = client.post(
        "/api/v1/rounds/",
        json={
            "course_id": course.id,
            "tee_box_id": tee_box.id,
            "player_id": player.id,
            "holes": 18,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["course_id"] == course.id
    assert data["player_id"] == player.id
    assert "id" in data


def test_get_round_not_found(client, db):
    player = make_player(db)
    token = get_token_for_player(client)

    resp = client.get(
        "/api/v1/rounds/nonexistent_round_id_000000",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404


def test_add_duplicate_round_hole(client, db):
    course = make_course(db)
    tee_box = make_tee_box(db, course.id)
    hole = make_tee_box_hole(db, tee_box.id, hole_number=1)
    player = make_player(db)
    token = get_token_for_player(client)

    # Create a round
    create_resp = client.post(
        "/api/v1/rounds/",
        json={
            "course_id": course.id,
            "tee_box_id": tee_box.id,
            "player_id": player.id,
            "holes": 18,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_resp.status_code == 201
    round_id = create_resp.json()["id"]

    hole_payload = {
        "round_id": round_id,
        "tee_box_hole_id": hole.id,
        "score": 4,
    }

    # Add the hole the first time — should succeed
    first_resp = client.post(
        "/api/v1/rounds/holes",
        json=hole_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert first_resp.status_code == 201

    # Add the same hole again — should return 422
    second_resp = client.post(
        "/api/v1/rounds/holes",
        json=hole_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert second_resp.status_code == 422
