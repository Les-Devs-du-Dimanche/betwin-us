from random import randint, choice

from numpy import zeros

from .room import Room
from ...consts import DoorState, Facing, TILE_SIZE
from ...hinting import LevelData, ObjectGroup, TileLayer


class Generator:
    
    ROOM_GRID_SIZE = 8
    ROOM_SIZE = 10
    
    @classmethod
    def generate(cls) -> LevelData:
        cls.room_grid = zeros((cls.ROOM_GRID_SIZE, cls.ROOM_GRID_SIZE)).tolist()
        cls.dead_ends = []
        
        Room.rooms = []
        cls.gen_entry_room()
        cls.gen_room(cls.entry_room)
        cls.gen_exit_room()
        
        dict_level = cls.get_json()
        
        # set worldspawn
        for layer in dict_level['layers']:
            if layer['name'] == 'data':
                layer['objects'].append({
                    "height": 0,
                    # "id": 1,
                    "name": "Worldspawn",
                    "point": True,
                    # "rotation": 0,
                    "type": "worldspawn",
                    # "visible": True,
                    "width": 0,
                    "x": (cls.entry_room.pos[0] + 0.5) * cls.ROOM_SIZE * TILE_SIZE,
                    "y": (cls.entry_room.pos[1] + 0.5) * cls.ROOM_SIZE * TILE_SIZE
                })
                
        return dict_level
        
    @classmethod
    def gen_entry_room(cls):
        
        pos = (
            randint(0, cls.ROOM_GRID_SIZE - 1),
            randint(0, cls.ROOM_GRID_SIZE - 1)
        )
        
        doorstate = {
            Facing.NORTH: DoorState.ALLOWED,
            Facing.EAST: DoorState.ALLOWED,
            Facing.SOUTH: DoorState.ALLOWED,
            Facing.WEST: DoorState.ALLOWED,
        }
        
        if pos[0] == 0:
            doorstate[Facing.WEST] = DoorState.FORBIDDEN
        elif pos[0] == cls.ROOM_GRID_SIZE - 1:
            doorstate[Facing.EAST] = DoorState.FORBIDDEN
        if pos[1] == 0:
            doorstate[Facing.NORTH] = DoorState.FORBIDDEN
        elif pos[1] == cls.ROOM_GRID_SIZE - 1:
            doorstate[Facing.SOUTH] = DoorState.FORBIDDEN
        
        cls.entry_room = Room(pos, doorstate)
        cls.room_grid[pos[1]][pos[0]] = cls.entry_room
    
    @classmethod
    def gen_exit_room(cls):
        if cls.dead_ends:
            cls.exit_room = choice(cls.dead_ends)
        else:
            rooms = Room.rooms
            rooms.remove(cls.entry_room)
            cls.exit_room = choice(rooms)
    
    @classmethod
    def gen_room(cls, room: Room):
        for door in room.doors:
            
            if cls.room_grid[door.destination[1]][door.destination[0]] == 0:
            
                facing_posibilities = Room.get_adjacent_rooms(door.destination, cls.room_grid)
                
                _room = Room(door.destination, facing_posibilities)
                if len(_room.doors) == 1:
                    cls.dead_ends.append(_room)
                
                cls.room_grid[door.destination[1]][door.destination[0]] = _room
                
                cls.gen_room(_room)
    
    @classmethod   
    def get_json(cls) -> LevelData:
        
        json = {
            'tilesets':[
                {
                    'firstgid':1,
                    'source':'..\/tilesets\/floor.tsx',
                }, 
                {
                    'firstgid':280,
                    'source':'..\/tilesets\/relief.tsx',
                },
            ],
            "height": 80,
            "width": 80
        }
        
        layers = [
            {
                'data': zeros((cls.ROOM_GRID_SIZE * cls.ROOM_SIZE, cls.ROOM_GRID_SIZE * cls.ROOM_SIZE)).tolist(),
                'height': 80,
                'name': 'floor',
                'type': 'tilelayer',
                'width': 80,
                'x': 0,
                'y': 0,
            }, 
            {
                'data': zeros((cls.ROOM_GRID_SIZE * cls.ROOM_SIZE, cls.ROOM_GRID_SIZE * cls.ROOM_SIZE)).tolist(),
                'height': 80,
                'name': 'relief',
                'type': 'tilelayer',
                'width': 80,
                'x': 0,
                'y': 0,
            },
            {
                # 'id': 3,
                'name': 'entities',
                'objects': [],
                'type': 'objectgroup',
                'x': 0,
                'y': 0,
            }, 
            {
                # 'id': 4,
                'name': 'data',
                'objects': [],
                'type': 'objectgroup',
                'x': 0,
                'y': 0,
            },
        ]
        
        for room in Room.rooms:
            _layers = {}
            
            for layer in room.layers:
                _layers[layer['name']] = layer
                
            for i, layer in enumerate(layers):
                if layer['name'] in _layers:
                    layers[i] = cls.past_layer(layer, _layers[layer['name']], room.pos)
        
        for layer in layers:
            if layer['type'] == 'tilelayer':
                data = []
                for row in layer['data']:
                    data += row
                layer['data'] = data
        
        json['layers'] = layers
        return json
        
    @classmethod
    def past_layer(cls, _on: TileLayer | ObjectGroup, _past: TileLayer | ObjectGroup, pos: tuple[int, int]) -> list[list[int]]:
        if _on['type'] == 'tilelayer':
            for y, row in enumerate(_past['data']):
                for x, tile_id in enumerate(row):
                    _y = y + pos[1] * cls.ROOM_SIZE
                    _x = x + pos[0] * cls.ROOM_SIZE
                    _on['data'][_y][_x] = tile_id
                    
        else:
            for obj in _past['objects']:
                if 'door' not in obj['name']:
                    _on['objects'].append(obj)
        return _on
