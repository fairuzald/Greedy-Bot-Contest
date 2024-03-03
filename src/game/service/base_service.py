from game.models import GameObject, Board, Position
from ..util import get_direction

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

        # Check if kuadran sama
        if delta_x_goal * delta_x_base >= 0 and delta_y_goal * delta_y_base >= 0:
            # Checks if the base is in the same direction as the goal
            if abs(delta_x_goal) >= abs(delta_x_base) and abs(delta_y_goal) >= abs(delta_y_base):
                return (True, self.bot.properties.base)     # Menghasilkan benar dan posisi base sebagai goal position yang baru
            
        return (False, None)    # Menghasilkan false dan none