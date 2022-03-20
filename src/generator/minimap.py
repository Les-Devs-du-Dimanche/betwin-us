from email.encoders import encode_noop
import json 


class Minimap :

    def __init__(self, name : str) -> None :
        with open(f"ressources/map/{name}.tmj", "r", encoding='utf8') as r_file :
            r_file = json.load(r_file)
        self.raw = r_file
        self.door = {}
        for object in self.raw["layers"][1]["objects"] :
            self.door[object['name']] = (object['x'], object['y'])
    