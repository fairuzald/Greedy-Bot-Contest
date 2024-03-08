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
        # TODO: DOne
        time_start = datetime.now()
        props = board_bot.properties
        diamonds = []
        portals = []
        enemies = []
        
        # TODO: DOne
        my_base_pos = board_bot.properties.base
        
        # TODO: DOne
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

        # TODO : Done
        if(getDistanceBetween(board_bot.position, portals[0])  <= getDistanceBetween(board_bot.position, portals[1])):
            near_portal = portals[0]
            far_portal = portals[1]
        else:
            near_portal = portals[1]
            far_portal = portals[0]
        
        
        # TODO: Done
        nearest_diamond_with_base = getNearestDiamondWithBase(board_bot.position, diamonds, my_base_pos)

        if(board_bot.properties.milliseconds_left <10000 and props.diamonds > 0):
            print("1")
            self.goal_position = my_base_pos
        elif props.diamonds == 5:
            # Move to base
            print("2")
            self.goal_position = my_base_pos
            # Jika jara kdiamond lebih jauh daripada red 
        elif(getDistanceBetween(board_bot.position, nearest_diamond_with_base) > getDistanceBetween(board_bot.position, red_button)):
            print("3")
            self.goal_position = red_button
        elif(getDistanceBetween(board_bot.position, nearest_diamond_with_base) > getDistanceBetween(board_bot.position, my_base_pos) and isSearah(board_bot.position, nearest_diamond_with_base, my_base_pos) and props.diamonds > 2):
            print("4")
            self.goal_position = my_base_pos
        else:
            nearest_diamond = getNearestDiamond(board_bot.position, diamonds)
            if(getDistanceBetween(board_bot.position, nearest_diamond) <=2):
                self.goal_position = nearest_diamond
            else:
                self.goal_position = nearest_diamond_with_base


        if(getDistanceWithPortalRelBase(board_bot.position, near_portal, far_portal, self.goal_position, my_base_pos) < getDistanceBetween(board_bot.position, self.goal_position)+getDistanceBetween(self.goal_position, my_base_pos)):
            self.goal_position = near_portal
        
        current_position = board_bot.position
        if self.goal_position:
            delta_x, delta_y = get_direction_v2(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y
            )
            
            curplusportal = Position(x=current_position.x+delta_x,y=current_position.y+delta_y)
            
            if(self.goal_position != near_portal and curplusportal==near_portal):
                print("dodge portal")
                self.goal_position = dodge_tele(current_position, near_portal, far_portal, self.goal_position)
                delta_x,delta_y = get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
            
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

# TODO: DONE
def getDistanceBetween (curr_pos:Position, target_pos:Position) -> int:
        return abs(curr_pos.x - target_pos.x) + abs(curr_pos.y - target_pos.y)
# TODO: DONE
def getNearestObjectPosition(curr_pos:Position, target_pos: List[Position]) -> Position:
        nearest = None
        nearest_distance = float('inf')
        for obj in target_pos:
            distance = getDistanceBetween(curr_pos, obj)
            if distance < nearest_distance:
                nearest = obj
                nearest_distance = distance
        return nearest
# TODO: DONE
def getNearestDiamond(curr_po :Position, diamonds : List[Position]) -> Position:
    min_distance = 100000
    nearest_diamond = None
    for diamond in diamonds:
        distance = getDistanceBetween(curr_po, diamond)
        if(distance < min_distance):
            min_distance = distance
            nearest_diamond = diamond
    return nearest_diamond

# Todo: Done
def getNearestDiamondWithBase(curr_pos: Position, diamonds: List[Position], base_pos: Position) -> Position:
    min_distance = float('inf')
    nearest_diamond = None
    for diamond in diamonds:
       
        if(len(diamonds)>=3):
            diamond_list = [d for d in diamonds if d != diamond]
            distance = (
                getDistanceBetween(curr_pos, diamond) +
                getDistanceBetween(diamond, base_pos) +
                getDistanceBetween(diamond, getNearestObjectPosition(diamond, diamond_list))
            )
        else:
             distance = (
                getDistanceBetween(curr_pos, diamond) +
                getDistanceBetween(diamond, base_pos) )
        if distance < min_distance:
            min_distance = distance
            nearest_diamond = diamond
    return nearest_diamond

#TODO: Done
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

#TODO : Done
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

def dodge_tele(curr_po:Position, near_tele:Position, far_tele:Position, goal_po:Position) -> Position:       # Cara pake: if (langkah selanjutnya ke portal) then jalanin fungsi dodge_tele
    # Mendapatkan delta_x dan delta_y dari curr_po ke goal_po
    delta_x = goal_po.x - curr_po.x
    delta_y = goal_po.y - curr_po.y

    if curr_po.y == goal_po.y:                                                                                                          #
        if curr_po.y + 1 == far_tele.y or curr_po.y - 1 == far_tele.y:                                                                  #
            return Position(x = curr_po.x, y = curr_po.y + 1 if curr_po.y + 1 == far_tele.y else curr_po.y - 1)                         #
        return Position(x = curr_po.x, y = curr_po.y + 1 if curr_po.y + 1 < 15 else curr_po.y - 1)      # 15 adalah batas board         #   Ini kondisi saat curr_po segaris sama goal_po
    elif curr_po.x == goal_po.x:                                                                                                        #
        if curr_po.x + 1 == far_tele.x or curr_po.x - 1 == far_tele.x:                                                                  #
            return Position(x = curr_po.x + 1 if curr_po.x + 1 == far_tele.x else curr_po.x - 1, y = curr_po.y)                         #
        return Position(x = curr_po.x + 1 if curr_po.x + 1 < 15 else curr_po.x - 1, y = curr_po.y)       # 15 adalah batas board        #
        
    elif curr_po.y == near_tele.y:      # curr_po satu horisontal dengan near_tele                                                      #
        return Position(x = curr_po.x, y = curr_po.y +  1 if delta_y > 0 else curr_po.y - 1)                                            #   Ini kondisi saat curr_po tidak segaris sama goal_po
    elif curr_po.x == near_tele.x:      # curr_po satu vertikal dengan near_tele                                                        #
        return Position(x = curr_po.x + 1 if delta_x > 0 else curr_po.x - 1, y = curr_po.y)                                             #   
    
    else:               # Kalo ga masuk ke kondisi itu, return goal_po aja (ga ngerubah goal_po yg sebelumnya)
        return goal_po