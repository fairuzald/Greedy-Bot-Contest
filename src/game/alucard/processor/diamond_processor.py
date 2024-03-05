from game.alucard.processor.processor import Processor
from game.models import GameObject
from game.models import Position
from typing import List
from game.alucard.service.math_services import MathService

class DiamondProcessor(Processor):
    goal_position = None

    def __init__(self, bot: GameObject, width: int, height: int, diamond_position_list: List[Position]):
        super().__init__(bot)
        self.diamond_position_list = diamond_position_list
        self.width = width
        self.height = height
        self.mathService = MathService()  # Assuming MathService needs an instance

    def get_distance(self, pos1: Position, pos2: Position) -> float:
        # Calculate the Euclidean distance between two positions.
        return self.mathService.calculateDistance(pos1, pos2)

    def get_nearest_diamond(self) -> Position:
        #  Get the nearest diamond position to the bot.
        return self.mathService.getNearestObjectPosition(self.bot.position, self.diamond_position_list)

    def get_best_cluster_diamond(self) -> Position:
        # Get the diamond position from the cluster with the maximum number of diamonds.
        # Divides the board into four clusters and calculates the nearest diamond in each cluster.
        # Returns the position with the maximum number of diamonds.
        current_pos = self.bot.position

        cluster = [0] * 4
        nearest = [99999] * 4
        positions = [Position(0, 0)] * 4

        for diamond in self.diamond_position_list:
            # Determine the cluster based on diamond position
            if diamond.x < self.width / 2 and diamond.y < self.height / 2:
                index = 0
            elif diamond.x < self.width / 2 and diamond.y >= self.height / 2:
                index = 1
            elif diamond.x >= self.width / 2 and diamond.y < self.height / 2:
                index = 2
            else:
                index = 3

            # Update nearest position and increment cluster count
            if self.get_distance(current_pos, diamond) < nearest[index]:
                nearest[index] = self.get_distance(current_pos, diamond)
                positions[index] = diamond
            cluster[index] += 1

        # Return the position with the maximum number of diamonds in the cluster
        return positions[cluster.index(max(cluster))]

    def process(self):
        # Process method for the DiamondProcessor.
        self.goal_position = self.get_nearest_diamond()
