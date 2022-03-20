import json
import os
from typing import Any

from .functions import path


class Settings:
    
    FILE_PATH = path('config/settings.json')
    DEFAULT = {
        'lang': 'en',
        'volume.music' : 0.5,
        'volume.enemies' : 0.5,
        'volume.player' : 0.5,
        'volume.gui' : 0.5,
    }
    
    @classmethod
    def load(cls):
        if os.path.exists(cls.FILE_PATH):
            with open(cls.FILE_PATH, 'r') as file:
                cls.__data = json.loads(file.read())
        else:
            cls.__data = cls.DEFAULT
    
    def __class_getitem__(cls, key: str) -> Any:
        return cls.__data[key]
    
    @classmethod
    def set(cls, key: str, value: Any):
        cls.__data[key] = value
        
        with open(cls.FILE_PATH, 'w') as file:
            file.write(json.dumps(cls.__data, indent=4))
 