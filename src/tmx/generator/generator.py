from random import randint, choice

from numpy import zeros

from .room import Room
from ...consts import DoorState, Facing
from ...functions import reverce_facing
from ...hinting import LevelData


class Generator:
    
    ROOM_GRID_SIZE = 8
    ROOM_SIZE = 10
    
    @classmethod
    def generate(cls) -> LevelData:
        cls.room_grid = zeros((cls.ROOM_GRID_SIZE, cls.ROOM_GRID_SIZE))
        cls.dead_ends = []
        
        Room.rooms = []
        cls.gen_entry_room()
        cls.gen_room(cls.entry_room)
        cls.gen_exit_room()
        
        return cls.get_json()
        
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
        cls.exit_room = choice(cls.dead_ends)
    
    @classmethod
    def gen_room(cls, room: Room):
        for door in room.doors:            
            adjacent_rooms = Room.get_adjacent_room(door.destination)
            facing_posibilities = {}
            for facing, posibility in adjacent_rooms.items() :
                if f := reverce_facing[door.facing] == facing :
                    facing_posibilities[f] = DoorState.FORCED
                    continue
                
                if posibility :
                    facing_posibilities[facing] = DoorState.ALLOWED
                else :
                    facing_posibilities[facing] = DoorState.FORBIDDEN
                
                _room = Room(door.destination, facing_posibilities)
                if _room.nb_door == 1 :
                    cls.dead_ends.append(_room)
                cls.room_grid[door.destination[0]][door.destination[1]] = _room
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
        }
        
        layers = [
            {
                'data': zeros((cls.ROOM_GRID_SIZE * cls.ROOM_SIZE, cls.ROOM_GRID_SIZE * cls.ROOM_SIZE)),
                'height':48,
                'name':'floor',
                'type':'tilelayer',
                'width':48,
                'x':0,
                'y':0
            }, 
            {
                'data': zeros((cls.ROOM_GRID_SIZE * cls.ROOM_SIZE, cls.ROOM_GRID_SIZE * cls.ROOM_SIZE)),
                'height':48,
                'name':'relief',
                'properties': [],
                'type':'tilelayer',
                'width':48,
                'x':0,
                'y':0
            },
            {
                'name':'entities',
                'objects': [],
                'type':'objectgroup',
                'x':0,
                'y':0
            }, 
            {
                'id':4,
                'name':'data',
                'objects': [],
                'type':'objectgroup',
                'x':0,
                'y':0
            }
        ]
        for room in Room.rooms:
            for layer in room.layers:
                for i, _layer in enumerate(layers):
                    if layer['name'] == _layer['name']:
                        layer_data = cls.past_room_on_layer(layer, _layer)
                        layers[i]['data'] = layer_data
                        break
                 
        json['layers'] = layers
        
    @classmethod
    def past_room_on_layer(cls, room: Room, layer: list[list[int]]) -> list[list[int]]:
        for room in Room.rooms :
            for y, row in enumerate(room.data):
                for x, tile_id in enumerate(row):
                    layer[y + room.pos[1]][x + room.x] = tile_id
                
            for y, row in enumerate(room.data) :
                for x, tile_id in enumerate(row):
                    layer[y + room.pos[1][x + room.x]] = tile_id
