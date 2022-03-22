from multiprocessing import Process, Queue

from numpy import ones as create_empty_matrix
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pygame import Vector2

from ..consts import TILE_SIZE
from ..group import Groups
from ..hinting import Coords
from ..time import Time

# hinting
if 0:
    from .entity import Entity
    from ..tmx.level import Level


class PathFinder:
    
    finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)

    TIMEOUT = 500 # ms

    @classmethod
    def start(cls, level: 'Level') :
                        
        cls.input_queue =  Queue()
        cls.output_queue = Queue()
        
        cls.waiting_entities = {}
        cls.ready_entities   = {}
        
        Process(
            name   = 'PathFindingProcess',
            target = cls._process,
            args   = (cls.input_queue, cls.output_queue),
            daemon = True
        ).start()
        
        cls.load_grid(level)
    
    @classmethod
    def obstacle_between(cls, pos1: Coords, pos2: Coords) -> bool:
        if hasattr(pos1, 'rect'):
            pos1 = Vector2(pos1.rect.center)
        else:
            pos1 = Vector2(pos1)
            
        if hasattr(pos2, 'rect'):
            pos2 = Vector2(pos2.rect.center)
        else:
            pos2 = Vector2(pos2)
        
        v = pos2 - pos1
        d = v.length()
        
        if d != 0:
            v = v.normalize()
                    
            for i in range(1, int(d)):
                for sprite in Groups.obstacles:
                    if sprite.rect.collidepoint(pos1 + v * i):
                        return True
        return False
    
    @classmethod
    def load_grid(cls, level: 'Level'):
        matrix = create_empty_matrix((level.width // TILE_SIZE, level.height // TILE_SIZE))
        for obj in Groups.obstacles:
            rect = obj.rect
            x, y = rect.x // TILE_SIZE, rect.y // TILE_SIZE
            
            for w in range(rect.width // TILE_SIZE):
                for h in range(rect.height // TILE_SIZE):
                    matrix[y + h][x + w] = 0
            
        cls.grid = Grid(matrix=matrix)
        cls.input_queue.put(('grid', cls.grid))
        
    @classmethod
    def update_grid(cls, pos: Vector2, walkable: bool):
        cls.grid.node(*pos).walkable = walkable
        cls.input_queue.put(('grid', cls.grid))
    
    @classmethod
    def find(cls, _from: 'Entity', _to: 'Entity') -> tuple[int, int] | None:
        
        if _from not in cls.waiting_entities:
            start = Vector2(_from.rect.center)
            end = Vector2(_to.rect.center)

            cls.input_queue.put((start, end))
            cls.waiting_entities[_from] = Time.get()
            
        if _from in cls.ready_entities:
            return cls.ready_entities.pop(_from)
            
    @classmethod
    def update(cls):
        while not cls.output_queue.empty():
            pos = cls.output_queue.get()
            
            entity = list(cls.waiting_entities.keys())[0]
            timeout = cls.waiting_entities.pop(entity)
            
            if Time.get() < timeout + cls.TIMEOUT:
                cls.ready_entities[entity] = pos
    
    @classmethod
    def _process(cls, input_queue: Queue, output_queue: Queue):
        while True:
            # get first queue element
            data = input_queue.get()
            if data[0] == 'grid':
                cls.grid = data[1]
                continue
            else:
                start, end = data 
            
            # setup start and end points
            start_pos = start // TILE_SIZE
            end_pos = end // TILE_SIZE

            # find path
            start_node = cls.grid.node(int(start_pos.x), int(start_pos.y))
            end_node = cls.grid.node(int(end_pos.x), int(end_pos.y))
            
            edited_node = None # cause of player hitbox, end_point sometimes placed in unwalkable node
            if not end_node.walkable:
                edited_node = end_node
                edited_node.walkable = True
            
            path, _ = cls.finder.find_path(start_node, end_node, cls.grid)
            
            cls.grid.cleanup()
                    
            # get the next tile to go
            if len(path) > 1:
                goto = Vector2(path[1]) * TILE_SIZE + 0.5 * Vector2(TILE_SIZE)
                output_queue.put(goto)
            else:
                output_queue.put(None)
                                
            if edited_node:
                edited_node.walkable = False
