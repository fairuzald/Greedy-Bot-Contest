from game.alucard.processor.processor import Processor
from game.models import GameObject, Board
from game.models import Position
from game.alucard.processor.diamond_processor import DiamondProcessor
from game.alucard.processor.teleport_processor import TeleportProcessor
from typing import List
from game.alucard.service.math_services import MathService
from game.alucard.service.object_services import ObjectServices
from game.alucard.processor.red_processor import RedProcessor
from game.alucard.processor.bot_processor import BotProcessor
from game.util import position_equals

class MainProcessor():
    # Current proses berisi string berupa teleport/diamond
    curr_process = None
    goal_position: Position
    teleport_threshold = 4
    red_threshold = 4
    bot_threshold = 3
    teleports_position: List[Position] = []
    red_position: List[Position] = []
    enemy_position: List[Position] = []
    base_position: Position
    
    def __init__(self, bot: GameObject, board: Board):
        self.bot = bot
        self.board = board
        self.teleports_position = [obj.position for obj in ObjectServices.teleport(self.board.game_objects)]
        self.red_position = [obj.position for obj in ObjectServices.red_button(self.board.game_objects)]
        self.enemy_position = [obj.position for obj in self.get_enemies]
        self.diamond_positions = self.get_diamond_position_list
        self.base_position = self.bot.properties.base
        self.diamondProcessor = DiamondProcessor(self.bot, self.board.width, self.board.height, self.diamond_positions)
        self.teleportProcessor = TeleportProcessor(self.bot, self.teleports_position, self.diamond_positions)
        self.redProcessor = RedProcessor(self.bot, self.get_enemies)
        self.botProcessor = BotProcessor(self.bot, self.diamond_positions, self.enemy_position, self.bot_threshold)

    # Mendapatkan posisi diamond
    @property
    def get_diamond_position_list(self) -> List[Position]:
        diamonds = ObjectServices.diamonds(self.board.game_objects)
        dm1 = []
        dm2 = []
        for d in diamonds:
            if d.properties.points == 1:
                dm1.append(d.position)
            elif d.properties.points == 2:
                dm2.append(d.position)

        if self.bot.properties.diamonds == 4:
            return dm1
        else:
            # return concatenated dm1 and dm2
            return dm1 + dm2
    
    @property
    def get_enemies(self) -> List[Position]:
        return ObjectServices.enemy(self.bot, self.board.game_objects)
    
    def process(self):
        is_enemy_near = MathService.isObjectInArea(self.bot.position, self.enemy_position, self.bot_threshold)
        if is_enemy_near:
            self.curr_process = "bot"
        elif self.bot.properties.diamonds==5:
            self.curr_process = "base"
        elif MathService.isObjectInArea(self.bot.position, self.teleports_position, self.bot_threshold):
            self.curr_process = "teleport"
        elif self.bot.properties.milliseconds_left <= 7000 and MathService.isObjectInArea(self.bot.position, self.red_position, self.red_threshold) and self.redProcessor.is_bot_score_lower_than_enemies:
            self.curr_process = "red"
        else:
            self.curr_process = "diamond"
        
        if self.curr_process == "bot":
            self.botProcessor.process()
            self.goal_position = self.botProcessor.goal_position
        elif self.curr_process == "base":
            self.goal_position = self.base_position
        elif self.curr_process == "teleport":
            self.teleportProcessor.process()
            self.goal_position = self.teleportProcessor.goal_position
            self.curr_process = self.teleportProcessor.curr_process
        elif self.curr_process == "red":
            self.goal_position = self.red_position[0]
            if position_equals(self.bot.position, self.red_position[0]):
                self.curr_process = "diamond"
        else:
            self.goal_position = self.diamondProcessor.goal_position
            

        print("Current Process: ", self.curr_process)
