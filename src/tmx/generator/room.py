from numpy import zeros

from ...consts import Facing, DoorState
from ...hinting import DoorStateDict


class Room:
    
    LEVEL_DIM = 8, 8
    grid = zeros(LEVEL_DIM)
    rooms = []
    
    def __init__(self, pos: tuple[int, int], door_state: DoorStateDict):
        self.pos = pos
        self.rooms.append(self)
        
    @classmethod
    def get_adjacent_rooms(cls, pos: tuple[int, int]):
        
        north = DoorState.FORBIDDEN
        if 0 <= pos[1] - 1 < len(cls.grid):
            if cls.grid[pos[1] - 1][pos[0]] == 0:
                north = DoorState.ALLOWED
                
        south = DoorState.FORBIDDEN
        if 0 <= pos[1] + 1 < len(cls.grid):
            if cls.grid[pos[1] + 1][pos[0]] == 0:
                north = DoorState.ALLOWED
                
        east = DoorState.FORBIDDEN
        if 0 <= pos[0] + 1 < len(cls.grid):
            if cls.grid[pos[1]][pos[0] + 1] == 0:
                north = DoorState.ALLOWED
                
        west = DoorState.FORBIDDEN
        if 0 <= pos[0] - 1 < len(cls.grid):
            if cls.grid[pos[1]][pos[0] - 1] == 0:
                north = DoorState.ALLOWED
    
        return {
            Facing.NORTH: north,
            Facing.SOUTH: south,
            Facing.EAST: east,
            Facing.WEST: west,
        }
    