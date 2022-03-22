from src.functions import path

import json 


class Room :

    def __init__(self, name : str) -> None :
        with open(path(f"assets/tmx/rooms/{name}.tmj"), "r", encoding='utf8') as r_file :
            r_file = json.load(r_file)
        self.raw = r_file
        self.doors = {}
        for object in self.raw["layers"][1]["objects"] :
            self.doors[object['name']] = (object['x'], object['y'])
    
    def nb_doors(self) :
        return len(self.doors.keys())
    