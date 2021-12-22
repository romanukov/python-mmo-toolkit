from abc import ABC, abstractmethod

from backend.common.logic.auth import IAuth
from backend.common.logic.service import IService
from backend.common.network.rpc.decorators import method
from backend.common.network.session.context import context
from backend.ioc import depends
from backend.logic.events import emit_event
from backend.logic.models import (
    LocationDataModel, PlayerDataModel, IdModel, AuthorizationModel,
    CoordinatesModel,
)
from backend.logic.repos import LocationsRepo, PlayersRepo
from backend.logic.serializers import serialize_location, serialize_player


class ILogicService(IService, ABC):
    @abstractmethod
    def authorize(self, auth_data: AuthorizationModel) -> dict: ...

    @abstractmethod
    def mark_player_as_online(self, player_id: int = None) -> None: ...

    @abstractmethod
    def mark_player_as_offline(self, player_id: int = None) -> None: ...

    @abstractmethod
    def notify_location_about_player_data_changed(self): ...

    @abstractmethod
    def notify_location_about_player_entered(self): ...

    @abstractmethod
    def notify_location_about_player_leave(self): ...

    @abstractmethod
    def create_player(self, player_data: PlayerDataModel) -> dict: ...

    @abstractmethod
    def get_player_data(self) -> dict: ...

    @abstractmethod
    def get_player_by_id(self, player_id: IdModel) -> dict: ...

    @abstractmethod
    def get_player_location(self) -> dict: ...

    @abstractmethod
    def get_locations_around(self) -> list[list[dict]]: ...

    @abstractmethod
    def move_to_location(self, coordinates: CoordinatesModel) -> dict: ...

    @abstractmethod
    def get_players_on_location(self) -> list[dict]: ...

    @abstractmethod
    def create_location(self, location_data: LocationDataModel) -> dict: ...

    @abstractmethod
    def get_location_by_id(self, location_id: IdModel) -> dict: ...


class LogicService(ILogicService):
    locations_repo: LocationsRepo = LocationsRepo()
    players_repo: PlayersRepo = PlayersRepo()
    _auth: IAuth = depends(IAuth)

    @method
    def authorize(self, auth_data: AuthorizationModel) -> dict:
        token = self._auth.authorize(auth_data.login, auth_data.password)
        return dict(token=token)

    def mark_player_as_online(self, player_id: int = None) -> None:
        if not player_id:
            player_id = context.session.player_id
        self.players_repo.set_online(player_id, True)
        self.notify_location_about_player_data_changed()

    def mark_player_as_offline(self, player_id: int = None) -> None:
        if not player_id:
            player_id = context.session.player_id
        self.players_repo.set_online(player_id, False)
        self.notify_location_about_player_data_changed()

    def notify_location_about_player_data_changed(self):
        player = self.players_repo.get_by_id(context.session.player_id)
        for location_player in player.location.players:
            if player.id != location_player.id:
                emit_event(
                    location_player.id,
                    'player_data_changed',
                    serialize_player(player),
                )

    def notify_location_about_player_entered(self):
        player = self.players_repo.get_by_id(context.session.player_id)
        for location_player in player.location.players:
            if player.id != location_player.id:
                emit_event(
                    location_player.id,
                    'player_entered_on_location',
                    serialize_player(player),
                )

    def notify_location_about_player_leave(self):
        player = self.players_repo.get_by_id(context.session.player_id)
        for location_player in player.location.players:
            if player.id != location_player.id:
                emit_event(
                    location_player.id,
                    'player_leave_on_location',
                    serialize_player(player),
                )

    # Player

    @method
    def create_player(self, player_data: PlayerDataModel) -> dict:
        player = self.players_repo.create(**player_data.dict())
        return serialize_player(player)

    @method
    def get_player_data(self) -> dict:
        player = self.players_repo.get_by_id(context.session.player_id)
        return serialize_player(player)

    @method
    def get_player_by_id(self, player_id: IdModel) -> dict:
        player = self.players_repo.get_by_id(player_id.id)
        return serialize_player(player)

    @method
    def get_player_location(self) -> dict:
        player = self.players_repo.get_by_id(context.session.player_id)
        location = self.locations_repo.get_by_coordinates(player.location_x, player.location_y)
        return serialize_location(location)

    @method
    def get_locations_around(self) -> list[list[dict]]:
        player = self.players_repo.get_by_id(context.session.player_id)
        locations = self.locations_repo.get_locations_in_radius(player.location_x, player.location_y, 2)
        return [
            [(serialize_location(location) if location else None) for location in row] for row in locations
        ]

    @method
    def move_to_location(self, coordinates: CoordinatesModel) -> dict:
        self.notify_location_about_player_leave()
        player = self.players_repo.set_location(context.session.player_id, coordinates.x, coordinates.y)
        self.notify_location_about_player_entered()
        return serialize_player(player)

    @method
    def get_players_on_location(self) -> list[dict]:
        player = self.players_repo.get_by_id(context.session.player_id)
        return [
            serialize_player(location_player) for location_player in player.location.players
        ]
    
    # Location
    
    @method
    def create_location(self, location_data: LocationDataModel) -> dict:
        location = self.locations_repo.create(**location_data.dict())
        return serialize_location(location)

    @method
    def get_location_by_id(self, location_id: IdModel) -> dict:
        location = self.locations_repo.get_by_id(location_id.id)
        return serialize_location(location)
