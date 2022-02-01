import datetime as dt
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from uuid import UUID
from uuid import uuid4

from api.api_models import GameStatus
from api.api_models import PlayerKind


T = TypeVar('T', bound='DatabaseModel')


class DatabaseModel(Generic[T]):
    def __init__(self) -> None:
        self.id = uuid4()
        self.created_at = dt.datetime.utcnow()

    def save(self) -> None:
        database.append(self)

    @classmethod
    def get_many(cls) -> List[T]:
        return [item for item in database if isinstance(item, cls)]

    @classmethod
    def get_one(cls, id_: UUID) -> Optional[T]:
        for item in database:
            if item.id == id_:
                assert isinstance(item, cls)
                return item
        return None


class Game(DatabaseModel):
    def __init__(
        self,
        player_one_id: UUID,
        player_two_id: Optional[UUID],
        status: GameStatus,
    ) -> None:
        super().__init__()
        self.player_one_id = player_one_id
        self.player_two_id = \
            player_two_id or Player.get_default_computer_player().id
        self.status = status


class Move(DatabaseModel):
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


class Player(DatabaseModel):
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
database: List[DatabaseModel] = [
    Player(name='Computer', kind=PlayerKind.COMPUTER),
]
