import pytest
from sqlalchemy.exc import IntegrityError
from ulid import ULID

from db.models import Course, TeeBox


def get_auth_token(client):
    client.post("/api/v1/auth/signup", json={
        "email": "test@example.com",
        "password": "testpass123",
        "name": "Test User",
        "zip": "12345"
    })
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json()["access_token"]


def test_get_courses_empty(client):
    resp = client.get("/api/v1/courses/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_course(client):
    token = get_auth_token(client)
    resp = client.post(
        "/api/v1/courses/",
        json={
            "name": "Pebble Beach Golf Links",
            "address": "1700 17-Mile Drive",
            "city": "Pebble Beach",
            "state": "CA",
            "zip": "93953",
            "website": "https://www.pebblebeach.com",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Pebble Beach Golf Links"
    assert "id" in data


def test_get_course_by_id(client):
    token = get_auth_token(client)
    create_resp = client.post(
        "/api/v1/courses/",
        json={
            "name": "Augusta National Golf Club",
            "address": "2604 Washington Rd",
            "city": "Augusta",
            "state": "GA",
            "zip": "30904",
            "website": "https://www.augusta.com",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    course_id = create_resp.json()["id"]

    resp = client.get(f"/api/v1/courses/{course_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == course_id
    assert resp.json()["name"] == "Augusta National Golf Club"


def test_get_course_not_found(client):
    resp = client.get("/api/v1/courses/nonexistent_id_000000000000")
    assert resp.status_code == 404


def test_tee_box_name_unique_per_course(db):
    # Two different courses should both be allowed to have a tee box named "Blue".
    # This test documents the expected behavior after the uniqueness-per-course bug fix.
    # With the current schema (unique=True globally on TeeBox.name), the second insert
    # will raise an IntegrityError — demonstrating the bug.
    course1 = Course(
        id=str(ULID()),
        name="Course Alpha",
        address="1 Alpha Way",
        city="Springfield",
        state="IL",
        zip="62701",
        website="https://alpha.example.com",
    )
    course2 = Course(
        id=str(ULID()),
        name="Course Beta",
        address="2 Beta Way",
        city="Springfield",
        state="IL",
        zip="62701",
        website="https://beta.example.com",
    )
    db.add(course1)
    db.add(course2)
    db.commit()

    tee1 = TeeBox(
        id=str(ULID()),
        name="Blue",
        course_id=course1.id,
        rating=71.5,
        slope=130,
    )
    db.add(tee1)
    db.commit()

    tee2 = TeeBox(
        id=str(ULID()),
        name="Blue",
        course_id=course2.id,
        rating=69.0,
        slope=120,
    )
    db.add(tee2)
    # After the fix, this commit should succeed with no error.
    # Until the fix is applied, it will raise IntegrityError due to the global unique constraint.
    db.commit()

    db.refresh(tee1)
    db.refresh(tee2)
    assert tee1.name == tee2.name == "Blue"
    assert tee1.course_id != tee2.course_id
