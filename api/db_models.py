import datetime as dt
from typing import Any
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from uuid import UUID
from uuid import uuid4

from api.api_models import GameStatus
from api.api_models import PlayerKind


# TODO: pydantic-ify these models


T = TypeVar('T')


class DatabaseModel(Generic[T]):
    def __init__(self) -> None:
        self.id = uuid4()
        self.created_at = dt.datetime.utcnow()

    def save(self) -> None:
        database.append(self)

    @classmethod
    def get_many(cls) -> List['DatabaseModel[T]']:
        return [item for item in database if isinstance(item, cls)]

    @classmethod
    def get_one(cls, id_: UUID) -> Optional['DatabaseModel[T]']:
        for item in database:
            if item.id == id_:
                assert isinstance(item, cls)
                return item
        return None


class Game(DatabaseModel['Game']):
    def __init__(
        self,
        player_one_id: UUID,
        player_two_id: Optional[UUID],
        status: Optional[GameStatus] = None,
    ) -> None:
        super().__init__()
        self.player_one_id = player_one_id
        self.player_two_id = \
            player_two_id or Player.get_default_computer_player().id
        self.status = status or GameStatus.IN_PROGRESS

    @classmethod
    def get_many_by_player(cls, player_id: UUID) -> List['Game']:
        return [
            item for item in database
            if (
                isinstance(item, Game) and
                (
                    player_id == item.player_one_id or
                    player_id == item.player_two_id
                )
            )
        ]


class Move(DatabaseModel['Move']):
    def __init__(
        self,
        game_id: UUID,
        player_id: UUID,
        x: int,
        y: int,
    ) -> None:
        super().__init__()
        self.game_id = game_id
        self.player_id = player_id
        self.x = x
        self.y = y

    @classmethod
    def get_many_by_game(cls, game_id: UUID) -> List['Move']:
        return [
            item for item in database
            if isinstance(item, Move) and item.game_id == game_id
        ]


class Player(DatabaseModel['Player']):
    def __init__(self, name: str, kind: PlayerKind) -> None:
        super().__init__()
        self.name = name
        self.kind = kind

    @classmethod
    def get_default_computer_player(cls) -> 'Player':
        default_computer_player = database[0]
        assert isinstance(default_computer_player, cls)
        return default_computer_player


# Initialize database with the computer player
database: List[DatabaseModel[Any]] = [  # FIXME fix the Any type here
    Player(name='Computer', kind=PlayerKind.COMPUTER),
]
