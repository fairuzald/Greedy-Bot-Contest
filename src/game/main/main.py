import random
from typing import Optional, List, Tuple
from game.logic.base import BaseLogic
from game.service.teleport_services import TeleportService
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals

class AlucardGreedy(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.logic = False
    
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        bot_position = board_bot.position
        teleport = board.teleport
        diamonds = board.diamonds
        service = TeleportService()
        nearest_teleport = service.get_nearest_teleport(bot_position, teleport)
        tel_nearest =service.get_nearest_diamond_by_teleport(bot_position, diamonds, teleport)
        if self.logic == False:
            self.logic = True
            self.goal_position = tel_nearest

    
        print(f"Nearest teleport: {tel_nearest}")
        # Analyze new state
        
        # if props.diamonds == 5:
        #     # Move to base
        #     base = board_bot.properties.base
        #     self.goal_position = base
        # else:
        #     # Just roam around
        #     self.goal_position = None

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
            print(f"Moving to {self.goal_position} delta {delta_x} {delta_y}")
            if(position_equals(current_position, self.goal_position) ):
                self.goal_position = None
                self.logic = False
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        return delta_x, delta_y
