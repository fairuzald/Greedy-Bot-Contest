from game.models import Position
from typing import List
from game.util import clamp

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
    
    @staticmethod
    def isSameDirection (curr_po:Position, target1_po:Position, target2_po :Position) -> bool:
        if(target1_po.x > curr_po.x and target2_po.x > curr_po.x and target1_po.y > curr_po.y and target2_po.y > curr_po.y):
            return True
        elif(target1_po.x < curr_po.x and target2_po.x < curr_po.x and target1_po.y > curr_po.y and target2_po.y > curr_po.y):
            return True
        elif(target1_po.x < curr_po.x and target2_po.x < curr_po.x and target1_po.y < curr_po.y and target2_po.y < curr_po.y):
            return True
        elif(target1_po.x > curr_po.x and target2_po.x > curr_po.x and target1_po.y < curr_po.y and target2_po.y < curr_po.y):
            return True
        return False
    
    @staticmethod
    def get_direction_v2(current_x, current_y, dest_x, dest_y):
            delta_x = clamp(dest_x - current_x, -1, 1)
            delta_y = clamp(dest_y - current_y, -1, 1)
            
            if(delta_x == 0 or delta_y == 0):
                return(delta_x, delta_y)
            else:
                if(current_x%2==1):
                    return(delta_x, 0)
                else:
                    return(0, delta_y)
