from typing import Any

from fastapi import APIRouter


# The return type for routes is complicated.
# see: https://github.com/tiangolo/fastapi/issues/101#issuecomment-475994050
APIResponse = Any

# TODO: Split into {health,game,move,player}_router?
main_router = APIRouter()


@main_router.get('/ping')
def ping() -> APIResponse:
    return {'ping': 'pong'}
