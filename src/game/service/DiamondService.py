
from game.models import Board,Position
from typing import List
class DiamondService:
    status1 = False
    status2 = False
    
    def __init__(self):
        pass
    
    def get_list_of_diamonds(self,board : Board) -> list[Position]:
        diamond_list = []
        for obj in board.game_objects:
            if(obj.type == "DiamondGameObject"):
                diamond_list.append(obj.position)
        return diamond_list
    
    def get_distance(self,current_pos : Position, target_pos : Position) -> int:
        return abs(current_pos.x - target_pos.x) + abs(current_pos.y - target_pos.y)
    
    
    def get_nearest_diamond(self,board : Board,current_pos : Position ) -> Position:
        min = float('inf')
        pos = Position(0,0)
        diamonds = self.get_list_of_diamonds(board)
        for diamond in diamonds:
            if self.get_distance(current_pos,diamond) < min:
                min = self.get_distance(current_pos,diamond)
                pos = diamond
        return pos
                
    def get_diamonds_by_cluster(self,board : Board) -> List[int]:
        width = board.width
        height = board.height
        
        for i in range(width):
            for j in range(height):
                if(i<width/2):
                    if(j<height/2):
                        if(board.game_objects[i][j] == "DiamondGameObject"):
                            self.status1 = True
                            
                    # not completed