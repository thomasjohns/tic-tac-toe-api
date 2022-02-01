from enum import Enum

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
