from .enemy.cursed_chest import CursedChest
from .enemy.slime import Slime
from .enemy.firesoul import Firesoul
from .enemy.red_slime import RedSlime
from .enemy.brain import Brain

entity_dict = {
    'slime': Slime,
    'firesoul' : Firesoul, 
    'cursed_chest' : CursedChest,    
    'red_slime' : RedSlime,
    'brain' : Brain
}