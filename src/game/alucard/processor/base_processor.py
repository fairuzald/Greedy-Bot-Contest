from processor.processor import Processor
from game.models import GameObject, Board

class BaseProcessor(Processor):
    # Nyala kalau inventory penuh
    status_base_processor = False 

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)

    def process(self):
        print('FoodProcessor process')
