from pygame import Rect
from pygame.draw import rect as draw_rect
from pygame.mouse import get_pos as get_mouse_pos
from pygame.mouse import get_pressed as get_mouse_pressed

from .component import Component


class Slider(Component):
    
    click_event = False
    
    # display settings
    BACKGROUND_COLOR = '#7A7A7A'
    TRIGGER_COLOR = '#949494'
    BORDER_COLOR = '#404040'
    BORDER_WIDTH = 5
    CURSOR_COLOR = '#2e2e2e'
    CURSOR_WIDTH = 5
    
    def __init__(self, rect: tuple[int, int, int, int], target, attribute: str, min: float = 0, max: float = 1):
        super().__init__(rect)
        
        self.target = target
        self.attribute = attribute
        self.min = min
        self.max = max
        
        self.triggered = False
        self.cursor: float = getattr(target, attribute)
        self.cursor_rect = Rect(0, self.rect.y + 2 * self.BORDER_WIDTH, self.CURSOR_WIDTH, self.rect.height - 4 * self.BORDER_WIDTH)
        self.set_cursor_x()
        
    def set_cursor_x(self):
        self.cursor_rect.centerx = (self.rect.width - 6 * self.BORDER_WIDTH) * self.cursor / (self.max - self.min) + self.rect.x + 3 * self.BORDER_WIDTH
        
    def update(self):
        if self.rect.collidepoint(get_mouse_pos()):
            if self.click_event:
                self.triggered = True
                
        if get_mouse_pressed()[0]: # left mouse button pressed
            if self.triggered:
                
                x = get_mouse_pos()[0]

                self.cursor = (self.max - self.min) * (x - self.rect.x) / (self.rect.width)
                self.cursor = max(self.min, self.cursor)
                self.cursor = min(self.max, self.cursor)
                
                self.set_cursor_x()
                
                setattr(self.target, self.attribute, self.cursor)
                
        else:
            self.triggered = False
    
    def draw(self):
        if self.triggered:
            draw_rect(
                self.display_surface,
                self.TRIGGER_COLOR,
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
        
        # cursor
        draw_rect(
            self.display_surface,
            self.CURSOR_COLOR,
            self.cursor_rect
        )
