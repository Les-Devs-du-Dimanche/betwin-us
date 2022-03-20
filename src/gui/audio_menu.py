from .base_menu import BaseMenu
from .components import Button, Slider, Label

from ..sound import Sound


class AudioMenu(BaseMenu):
    
    def __init__(self):
        super().__init__()
        
        self.components = [
            s := Slider((440, 100, 400, 50), Sound, 'music_volume'),   Label(s, 'volume.music'),
            s := Slider((440, 200, 400, 50), Sound, 'enemies_volume'), Label(s, 'volume.enemies'),
            s := Slider((440, 300, 400, 50), Sound, 'player_volume'),  Label(s, 'volume.player'),
            s := Slider((440, 400, 400, 50), Sound, 'gui_volume'),     Label(s, 'volume.gui'),
            
            Button((440, 500, 400, 50), 'menu.back', self.escape),
        ]
