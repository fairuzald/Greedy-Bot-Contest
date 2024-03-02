from processor.processor import Processor
from game.models import GameObject, Board, Position

class BotProcessor(Processor):
    # Nyala kalau nyampe threshold
    status_bot_processor = False 
    
    # delta x + delta y
    threshold = 2

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)
        self.arr_position = [       # Semua kemungkinan posisi yang berada pada threshold
            Position(x=0, y=2),
            Position(x=1, y=1),
            Position(x=2, y=0),
            Position(x=1, y=-1),
            Position(x=0, y=-2),
            Position(x=-1, y=-1),
            Position(x=-2, y=0),
            Position(x=-1, y=1)
        ]

    def process(self):
        print('FoodProcessor process')
        # Check surroundings if there are any enemies within threshold
        # checked position (x,y): (0,2), (1,1), (2,0), (1,-1), (0,-2), (-1,-1), (-2,0), (-1,1)
        for pos in self.arr_position:
            if pos == self.bot.position:
                self.status_bot_processor = True
                break
            else:
                self.status_bot_processor = False
