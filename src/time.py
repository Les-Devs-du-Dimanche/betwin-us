from pygame.time import get_ticks


class Time:
    
    paused = False
    
    @classmethod
    def pause(cls):
        cls.paused = True
        
    @classmethod
    def resume(cls):
        cls.paused = False
