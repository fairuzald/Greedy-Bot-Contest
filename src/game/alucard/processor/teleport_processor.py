from game.alucard.processor.processor import Processor
from game.models import GameObject, Board, Position
from game.alucard.service.math_services import MathService
from game.alucard.service.object_services import ObjectServices
from game.alucard.processor.diamond_processor import DiamondProcessor
from game.util import position_equals,clamp

from typing import List


class TeleportProcessor(Processor):
    curr_process = "teleport"
    
    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)
        self.goal_position = None 
        self.isGoToTeleport = False
    
    def get_teleport_position_list(self) -> List[Position]:
        return [obj.position for obj in ObjectServices.teleport(self.board.game_objects)]
    
    def get_nearest_teleport(self) -> Position:
        return MathService.getNearestObjectPosition(self.bot.position, self.get_teleport_position_list())
    
    def get_nearest_diamond_by_teleport(self) -> Position:
        diamonds = ObjectServices.diamonds(self.board.game_objects)
        use_teleport = False
        minimum_distance = float('inf')
        for diamond in diamonds:
            distance = MathService.getDistanceBetween(self.bot.position, diamond.position)
            distance_use_teleport = MathService.getDistanceBetweenTransition(self.bot.position, self.get_nearest_teleport(), diamond.position)
            # Bandingkan jarak yang ditempuh dengan teleport dan tidak
            if(distance_use_teleport < distance):
                if(distance_use_teleport < minimum_distance):
                    minimum_distance = distance_use_teleport
                    use_teleport = True
            else:
                if(distance < minimum_distance):
                    minimum_distance = distance
                    use_teleport = False
        return use_teleport
    
    def process(self):
        status_teleport = self.get_nearest_diamond_by_teleport()
        if(status_teleport==False):
            self.curr_process = "diamond"
        else:
            self.goal_position = self.get_nearest_teleport()
            if(position_equals(self.bot.position, self.goal_position)):
                self.curr_process = "diamond"
            else:
                self.curr_process = "teleport"
        
    
    def get_direction_v2(self,current_x, current_y, dest_x, dest_y):
            delta_x = clamp(dest_x - current_x, -1, 1)
            delta_y = clamp(dest_y - current_y, -1, 1)
            
            
            portalPos = self.get_nearest_teleport()
            
            if (current_x+delta_x==portalPos.x and current_y==portalPos.y):
                return (0, delta_y)
            
            elif(current_y+delta_y==portalPos.y and current_x==portalPos.x):
                return (delta_x, 0)
            else:
                # make it like random using mod but only 1 step
                if(delta_x == 0 or delta_y == 0):
                    return(delta_x, delta_y)
                else:
                    if(current_x%2==1):
                        return(delta_x, 0)
                    else:
                        return(0, delta_y)