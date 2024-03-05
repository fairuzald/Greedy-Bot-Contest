from game.models import GameObject, Board, Position
from game.util import get_direction
from typing import List
from game.alucard.service.math_services import MathService
from game.alucard.service.object_services import ObjectServices


class BaseService:
    def __init__(self, bot: GameObject, board: Board):
        super().__init__()
        self.board = board
        self.bot = bot
