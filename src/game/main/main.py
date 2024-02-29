import random
from typing import Optional, List
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class AlucardGreedy(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    def teleport_positions(self, teleport: List[GameObject]):
        position_array = [d.position for d in teleport]
        return position_array

    def get_distance_teleport_bot(self, bot: GameObject, teleport: List[GameObject]):
        array_dis = [(dis.x - bot.position.x, dis.y - bot.position.y) for dis in self.teleport_positions(teleport)]
        return array_dis

    def get_nearest_teleport(self, bot: GameObject, teleport: List[GameObject]):
        array_dis = self.get_distance_teleport_bot(bot, teleport)
        min_distance = float('inf')
        nearest_position = None

        for d in array_dis:
            x, y = d
            distance = abs(x - bot.position.x) + abs(y - bot.position.y)

            if distance < min_distance:
                min_distance = distance
                nearest_position = Position(x, y)

        return nearest_position
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        teleport = board.teleport
        nearest_teleport = self.get_nearest_teleport(board_bot, teleport)

        print(nearest_teleport)
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Just roam around
            self.goal_position = None

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
