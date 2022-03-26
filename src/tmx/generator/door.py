from ...consts import Facing


class Door:
    
    def __init__(self, facing: Facing, pos: tuple[int, int]):
        if facing == Facing.NORTH:
            self.destination = [pos[0], pos[1] - 1]
        elif facing == Facing.EAST:
            self.destination = [pos[0] + 1, pos[1]]
        elif facing == Facing.SOUTH:
            self.destination = [pos[0], pos[1] + 1]
        elif facing == Facing.WEST:
            self.destination = [pos[0] - 1, pos[1]]
