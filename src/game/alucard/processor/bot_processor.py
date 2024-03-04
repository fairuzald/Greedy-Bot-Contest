from processor.processor import Processor
from game.models import GameObject, Board, Position
from game.alucard.service.object_services import ObjectServices
from game.alucard.service.math_services import MathService
from service.bot_service import BaseService

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

        # Mencari posisi musuh yang ada di sekitar bot
        existence_enemy = [False, False, False, False, False, False, False, False]
        #                  (0,2), (1,1), (2,0),(1,-1),(0,-2),(-1,-1),(-2,0),(-1,1)
        for i in range(8):
            for en_position in enemies_position:
                if self.arr_position[i] == en_position:
                    existence_enemy[i] = True
                    break


        if is_enemy_near:
            # Kabur
            self.goal_position = BaseService.tujuan_kabur(self, self.bot.position, enemies_position)
            
        
        
