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

class MainProcessor(Processor):
    # Current proses berisi string berupa teleport/diamond
    curr_process = None
    goal_position: Position
    teleport_threshold = 4
    red_threshold = 4
    bot_threshold = 2
    teleports_position: List[Position] = []
    red_position: List[Position] = []
    enemy_position: List[Position] = []

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)
        self.teleports_position = [obj.position for obj in ObjectServices.teleport(self.board.game_objects)]
        self.red_position = [obj.position for obj in ObjectServices.red_button(self.board.game_objects)]
        self.enemy_position = [obj.position for obj in ObjectServices.enemy(self.bot, self.board.game_objects)]
        self.base_position = self.bot.properties.base
        self.diamondProcessor = DiamondProcessor(self.bot, self.board)
        self.teleportProcessor = TeleportProcessor(self.bot, self.board)
        self.redProcessor = RedProcessor(self.bot, self.board)
        self.botProcessor = BotProcessor(self.bot, self.board, self.enemy_position)

    
    def process(self):
        is_enemy_near = MathService.isObjectInArea(self.bot.position, self.enemy_position, self.bot_threshold)
        if is_enemy_near:
            self.curr_process = "bot"
        elif self.bot.properties.diamonds==5:
            self.curr_process = "base"
        elif MathService.isObjectInArea(self.bot.position, self.teleports_position, self.bot_threshold):
            self.curr_process = "teleport"
        elif self.bot.properties.milliseconds_left <= 7000 and MathService.isObjectInArea(self.bot.position, self.red_position, self.red_threshold) and self.redProcessor.minimum:
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
            self.diamondProcessor.process()
            self.goal_position = self.diamondProcessor.goal_position
        
        print("Current Process: ", self.curr_process)
