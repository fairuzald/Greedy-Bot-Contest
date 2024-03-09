from game.models import GameObject, Board
from game.models import Position
from game.alucard.processor.diamond_processor import DiamondProcessor
from typing import List
from game.alucard.service.math_services import MathService
from game.alucard.processor.red_processor import RedProcessor
from game.alucard.processor.bot_processor import BotProcessor
from game.util import clamp
from game.util import position_equals
import random
class MainProcessor():
    # Current proses berisi string berupa teleport/diamond
    curr_process = None
    goal_position: Position
    teleport_threshold = 4
    red_threshold = 4
    bot_threshold = 1
    teleports_position: List[Position] = []
    red_position: List[Position] = []
    enemy_position: List[Position] = []
    base_position: Position
    delta_x: int
    delta_y: int
    
    def __init__(self, bot: GameObject, board: Board):
        # Initialize instance variables to store information about game objects and positions.
        self.bot = bot
        self.board = board
        self.teleports_position = []
        self.red_position = []
        self.enemy_position = []
        self.diamond_positions = []
        self.enemies = []
        self.diamonds = []

        # Store the base position of the bot.
        self.base_position = self.bot.properties.base

        # Iterate through the game objects on the board and categorize them based on their type.
        for obj in self.board.game_objects:
            if obj.type == "DiamondGameObject":
                # Exclude certain diamonds based on conditions.
                if self.bot.properties.diamonds >= 4 and obj.properties.points == 2:
                    pass
                else:
                    self.diamonds.append(obj)
                    self.diamond_positions.append(obj.position)
            elif obj.type == "TeleportGameObject":
                self.teleports_position.append(obj.position)
            elif obj.type == "BotGameObject":
                # Store the positions of enemy bots.
                if bot.properties.name != obj.properties.name:
                    self.enemy_position.append(obj.position)
            elif obj.type == "DiamondButtonGameObject":
                # Store the positions of red diamond buttons.
                self.red_position.append(obj.position)

        # Initialize instances of different processors for handling diamonds, red buttons, and enemy bots.
        self.diamondProcessor = DiamondProcessor(self.bot, self.board.width, self.board.height, self.diamond_positions, self.red_position[0], self.diamonds)
        self.redProcessor = RedProcessor(self.bot, self.enemies)
        self.botProcessor = BotProcessor(self.bot, self.diamond_positions, self.enemy_position, self.bot_threshold)
    
    # Calculate the total distance from the bot's position to the goal position using portals and base.
    def getDistanceWithPortalRelBase(self) -> int:
        return (MathService.getDistanceBetween(self.bot.position, self.teleports_position[0]) +
                MathService.getDistanceBetween(self.teleports_position[1], self.goal_position) +
                min(MathService.getDistanceBetween(self.goal_position, self.base_position),
                    MathService.getDistanceBetween(self.goal_position, self.teleports_position[1]) +
                    MathService.getDistanceBetween(self.teleports_position[0], self.base_position)))

    # Calculate the direction (delta_x, delta_y) from the current position to the destination position.
    def get_direction_v2(self, current_x, current_y, dest_x, dest_y):
        delta_x = clamp(dest_x - current_x, -1, 1)
        delta_y = clamp(dest_y - current_y, -1, 1)

        # Ensure the bot moves either horizontally or vertically.
        if delta_x == 0 or delta_y == 0:
            return delta_x, delta_y
        else:
            # Adjust movement to follow the grid pattern.
            if current_x % 2 == 1:
                return delta_x, 0
            else:
                return 0, delta_y
                
       # Function to dodge a teleport when moving towards a goal position.
    def dodge_tele(self, curr_po: Position, near_tele: Position, far_tele: Position, goal_po: Position) -> Position:
        # Calculate the delta_x and delta_y from the current position to the goal position.
        delta_x = goal_po.x - curr_po.x
        delta_y = goal_po.y - curr_po.y

        # Conditions for handling movement when the current position is in the same line as the goal position.
        if curr_po.y == goal_po.y:
            if curr_po.y + 1 == far_tele.y or curr_po.y - 1 == far_tele.y:
                return Position(x=curr_po.x, y=curr_po.y + 1 if curr_po.y + 1 == far_tele.y else curr_po.y - 1)
            return Position(x=curr_po.x, y=curr_po.y + 1 if curr_po.y + 1 < 15 else curr_po.y - 1)

        elif curr_po.x == goal_po.x:
            if curr_po.x + 1 == far_tele.x or curr_po.x - 1 == far_tele.x:
                return Position(x=curr_po.x + 1 if curr_po.x + 1 == far_tele.x else curr_po.x - 1, y=curr_po.y)
            return Position(x=curr_po.x + 1 if curr_po.x + 1 < 15 else curr_po.x - 1, y=curr_po.y)

        # Conditions for handling movement when the current position is not in the same line as the goal position.
        elif curr_po.y == near_tele.y:
            return Position(x=curr_po.x, y=curr_po.y + 1 if delta_y > 0 else curr_po.y - 1)

        elif curr_po.x == near_tele.x:
            return Position(x=curr_po.x + 1 if delta_x > 0 else curr_po.x - 1, y=curr_po.y)

        else:
            # If none of the conditions are met, return the goal position without modification.
            return goal_po

    # Main processing method for the bot's decision-making logic.
    def process(self):
        # Check if an enemy is nearby.
        # is_enemy_near = MathService.isObjectInArea(self.bot.position, self.enemy_position, self.bot_threshold)

        # Swap teleport positions based on distance.
        if MathService.getDistanceBetween(self.bot.position, self.teleports_position[0]) >= MathService.getDistanceBetween(self.bot.position, self.teleports_position[1]):
            self.teleports_position[0], self.teleports_position[1] = self.teleports_position[1], self.teleports_position[0]

        # Set the goal position based on various conditions.
        if (self.bot.properties.milliseconds_left < 10000 and self.bot.properties.diamonds > 0) or self.bot.properties.diamonds == 5:
            self.goal_position = self.base_position
        # elif self.bot.properties.milliseconds_left <= 7000 and MathService.isObjectInArea(self.bot.position, self.red_position, self.red_threshold) and self.redProcessor.is_bot_score_lower_than_enemies:
        #     self.goal_position = self.red_position[0]
        else:
            # Process the diamond logic.
            self.diamondProcessor.process()
            self.goal_position = self.diamondProcessor.goal_position

        # Adjust goal position based on teleport locations.
        if self.getDistanceWithPortalRelBase() < MathService.getDistanceBetween(self.bot.position, self.goal_position) + MathService.getDistanceBetween(self.goal_position, self.base_position):
            self.goal_position = self.teleports_position[0]

        if self.goal_position:
            # Calculate the direction based on the current and goal positions.
            delta_x, delta_y = self.get_direction_v2(
                self.bot.position.x,
                self.bot.position.y,
                self.goal_position.x,
                self.goal_position.y
            )

            # Check for teleport dodging conditions and update the goal position if necessary.
            curplusportal = Position(x=self.bot.position.x + delta_x, y=self.bot.position.y + delta_y)
            if self.goal_position != self.teleports_position[0] and curplusportal == self.teleports_position[0]:
                print("dodge portal")
                self.goal_position = self.dodge_tele(self.bot.position, self.teleports_position[0], self.teleports_position[1], self.goal_position)
                delta_x, delta_y = self.get_direction_v2(self.bot.position.x, self.bot.position.y, self.goal_position.x, self.goal_position.y)
        else:
            # Roam around if no specific goal position is set.
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(self.directions)

        # Store the calculated delta_x and delta_y for movement.
        self.delta_x = delta_x
        self.delta_y = delta_y
