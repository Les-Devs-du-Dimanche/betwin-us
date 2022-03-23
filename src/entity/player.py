from pygame import Vector2
from pygame.key import get_pressed

from ..keybinds import Keybinds
from .entity import Entity
from ..consts import Facing


class Player(Entity):
    
    animation_name = 'entity.player'
    
    HITBOX = -20, -48
    
    def __init__(self, pos: Vector2):
        super().__init__(pos)
        
        self.movements_locked = False
        
    def _input(self):
        if not self.movements_locked:
            keys = get_pressed()
            
            self.status = self.Status.IDLE
            
            if keys[Keybinds['player.move.north']]:
                self.direction.y = -1
                self.facing = Facing.NORTH
                self.status = self.Status.WALKING
            elif keys[Keybinds['player.move.south']]:
                self.direction.y = 1
                self.facing = Facing.SOUTH
                self.status = self.Status.WALKING
            else:
                self.direction.y = 0
                
            if keys[Keybinds['player.move.west']]:
                self.direction.x = -1
                self.facing = Facing.WEST
                self.status = self.Status.WALKING
            elif keys[Keybinds['player.move.east']]:
                self.direction.x = 1
                self.facing = Facing.EAST
                self.status = self.Status.WALKING
            else:
                self.direction.x = 0
                
            # set vector lenght to 1 -> prevent speed augmentation during diagonal moves
            if self.direction.length() != 0:
                self.direction = self.direction.normalize()
    