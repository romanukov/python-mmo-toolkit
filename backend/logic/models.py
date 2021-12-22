from dataclasses import dataclass

from backend.logic.enums import GroundType, Gender


@dataclass
class IdModel:
    id: int


@dataclass
class CoordinatesModel:
    x: int
    y: int


@dataclass
class LocationDataModel:
    x: int
    y: int
    name: str
    ground_type: GroundType


@dataclass
class LocationModel:
    x: int
    y: int
    name: str
    ground_type: GroundType


@dataclass
class PlayerDataModel:
    name: str
    gender: Gender
    password: str = None


@dataclass
class AuthorizationModel:
    login: str
    password: str = None


@dataclass
class TokenModel:
    token: str


@dataclass
class PlayerModel:
    id: int
    name: str
    gender: Gender
