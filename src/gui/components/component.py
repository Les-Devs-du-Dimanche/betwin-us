from pygame import Rect
from pygame.display import get_surface as get_screen


class Component:
    
    def __init__(self, rect: tuple[int, int, int, int]):
        self.rect = Rect(rect)
        
        self.display_surface = get_screen()
        
    def update(self):
        pass
    
    def draw(self):
        pass
