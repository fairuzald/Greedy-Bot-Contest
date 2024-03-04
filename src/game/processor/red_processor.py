from game.processor.processor import Processor
from game.models import GameObject, Board
from game.service.object_services import ObjectServices
from game.service.math_services import MathService
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
    
    # Jika bot kita lebih rendah dari yang lain, maka arahkan bot kita ke red button
    def process(self):
        red_position = ObjectServices.red_button(self.board.game_objects)[0].position
        requirement1 = self.bot.properties.milliseconds_left <= 7000
        requirement2 = MathService.getDistanceBetween(self.bot.position, red_position) <=4
        if(requirement1 and requirement2  and self.minimum):
            self.goal_position =  red_position
