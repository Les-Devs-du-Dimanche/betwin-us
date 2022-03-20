from .display.assets import Assets
from .settings import Settings


class Meta(type):
    
    @property
    def music_volume(cls) -> float:
        return cls._music_volume

    @music_volume.setter
    def music_volume(cls, value: float):
        cls._music_volume = value
        Settings.set('volume.music', value)
        
    @property
    def enemies_volume(cls) -> float:
        return cls._enemies_volume

    @enemies_volume.setter
    def enemies_volume(cls, value: float):
        cls._enemies_volume = value
        Settings.set('volume.enemies', value)
        
    @property
    def player_volume(cls) -> float:
        return cls._player_volume

    @player_volume.setter
    def player_volume(cls, value: float):
        cls._player_volume = value
        Settings.set('volume.player', value)
        
    @property
    def gui_volume(cls) -> float:
        return cls._gui_volume

    @gui_volume.setter
    def gui_volume(cls, value: float):
        cls._gui_volume = value
        Settings.set('volume.gui', value)

class Sound(metaclass=Meta):
    
    @classmethod
    def init(cls, music: float, enemies: float, player: float, gui: float):
        cls._music_volume = music
        cls._enemies_volume = enemies
        cls._player_volume = player
        cls._gui_volume = gui        
    
    @classmethod
    def _play(cls, key: str, volume: float):
        sound = Assets.get(key)
        sound.set_volume(volume)
        sound.play()
        
    @classmethod
    def player(cls, key: str):
        cls._play(key, cls.player_volume)
    
    @classmethod
    def enemy(cls, key: str):
        cls._play(key, cls.enemies_volume)
        
    @classmethod
    def gui(cls, key: str):
        cls._play(key, cls.gui_volume)
    