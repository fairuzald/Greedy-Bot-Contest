from game.processor.processor import Processor
from game.models import GameObject, Board
from game.models import Position
from game.processor.diamond_processor import DiamondProcessor
from game.processor.teleport_processor import TeleportProcessor
from typing import List
from game.service.math_services import MathService

class MainProcessor(Processor):
    goal_position: Position

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)

    def process(self):
        diamondProcessor = DiamondProcessor(self.bot, self.board)
        teleportProcessor = TeleportProcessor(self.bot, self.board)
        