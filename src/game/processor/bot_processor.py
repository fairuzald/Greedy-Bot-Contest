from processor.processor import Processor
from game.models import GameObject, Board, Position
from game.service.object_services import ObjectServices
from game.service.math_services import MathService
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

    def bot_process(self):
        # Check surroundings if there are any enemies within threshold
        # checked position of bot (x,y): (0,2), (1,1), (2,0), (1,-1), (0,-2), (-1,-1), (-2,0), (-1,1)
        # for pos in self.arr_position:
        #     for bot in self.board.bots:
        #         if pos == bot.position:
        #             self.status_bot_processor = True
        #             break
        #         else:
        #             self.status_bot_processor = False
        enemies_position = [en.position for en in ObjectServices.enemy(self.bot, self.board.game_objects)]
        is_enemy_near = MathService.isObjectInArea(self.bot.position, enemies_position, self.threshold)
        print("Is enemy near: ", is_enemy_near)
        
        
