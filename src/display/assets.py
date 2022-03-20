import json

from pygame.image import load as load_image

from ..utils.functions import path
from .animation import Animation


class Assets:
    
    FILE_PATH = path('assets/load.json')
    
    @classmethod
    def load(cls):
        with open(cls.FILE_PATH, 'r') as file:
            data = json.loads(file.read())
        
        cls.textures = {}
        
        for key, value in data.items():
            extension = value.split('.')[-1]
            
            if extension == 'json': # load animation
                
                with open(path('assets/' + value), 'r') as file:
                    animation_data = json.loads(file.read())
                
                image_path = path(f'assets/{value[:-4]}png')
                surface = load_image(image_path).convert_alpha()
                
                cls.textures[key] = Animation(animation_data, surface)
                
    @classmethod
    def get(cls, key: str) -> Animation:
        asset = cls.textures.get(key)
        if asset:
            if isinstance(asset, Animation):
                return asset.copy()
