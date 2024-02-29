from processor.processor import Processor
from game.models import GameObject, Board

class Teleport(Processor):
    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)

    def process(self):
        print('FoodProcessor process')
