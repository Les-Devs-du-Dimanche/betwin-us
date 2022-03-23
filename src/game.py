import sys

import pygame

from .entity.pathfinder import PathFinder
from .consts import DISPLAY_SIZE, DT_SPEED, FPS
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
        if self.level.cinematic:
            self.camera_target = self.level.cinematic.camera
            self.player.movements_locked = True
        else:
            self.camera_target = self.player
        
        PathFinder.start(self.level)
    
    def run(self):
        while True:
            
            Button.click_event = False
            KeyButton.key_event = 0
            Slider.click_event = False
            
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.escape()
                        
                    elif event.key == pygame.K_SPACE:
                        if self.level.cinematic:
                            self.level.cinematic = None
                            self.camera_target = self.player
                            self.player.movements_locked = False
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
            
            self.update()
            self.render()
                        
            self.clock.tick(FPS)
            
    def update(self):
        dt = self.clock.get_time() * DT_SPEED
        
        if not Time.paused:
            if self.level.cinematic:
                if self.level.cinematic.done:
                    self.camera_target = self.player
                    self.level.cinematic = None
                    self.player.movements_locked = False
                else:
                    self.level.cinematic.update(dt)
                    
            Groups.to_update.update(dt)
            PathFinder.update()
        else:
            self.menu.update()
        
    def render(self):        
        Groups.background.draw(self.camera_target)
        Groups.visible.draw(self.camera_target)
        
        if Time.paused:
            self.menu.draw()
        
        try:
            offset = pygame.Vector2(self.level.cinematic.camera.rect.center) - Groups.visible.screen_center
            pygame.draw.line(
                self.screen,
                (255, 0, 0),
                pygame.Vector2(self.level.cinematic.camera.rect.center) - offset,
                self.level.cinematic.camera.target - offset,
                3
            )
            
            pygame.draw.line(
                self.screen,
                (0, 0, 255),
                pygame.Vector2(self.level.cinematic.camera.rect.center) - offset,
                pygame.Vector2(self.level.cinematic.camera.rect.center) + self.level.cinematic.camera.direction * 50 - offset,
                5
            )
        except:
            pass
        
        pygame.display.flip()
                    
    def quit(self):
        pygame.mixer.fadeout(500)
        pygame.quit()
        sys.exit()
