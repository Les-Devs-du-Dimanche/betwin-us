from pygame.sprite import Group

from .camera import Camera


class Groups:
    
    @classmethod
    def init(cls):
        cls.background = Camera()
        cls.visible    = Camera()
        cls.to_update  = Group()
        
        cls.obstacles = Group()
        cls.entities  = Group()
