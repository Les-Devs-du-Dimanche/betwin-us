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
    
    nb_template = 7
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
    
    def __init__(self, pos: tuple[int, int], door_state: DoorStateDict):
        self.pos = pos
        self.rooms.append(self)
        
        allowed_doors = []
        forced_doors = []
        
        for facing, state in door_state.items():
            if state == DoorState.ALLOWED:
                allowed_doors.append(facing)
            elif state == DoorState.FORCED:
                forced_doors.append(facing)
        
        if allowed_doors:
            nb = randint(0, len(allowed_doors))
            forced_doors += sample(allowed_doors, nb)
        
        self.doors = []
        for facing in forced_doors:
            self.doors.append(Door(facing, pos))
            
        possible_templates = []
        for template in self.templates:
            if template[0] == str(forced_doors):
                possible_templates.append(template)
                
        self.template = choice(possible_templates)[1]
        self.layers = []
        for layer in self.template['layer']:
            if layer['type'] == 'tilelayer':
            
                data = []
                
                for i, tile in enumerate(layer['data']):
                    row = i // self.template['height']
                    if len(data) == row:
                        data.append([])
                    
                    col = i % self.template['width']
                    data[row][col] = tile
                    
                layer['data'] = data
                
            self.layers.append(layer)
        