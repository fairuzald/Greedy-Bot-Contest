from game.alucard.processor.processor import Processor
from game.models import GameObject, Position
from game.alucard.service.object_services import ObjectServices
from game.alucard.service.math_services import MathService
from game.util import get_direction
from typing import List

class BotProcessor(Processor):

    def __init__(self, bot: GameObject, diamond_list_positions: List[Position], enemies_position: List[GameObject], threshold: int):
        super().__init__(bot)
        self.diamond_list_positions = diamond_list_positions
        self.threshold = threshold
        self.enemies_position = enemies_position
        self.goal_position = None

        # Generate a list of possible positions within the threshold
        self.arr_position = [
            Position(x=0 + bot.position.x, y=2 + bot.position.y),
            Position(x=1 + bot.position.x, y=1 + bot.position.y),
            Position(x=2 + bot.position.x, y=0 + bot.position.y),
            Position(x=1 + bot.position.x, y=-1 + bot.position.y),
            Position(x=0 + bot.position.x, y=-2 + bot.position.y),
            Position(x=-1 + bot.position.x, y=-1 + bot.position.y),
            Position(x=-2 + bot.position.x, y=0 + bot.position.y),
            Position(x=-1 + bot.position.x, y=1 + bot.position.y)
        ]

    def tujuan_kabur(self, goal_pos_awal: Position) -> Position:
        # Determine the escape position considering enemies and the nearest diamond.
        curr_pos = self.bot.position

        # Options for escape: right, left, up, down
        opsi_kabur = [Position(x=curr_pos.x, y=curr_pos.y + 1),
                      Position(x=curr_pos.x + 1, y=curr_pos.y),
                      Position(x=curr_pos.x, y=curr_pos.y - 1),
                      Position(x=curr_pos.x - 1, y=curr_pos.y)]

        # Remove escape options if enemies are in the area
        opsi_kabur = [opsi for opsi in opsi_kabur if not MathService.isObjectInArea(opsi, self.enemies_position, 2)]

        # Find the nearest diamond
        # nearest_diamond = MathService.getNearestObjectPosition(curr_pos, self.diamond_list_positions)

        # Get direction towards the nearest diamond
        x_to_goal_pos, y_to_goal_pos = get_direction(curr_pos.x, curr_pos.y, goal_pos_awal.x, goal_pos_awal.y)          # TODO: Ubah pake fungsi get direct v2 yang baru dari rehan

        if not opsi_kabur:
            # If no escape options, move towards the nearest diamond
            return Position(x=curr_pos.x + x_to_goal_pos, y=curr_pos.y + y_to_goal_pos)
        else:
            for opsi in opsi_kabur:
                xdes, ydes = get_direction(curr_pos.x, curr_pos.y, opsi.x, opsi.y)
                # If escape direction is the same as the direction towards the nearest diamond
                if xdes == x_to_goal_pos and ydes == y_to_goal_pos:
                    return opsi

            # Find an alternative escape target that aligns with the direction towards the nearest diamond
            if x_to_goal_pos == 0:  # Direction is up or down
                return next((opsi for opsi in opsi_kabur if opsi.x == curr_pos.x + 1 or opsi.x == curr_pos.x - 1), opsi_kabur[0])
            elif y_to_goal_pos == 0:  # Direction is left or right
                return next((opsi for opsi in opsi_kabur if opsi.y == curr_pos.y + 1 or opsi.y == curr_pos.y - 1), opsi_kabur[0])

            return Position(x=curr_pos.x + x_to_goal_pos, y=curr_pos.y + y_to_goal_pos)

    def process(self, goal_pos_awal: Position):
        # Process method for the BotProcessor.
        self.goal_position = self.tujuan_kabur(goal_pos_awal)
