from game.processor.processor import Processor
from game.models import GameObject, Board
from game.models import Position
from game.processor.diamond_processor import DiamondProcessor
from game.processor.teleport_processor import TeleportProcessor
from typing import List
from game.service.math_services import MathService
from game.service.object_services import ObjectServices
import time 
class MainProcessor(Processor):
    # Current proses berisi string berupa teleport/diamond
    curr_process = None
    goal_position: Position
    teleports_position: List[Position] = []
    teleport_threshold = 4

    def __init__(self, bot: GameObject, board: Board):
        super().__init__(bot, board)

    def process(self):
        diamondProcessor = DiamondProcessor(self.bot, self.board)
        teleportProcessor = TeleportProcessor(self.bot, self.board)
        if(self.teleports_position == []):
            self.teleports_position = [obj.position for obj in ObjectServices.teleport(self.board.game_objects)]
        # if teleport in area of bot, then process teleport
        if(MathService.isObjectInArea(self.bot.position,self.teleports_position,self.teleport_threshold)):
            self.curr_process = "teleport"
        else:
            self.curr_process = "diamond"
            
        if(self.curr_process == "teleport"):
            teleportProcessor.process()
            self.goal_position = teleportProcessor.goal_position
            self.curr_process = teleportProcessor.curr_process
        else:
            diamondProcessor.process()
            self.goal_position = diamondProcessor.goal_position
        print("Current Process: ", self.curr_process)
        