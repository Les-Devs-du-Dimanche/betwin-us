from src.generator.room import Room
from src.functions import path 

import random as rm

class RoomList :
    
    def __init__(self, create_room : int) -> None:
        for element in range(create_room):
            self.__setattr__(f"room_{element + 1}", Room(f"map_{element + 1}"))


class Generator :
    
    def __init__(self, size = None, min = 3, max = 5) -> None:
        self.matrix = self.generate_matrix(min, max)
    
    def generate_matrix(min=3, max=6) -> list:
        size = rm.randint(min, max)
        matrix = []
        for i in range(size):
            matrix.append([])
            for element in range(size):
                matrix[i].append(None)
        return matrix
   