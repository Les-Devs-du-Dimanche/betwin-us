import xml.etree.ElementTree as Element

from pygame import Surface
from pygame.image import load as load_image
from pygame.locals import SRCALPHA

from ..consts import TILE_SIZE
from ..hinting import Tileset as _Tileset
from ..functions import path


class Tileset:
    
    def __init__(self, data: list[_Tileset]):
        
        self.tiles = {
            0: Surface((TILE_SIZE, TILE_SIZE), SRCALPHA),
        }
        
        for tileset in data:
        
            firstgrid = tileset['firstgid']
            
            file_name = tileset['source'].split('/')[-1]
            tree = Element.parse(path('assets/tmx/tilesets/' + file_name))
            root = tree.getroot()
            
            tile_count = int(root.attrib['tilecount'])
            columns = int(root.attrib['columns'])
            
            image_root = root.find('image')
            image_filename = image_root.attrib['source'].split('/')[-1]
            image = load_image(path('assets/textures/tilesets/' + image_filename)).convert_alpha()
            
            for i in range(tile_count):
                x = (i % columns) * TILE_SIZE
                y = (i // columns) * TILE_SIZE
                
                s = Surface((TILE_SIZE, TILE_SIZE), SRCALPHA)
                s.blit(
                    image,
                    (0, 0),
                    (x, y, TILE_SIZE, TILE_SIZE)
                )
                self.tiles[firstgrid + i] = s
    
    def get(self, tile: int) -> Surface:
        return self.tiles[tile]
