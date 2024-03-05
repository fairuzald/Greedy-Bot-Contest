from game.alucard.processor.processor import Processor
from game.models import GameObject, Board, Position
from game.alucard.service.object_services import ObjectServices
from game.alucard.service.math_services import MathService
from game.alucard.service.bot_service import BaseService
from game.util import get_direction
from typing import List
class BotProcessor(Processor):
    # Nyala kalau nyampe threshold
    status_bot_processor = False 
    # delta x + delta y
    threshold = 2

    def __init__(self, bot: GameObject, board: Board, enemies_position: List[GameObject]):
        super().__init__(bot, board)
        self.arr_position = [       # Semua kemungkinan posisi yang berada pada threshold
            Position(x=0 + bot.position.x, y=2 + bot.position.y),
            Position(x=1 + bot.position.x , y=1 + bot.position.y),
            Position(x=2 + bot.position.x, y=0 + bot.position.y),
            Position(x=1 + bot.position.x, y=-1 + bot.position.y),
            Position(x=0 + bot.position.x, y=-2 + bot.position.y),
            Position(x=-1 + bot.position.x, y=-1 + bot.position.y),
            Position(x=-2 + bot.position.x, y=0 + bot.position.y),
            Position(x=-1 + bot.position.x, y=1 + bot.position.y)
        ]
        self.enemies_position = enemies_position
        self.goal_position = None
        
    def tujuan_kabur(self, curr_pos: Position, enemies_position: List[GameObject]) -> Position:
          # Mencari arah kabur yang aman dan paling searah dengan diamond terdekat
        opsi_kabur = [Position(x=curr_pos.x, y=curr_pos.y+1), 
                      Position(x=curr_pos.x+1, y=curr_pos.y), 
                      Position(x=curr_pos.x, y=curr_pos.y-1), 
                      Position(x=curr_pos.x-1, y=curr_pos.y)]
        
        for opsi in opsi_kabur:
            if MathService.isObjectInArea(opsi, enemies_position, 1):
                opsi_kabur.remove(opsi)

        diamond_list = [diamond.position for diamond in ObjectServices.diamonds(self.board.game_objects)]
        tes = MathService.getNearestObjectPosition(curr_pos, diamond_list)
        x,yes = get_direction(curr_pos.x, curr_pos.y,tes.x, tes.y )

        if opsi_kabur == []:        # Pasrah (trobos ae bot musuh)
            return Position(x=curr_pos.x + x, y=curr_pos.y + yes)
        else:
            for opsi in opsi_kabur:
                xdes, ydes = get_direction(curr_pos.x, curr_pos.y, opsi.x, opsi.y)
                if xdes ==x and ydes == yes:   # Jika arah kabur sama dengan arah diamond terdekat
                    return opsi
            # Mencari tujuan kabur alternatif yang paling searah dengan diamond terdekat
            if x == 0:   # arah ke atas atau bawah
                for opsi in opsi_kabur:
                    if opsi.x == curr_pos.x+1 or opsi.x == curr_pos.x-1:
                        return opsi
            elif yes == 0:
                for opsi in opsi_kabur:
                    if opsi.y == curr_pos.y+1 or opsi.y == curr_pos.y-1:
                        return opsi
            return Position(x=curr_pos.x + x, y=curr_pos.y + yes) 
        
    def process(self):
        self.goal_position = self.tujuan_kabur( self.bot.position, self.enemies_position)
            
        
        
