from game.processor.processor import Processor
from game.models import GameObject, Board
from game.models import Position
from typing import List
from game.service.math_services import MathService
from game.service.object_services import ObjectServices
class DiamondProcessor(Processor):
    # priority 1 nyari diamond nyala kalau yang lain ga nyalla
    status_diamond_processor = False
    # priority 2 nyari diamond nyala sambil lari dari musuh, dinyalain kalau musuh masuk threshold bot
    status_diamond_processor2 = False
    goal_position = None

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)

    def get_diamond_position_list(self) -> List[Position]:
        diamond_list = [position.position for position in ObjectServices.diamonds(self.board.game_objects)]
        return diamond_list
                
    def get_nearest_diamond(self) -> Position:
        return self.mathService.getNearestObjectPosition(self.bot.position, self.get_diamond_position_list())
    
    def get_best_cluster_diamond(self) -> List[int]:
        width = self.board.width
        height = self.board.height
        current_pos = self.bot.position
        
        cluster = [0] * 4
        nearest = [99999] * 4
        positions = [Position(0,0)] * 4
        diamonds = self.get_diamond_position_list(self.board)
        
        for diamond in diamonds:
            if diamond.x < width/2 and diamond.y < height/2:
                if(self.get_distance(current_pos,diamond) < nearest[0]):
                    nearest[0] = self.get_distance(current_pos,diamond)
                    positions[0] = diamond
                cluster[0] += 1
            elif diamond.x < width/2 and diamond.y >= height/2:
                if(self.get_distance(current_pos,diamond) < nearest[1]):
                    nearest[1] = self.get_distance(current_pos,diamond)
                    positions[1] = diamond
                cluster[1] += 1
            elif diamond.x >= width/2 and diamond.y < height/2:
                if(self.get_distance(current_pos,diamond) < nearest[2]):
                    nearest[2] = self.get_distance(current_pos,diamond)
                    positions[2] = diamond
                
                cluster[2] += 1
            else:
                if(self.get_distance(current_pos,diamond) < nearest[3]):
                    nearest[3] = self.get_distance(current_pos,diamond)
                    positions[3] = diamond
                cluster[3] += 1
                
        return positions[cluster.index(max(cluster))]
    
    def process(self):
        mathService = MathService()
        self.goal_position = mathService.getNearestObjectPosition(self.bot.position, self.get_diamond_position_list())
