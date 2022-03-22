from os import sep
from os.path import join
from pathlib import Path

from .group import Groups
from .consts import Facing

# hinting
if 0: from .entity.player import Player


BASE_DIR = Path(__file__).resolve().parent.parent

def path(relative_path: str) -> str:
    return str(BASE_DIR) + sep + join(*relative_path.split('/'))

def get_player() -> 'Player':
    for sprite in Groups.entities.sprites():
        # isinstance(sprite, Player)
        if type(sprite).__name__ == 'Player':
            return sprite

reverce_facing = {
    Facing.NORTH: Facing.SOUTH,
    Facing.SOUTH: Facing.NORTH,
    Facing.EAST: Facing.WEST,
    Facing.WEST: Facing.EAST,
}
