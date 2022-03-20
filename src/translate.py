import json

from .functions import path
from .settings import Settings


class Translate:
    
    class Lang:
        FR = 'fr'
        EN = 'en'
    
    @classmethod
    def load(cls, lang: Lang | str):
        Settings.set('lang', lang)
        
        with open(path(f'assets/langs/{lang}.json'), 'r', encoding='utf-8') as file:
            cls.__data = json.loads(file.read())
            
    def __class_getitem__(cls, key: str) -> str:
        return cls.__data.get(key, key)
