from game.alucard.processor.processor import Processor
from game.models import GameObject, Position
from game.alucard.service.math_services import MathService
from game.alucard.service.object_services import ObjectServices
from game.alucard.processor.diamond_processor import DiamondProcessor
from game.util import position_equals

from typing import List

class TeleportProcessor(Processor):
    curr_process = "teleport"
    
    def __init__(self, bot: GameObject, teleport_positions: List[Position], diamond_positions: List[Position]):
        super().__init__(bot)
        self.teleport_positions = teleport_positions
        self.diamond_positions = diamond_positions
        self.goal_position = None 
        self.isGoToTeleport = False
        self.nearest_position_teleport = self.get_nearest_teleport
    
    @property
    def get_nearest_teleport(self) -> Position:
        # """Get the nearest teleport position to the bot."""
        return MathService.getNearestObjectPosition(self.bot.position, self.teleport_positions)
    
    def is_use_teleport_diamond(self) -> Position:
        # Check if using teleport to reach a diamond is more efficient than direct movement.
        # Returns True if teleport is more efficient, False otherwise.
        use_teleport = False
        minimum_distance = float('inf')
        
        for dm_pos in self.diamond_positions:
            distance = MathService.getDistanceBetween(self.bot.position, dm_pos)
            distance_use_teleport = MathService.getDistanceBetweenTransition(self.bot.position, self.nearest_position_teleport, dm_pos)
            
            # Compare the distance traveled with teleport and without teleport
            if distance_use_teleport < distance:
                if distance_use_teleport < minimum_distance:
                    minimum_distance = distance_use_teleport
                    use_teleport = True
            else:
                if distance < minimum_distance:
                    minimum_distance = distance
                    use_teleport = False
                    
        return use_teleport
    
    def process(self):
        # """Process method for the TeleportProcessor."""
        if not self.is_use_teleport_diamond():
            self.curr_process = "diamond"
        else:
            self.goal_position = self.nearest_position_teleport
            if position_equals(self.bot.position, self.goal_position):
                self.curr_process = "diamond"
            else:
                self.curr_process = "teleport"
