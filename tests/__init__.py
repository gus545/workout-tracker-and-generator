import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_get_workouts(client):
    res = client.get('/workouts')
    assert res.status_code == 200
