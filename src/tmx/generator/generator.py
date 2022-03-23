from numpy import zeros

from room import Room
from ...consts import DoorState, Facing
from ...functions import reverce_facing


class Generator :
    
    def __init__(self) -> None: 
        self.rg_dim = 8
        self.room_dim = int
        self.room_grid = zeros((self.rg_dim, self.rg_dim))
        self.impass = []
        
    def gen_entry_room(self) :
        pass 
    
    def gen_room(self, room : Room, room_to_generate : int):
        if room_to_generate == 0 : return
        
        for door in room.doors() :
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
                    self.impass.append(_room)
                self.room_grid[door.destination[0]][door.destination[1]] = _room
                self.gen_room(_room, room_to_generate)
                
        def transform_room_grid_to_json(self) :
            data = zeros((self.rg_dim * self.room_dim, self.rg_dim * self.room_dim))
            
            for room in Room.rooms :
                for y, row in enumerate(room.data):
                    for x, tile_id in enumerate(row):
                        data[y + room.pos[1]][x+room.x] = tile_id
                    
                for y, row in enumerate(room.data) :
                    for x, tile_id in enumerate(row):
                        data[y + room.pos[1][x+room.x]] = tile_id