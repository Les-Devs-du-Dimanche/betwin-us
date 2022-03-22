from pygame import Surface, Rect
from pygame.sprite import Sprite, Group

from ...group import Groups


class Tile(Sprite):
        
    def __init__(self, groups: list[Group], surface: Surface, rect: tuple[int, int, int, int] = None):
        super().__init__(*groups)
        
        self.image = surface
        
        if rect:
            self.rect = Rect(rect)
        else:
            self.rect = surface.get_rect()
