from game.alucard.processor.processor import Processor
from game.models import GameObject, Board
from game.models import Position
from game.alucard.processor.diamond_processor import DiamondProcessor
from game.alucard.processor.teleport_processor import TeleportProcessor
from typing import List
from game.alucard.service.math_services import MathService
from game.alucard.service.object_services import ObjectServices
from game.alucard.processor.red_processor import RedProcessor
from game.util import position_equals

class MainProcessor(Processor):
    # Current proses berisi string berupa teleport/diamond
    curr_process = None
    goal_position: Position
    teleports_position: List[Position] = []
    red_position: List[Position] = []
    teleport_threshold = 4
    red_threshold = 4

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)
        self.diamondProcessor = DiamondProcessor(self.bot, self.board)
        self.teleportProcessor = TeleportProcessor(self.bot, self.board)
        self.redProcessor = RedProcessor(self.bot, self.board)

    def process(self):
        if not self.teleports_position:
            self.teleports_position = [obj.position for obj in ObjectServices.teleport(self.board.game_objects)]
        if not self.red_position:
            self.red_position = [obj.position for obj in ObjectServices.red_button(self.board.game_objects)]

        
        # if teleport in the area of bot, then process teleport
        if MathService.isObjectInArea(self.bot.position, self.teleports_position, self.teleport_threshold):
            self.curr_process = "teleport"
        elif self.bot.properties.milliseconds_left <= 7000 and MathService.isObjectInArea(self.bot.position, self.red_position, self.red_threshold) and self.redProcessor.minimum:
            self.curr_process = "red"
        else:
            self.curr_process = "diamond"
            
        if self.curr_process == "teleport":
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
