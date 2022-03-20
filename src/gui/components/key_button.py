from pygame.key import name as get_key_name
from pygame.locals import K_ESCAPE, K_LMETA, K_RMETA

from .button import Button

from ...keybinds import Keybinds


class KeyButton(Button):
    
    FORBIDDEN_KEYS = [
        K_ESCAPE,
        K_LMETA,
        K_RMETA,
    ]
    
    key_event = 0
    
    _keybuttons: list['KeyButton'] = []
    
    def __init__(self, rect: tuple[int, int, int, int], key_code: str):
        self.key_code = key_code
        super().__init__(rect, self.get_text(), self.on_click)
        KeyButton._keybuttons.append(self)
        
        self.listening = False

    def on_click(self):
        self.listening = True
        
    def update(self):
        super().update()
        
        if self.listening and self.key_event:
            if self.key_event not in self.FORBIDDEN_KEYS:
                Keybinds.set(self.key_code, self.key_event)
                self.text = self.get_text()
            self.listening = False
            
    def get_text(self) -> str:
        key_name = get_key_name(Keybinds[self.key_code])
        
        if len(key_name) == 1:
            return key_name.upper()
        else:
            return'key.' + key_name.replace(" ", "_")
    
    @classmethod
    def reset(cls):
        for kb in cls._keybuttons:
            kb.listening = False    
