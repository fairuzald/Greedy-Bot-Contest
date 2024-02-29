from processor.processor import Processor
from game.models import GameObject, Board

class DiamondProcessor(Processor):
    # priority 1 nyari diamond nyala kalau yang lain ga nyalla
    status_diamond_processor = False
    
    # priority 2 nyari diamond nyala sambil lari dari musuh, dinyalain kalau musuh masuk threshold bot
    status_diamond_processor2 = False 

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)

    def process(self):
        print('FoodProcessor process')
