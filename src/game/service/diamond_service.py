from game.models import GameObject, Board, Position
from typing import List
class DiamondService:
    def __init__(self, bot: GameObject, board: Board):
        super().__init__()
        self.board = board
        self.processed = False
        self.bot = bot

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
                
    def get_diamonds_by_cluster(self,board : Board,current_pos : Position) -> List[int]:
        width = board.width
        height = board.height
        cluster = [0] * 4
        nearest = [99999] * 4
        positions = [Position(0,0)] * 4
        diamonds = self.get_list_of_diamonds(board)
        
        for diamond in diamonds:
            if diamond.x < width/2 and diamond.y < height/2:
                if(self.get_distance(current_pos,diamond) < nearest[0]):
                    nearest[0] = self.get_distance(current_pos,diamond)
                    positions[0] = diamond
                cluster[0] += 1
            elif diamond.x < width/2 and diamond.y >= height/2:
                if(self.get_distance(current_pos,diamond) < nearest[1]):
                    nearest[1] = self.get_distance(current_pos,diamond)
                    positions[1] = diamond
                cluster[1] += 1
            elif diamond.x >= width/2 and diamond.y < height/2:
                if(self.get_distance(current_pos,diamond) < nearest[2]):
                    nearest[2] = self.get_distance(current_pos,diamond)
                    positions[2] = diamond
                
                cluster[2] += 1
            else:
                if(self.get_distance(current_pos,diamond) < nearest[3]):
                    nearest[3] = self.get_distance(current_pos,diamond)
                    positions[3] = diamond
                cluster[3] += 1
                
        return positions[cluster.index(max(cluster))]