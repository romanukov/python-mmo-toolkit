from backend.logic.entities import Location, Player, PlayerStats


def serialize_location(location: Location) -> dict:
    return dict(
        x=location.x,
        y=location.y,
        name=location.name,
        ground_type=location.ground_type.value,
    )


def serialize_player(player: Player) -> dict:
    return dict(
        id=player.id,
        name=player.name,
        gender=player.gender.value,
        online=player.online,
        stats=serialize_stats(player.stats),
    )


def serialize_stats(stats: PlayerStats) -> dict:
    return dict(
        level=stats.level,
        hp=stats.hp,
        mp=stats.mp,
        strength=stats.strength,
        dexterity=stats.dexterity,
        stamina=stats.stamina,
    )
