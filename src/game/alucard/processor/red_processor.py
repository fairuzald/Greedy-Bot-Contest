from game.alucard.processor.processor import Processor
from game.models import GameObject
from typing import List

class RedProcessor(Processor):
    def __init__(self, bot: GameObject, enemies: List[GameObject]):
        super().__init__(bot)
        self.goal_position = None
        self.enemies = enemies
    
    @property
    def is_bot_score_lower_than_enemies(self) -> bool:
        # Check if the score of our bot is lower than any of the enemy bots.
        if not self.enemies:
            # If there are no enemies, return False
            return False
        
        minimum_score = float('inf')
        for enemy in self.enemies:
            if minimum_score < enemy.properties.score:
                minimum_score = enemy.properties.score
        
        # Return True if our bot's score is lower or equal to the minimum enemy score
        return self.bot.properties.score <= minimum_score
    
    def process(self):
        pass
