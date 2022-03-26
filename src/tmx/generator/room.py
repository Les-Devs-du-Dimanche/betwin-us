from json import loads as json_loads
from random import randint, sample, choice

from numpy import zeros

from ...consts import Facing, DoorState
from ...hinting import DoorStateDict
from ...functions import path
from .door import Door


class Room:
    
    LEVEL_DIM = 8, 8
    grid = zeros(LEVEL_DIM)
    rooms = []
    
    nb_template = 15
    templates = []
    
    @classmethod
    def load(cls):
        for i in range(cls.nb_template):
            with open(path(f'assets/tmx/rooms/room_{i}.json'), 'r') as file:
                data = json_loads(file.read())
            
            doors = []
            
            for layer in data['layers']:
                if layer['name'] == 'data':
                    for obj in layer['objects']:
                        if obj['name'] == 'north_door':
                            doors.append(Facing.NORTH)
                        elif obj['name'] == 'east_door':
                            doors.append(Facing.EAST)
                        elif obj['name'] == 'south_door':
                            doors.append(Facing.SOUTH)
                        elif obj['name'] == 'west_door':
                            doors.append(Facing.WEST)                    
                    break
            
            cls.templates.append((set(doors), data))
    
    @classmethod
    def get_adjacent_rooms(cls, pos: tuple[int, int], grid: list[list[int]]) -> DoorStateDict:

        north = DoorState.FORBIDDEN
        if 0 <= pos[1] - 1 < len(cls.grid):
            room = grid[pos[1] - 1][pos[0]]
            
            if room == 0:
                north = DoorState.ALLOWED
            else:
                for door in room.doors:
                    if door.facing == Facing.SOUTH:
                        north = DoorState.FORCED
                        break
                
        south = DoorState.FORBIDDEN
        if 0 <= pos[1] + 1 < len(cls.grid):
            room = grid[pos[1] + 1][pos[0]]
            
            if room == 0:
                south = DoorState.ALLOWED
            else:
                for door in room.doors:
                    if door.facing == Facing.NORTH:
                        south = DoorState.FORCED
                        break
                
        east = DoorState.FORBIDDEN
        if 0 <= pos[0] + 1 < len(cls.grid):
            room = grid[pos[1]][pos[0] + 1]
            
            if room == 0:
                east = DoorState.ALLOWED
            else:
                for door in room.doors:
                    if door.facing == Facing.WEST:
                        east = DoorState.FORCED
                        break
                
        west = DoorState.FORBIDDEN
        if 0 <= pos[0] - 1 < len(cls.grid):
            room = grid[pos[1]][pos[0] - 1]
            
            if room == 0:
                west = DoorState.ALLOWED
            else:
                for door in room.doors:
                    if door.facing == Facing.EAST:
                        west = DoorState.FORCED
                        break
                
        return {
            Facing.NORTH: north,
            Facing.SOUTH: south,
            Facing.EAST: east,
            Facing.WEST: west,
        }
    
    def __init__(self, pos: tuple[int, int], door_state: DoorStateDict):
        self.pos = tuple(pos)
        self.rooms.append(self)
           
        allowed_doors = []
        forced_doors = []
        
        for facing, state in door_state.items():
            if state == DoorState.ALLOWED:
                allowed_doors.append(facing)
            elif state == DoorState.FORCED:
                forced_doors.append(facing)
        
        if allowed_doors:
            if len(forced_doors) == 0:
                _min = 1
            else:
                _min = 0
            nb = randint(_min, len(allowed_doors))
            forced_doors += sample(allowed_doors, nb)
            
        self.doors = []
        for facing in forced_doors:
            self.doors.append(Door(facing, pos))
            
        self.facings = set(forced_doors)
            
        possible_templates = []
        for template in self.templates:
            if template[0] == self.facings:
                possible_templates.append(template[1])

        self.template = choice(possible_templates).copy()
        self.layers = []
        for layer in self.template['layers']:
            if layer['type'] == 'tilelayer':
            
                data = []
                
                for i, tile in enumerate(layer['data']):
                    row = i // self.template['width']
                    if len(data) == row:
                        data.append([])
                    
                    data[row].append(tile)
                
                _layer = layer.copy()
                _layer['data'] = data
                
            self.layers.append(_layer)
        
        # if self.facings == {Facing.WEST}:
        #     print(self.pos)

    def __repr__(self):
        return f'R{self.pos}'