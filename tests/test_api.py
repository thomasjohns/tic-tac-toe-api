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
