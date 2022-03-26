from json import loads as json_loads

from pygame import Surface, Vector2
from pygame.locals import SRCALPHA

from ..consts import TILE_SIZE
from ..display.assets import Assets
from ..functions import path
from ..group import Groups
from ..hinting import LevelData, ObjectGroup, TileLayer, Object
from .tile import Tile
from ..entity.dict import entity_dict
from .cinematic.cinematic import Cinematic
from .generator.generator import Generator


class Level:
    
    @classmethod
    def generate(cls) -> 'Level':
        level_dict = Generator.generate()
        return Level(level_dict)
    
    @classmethod
    def load(cls, filename: str) -> 'Level':
        with open(path('assets/tmx/' + filename), 'r') as file:
            data = json_loads(file.read())
    
        return Level(data)
    
    def __init__(self, data: LevelData):
        
        self.cinematic = None
        
        self.width  = TILE_SIZE * int(data['width'])
        self.height = TILE_SIZE * int(data['height'])
        
        # tileset            
        tileset_id = ''.join(
            tileset['source'].split('/')[-1]
            for tileset in data['tilesets']
        )
        self.tileset = Assets.get(data['tilesets'], id = tileset_id)
        
        # layers
        for layer_data in data['layers']:
            if layer_data['type'] == 'tilelayer':
                self.load_tile_layer(layer_data)
            else: # object group
                self.load_object_group(layer_data)
    
    def load_tile_layer(self, layer_data: TileLayer):
        use_sprites = False
        
        # properties
        if 'properties' in layer_data:
            for property in layer_data['properties']:
                if property['name'] == 'sprites' and property['value']:
                    use_sprites = True
                
        # building layer
        width = layer_data['width']
        height = layer_data['height']
        
        if use_sprites:
            for i, tile_int in enumerate(layer_data['data']):
                if tile_int:
                    tile_surface = self.tileset.get(tile_int)
                    x = (i % width) * TILE_SIZE
                    y = (i // height) * TILE_SIZE
                    
                    Tile([Groups.visible, Groups.obstacles], tile_surface, [x, y, TILE_SIZE, TILE_SIZE])
        
        else:
            layer_surface = Surface((TILE_SIZE * width, TILE_SIZE * height), SRCALPHA)
            
            for i, tile_int in enumerate(layer_data['data']):
                tile_surface = self.tileset.get(tile_int)
                x = (i % width) * TILE_SIZE
                y = (i // height) * TILE_SIZE
                
                layer_surface.blit(
                    tile_surface,
                    (x, y)
                )
                
            Tile([Groups.background], layer_surface)
                
    def load_object_group(self, layer_data: ObjectGroup):
        if layer_data['name'] == 'data':
            for obj in layer_data['objects']:
                if obj['type'] == 'worldspawn':
                    self.worldspawn = Vector2(obj['x'], obj['y'])
                    
        elif layer_data['name'] == 'entities':
            for obj in layer_data['objects']:
                if obj['type'] in entity_dict:
                    entity_dict[obj['type']](Vector2(obj['x'], obj['y']))
                    
        elif layer_data['name'] == 'cinematic':
            objs = [self.clean_object_properties(obj) for obj in layer_data['objects']]
            self.cinematic = Cinematic(objs)
            
    def clean_object_properties(self, obj: Object) -> Object:
        if 'properties' in obj:
            properties = {}
            
            for p in obj['properties']:
                
                type = p["type"]
                if type == 'string':
                    type = 'str'
                
                properties[p['name']] = eval(f'{type}("{p["value"]}")')
                
            obj['properties'] = properties
        
        return obj
