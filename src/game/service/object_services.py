from game.models import GameObject, Board, Position, Bot
from typing import List, Optional

class ObjectServices: 
    @staticmethod
    def bots(game_objects:List[GameObject]) -> List[GameObject]:
        return [d for d in game_objects if d.type == "BotGameObject"]
    
    @staticmethod
    def enemy(bot:Bot, game_objects:List[GameObject]) -> List[GameObject]:
        return [d for d in game_objects if d.type == "BotGameObject" and d.properties.name != bot.properties.name]
       
    @staticmethod
    def teleport(game_objects:List[GameObject]) -> List[GameObject]:
        return [d for d in game_objects if d.type == "TeleportGameObject"]

    @staticmethod
    def diamonds(game_objects:List[GameObject]) -> List[GameObject]:
        return [d for d in game_objects if d.type == "DiamondGameObject"]
    
    @staticmethod
    def red_button(game_objects:List[GameObject]) -> List[GameObject]:
        return [d for d in game_objects if d.type == "DiamondButtonGameObject"]
    
    