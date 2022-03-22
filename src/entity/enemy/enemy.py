from pygame import Vector2

from ...consts import TILE_SIZE
from ...functions import get_player
from ..entity import Entity
from ..pathfinder import PathFinder


class Enemy(Entity):
    
    VIEW_RADIUS = TILE_SIZE * 4
    ATTACK_RADUIS = TILE_SIZE * 1
    
    class Speed:
        WALK = 2
        RUN = 5
        
    def __init__(self, pos: Vector2):
        super().__init__(pos)
        
        self.chase_enabled = False
    
    def _input(self):
        
        player = get_player()
        
        if not self.chase_enabled:
            distance = Vector2(player.rect.center) - Vector2(self.rect.center)
            if distance.length() <= self.VIEW_RADIUS and not PathFinder.obstacle_between(self, player):
                self.status = self.Status.WALKING
                self.chase_enabled = True
        
        else:
            # avoid obstacle
            if PathFinder.obstacle_between(self, player):
                if self.destination_target is None:
                    target = PathFinder.find(self, player)
                    if target:
                        self._go_towards(target)
            
            else: # move straight towards the player
                self.destination_target = None
                self.direction = Vector2(player.rect.center) - Vector2(self.rect.center)
                if self.direction.length() != 0:
                    self.direction = self.direction.normalize()
