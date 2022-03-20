import sys

import pygame

from .consts import DISPLAY_SIZE, FPS
from .display.assets import Assets
from .entity.player import Player
from .group import Groups
from .gui.components import Button, KeyButton, Slider
from .gui.menu import Menu
from .keybinds import Keybinds
from .settings import Settings
from .sound import Sound
from .time import Time
from .translate import Translate


class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()
        
        Assets.load()
        Settings.load()
        Sound.init(
            music = Settings['volume.music'],
            enemies = Settings['volume.enemies'],
            player = Settings['volume.player'],
            gui = Settings['volume.gui'],
        )
        Translate.load(Settings['lang'])
        Keybinds.load()
        Groups.init()
        
        self.player = Player(pygame.Vector2(100, 100))
        
        self.menu = Menu(self.quit)
    
    def run(self):
        while True:
            
            Button.click_event = False
            KeyButton.key_event = None
            Slider.click_event = False
            
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.escape()
                    else:
                        print(event.key)
                
                elif event.type == pygame.KEYUP:
                    KeyButton.key_event = event.key
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    Button.click_event = True
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    KeyButton.reset()
                    Slider.click_event = True
                    
                elif event.type == pygame.QUIT:
                    self.quit()
                    
            self.update()
            self.render()
                        
            self.clock.tick(FPS)
            
    def update(self):
        dt = self.clock.get_time()
        
        if not Time.paused:
            Groups.to_update.update(dt)
        else:
            self.menu.update()
        
    def render(self):
        # NOTE: tmp
        self.screen.fill((108, 145, 97))
        
        Groups.background.draw(self.player)
        Groups.visible.draw(self.player)
        
        if Time.paused:
            self.menu.draw()
        
        pygame.display.flip()
                    
    def quit(self):
        pygame.mixer.fadeout(500)
        pygame.quit()
        sys.exit()
