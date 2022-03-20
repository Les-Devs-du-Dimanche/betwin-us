from typing import Protocol, TypedDict

from pygame import Rect, Surface

from .consts import Facing

if 0: from .entity.entity import Entity


class HasRect(Protocol):
    rect: Rect
    
class AnimationDict(TypedDict):
    speed: float
    animations: dict[str, tuple[int, int]] # row | nb of tile

class AnimationTarget(Protocol):
    
    facing: Facing
    status: 'Entity.Status'

AnimationFrames = dict[str, list[Surface]]
