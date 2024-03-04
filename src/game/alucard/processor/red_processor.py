from game.alucard.processor.processor import Processor
from game.models import GameObject, Board
from game.alucard.service.object_services import ObjectServices
from game.alucard.service.math_services import MathService
class RedProcessor(Processor):
    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)
        self.goal_position = None
    
    # Cek apakah skor bot kita sekarang lebih rendah dari pada bot yang lain
    @property
    def minimum(self):
        enemy = ObjectServices.enemy(self.bot, self.board.game_objects)
        if(len(enemy) == 0):
            return False
        minimum_score = float('inf')
        for e in enemy:
            if minimum_score < e.score:
                minimum_score = e.score
        return self.bot.score <= minimum_score
    
    def process(self):
        pass