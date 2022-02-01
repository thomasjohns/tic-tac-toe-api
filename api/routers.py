from typing import Any
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException

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
