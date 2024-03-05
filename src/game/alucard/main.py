import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction
from game.alucard.processor.main_processor import MainProcessor
from game.alucard.processor.bot_processor import BotProcessor
import time
class AlucardGreedy(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        curr_bot = board_bot
        props = curr_bot.properties
        mainProcessor = MainProcessor(curr_bot,board)
        # start = time.time()
        
        # Analyze new state
        mainProcessor.process()
        self.goal_position = mainProcessor.goal_position
           
        current_position = curr_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        # end = time.time()
        # print("Time: ", (end - start) * 1000)
        return delta_x, delta_y
