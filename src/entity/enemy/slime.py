from .enemy import Enemy


class Slime(Enemy):
    
    animation_name = 'entity.slime'
    health = 50
    
    HITBOX = -48, -62
 