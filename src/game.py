import sys

import pygame

# from .entity.pathfinder import PathFinder
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
        
        # NOTE: Not enough fast
        # PathFinder.start(self.level)
        
        self.font = Assets.get('font.menu', size=24)
    
    def run(self):
        while True:
            
            Button.click_event = False
            KeyButton.key_event = 0
            Slider.click_event = False
            self.player.click_event = None
            
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.escape()
                        
                    elif event.key == pygame.K_SPACE:
                        if self.level.cinematic:
                            self.end_cinematic()
                    # else:
                    #     print(event.key)
                
                elif event.type == pygame.KEYUP:
                    KeyButton.key_event = event.key
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    Button.click_event = True
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Slider.click_event = True
                    self.player.click_event = event
                    
                elif event.type == pygame.QUIT:
                    self.quit()

                elif event.type == self.player.switch:
                    self.player.switch_mode()                           
            
            self.update()
            self.render()
                        
            self.clock.tick(FPS)
    
    def attack_logic(self):
        # player attacks
        for attack in Groups.player_attacks:
            attack_mask = pygame.mask.from_surface(attack.image)
            
            sprites = pygame.sprite.spritecollide(attack, Groups.entities, False)
            for sprite in sprites:
                if sprite == self.player: continue
                    
                sprite_mask = pygame.mask.from_surface(sprite.image)
                offset = sprite.pos - pygame.Vector2(attack.rect.center)
                if attack_mask.overlap(sprite_mask, offset):
                    sprite.get_damages(attack)
                    
        # enemies attacks
        for attack in Groups.enemies_attacks:
            attack_mask = pygame.mask.from_surface(attack.image)
            
            player_mask = pygame.mask.from_surface(self.player.image)
            offset = self.player.pos - pygame.Vector2(attack.rect.center)
            if attack_mask.overlap(player_mask, offset):
                self.player.get_damages(attack)
    
    def end_cinematic(self):
        self.camera_target = self.player
        self.level.cinematic = None
        
        for entity in Groups.entities.sprites():
            entity.movements_locked = False
            
    def update(self):
        dt = self.clock.get_time() * DT_SPEED
        
        if not Time.paused:
            if self.level.cinematic:
                if self.level.cinematic.done:
                    self.end_cinematic()
                else:
                    self.level.cinematic.update(dt)
                    
            Groups.to_update.update(dt)
            self.attack_logic()
            # PathFinder.update()
        else:
            self.menu.update()
        
    def render(self):        
        Groups.background.draw(self.camera_target)
        Groups.visible.draw(self.camera_target)
        
        if Time.paused:
            self.menu.draw()
        
        # Show fps
        # surface = self.font.render(str(round(self.clock.get_fps())), True, (255, 255, 255))
        surface = self.font.render(str(self.player.status), True, (255, 255, 255))
        self.screen.blit(
            surface,
            surface.get_rect(topleft=(10, 10))
        )
                
        pygame.display.flip()
                    
    def quit(self):
        pygame.mixer.fadeout(500)
        pygame.quit()
        sys.exit()
