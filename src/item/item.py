from pygame.sprite import Sprite

from ..display.assets import Assets
from ..group import Groups
from ..consts import Facing
from ..time import Time

# hinting
if 0: from ..entity.entity import Entity


class Item(Sprite):
    
    texture: str
    damages: int
    
    visible_time: int
    cooldown: int
    
    def __init__(self, owner: 'Entity'):
        super().__init__()
        
        self.owner = owner
        
        self.animation = Assets.get(self.texture)
        self.animation.set_target(self)
        
        self.shown = False
        
    def update(self, dt: int):
        self.facing = self.owner.facing
        
        self.animation.update(dt)
        self.image = self.animation.get_surface()
        
        if self.facing == Facing.NORTH:
            pos = {'midbottom': self.owner.rect.midtop}
        elif self.facing == Facing.EAST:
            pos = {'midleft': self.owner.rect.midright}
        elif self.facing == Facing.SOUTH:
            pos = {'midtop': self.owner.rect.midbottom}
        else:
            pos = {'midright': self.owner.rect.midleft}
        
        self.rect = self.image.get_rect(**pos)
        
        # hide
        if Time.get() >= self.show_time + self.visible_time:
            self.remove(Groups.visible)
            if hasattr(self.owner, 'weapon'):
                self.remove(Groups.entity_weapons)
            else:
                self.remove(Groups.enemies_attacks)
            
            if Time.get() >= self.show_time + self.visible_time + self.cooldown:
                self.kill()
                self.shown = False
    
    def show(self):
        self.add(Groups.visible, Groups.to_update)
        
        if hasattr(self.owner, 'weapon'):
            self.add(Groups.enemies_attacks)
        else:
            self.add(Groups.player_attacks)
        
        self.show_time = Time.get()
        self.shown = True
        self.update(0)
        
