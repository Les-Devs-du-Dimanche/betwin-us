from ...consts import Facing

class Door:
    
    def __init__(self, name : str):
        self.name = name 
        if "north" in self.name :
            self.orientation = Facing.NORTH
        elif "east" in self.name :
            self.orientation = Facing.EAST
        elif "south" in self.name :
            self.orientation = Facing.SOUTH
        elif "west" in self.name :
            self.orientation = Facing.WEST
