from abc import ABC, abstractmethod
from typing import List, Dict
from game.models import GameObject, Board

class Processor(ABC):
    bot: GameObject
    board: Board
    processed: bool
    
    def __init__(self, bot: GameObject, board: Board):
        self.bot = bot
        self.board = board
        self.processed = False

    def run(self):
        self.process()
        
    @abstractmethod
    def process(self):
        raise NotImplementedError()
        pass
