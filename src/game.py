import sys

import pygame

from .entity.pathfinder import PathFinder
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
from .tmx.level import Level

from .tmx.tile import Tile


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
        
        self.menu = Menu(self.quit)
        
        self.level = Level.load('cinematics/forest.json')
        self.player = Player(self.level.worldspawn)
        
        PathFinder.start(self.level)
        
        # NOTE : DEBUG square at cursor 1/2
        # s = pygame.Surface((64, 64), pygame.SRCALPHA)
        # pygame.draw.rect(
        #     s, (255, 0, 0),
        #     (0, 0, 64, 64),
        #     3
        # )
        # self.select = Tile([Groups.visible], s)
    
    def run(self):
        while True:
            
            Button.click_event = False
            KeyButton.key_event = 0
            Slider.click_event = False
            
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.escape()
                    # else:
                    #     print(event.key)
                
                elif event.type == pygame.KEYUP:
                    KeyButton.key_event = event.key
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    Button.click_event = True
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Slider.click_event = True
                    
                elif event.type == pygame.QUIT:
                    self.quit()
            
            # NOTE : DEBUG square at cursor 2/2
            # mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) + Groups.visible.offset
            # self.select.rect.center = mouse_pos
            
            self.update()
            self.render()
                        
            self.clock.tick(FPS)
            
    def update(self):
        dt = self.clock.get_time()
        
        if not Time.paused:
            Groups.to_update.update(dt)
            PathFinder.update()
        else:
            self.menu.update()
        
    def render(self):
        # NOTE: tmp
        # self.screen.fill((108, 145, 97))
        
        Groups.background.draw(self.player)
        Groups.visible.draw(self.player)
        
        if Time.paused:
            self.menu.draw()
        
        pygame.display.flip()
                    
    def quit(self):
        pygame.mixer.fadeout(500)
        pygame.quit()
        sys.exit()
