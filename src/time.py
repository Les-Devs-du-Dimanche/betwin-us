from pygame.time import get_ticks


class Time:
    
    paused = False
    offset = 0
    
    @classmethod
    def pause(cls):
        cls.paused_time = get_ticks()
        cls.paused = True
        
    @classmethod
    def resume(cls):
        cls.offset += get_ticks() - cls.paused_time
        cls.paused = False
        
    @classmethod
    def get(cls) -> int:
        if cls.paused:
            return cls.pause_time
        else:
            return get_ticks() - cls.offset
