from processor.processor import Processor
from game.models import GameObject, Board
from ..service.base_service import *

class BaseProcessor(Processor):
    # Nyala kalau inventory penuh
    status_base_processor = False 

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)

    def process(self):
        self.status_base_processor, temp_position = BaseService.is_base_same_direction(self.bot.position, self.goal_position)
        if self.status_base_processor:
            self.goal_position = temp_position
        elif self.bot.position == self.bot.properties.base:
            self.status_base_processor = False
        else:
            self.status_base_processor = False
            