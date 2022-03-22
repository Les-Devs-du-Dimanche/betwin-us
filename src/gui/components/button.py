from typing import Callable

from pygame.draw import rect as draw_rect
from pygame.mouse import get_pos as get_mouse_pos

from ...display.assets import Assets
from ...translate import Translate
from ...sound import Sound

from .component import Component


class Button(Component):
    
    click_event = False
    
    # display settings
    BACKGROUND_COLOR = '#7A7A7A'
    HOVER_COLOR = '#949494'
    BORDER_COLOR = '#404040'
    BORDER_WIDTH = 5
    TEXT_COLOR = '#FFFFFF'
    TEXT_SIZE = 24
    
    def __init__(self, rect: tuple[int, int, int, int], text: str, on_click: Callable, **kwargs):
        super().__init__(rect)
        
        self.text = text
        
        self.on_click = on_click
        self.kwargs = kwargs
        
        self.font = Assets.get('font.menu', size=self.TEXT_SIZE)
        
        self.hovered = False
        
    def update(self):
        if self.rect.collidepoint(get_mouse_pos()):
            self.hovered = True
            
            if self.click_event:
                if self.text == 'menu.back':
                    Sound.gui('sounds.back')
                else:
                    Sound.gui('sounds.click')
                self.on_click(**self.kwargs)
            
        else:
            self.hovered = False
    
    def draw(self):
        # background
        if self.hovered \
        or (hasattr(self, 'listening') and self.listening):
            draw_rect(
                self.display_surface,
                self.HOVER_COLOR,
                self.rect
            )
        else:
            draw_rect(
                self.display_surface,
                self.BACKGROUND_COLOR,
                self.rect
            )
        
        # border
        draw_rect(
            self.display_surface,
            self.BORDER_COLOR,
            self.rect,
            self.BORDER_WIDTH
        )
        
        # text
        text_surface = self.font.render(Translate[self.text], True, self.TEXT_COLOR)
        self.display_surface.blit(
            text_surface,
            text_surface.get_rect(center=self.rect.center)
        )
        