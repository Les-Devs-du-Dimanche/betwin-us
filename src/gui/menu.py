from typing import Callable
import webbrowser

from pygame import Surface
from pygame.locals import SRCALPHA
from pygame.display import get_surface as get_screen

from ..consts import DISPLAY_SIZE
from ..time import Time

from .base_menu import BaseMenu
from .components import Button

from .settings_menu import SettingsMenu


class Menu(BaseMenu):
    
    LINK = 'https://github.com/Les-Devs-du-Dimanche/betwin-us'
    
    BACKGROUND_ALPHA = 128
    
    def __init__(self, quit_game: Callable):
        super().__init__()
        
        self.display_surface = get_screen()
        self.background = Surface(DISPLAY_SIZE, SRCALPHA)
        self.background.fill((0, 0, 0, self.BACKGROUND_ALPHA))
        
        self.submenues = [
            (sm := SettingsMenu()),
        ]
        
        self.components = [
            Button((440, 185, 400, 50), 'menu.quit', quit_game),
            Button((440, 285, 400, 50), 'menu.settings', sm.escape),
            Button((440, 385, 400, 50), 'menu.our_site', self.open_link),
            Button((440, 485, 400, 50), 'menu.resume', self.escape),
        ]

    def open_link(self):
        webbrowser.open(self.LINK)
    
    def escape(self):
        super().escape()
        if not self.opened:
            Time.resume()
    
    def draw(self):
        self.display_surface.blit(
            self.background,
            (0, 0)
        )
        super().draw()
