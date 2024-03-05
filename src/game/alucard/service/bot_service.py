from game.models import GameObject, Board, Position
from game.util import get_direction
from typing import List
from game.alucard.service.math_services import MathService
from game.alucard.service.object_services import ObjectServices


class BaseService:
    def __init__(self, bot: GameObject, board: Board):
        super().__init__()
        self.board = board
        self.bot = bot
    
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