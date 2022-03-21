from enum import Enum
from typing import Literal

from pygame import Rect, Vector2
from pygame.sprite import Sprite

from ..consts import DT_SPEED, TILE_SIZE, Facing
from ..display.assets import Assets
from ..group import Groups


class Entity(Sprite):
    
    animation_name: str
    
    HITBOX: tuple[int, int]
    
    class Speed:
        WALK = 3
        RUN = 5
        
    class Status(Enum):
        IDLE = 0
        WALKING = 1
        ATTACKING = 2
    
    def __init__(self, pos: Vector2):
        super().__init__(Groups.entities, Groups.visible, Groups.to_update)
        
        self.animation = Assets.get(self.animation_name)
        self.animation.set_target(self)
        
        self.rect = Rect(*pos, TILE_SIZE, TILE_SIZE)
        self.hitbox = self.rect.inflate(self.HITBOX)
        
        self.direction = Vector2()
        self.speed = self.Speed.WALK
        self.status = self.Status.IDLE
        self.facing = Facing.SOUTH
        
    def update(self, dt: int):
        self._input()
        self._move(dt)
        self._animate(dt)
        
    def _input(self):
        pass
    
    def _move(self, dt: int):
        self.hitbox.x += self.direction.x * dt * DT_SPEED * self.speed
        self._collision('h')
        self.hitbox.y += self.direction.y * dt * DT_SPEED * self.speed
        self._collision('v')
        
        self.rect.center = self.hitbox.center    
    
    def _collision(self, orientation: Literal['v', 'h']):
        for sprite in Groups.obstacles:
            if self.hitbox.colliderect(sprite.rect):
                
                if orientation == 'h':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    else:
                        self.hitbox.left = sprite.rect.right
                    
                elif orientation == 'v':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    else:
                        self.hitbox.top = sprite.rect.bottom
    
    def _animate(self, dt: int):
        self.animation.update(dt)
        self.image = self.animation.get_surface()

