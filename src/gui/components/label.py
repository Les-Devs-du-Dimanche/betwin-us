from pygame import Vector2

from .component import Component

from ...display.assets import Assets
from ...translate import Translate


class Label(Component):
    
    TEXT_SIZE = 16
    TEXT_COLOR = '#FFFFFF'
    
    offset = Vector2(0, -2)
    
    def __init__(self, component: Component, text: str):
        super().__init__((0, 0, 0, 0))
        self.text = text
        self.component = component
        
        self.font = Assets.get('font.menu', self.TEXT_SIZE)
    
    def draw(self):
        
        text_surface = self.font.render(Translate[self.text], True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(midbottom=Vector2(self.component.rect.midtop) + self.offset)
        
        self.display_surface.blit(
            text_surface,
            text_rect
        )
