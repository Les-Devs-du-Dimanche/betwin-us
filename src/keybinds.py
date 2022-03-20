from typing import Callable
from .functions import path
from .settings import Settings


class Keybinds(Settings):
    
    FILE_PATH = path('config/keybinds.json')
    DEFAULT = {
        'player.move.north': 122, # Z
        'player.move.east' : 100, # D
        'player.move.south': 115, # S
        'player.move.west' : 113, # Q
    }
        
    __class_getitem__: Callable[[str], int]
    set: Callable[[str, int], None]
