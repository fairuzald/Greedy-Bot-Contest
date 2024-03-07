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

    def is_obj_same_direction(self, curr_pos: Position, obj_pos: Position, goal_pos: Position) -> tuple[bool, Position]:      # Position -> self.goal_position yang baru (yaitu Position base jika bool=True, dan none jika bool=False)
        delta_x_goal, delta_y_goal = self.get_delta(curr_pos, goal_pos)
        delta_x_obj, delta_y_obj = self.get_delta(curr_pos, obj_pos)         # TODO: Buat fungsi untuk mencari diamond mana aja yang searah dengan arah pulang (dipake di is go home), caranya buat looping dan ganti variabel goal_pos jadi pos_base nya dan self.bot.properties.base jadi posisi tiap diamond yg mau di cek (pake loop). Abis tu kekumpul list of diamond yang searah dgn arah base, dicari yang nearest yang mana, abistu ulang lagi proses dari awal

        # Kalo udah di base, langsung return false
        if curr_pos == obj_pos:
            return (False, None)
        
        # Check if kuadran sama
        if delta_x_goal * delta_x_obj >= 0 and delta_y_goal * delta_y_obj >= 0:
            # Checks if the base is in the same direction as the goal
            if abs(delta_x_goal) >= abs(delta_x_obj) and abs(delta_y_goal) >= abs(delta_y_obj):
                return (True, obj_pos)     # Menghasilkan benar dan posisi base sebagai goal position yang baru
            
        return (False, None)    # Menghasilkan false dan none
    
    def is_go_home (self, curr_pos: Position) -> bool:
        distance = MathService.getDistanceBetween(curr_pos, self.bot.properties.base)
        distance_use_teleport = MathService.getDistanceBetweenTransition(curr_pos, TeleportProcessor.get_nearest_teleport(), self.bot.properties.base)
        if (distance_use_teleport < distance and distance_use_teleport * 1000 == self.bot.properties.milliseconds_left):
            return True
        elif distance * 1000 == self.bot.properties.milliseconds_left:
            return True
        return False