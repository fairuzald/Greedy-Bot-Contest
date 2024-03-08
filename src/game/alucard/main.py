import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from game.alucard.processor.main_processor import MainProcessor
from game.alucard.processor.bot_processor import BotProcessor
class AlucardGreedy(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        curr_bot = board_bot
        mainProcessor = MainProcessor(curr_bot,board)
        # start = time.time()
        
        # Analyze new state
        mainProcessor.process()
        self.goal_position = mainProcessor.goal_position
        delta_x = mainProcessor.delta_x
        delta_y = mainProcessor.delta_y
           
        return delta_x, delta_y
