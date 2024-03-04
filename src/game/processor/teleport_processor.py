from game.processor.processor import Processor
from game.models import GameObject, Board, Position
from game.service.math_services import MathService
from game.service.object_services import ObjectServices
from game.processor.diamond_processor import DiamondProcessor
from typing import List

class TeleportProcessor(Processor):
    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)
        self.mathService = MathService()
        self.objectService = ObjectServices(self.board.game_objects)
        self.goal_position = None 
    
    def get_teleport_position_list(self) -> List[Position]:
        return [position.position for position in self.objectService.teleports]
    
    def get_nearest_teleport(self) -> Position:
        return self.mathService.getNearestObjectPosition(self.bot.position, self.get_teleport_position_list())
    
    def get_nearest_diamond_by_teleport(self) -> Position:
        # Assuming you have a get_diamond_position_list method in ObjectService
        diamonds_position = [d.position for d in self.objectService.diamonds]
        # diamondService = DiamondProcessor(self.bot, self.board)
        
        nearest = self.mathService.getNearestObjectPosition(self.get_nearest_teleport(), diamonds_position)
        return nearest
