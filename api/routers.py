from typing import Any

from fastapi import APIRouter

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


@main_router.get('/players')
def list_players() -> APIResponse:
    return Player.get_many()
