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
from game.util import clamp
from game.util import position_equals
import random
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
    delta_x: int
    delta_y: int
    
    def __init__(self, bot: GameObject, board: Board):
        self.bot = bot
        self.board = board
        self.teleports_position = []
        self.red_position = []
        self.enemy_position = []
        self.diamond_positions = []
        self.enemies =[]

        self.base_position = self.bot.properties.base
        
        for obj in self.board.game_objects:
            if(obj.type == "DiamondGameObject"):
                if(self.bot.properties.diamonds >= 4 and obj.properties.points == 2 ):
                    pass
                else:
                    self.diamond_positions.append(obj.position)
            elif(obj.type == "TeleportGameObject"):
                self.teleports_position.append(obj.position)
            elif(obj.type == "BotGameObject"):
                if(bot.properties.name != obj.properties.name):
                    self.enemy_position.append(obj.position)
            elif(obj.type == "DiamondButtonGameObject"):
                self.red_position.append(obj.position)
    
        self.diamondProcessor = DiamondProcessor(self.bot, self.board.width, self.board.height, self.diamond_positions, self.red_position[0])
        self.teleportProcessor = TeleportProcessor(self.bot, self.teleports_position, self.diamond_positions)
        self.redProcessor = RedProcessor(self.bot, self.enemies)
        self.botProcessor = BotProcessor(self.bot, self.diamond_positions, self.enemy_position, self.bot_threshold)
    
        
    def getDistanceWithPortalRelBase(self) -> int:
        return (MathService.getDistanceBetween(self.bot.position, self.teleports_position[0]) + MathService.getDistanceBetween(self.teleports_position[1], self.goal_position) + 
                min(MathService.getDistanceBetween(self.goal_position, self.base_position), MathService.getDistanceBetween(self.goal_position, self.teleports_position[1]) + 
                    MathService.getDistanceBetween(self.teleports_position[0],self.base_position)))
    
    def get_direction_v2(self,current_x, current_y, dest_x, dest_y):
            delta_x = clamp(dest_x - current_x, -1, 1)
            delta_y = clamp(dest_y - current_y, -1, 1)
            
            if(delta_x == 0 or delta_y == 0):
                return(delta_x, delta_y)
            else:
                if(current_x%2==1):
                    return(delta_x, 0)
                else:
                    return(0, delta_y)
    
    def process(self):
        # is_enemy_near = MathService.isObjectInArea(self.bot.position, self.enemy_position, self.bot_threshold)
        # if is_enemy_near:
        #     self.curr_process = "bot"
        if(MathService.getDistanceBetween(self.bot.position, self.teleports_position[0])  >= MathService.getDistanceBetween(self.bot.position, self.teleports_position[1])):
            self.teleports_position[0], self.teleports_position[1] = self.teleports_position[1], self.teleports_position[0]
        
        if MathService.isObjectInArea(self.bot.position, self.teleports_position, self.bot_threshold):
            self.curr_process = "teleport"
        elif self.bot.properties.milliseconds_left <= 7000 and MathService.isObjectInArea(self.bot.position, self.red_position, self.red_threshold) and self.redProcessor.is_bot_score_lower_than_enemies:
            self.curr_process = "red"
        else:
            self.curr_process = "diamond"
        
        if (self.bot.properties.milliseconds_left < 10000 and self.bot.properties.diamonds > 0):
            self.goal_position = self.base_position
        elif self.bot.properties.diamonds ==5:
            self.goal_position = self.base_position
        # elif self.curr_process == "bot":
        #     self.botProcessor.process()
        #     self.goal_position = self.botProcessor.goal_position
        # elif self.curr_process == "base":
        #     self.goal_position = self.base_position
        # elif self.curr_process == "teleport":
        #     self.teleportProcessor.process()
        #     self.goal_position = self.teleportProcessor.goal_position
        #     self.curr_process = self.teleportProcessor.curr_process
        # elif self.curr_process == "red":
        #     self.goal_position = self.red_position[0]
        #     if position_equals(self.bot.position, self.red_position[0]):
        #         self.curr_process = "diamond"
        else:
            self.diamondProcessor.process()
            self.goal_position = self.diamondProcessor.goal_position
            
        if(self.getDistanceWithPortalRelBase() < MathService.getDistanceBetween(self.bot.position, self.goal_position)+
           MathService.getDistanceBetween(self.goal_position, self.base_position)):
            self.goal_position = self.teleports_position[0]
      
        if self.goal_position:
            delta_x, delta_y = self.get_direction_v2(
                self.bot.position.x,
                self.bot.position.y,
                self.goal_position.x,
                self.goal_position.y
            )
            
            # curplusportal = Position(x=current_position.x+delta_x,y=current_position.y+delta_y)
            
            # if(self.goal_position != near_portal and curplusportal==near_portal):
            #     print("dodge portal")
            #     self.goal_position = dodge_tele(current_position, near_portal, far_portal, self.goal_position)
            #     delta_x,delta_y = get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
            
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        self.delta_x = delta_x
        self.delta_y = delta_y