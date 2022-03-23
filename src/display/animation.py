from pygame import Surface
from pygame.locals import SRCALPHA

from ..consts import TILE_SIZE
from ..hinting import AnimationDict, AnimationFrames, AnimationTarget


class Animation:
    
    def __init__(self, data: AnimationDict, surface: Surface = None, _frames: AnimationFrames = None):
        self.frame_idx = 0
        
        self._data = data
        self.speed = data['speed']

        if _frames:
            self.frames = _frames
        else:
            self.frames = {}
            for key, value in data['animations'].items():
                row, col = value
                
                frames = []
                for x in range(col):
                    s = Surface((TILE_SIZE, TILE_SIZE), SRCALPHA)
                    s.blit(
                        surface,
                        (0, 0),
                        (x * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )
                    frames.append(s)

                self.frames[key] = frames
                
                
                    
    def update(self, dt: int):
        self.current_key = self.target.facing.name.lower() + '_' + self.target.status.name.lower()
        
        self.frame_idx += self.speed * dt
        self.frame_idx %= len(self.frames[self.current_key])
        
    def set_target(self, target: AnimationTarget):
        self.target = target

    def get_surface(self) -> Surface:
        # print(self.current_key)
        return self.frames[self.current_key][int(self.frame_idx)]
    
    def copy(self) -> 'Animation':
        return Animation(self._data, _frames=self.frames)
