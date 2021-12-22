from sqlalchemy.exc import NoResultFound

from backend.logic.database import session
from backend.logic.enums import GroundType
from backend.logic.entities import Location, Player
from backend.logic.errors import GameError, ErrorCodes


class LocationsRepo:
    def create(self, x: int, y: int, name: str, ground_type: GroundType) -> Location:
        session.begin()
        location = Location(
            x=x, y=y,
            name=name,
            ground_type=ground_type,
        )
        session.add(location)
        session.flush()
        session.commit()
        return location

    def get_by_coordinates(self, x: int, y: int) -> Location:
        location = session.query(Location).get((x, y))
        return location

    def get_locations_in_radius(self, center_x: int, center_y: int, radius: int = 1) -> list[list[Location]]:
        if radius < 1:
            raise ...
        
        locations = []
        start_x = center_x - radius + 1
        end_x = center_x + radius
        start_y = center_y - radius + 1
        end_y = center_y + radius
        for y in range(start_y, end_y):
            row = []
            for x in range(start_x, end_x):
                location = session.query(Location).get((x, y))
                row.append(location)
            locations.append(row)
        return locations
    
    def update(self, location_id: int, location_data: dict) -> Location:
        session.begin()
        location = session.query(Location).get(location_id)
        for key, value in location_data.items():
            setattr(location, key, value)
        session.add(location)
        session.commit()
        return location


class PlayersRepo:
    def create(self, name: str) -> Player:
        session.begin()
        player = Player(
            name=name,
        )
        session.add(player)
        session.flush()
        session.commit()
        return player

    def get_by_id(self, player_id: int) -> Player:
        session.begin()
        player = session.query(Player).get(player_id)
        session.commit()
        return player

    def get_by_name_and_password(self, name: str, password: str) -> Player:
        session.begin()
        try:
            player = session.query(Player).filter_by(name=name, password=password).one()
            session.commit()
            return player
        except NoResultFound:
            session.rollback()
            raise GameError(ErrorCodes.BAD_CREDENTIALS)

    def set_online(self, player_id: int, online: bool) -> Player:
        session.begin()
        player = session.query(Player).get(player_id)
        player.online = online
        session.commit()
        return player

    def set_location(self, player_id: int, x: int, y: int) -> Player:
        session.begin()
        player = session.query(Player).get(player_id)
        player.location_x = x
        player.location_y = y
        session.commit()
        return player
    
    def update(self, player_id: int, player_data: dict) -> Location:
        session.begin()
        player = session.query(Player).get(player_id)
        for key, value in player_data.items():
            setattr(player, key, value)
        session.add(player)
        session.commit()
        return player
