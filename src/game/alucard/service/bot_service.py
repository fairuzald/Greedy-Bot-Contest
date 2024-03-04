from game.models import GameObject, Board, Position
from game.util import get_direction
from typing import List
from game.alucard.service.math_services import MathService
from processor.diamond_processor import DiamondProcessor


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

        diamond_list = DiamondProcessor.get_diamond_position_list(self.board)
        
        arah_diamond = get_direction(curr_pos, MathService.getNearestObjectPosition(curr_pos, diamond_list))

        if opsi_kabur == []:        # Pasrah (trobos ae bot musuh)
            return Position(x=curr_pos.x + arah_diamond[0], y=curr_pos.y + arah_diamond[1])
        else:
            for opsi in opsi_kabur:
                if get_direction(curr_pos, opsi) == arah_diamond:
                    return opsi
            # Mencari tujuan kabur alternatif yang paling searah dengan diamond terdekat
            if arah_diamond[0] == 0:   # arah ke atas atau bawah
                for opsi in opsi_kabur:
                    if opsi.x == curr_pos.x+1 or opsi.x == curr_pos.x-1:
                        return opsi
            elif arah_diamond[1] == 0:
                for opsi in opsi_kabur:
                    if opsi.y == curr_pos.y+1 or opsi.y == curr_pos.y-1:
                        return opsi
            return Position(x=curr_pos.x + arah_diamond[0], y=curr_pos.y + arah_diamond[1]) 