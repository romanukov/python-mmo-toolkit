from typing import Optional
from uuid import uuid4

from backend.common.logic.auth import IAuth
from backend.logic.repos import PlayersRepo


_players: dict[str, int] = {}


class LogicAuth(IAuth):
    def authenticate(self, token) -> Optional[int]:
        if token in _players:
            return _players[token]
        return None

    def authorize(self, player_name, password) -> str:
        players_repo = PlayersRepo()
        player = players_repo.get_by_name_and_password(player_name, password)
        if not player:
            raise ...
        token = self._tokenize(player.id)
        _players[token] = player.id
        return token

    def _tokenize(self, player_id: int):
        uuid = str(uuid4())
        return f'{uuid}__{player_id}'
