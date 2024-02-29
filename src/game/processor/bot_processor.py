from processor.processor import Processor
from game.models import GameObject, Board

class BotProcessor(Processor):
    # Nyala kalau nyampe threshold
    status_bot_processor = False 
    
    # delta x + delta y
    threshold = 2

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)

    def process(self):
        print('FoodProcessor process')
