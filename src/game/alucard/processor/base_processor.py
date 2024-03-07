from processor.processor import Processor
from game.models import GameObject, Board, Position
from processor.teleport_processor import TeleportProcessor
from game.alucard.service.math_services import MathService
from typing import List


class BaseProcessor(Processor):
    # Nyala kalau inventory penuh
    # status_base_processor = False 

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)
    
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
    
    def is_go_home (self, bot_go_home: GameObject) -> bool:
        distance = MathService.getDistanceBetween(bot_go_home.position, bot_go_home.properties.base)
        distance_use_teleport = MathService.getDistanceBetweenTransition(bot_go_home.position, TeleportProcessor.get_nearest_teleport(), bot_go_home.properties.base)
        if (distance_use_teleport < distance and distance_use_teleport * 1000 == bot_go_home.properties.milliseconds_left):
            return True
        elif distance * 1000 == bot_go_home.properties.milliseconds_left:
            return True
        return False

    def process(self, diamond_positions: List[Position]):   # ini self nya nge rujuk ke main processor
        bool_base_searah, base_pos = self.is_obj_same_direction(self.bot.position, self.bot.properties.base, self.goal_position)
        if self.is_go_home(self.bot.position):
            # TODO
            # Buat list semua diamond yang searah dengan base
            diamonds_searah = [] # List of diamond position yang searah dengan base
            for diamond_pos in diamond_positions:
                bool_diamond_searah, pos = self.is_obj_same_direction(self.bot.position, diamond_pos, self.bot.properties.base)
                if bool_diamond_searah:
                    diamonds_searah.append(pos)

            # Dari list diamond, cari yang terdekat dengan bot, lalu set goal pos nya ke sana (setelah sampe, masuk lagi ke curr_process )
            if diamonds_searah:
                nearest_diamond = MathService.getNearestObjectPosition(self.bot.position, diamonds_searah)
                self.goal_position = nearest_diamond
            else:
                self.goal_position = self.bot.properties.base
            # self.status_base_processor = True
        elif bool_base_searah:
            self.goal_position = base_pos
        elif self.bot.properties.diamonds==5:
            # self.status_base_processor = False
            self.goal_position = self.bot.properties.base
            
        else:
            # self.status_base_processor = False
            print("masuk else base processor") # Ini cuman buat error detector ae (harusnya ga akan pernah masuk ke kondisi ini), kalo misalnya masuk ke else, berarti ada yang salah di kondisi sebelumnya (ada kondisi yang lost)