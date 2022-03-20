import sys

import pygame


class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    
    def quit(self):
        pygame.quit()
        sys.exit()
