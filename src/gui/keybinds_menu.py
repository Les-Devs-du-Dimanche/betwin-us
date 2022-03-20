from .base_menu import BaseMenu
from .components import Button, KeyButton, Label


class KeybindsMenu(BaseMenu):
    
    def __init__(self):
        super().__init__()
        
        col1 = 100
        col2 = 286
        col3 = 472
        col4 = 658
        col5 = 844
        col6 = 1030
        
        row1 = 100
        row2 = 200
        row3 = 300
        row4 = 400
        
        self.components = [
            k := KeyButton((col1, row1, 150, 50), 'player.move.north'), Label(k, 'keybind.player.move.north'),
            k := KeyButton((col1, row2, 150, 50), 'player.move.south'), Label(k, 'keybind.player.move.south'),
            k := KeyButton((col1, row3, 150, 50), 'player.move.east'),  Label(k, 'keybind.player.move.east'),
            k := KeyButton((col1, row4, 150, 50), 'player.move.west'),  Label(k, 'keybind.player.move.west'),
            
            Button((440, 500, 400, 50), 'menu.back', self.escape),
        ]
