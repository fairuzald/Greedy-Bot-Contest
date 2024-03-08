from game.alucard.processor.processor import Processor
from game.models import GameObject
from game.models import Position
from typing import List
from game.alucard.service.math_services import MathService
from game.alucard.service.math_services import MathService

class DiamondProcessor(Processor):
    goal_position = None

    def __init__(self, bot: GameObject, width: int, height: int, diamond_position_list: List[Position], red_button_position:Position):
        super().__init__(bot)
        self.diamond_position_list = diamond_position_list
        self.width = width
        self.height = height
        self.red_button_position = red_button_position

    def get_distance(self, pos1: Position, pos2: Position) -> float:
        # Calculate the Euclidean distance between two positions.
        return MathService.calculateDistance(pos1, pos2)

    def get_nearest_diamond(self) -> Position:
        #  Get the nearest diamond position to the bot.
        return MathService.getNearestObjectPosition(self.bot.position, self.diamond_position_list)
    
    def get_nearest_diamond_base(self) -> Position:
        min_distance = float('inf')
        nearest_diamond = None
        for diamond in self.diamond_position_list:
            if(len(self.diamond_position_list)>=3):
                diamond_list = [d for d in self.diamond_position_list if d != diamond]
                distance = (
                    MathService.getDistanceBetween(self.bot.position, diamond) +
                    MathService.getDistanceBetween(diamond, self.bot.properties.base) +
                    MathService.getDistanceBetween(diamond, MathService.getNearestObjectPosition(diamond, diamond_list))
                )
            else:
                distance = (
                    MathService.getDistanceBetween(self.bot.position, diamond) +
                    MathService.getDistanceBetween(diamond, self.bot.properties.base) )
            if distance < min_distance:
                min_distance = distance
                nearest_diamond = diamond
        return nearest_diamond


    def process(self):
        nearest_diamond_with_base = self.get_nearest_diamond_base()
        base_pos = self.bot.properties.base
        if(MathService.getDistanceBetween(self.bot.position, nearest_diamond_with_base) > MathService.getDistanceBetween(self.bot.position, self.red_button_position)):
            self.goal_position = self.red_button_position
        elif(MathService.getDistanceBetween(self.bot.position, nearest_diamond_with_base) > MathService.getDistanceBetween(self.bot.position, base_pos) and MathService.isSameDirection(self.bot.position, nearest_diamond_with_base, base_pos) and self.bot.properties.diamonds > 2):
            self.goal_position = base_pos
        else:
            nearest_diamond = self.get_nearest_diamond()
            if(MathService.getDistanceBetween(self.bot.position, nearest_diamond) <=2):
                self.goal_position = nearest_diamond
            else:
                self.goal_position = nearest_diamond_with_base

