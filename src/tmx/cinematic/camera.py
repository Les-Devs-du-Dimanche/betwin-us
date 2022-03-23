from dis import dis
from locale import normalize
from turtle import distance
from pygame import Vector2, Rect
from pygame.sprite import Sprite

from ...consts import TILE_SIZE
from ...group import Groups


class Camera(Sprite):
    
    ERROR_RADIUS = 4
    SPEED = TILE_SIZE
    
    def __init__(self):
        super().__init__(Groups.to_update)
        
        self.pos = Vector2()
        self.rect = Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.target = None

    def go_to(self, pos: Vector2, time: float):
        if time == 0:
            self.rect.center = pos
            self.pos = pos
        else:
            self.target = pos + Vector2(TILE_SIZE, TILE_SIZE) * 0.5
        
    def update(self, dt: int):
        if self.target:
            vec = self.target - Vector2(self.rect.center)
            direction = vec.normalize()
            distance = vec.length()
            # to_walk = min(distance, self.SPEED)
            
            
            self.pos += direction * self.SPEED * dt
            self.rect.center = self.pos
            
            if vec.length() <= self.ERROR_RADIUS:
                self.target = None
