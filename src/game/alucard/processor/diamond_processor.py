from game.alucard.processor.processor import Processor
from game.models import GameObject
from game.models import Position
from typing import List
from game.alucard.service.math_services import MathService

class DiamondProcessor(Processor):
    goal_position = None

    def __init__(self, bot: GameObject, width: int, height: int, diamond_position_list: List[Position], red_button_position: Position, diamonds: List[GameObject]):
        super().__init__(bot)
        self.diamond_position_list = diamond_position_list
        self.width = width
        self.height = height
        self.red_button_position = red_button_position
        self.diamonds = diamonds

