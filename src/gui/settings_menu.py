from .base_menu import BaseMenu
from .components import Button

from .keybinds_menu import KeybindsMenu
from .langs_menu import LangsMenu
from .audio_menu import AudioMenu

class SettingsMenu(BaseMenu):
    
    def __init__(self):
        super().__init__()
        
        self.submenues = [
            (km := KeybindsMenu()),
            (lm := LangsMenu()),
            (am := AudioMenu()),
        ]
        
        self.components = [
            Button((440, 185, 400, 50), 'menu.keybinds', km.escape),
            Button((440, 285, 400, 50), 'menu.langs', lm.escape),
            Button((440, 385, 400, 50), 'menu.audio', am.escape),
            Button((440, 485, 400, 50), 'menu.back', self.escape),
        ]
