import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_create_set(client):
    payload = {
        "workout_name": "Push Day",
        "exercise_id": "bench001",
        "set_number": 1,
        "weight": 135.0,
        "reps": 8,
        "date": "2025-05-07",
        "exercise_notes": "Felt strong today"
    }
    res = client.post("/sets", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert "inserted" in data
    assert data["inserted"][0]["exercise_id"] == "bench001"

def test_get_set(client):
    # Assumes previous test has inserted data
    res = client.get("/sets?date=2025-05-07&set_number=1&exercise_id=bench001")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert data[0]["set_number"] == 1
