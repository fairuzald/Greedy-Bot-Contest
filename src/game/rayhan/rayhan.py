from abc import ABC
from typing import Tuple

from game.models import Board, GameObject

import random
from typing import Optional,List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction,clamp
from datetime import datetime

class BaseLogic(ABC):
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        raise NotImplementedError()
    
class RayhanLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        # time start
        time_start = datetime.now()
        props = board_bot.properties
        diamonds = []
        portals = []
        enemies = []
        
        my_base_pos = board_bot.properties.base
        
        for obj in board.game_objects:
            if(obj.type == "DiamondGameObject"):
                if(props.diamonds >= 4 and obj.properties.points == 2 ):
                    pass
                else:
                    diamonds.append(obj.position)
                    
            elif(obj.type == "TeleportGameObject"):
                portals.append(obj.position)
            elif(obj.type == "BotGameObject"):
                enemies.append(obj.position)
            elif(obj.type == "DiamondButtonGameObject"):
                red_button = obj.position

        # Analyze new state
        
        if(getDistanceBetween(board_bot.position, portals[0])  <= getDistanceBetween(board_bot.position, portals[1])):
            self.goal_position = portals[0]
            near_portal = portals[0]
            far_portal = portals[0]
        else:
            near_portal = portals[1]
            far_portal = portals[0]
        
        nearest_diamond_with_base = getNearestDiamondWithBase(board_bot.position, diamonds, my_base_pos)

        if(board_bot.properties.milliseconds_left <10000 and props.diamonds > 0):
            print("1")
            self.goal_position = my_base_pos
        
        elif props.diamonds == 5:
            # Move to base
            print("2")
            self.goal_position = my_base_pos
            
        elif(getDistanceBetween(board_bot.position, nearest_diamond_with_base) > getDistanceBetween(board_bot.position, red_button)):
            print("3")
            self.goal_position = red_button

        elif(getDistanceBetween(board_bot.position, nearest_diamond_with_base) > getDistanceBetween(board_bot.position, my_base_pos) and isSearah(board_bot.position, nearest_diamond_with_base, my_base_pos) and props.diamonds > 2):
            print("4")
            self.goal_position = my_base_pos
        
        else:
            
            print("5")
            self.goal_position = nearest_diamond_with_base


        if(getDistanceWithPortalRelBase(board_bot.position, near_portal, far_portal, self.goal_position, my_base_pos) < getDistanceBetween(board_bot.position, self.goal_position)):
            self.goal_position = near_portal
        
        current_position = board_bot.position
        if self.goal_position:
            
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y
            
            )
            if(self.goal_position != near_portal and getDistanceBetween(current_position, near_portal) == 1):
                delta_x,delta_y = delta_y,delta_x
            
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
                
        time_end = datetime.now()
        print("Time: ", (time_end - time_start).microseconds)
        return delta_x, delta_y


def getDistanceBetween (curr_pos:Position, target_pos:Position) -> int:
        return abs(curr_pos.x - target_pos.x) + abs(curr_pos.y - target_pos.y)
    
def getNearestDiamondWithBase (curr_po :Position, diamonds : List[Position], base_pos : Position) -> Position:
    min_distance = 100000
    nearest_diamond = None
    for diamond in diamonds:
        distance = getDistanceBetween(curr_po, diamond) + getDistanceBetween(diamond, base_pos)
        if(distance < min_distance):
            min_distance = distance
            nearest_diamond = diamond
    return nearest_diamond

def isSearah (curr_po:Position, target1_po:Position, target2_po :Position) -> bool:
    # split to 4 quadrant based on curr_po then if target1 and target2 in same quadrant return true
    if(target1_po.x > curr_po.x and target2_po.x > curr_po.x and target1_po.y > curr_po.y and target2_po.y > curr_po.y):
        return True
    elif(target1_po.x < curr_po.x and target2_po.x < curr_po.x and target1_po.y > curr_po.y and target2_po.y > curr_po.y):
        return True
    elif(target1_po.x < curr_po.x and target2_po.x < curr_po.x and target1_po.y < curr_po.y and target2_po.y < curr_po.y):
        return True
    elif(target1_po.x > curr_po.x and target2_po.x > curr_po.x and target1_po.y < curr_po.y and target2_po.y < curr_po.y):
        return True
    return False

def getDistanceWithPortalRelBase(curr_po:Position, near_portal:Position, far_portal:Position,target_po: Position, base_pos:Position) -> int:
    return getDistanceBetween(curr_po, near_portal) + getDistanceBetween(far_portal, target_po) + min(getDistanceBetween(target_po, base_pos), getDistanceBetween(target_po, far_portal) + getDistanceBetween(near_portal,base_pos))


# def get_direction_v2(current_x, current_y, dest_x, dest_y,nearesttel):
#             delta_x = clamp(dest_x - current_x, -1, 1)
#             delta_y = clamp(dest_y - current_y, -1, 1)
            
            
#             portalPos = nearesttel
            
#             if()
            
#             if (current_x+delta_x==portalPos.x and current_y==portalPos.y):
#                 return (0, delta_y)
            
#             elif(current_y+delta_y==portalPos.y and current_x==portalPos.x):
#                 return (delta_x, 0)
#             else:
#                 # make it like random using mod but only 1 step
#                 if(delta_x == 0 or delta_y == 0):
#                     return(delta_x, delta_y)
#                 else:
#                     if(current_x%2==1):
#                         return(delta_x, 0)
#                     else:
#                         return(0, delta_y)