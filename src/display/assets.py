import json

from pygame.font import Font
from pygame.image import load as load_image
from pygame.mixer import Sound

from ..functions import path
from .animation import Animation
from .tileset import Tileset


class Assets:
    
    FILE_PATH = path('assets/load.json')
    
    @classmethod
    def load(cls):
        with open(cls.FILE_PATH, 'r') as file:
            data = json.loads(file.read())
        
        cls.__assets = {}
        cls.__fonts = {}
        cls.__tilesets = {}
        
        for key, value in data.items():
            extension = value.split('.')[-1]
            
            if extension == 'json': # load animation
                
                with open(path('assets/' + value), 'r') as file:
                    animation_data = json.loads(file.read())
                
                image_path = path(f'assets/{value[:-4]}png')
                surface = load_image(image_path).convert_alpha()
                
                cls.__assets[key] = Animation(animation_data, surface)
                
            elif extension == 'ttf':
                cls.__assets[key] = path('assets/' + value)
                
            elif extension == 'ogg':
                cls.__assets[key] = Sound(path('assets/' + value))
                
    @classmethod
    def get(cls, key: str, size: int = None, id: str = None) -> Animation | Font | Sound | Tileset:
        # tileset
        if isinstance(key, list):
            if id in cls.__tilesets:
                return cls.__tilesets[id]
            else:
                tileset = Tileset(key)
                cls.__tilesets[id] = tileset
                return tileset
            
        asset = cls.__assets.get(key)
        
        # animation
        if isinstance(asset, Animation):
            return asset.copy()
        
        # sound
        elif isinstance(asset, str):
            if key in cls.__fonts:
                return cls.__fonts[(key, size)]
            else:
                font = Font(asset, size)
                cls.__fonts[(key, size)] = font
                return font
        # image
        else:
            return asset
