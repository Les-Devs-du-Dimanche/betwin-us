from .camera import Camera
from .action import Action
from ...hinting import Object


class Cinematic:
    
    def __init__(self, actions: list[Object]):
        self.camera = Camera()
        self.actions = []
        
        for obj in sorted(actions, key=lambda o: o['properties']['order']):
            if obj['type'] == 'camera_move':
                self.actions.append(Action(
                    Action.Type.CAMERA_MOVE,
                    float(obj['properties']['time']),
                    pos=(int(obj['x']), int(obj['y'])),
                    camera=self.camera
                ))
            
        self.done = None
        self.action = None
        
    def update(self, dt: int):
        if not self.action:
            self.action = self.actions.pop(0)
            self.action.init()

        self.action.update(dt)
        
        if self.action.done:
            self.action = None
        
            if not self.actions:
                self.done = True
