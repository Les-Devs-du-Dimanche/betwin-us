from .base_menu import BaseMenu
from .components import Button

from ..translate import Translate


class LangsMenu(BaseMenu):
    
    def __init__(self):
        super().__init__()
        
        self.components = [
            Button((440, 185, 400, 50), 'lang.en', Translate.load, lang=Translate.Lang.EN),
            Button((440, 285, 400, 50), 'lang.fr', Translate.load, lang=Translate.Lang.FR),
            
            Button((440, 485, 400, 50), 'menu.back', self.escape),
        ]
