from game.models import GameObject, Board, Position
from game.util import get_direction
from game.alucard.service.math_services import MathService
from game.alucard.processor.teleport_processor import TeleportProcessor

class BaseService:
    def __init__(self, bot: GameObject, board: Board):
        super().__init__()
        self.board = board
        self.bot = bot
    
    def get_delta(self, curr_pos: Position, dest_pos: Position) -> tuple[int, int]:
        delta_x = dest_pos.x - curr_pos.x
        delta_y = dest_pos.y - curr_pos.y
        return (delta_x, delta_y)

    def is_base_same_direction(self, curr_pos: Position, goal_pos: Position) -> tuple[bool, Position]:      # Position -> self.goal_position yang baru (yaitu Position base jika bool=True, dan none jika bool=False)
        delta_x_goal, delta_y_goal = self.get_delta(curr_pos, goal_pos)
        delta_x_base, delta_y_base = self.get_delta(curr_pos, self.bot.properties.base)

        # Kalo udah di base, langsung return false
        if curr_pos == self.bot.properties.base:
            return (False, None)
        
        # Check if kuadran sama
        if delta_x_goal * delta_x_base >= 0 and delta_y_goal * delta_y_base >= 0:
            # Checks if the base is in the same direction as the goal
            if abs(delta_x_goal) >= abs(delta_x_base) and abs(delta_y_goal) >= abs(delta_y_base):
                return (True, self.bot.properties.base)     # Menghasilkan benar dan posisi base sebagai goal position yang baru
            
        return (False, None)    # Menghasilkan false dan none
    
    def is_go_home (self, curr_pos: Position) -> bool:
        distance = MathService.getDistanceBetween(curr_pos, self.bot.properties.base)
        distance_use_teleport = MathService.getDistanceBetweenTransition(curr_pos, TeleportProcessor.get_nearest_teleport(), self.bot.properties.base)
        if (distance_use_teleport < distance and distance_use_teleport * 1000 == self.bot.properties.milliseconds_left):
            return True
        elif distance * 1000 == self.bot.properties.milliseconds_left:
            return True
        return False