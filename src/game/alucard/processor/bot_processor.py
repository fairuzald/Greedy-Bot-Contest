from game.alucard.processor.processor import Processor
from game.models import GameObject, Board, Position
from game.alucard.service.object_services import ObjectServices
from game.alucard.service.math_services import MathService
from game.alucard.service.bot_service import BaseService

class BotProcessor(Processor):
    # Nyala kalau nyampe threshold
    status_bot_processor = False 
    
    # delta x + delta y
    threshold = 2

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)
        self.arr_position = [       # Semua kemungkinan posisi yang berada pada threshold
            Position(x=0 + bot.position.x, y=2 + bot.position.y),
            Position(x=1 + bot.position.x , y=1 + bot.position.y),
            Position(x=2 + bot.position.x, y=0 + bot.position.y),
            Position(x=1 + bot.position.x, y=-1 + bot.position.y),
            Position(x=0 + bot.position.x, y=-2 + bot.position.y),
            Position(x=-1 + bot.position.x, y=-1 + bot.position.y),
            Position(x=-2 + bot.position.x, y=0 + bot.position.y),
            Position(x=-1 + bot.position.x, y=1 + bot.position.y)
        ]
        self.goal_position = None

    def process(self):
        enemies_position = [en.position for en in ObjectServices.enemy(self.bot, self.board.game_objects)]
        is_enemy_near = MathService.isObjectInArea(self.bot.position, enemies_position, self.threshold)

        if is_enemy_near:
            # Kabur
            self.goal_position = BaseService.tujuan_kabur(self, self.bot.position, enemies_position)
            
        
        
