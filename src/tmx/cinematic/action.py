from enum import Enum

from pygame import Vector2

from .camera import Camera


class Action:
    
    class Type(Enum):
        CAMERA_MOVE = 0
        DIALOGUE = 1
    
    def __init__(self, type: Type, time: float, 
        pos: tuple[int, int] = None, camera: Camera = None # Type.CAMERA_MOVE
    ):
        self.done = False
        self.type = type
        self.time = time
        
        self.pos = pos
        self.camera = camera
        
    def init(self):
        if self.type == self.Type.CAMERA_MOVE:
            self.camera.go_to(Vector2(self.pos), self.time)
        
    def update(self, dt: int):
        if self.type == self.Type.CAMERA_MOVE:
            self.camera.update(dt)
            
            if self.camera.target is None:
                self.done = True
