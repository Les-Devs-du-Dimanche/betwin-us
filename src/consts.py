from enum import Enum

from pygame import Vector2


DISPLAY_SIZE = 1280, 720
FPS = 60
DT_SPEED = 0.001

TILE_SIZE = 64
CENTER_RECT = Vector2(TILE_SIZE, TILE_SIZE) / 2

class Facing(Enum):
    NORTH = 0
    EAST  = 1
    SOUTH = 2
    WEST  = 3

class DoorState(Enum):
    FORBIDDEN = 0
    ALLOWED = 1
    FORCED = 2
