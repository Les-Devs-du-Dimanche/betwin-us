from os import set_inheritable
from pygame import Vector2
import pygame
from pygame.key import get_pressed as get_key_pressed
from pygame.mouse import get_pressed as get_mouse_pressed
from random import randint as random_integer


from ..keybinds import Keybinds
from .entity import Entity
from ..consts import Facing
from ..item.sword import Sword


class Player(Entity):
    
    animation_name = 'entity.player'
    health = 100
    

    HITBOX = -20, -48
        
    def __init__(self, pos: Vector2):
        super().__init__(pos)
        
        self.click_event = None
        self.melee_weapon = Sword(self)
        self.evil = False
        switch = pygame.event.custom_type()
        # self.ranged_weapon = None

        self.appening = random_integer(60,60*3)
        pygame.time.set_timer(self.switch, self.appening * 1000)
        
    def _input(self):
        # movements
        keys = get_key_pressed()
        
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
        
        # attack        
        if self.click_event:
            if self.click_event.button == 1: # left click
                self.melee_weapon.show()
                self.status = self.Status.ATTACKING
                self.direction = Vector2()
                
            elif self.click_event.button == 3: # right click
                # self.ranged_weapon.show()
                # self.status = self.Status.ATTACKING
                # self.direction = Vector2()
                pass
    
    def update(self, dt: int):
        super().update(dt)
        
        if not self.melee_weapon.shown:# and not self.melee_weapon.visible:
            self.status = self.Status.IDLE
    
    def switch_mode(self) :
        self.switch = pygame.event.custom_type()
        if not self.evil  :            
            self.evil = True
            self.appening = random_integer(60,60*3)
            pygame.time.set_timer(self.switch, self.appening * 1000)
        else :
            self.evil = False 
            self.appening = 3000
            pygame.time.set_timer(self.switch, self.appening)