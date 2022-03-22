from numpy import zeros

from room import Room
from ...consts import Facing


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
            for facing, possibility in adjacent_rooms.items() :
                if f :=      
    