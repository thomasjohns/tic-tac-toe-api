from uuid import uuid4

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
    create_response = api_client.post(
        '/players',
        json={
            'name': 'Thomas',
            'kind': 'Human',
        },
    )
    assert create_response.status_code == 200
    id_ = create_response.json()['id']
    get_response = api_client.get(f'/players/{id_}')
    assert get_response.status_code == 200
    json = get_response.json()
    assert json['name'] == 'Thomas'
    assert json['kind'] == 'Human'


def test_get_player_by_id_404(api_client):
    missing_player_id = uuid4()
    response = api_client.get(f'/players/{missing_player_id}')
    assert response.status_code == 404
    assert response.json() == {
        'detail': f'Player with id={missing_player_id} not found.',
    }


# NOTE: tests become much less exhaustive and more coupled at this point


def test_game_crud(api_client):
    create_player_response = api_client.post(
        '/players',
        json={
            'name': 'Thomas',
            'kind': 'Human',
        },
    )
    assert create_player_response.status_code == 200

    player_id = create_player_response.json()['id']

    create_game_response = api_client.post(
        '/games',
        json={
            'player_one_id': player_id,
        },
    )
    assert create_game_response.status_code == 200

    game_id = create_game_response.json()['id']

    get_games_by_player_response = api_client.get(
        f'/games/?player_id={player_id}'
    )
    assert get_games_by_player_response.status_code == 200
    assert len(get_games_by_player_response.json()) == 1

    get_game_board_response = api_client.get(f'/games/{game_id}/board')
    assert get_game_board_response.status_code == 200
    assert get_game_board_response.json() == {
        'board': '''\
.|.|.
-----
.|.|.
-----
.|.|.
'''
    }


def test_move_crud(api_client):
    create_player_response = api_client.post(
        '/players',
        json={
            'name': 'Thomas',
            'kind': 'Human',
        },
    )
    assert create_player_response.status_code == 200

    player_id = create_player_response.json()['id']

    create_game_response = api_client.post(
        '/games',
        json={
            'player_one_id': player_id,
        },
    )
    assert create_game_response.status_code == 200

    game_id = create_game_response.json()['id']

    for move in [(0, 0), (1, 0)]:
        create_move_response = api_client.post(
            f'/games/{game_id}/moves',
            json={
                'player_id': player_id,
                'x': move[0],
                'y': move[1],
            },
        )
        assert create_move_response.status_code == 200

    game_boards_response = api_client.get(f'/games/{game_id}/moves/boards')
    assert game_boards_response.status_code == 200

    assert game_boards_response.json() == {'boards': [
        '''\
X|.|.
-----
.|.|.
-----
.|.|.
''',
        '''\
X|O|.
-----
.|.|.
-----
.|.|.
''',
        '''\
X|O|.
-----
X|.|.
-----
.|.|.
''',
        '''\
X|O|O
-----
X|.|.
-----
.|.|.
''',
    ]}

    # After this move, the game should be over because player one has a
    # winning game state. The computer should not make any move after the
    # game ended.

    # First make sure the game is still in progress before we make the move.
    get_current_game_state_response = api_client.get(f'/games/{game_id}')
    assert get_current_game_state_response.status_code == 200
    assert get_current_game_state_response.json()['status'] == 'InProgress'

    create_final_move_response = api_client.post(
        f'/games/{game_id}/moves',
        json={
            'player_id': player_id,
            'x': 2,
            'y': 0,
        },
    )
    assert create_final_move_response.status_code == 200

    game_boards_response = api_client.get(f'/games/{game_id}/moves/boards')
    assert game_boards_response.status_code == 200

    assert game_boards_response.json() == {'boards': [
        '''\
X|.|.
-----
.|.|.
-----
.|.|.
''',
        '''\
X|O|.
-----
.|.|.
-----
.|.|.
''',
        '''\
X|O|.
-----
X|.|.
-----
.|.|.
''',
        '''\
X|O|O
-----
X|.|.
-----
.|.|.
''',
        '''\
X|O|O
-----
X|.|.
-----
X|.|.
''',
    ]}

    get_final_game_state_response = api_client.get(f'/games/{game_id}')
    assert get_final_game_state_response.status_code == 200
    assert get_final_game_state_response.json()['status'] == 'PlayerOneWon'
