from __future__ import annotations

from enum import Enum
from typing import Literal

from pygame import Rect, Vector2
from pygame.sprite import Sprite

from ..consts import TILE_SIZE, Facing, CENTER_RECT
from ..display.assets import Assets
from ..group import Groups


class Entity(Sprite):
    
    animation_name: str
    
    HITBOX: tuple[int, int]
    
    DESTINATION_RADIUS = TILE_SIZE * 0.8
    
    class Speed:
        WALK = TILE_SIZE * 2.5 # 2.5 tiles/s
        
    class Status(Enum):
        IDLE = 0
        WALKING = 1
        ATTACKING = 2
    
    def __init__(self, pos: Vector2):
        super().__init__(Groups.entities, Groups.visible, Groups.to_update)
        
        self.animation = Assets.get(self.animation_name)
        self.animation.set_target(self)
        
        self.pos = Vector2(pos) + CENTER_RECT
        self.rect = Rect(*self.pos, TILE_SIZE, TILE_SIZE)
        self.hitbox = self.rect.inflate(self.HITBOX)
        
        self.direction = Vector2()
        self.speed = self.Speed.WALK
        self.status = self.Status.IDLE
        self.facing = Facing.SOUTH
        
        self.destination_target = None
        
    def update(self, dt: int):
        self._input()
        self._update_destination()
        self._move(dt)
        self._animate(dt)
        
    def _input(self):
        pass
    
    def _go_towards(self, target: 'Entity' | Vector2 | tuple[int, int]):
        if isinstance(target, Entity):
            self.destination_target = Vector2(target.rect.center)
        else:
            self.destination_target = Vector2(target)
                
        self.direction = self.destination_target - Vector2(self.rect.center)
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()
    
    def _update_destination(self):
        if self.destination_target:
            distance = (Vector2(self.rect.center) - self.destination_target).length()
            # print()
            if distance <= self.DESTINATION_RADIUS:
                self.destination_target = None
            else:
                self._go_towards(self.destination_target)
    
    def _move(self, dt: int):
        self.pos.x += self.direction.x * dt * self.speed
        self.hitbox.x = self.pos.x
        self._collision('h')
        
        self.pos.y += self.direction.y * dt * self.speed
        self.hitbox.y = self.pos.y
        self._collision('v')
        
        self.rect.center = self.hitbox.center    
    
    def _collision(self, orientation: Literal['v', 'h']):
        for sprite in Groups.obstacles:
            if self.hitbox.colliderect(sprite.rect):
                
                if orientation == 'h':
                    if self.direction.x > 0:
                        self.pos.x -= self.hitbox.right - sprite.rect.left
                        self.hitbox.right = sprite.rect.left
                    else:
                        self.pos.x += sprite.rect.right - self.hitbox.left
                        self.hitbox.left = sprite.rect.right
                    
                elif orientation == 'v':
                    if self.direction.y > 0:
                        self.pos.y -= self.hitbox.bottom - sprite.rect.top
                        self.hitbox.bottom = sprite.rect.top
                    else:
                        self.pos.y += sprite.rect.bottom - self.hitbox.top
                        self.hitbox.top = sprite.rect.bottom

    def _animate(self, dt: int):
        self.animation.update(dt)
        self.image = self.animation.get_surface()
