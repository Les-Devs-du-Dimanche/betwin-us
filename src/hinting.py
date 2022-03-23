from typing import Literal, Protocol, TypedDict, Any

from pygame import Rect, Surface, Vector2

from .consts import Facing, DoorState

if 0: from .entity.entity import Entity


class HasRect(Protocol):
    rect: Rect
    
Coords = HasRect | Vector2
    
class AnimationDict(TypedDict):
    speed: float
    animations: dict[str, tuple[int, int]] # row | nb of tile

class AnimationTarget(Protocol):
    
    facing: Facing
    status: 'Entity.Status'

AnimationFrames = dict[str, list[Surface]]

class DoorStateDict(TypedDict):
    Facing: DoorState

# Tiled json objects
class Property(TypedDict):

    name: str
    type: type
    value: Any

class TileLayer(TypedDict):
    
    # presents but not used :
    # 
    # id: int
    # x: int
    # y: int
    # opacity: int
    # visible: bool

    name: str
    type: Literal['tilelayer']
    
    width: int
    height: int

    data: list[int]
    
    properties: list[Property]      
    
class Object(TypedDict):
    
    # presents but not used :
    # 
    # id: int
    # rotation: int
    # visible: bool
    
    name: str
    type: str
    point: bool
    
    x: int
    y: int
    width: int
    height: int
    
    properties: list[Property]

class ObjectGroup(TypedDict):
    
    # presents but not used :
    # 
    # id: int
    # x: int
    # y: int  
    # opacity: int
    # visible: bool
    # draworder: Literal['topdown']
    
    name: str
    type: Literal['objectgroup']
    objects: list[Object]

class Tileset(TypedDict):
    firstgid: int
    source: str

class LevelData(TypedDict):
        
    # presents but not used :
    # 
    # width: int
    # height: int
    # infinite: bool
    # type: Literal['map']
    # tileheight: int
    # tilewidth: int
    # compressionlevel: int
    # nextlayerid: int
    # nextobjectid: int
    # version: str
    # tiledversion: str
    # orientation: Literal['orthogonal']
    # renderorder: Literal['right-down']
    
    layers: list[TileLayer | ObjectGroup]
    tilesets: list[Tileset]
