from itertools import cycle
from typing import Any
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException

from api.api_models import CreateGame
from api.api_models import CreatePlayer
from api.db_models import Game
from api.db_models import Move
from api.db_models import Player


# The return type for routes is complicated.
# see: https://github.com/tiangolo/fastapi/issues/101#issuecomment-475994050
APIResponse = Any

# TODO: Split into {health,game,move,player}_router?
main_router = APIRouter()


@main_router.get('/ping')
def ping() -> APIResponse:
    return {'ping': 'pong'}


# TODO: pydantic response_model
@main_router.post('/players')
def create_player(cp: CreatePlayer) -> APIResponse:
    player = Player(name=cp.name, kind=cp.kind)
    player.save()
    return player


# TODO: pydantic response_model
@main_router.get('/players')
def list_players() -> APIResponse:
    return Player.get_many()


# TODO: pydantic response_model
@main_router.get('/players/{player_id}')
def get_player_by_id(player_id: UUID) -> APIResponse:
    player = Player.get_one(id_=player_id)
    if player is None:
        raise HTTPException(
            status_code=404,
            detail=f'Player with id={player_id} not found.',
        )
    else:
        return player


# TODO: pydantic response_model
@main_router.get('/games')
def list_games() -> APIResponse:
    return Game.get_many()


# TODO: pydantic response_model
@main_router.get('/games/{game_id}')
def get_game_by_id(game_id: UUID) -> APIResponse:
    game = Game.get_one(id_=game_id)
    if game is None:
        raise HTTPException(
            status_code=404,
            detail=f'Game with id={game_id} not found.',
        )
    else:
        return game


def _get_board_str_from_moves(moves: List[Move]) -> str:
    board: List[List[str]] = [
        ['.', '.', '.'],
        ['.', '.', '.'],
        ['.', '.', '.'],
    ]
    letter = cycle('XO')
    for move in moves:
        board[move.x, move.y] = next(letter)  # type: ignore
    board_str = f'''
{board[0][0]}|{board[0][1]}|{board[0][2]}
-----
{board[1][0]}|{board[1][1]}|{board[1][2]}
-----
{board[2][0]}|{board[2][1]}|{board[2][2]}
'''
    return board_str


@main_router.get('/games/{game_id}/board')
def get_game_board(game_id: UUID) -> APIResponse:
    game = Game.get_one(id_=game_id)
    if game is None:
        raise HTTPException(
            status_code=404,
            detail=f'Game with id={game_id} not found.',
        )
    else:
        moves = Move.get_many_by_game(game_id=game.id)
        board_str = _get_board_str_from_moves(moves)
        return {'board': board_str}


# TODO: pydantic response_model
@main_router.get('/games/')
def get_games_by_player_id(player_id: UUID) -> APIResponse:
    player = Player.get_one(id_=player_id)
    if player is None:
        raise HTTPException(
            status_code=404,
            detail=f'Player with id={player_id} not found.',
        )
    games = Game.get_many_by_player(player_id=player_id)
    # FIXME: fix type ignore
    return sorted(games, key=lambda g: g.created_at)  # type: ignore


# TODO: pydantic response_model
@main_router.post('/games')
def create_game(cg: CreateGame) -> APIResponse:
    game = Game(cg.player_one_id, cg.player_two_id)
    game.save()
    return game
