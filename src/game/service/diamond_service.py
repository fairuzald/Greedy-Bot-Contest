from game.models import GameObject, Board, Position

class DiamondService:
    def __init__(self, bot: GameObject, board: Board):
        super().__init__()
        self.board = board
        self.processed = False
        self.bot = bot

    def get_nearest_diamond(self) -> Position:  
        return (1,0)

    def get_distance(self, curr: Position, tar: Position) -> int:
        return abs(curr.x - tar.x) + abs(curr.y - tar.y)