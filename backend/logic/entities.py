from sqlalchemy import Column, Integer, String, Enum, ForeignKey, ForeignKeyConstraint, Boolean, JSON
from sqlalchemy.orm import relationship

from backend.logic.database import BaseEntity
from backend.logic.enums import GroundType, Gender


class Location(BaseEntity):
    __tablename__ = 'locations'
    
    x = Column(Integer, primary_key=True)
    y = Column(Integer, primary_key=True)
    name = Column(String)
    ground_type = Column(Enum(GroundType))
    players = relationship(
        'Player',
        foreign_keys='[Player.location_x, Player.location_y]',
        backref="location"
    )


class PlayerStats(BaseEntity):
    __tablename__ = 'player_stats'
    
    id = Column(Integer, primary_key=True)
    
    level = Column(Integer, default=1)
    
    hp = Column(Integer, nullable=False)
    mp = Column(Integer, nullable=False)
    
    strength = Column(Integer, nullable=False)
    dexterity = Column(Integer, nullable=False)
    stamina = Column(Integer, nullable=False)


class Inventory(BaseEntity):
    __tablename__ = 'inventories'
    
    id = Column(Integer, primary_key=True)


class Item(BaseEntity):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String)
    inventory_id = Column(ForeignKey(Inventory.id))
    inventory = relationship(Inventory, uselist=True, backref='items')
    data = Column(JSON)


class Player(BaseEntity):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    gender = Column(Enum(Gender))
    location_x = Column(ForeignKey(Location.x))
    location_y = Column(ForeignKey(Location.y))
    online = Column(Boolean, default=False)
    stats_id = Column(ForeignKey('player_stats.id'), unique=True)
    stats = relationship('PlayerStats', uselist=False, backref='player')
    
    __table_args__ = (
        ForeignKeyConstraint(
            (location_x, location_y),
            (Location.x, Location.y)
        ),
        {},
    )
