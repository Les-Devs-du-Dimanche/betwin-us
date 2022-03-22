from enum import Enum


DISPLAY_SIZE = 1280, 720
FPS = 60
DT_SPEED = FPS / 1000

TILE_SIZE = 64

class Facing(Enum):
    NORTH = 0
    EAST  = 1
    SOUTH = 2
    WEST  = 3

class DoorState(Enum):
    FORBIDDEN = 0
    ALLOWED = 1
    FORCED = 2
