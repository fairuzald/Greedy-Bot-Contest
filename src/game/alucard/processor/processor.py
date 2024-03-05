from abc import ABC, abstractmethod
from game.models import GameObject

class Processor(ABC):
    bot: GameObject
    processed: bool
    
    def __init__(self, bot: GameObject):
        self.bot = bot
        self.processed = False

    def run(self):
        self.process()
        
    @abstractmethod
    def process(self):
        raise NotImplementedError()
