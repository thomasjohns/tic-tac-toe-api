import pytest
from starlette.testclient import TestClient

from api.main import app


@pytest.fixture(scope='module')
def api_client():
    _api_client = TestClient(app)
    yield _api_client


def test_404(api_client):
    response = api_client.get('/missing')
    assert response.status_code == 404


def test_ping(api_client):
    response = api_client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {'ping': 'pong'}


def test_get_players(api_client):
    response = api_client.get('/players')
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1
    id_ = json[0]['id']
    created_at = json[0]['created_at']
    assert response.json() == [
        {
            'id': id_,
            'name': 'Computer',
            'kind': 'Computer',
            'created_at': created_at,
        }
    ]


def test_create_and_get_player_by_id(api_client):
    pass
