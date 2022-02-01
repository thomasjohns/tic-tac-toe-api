from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GameStatus(str, Enum):
    IN_PROGRESS = 'InProgress'
    PLAYER_ONE_WON = 'PlayerOneWon'
    PLAYER_TWO_WON = 'PlayerTwoWon'
    SCRATCH = 'Scratch'


class PlayerKind(str, Enum):
    COMPUTER = 'Computer'
    HUMAN = 'Human'


class CreatePlayer(BaseModel):
    name: str
    kind: PlayerKind


class CreateGame(BaseModel):
    player_one_id: UUID
    player_two_id: Optional[UUID]
