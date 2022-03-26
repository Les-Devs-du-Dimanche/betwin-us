from .enemy import Enemy

class RedSlime(Enemy):

    animation_name = 'entity.red_slime'
    health = 50
    
    HITBOX = -48, -62
 