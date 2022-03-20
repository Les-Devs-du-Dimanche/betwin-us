from .components import Component, KeyButton

from ..time import Time


class BaseMenu:
    
    submenues: list['BaseMenu'] = []
    components: list[Component]
    
    def __init__(self):
        self.opened = False
            
    def escape(self):
        if self.opened:
            for submenu in self.submenues:
                if submenu.opened:
                    submenu.escape()
                    break
            else:
                for component in self.components:
                    if isinstance(component, KeyButton):
                        if component.listening:
                            component.listening = False
                            break
                else:
                    self.opened = False
        else:
            self.opened = True
            Time.pause()
    
    def update(self):
        for submenu in self.submenues:
            if submenu.opened:
                submenu.update()
                break
        else:
            for component in self.components:
                component.update()
            
    def draw(self):
        for submenu in self.submenues:
            if submenu.opened:
                submenu.draw()
                break
        else:
            for component in self.components:
                component.draw()
