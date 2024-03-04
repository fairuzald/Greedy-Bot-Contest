from game.models import Position
from typing import List
class MathService:
    @staticmethod
    def getDistanceBetween (curr_pos:Position, target_pos:Position) -> int:
        return abs(curr_pos.x - target_pos.x) + abs(curr_pos.y - target_pos.y)
    
    def getDistanceBetweenTransition (curr_pos:Position,transition:Position, target_pos:Position) -> int:
        return abs(curr_pos.x - transition.x) + abs(curr_pos.y - transition.y) + abs(transition.x - target_pos.x) + abs(transition.y - target_pos.y)

    
    @staticmethod 
    def getNearestObjectPosition(curr_pos:Position, target_pos: List[Position]) -> Position:
        nearest = None
        nearest_distance = float('inf')
        for obj in target_pos:
            distance = MathService.getDistanceBetween(curr_pos, obj)
            if distance < nearest_distance:
                nearest = obj
                nearest_distance = distance
        return nearest
    
    @staticmethod
    def getObjectsInArea(bot_position:Position, target_pos: List[Position], area:int) -> List[Position]:
        objects = []
        for obj in target_pos:
            if MathService.getDistanceBetween(bot_position, obj) <= area:
                objects.append(obj)
        return objects
    
    @staticmethod
    def isObjectInArea(bot_position:Position ,target_pos: List[Position], area:int) -> bool:
        for obj in target_pos:
            if MathService.getDistanceBetween(bot_position, obj) <= area:
                return True
        return False