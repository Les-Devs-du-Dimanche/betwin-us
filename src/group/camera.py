from pygame import Vector2
from pygame.display import get_surface as get_screen
from pygame.sprite import Group

from ..hinting import HasRect


class Camera(Group):
    
    def __init__(self):
        super().__init__()
        
        self.display_surface = get_screen()
        self.screen_center = Vector2(self.display_surface.get_size()) * 0.5
            
    def draw(self, center: HasRect):

        offset = Vector2(center.rect.center) - self.screen_center
        
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
                        
            self.display_surface.blit(
                sprite.image,
                sprite.rect.topleft - offset
            )
    