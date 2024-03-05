from game.models import GameObject, Board, Position
from game.util import get_direction
from typing import List
from game.alucard.service.math_services import MathService
from game.alucard.service.object_services import ObjectServices


class Coba:

        
    def kejar(self,board : Board, target):
        for obj in board.game_objects:
            if obj.properties.name == target:
                return obj.position
        
            
            