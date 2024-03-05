from processor.processor import Processor
from game.models import GameObject, Board
from ..service.base_service import *
from game.alucard.service.base_service import BaseService

class BaseProcessor(Processor):
    # Nyala kalau inventory penuh
    status_base_processor = False 

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)

    def process(self):
        self.status_base_processor, temp_position = BaseService.is_base_same_direction(self.bot.position, self.goal_position)
        if BaseService.is_go_home(self.bot.position):
            self.status_base_processor = True
            self.goal_position = self.bot.properties.base
        elif self.status_base_processor:
            self.goal_position = temp_position
        elif self.bot.position == self.bot.properties.base:
            self.status_base_processor = False
        else:
            self.status_base_processor = False
            