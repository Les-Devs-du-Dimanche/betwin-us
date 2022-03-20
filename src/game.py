import sys

import pygame

from .consts import DISPLAY_SIZE, FPS
from .display.assets import Assets
from .entity.player import Player
from .group import Groups
from .keybinds import Keybinds


class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()
        
        Assets.load()
        Keybinds.load()
        Groups.init()
        
        self.player = Player(pygame.Vector2(100, 100))
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    print(event.key)
                    
            self.update()
            self.render()
            
            # print(self.player.rect.center)
            
            self.clock.tick(FPS)
            
    def update(self):
        dt = self.clock.get_time()
        
        Groups.to_update.update(dt)
        
    def render(self):
        # NOTE: tmp
        self.screen.fill((0, 0, 0))
        
        Groups.background.draw(self.player)
        Groups.visible.draw(self.player)
        
        pygame.display.flip()
                    
    def quit(self):
        pygame.quit()
        sys.exit()
