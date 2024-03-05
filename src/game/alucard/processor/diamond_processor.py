from game.alucard.processor.processor import Processor
from game.models import GameObject, Board
from game.models import Position
from typing import List
from game.alucard.service.math_services import MathService
from game.alucard.service.object_services import ObjectServices
class DiamondProcessor(Processor):

    goal_position = None
    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)


    def get_diamond_position_list(self) -> List[Position]:
        diamond_list = [position.position for position in ObjectServices.diamonds(self.board.game_objects)]
        return diamond_list
                
    def get_nearest_diamond(self) -> Position:
        return self.mathService.getNearestObjectPosition(self.bot.position, self.get_diamond_position_list())
    
    def isOnMiddle(self,width,height,current_pos) -> bool:
        return (current_pos.x >= width/3 and current_pos.x <= 2*width/3 and current_pos.y >= height/3 and current_pos.y <= 2*height/3)

    
    def get_best_cluster_diamond(self) -> Position:
        width = self.board.width
        height = self.board.height
        current_pos = self.bot.position
        
        if (not self.isOnMiddle(width,height,current_pos)):
            return None
        
        cluster = [0] * 4
        nearest = [99999] * 4
        positions = [Position(0,0)] * 4
        diamonds = self.get_diamond_position_list()
        
        for diamond in diamonds:
            if diamond.x < width/2 and diamond.y < height/2:
                if(MathService.getDistanceBetween(current_pos,diamond) < nearest[0]):
                    nearest[0] = MathService.getDistanceBetween(current_pos,diamond)
                    positions[0] = diamond
                cluster[0] += 1
            elif diamond.x < width/2 and diamond.y >= height/2:
                if(MathService.getDistanceBetween(current_pos,diamond) < nearest[1]):
                    nearest[1] = MathService.getDistanceBetween(current_pos,diamond)
                    positions[1] = diamond
                cluster[1] += 1
            elif diamond.x >= width/2 and diamond.y < height/2:
                if(MathService.getDistanceBetween(current_pos,diamond) < nearest[2]):
                    nearest[2] = MathService.getDistanceBetween(current_pos,diamond)
                    positions[2] = diamond
                
                cluster[2] += 1
            else:
                if(MathService.getDistanceBetween(current_pos,diamond) < nearest[3]):
                    nearest[3] = MathService.getDistanceBetween(current_pos,diamond)
                    positions[3] = diamond
                cluster[3] += 1
                
        return positions[cluster.index(max(cluster))]
    
    def process(self):
        mathService = MathService()
        self.goal_position = mathService.getNearestObjectPosition(self.bot.position, self.get_diamond_position_list())
        
    def process_cluster(self):
        hasil = self.get_best_cluster_diamond()
        if(hasil==None):
            self.process()
        else:
            self.goal_position = hasil
    
