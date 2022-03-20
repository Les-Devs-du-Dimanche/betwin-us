import json
import os

from .utils.functions import path


class Keybinds:
    
    FILE_PATH = path('config/keybinds.json')
    DEFAULT = {
        'player.move.north': 122,
        'player.move.east' : 100,
        'player.move.south': 115,
        'player.move.west' : 113,
    }
    
    @classmethod
    def load(cls):
        if os.path.exists(cls.FILE_PATH):
            with open(cls.FILE_PATH, 'r') as file:
                cls.__keys = json.loads(file.read())
        else:
            cls.__keys = cls.DEFAULT
    
    def __class_getitem__(cls, key: str) -> int:
        return cls.__keys[key]
    
    @classmethod
    def set(cls, key: str, value: int):
        cls.__keys[key] = value
        
        with open(cls.FILE_PATH, 'w') as file:
            file.write(json.dumps(cls.__keys, indent=4))
 