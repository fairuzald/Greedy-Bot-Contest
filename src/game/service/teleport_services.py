
from typing import List
from game.models import Position, GameObject, Board

class TeleportService:
    def __init__(self):
        pass
    
    # Get the distance between bot and 1 teleport
    def get_distance(self, origin: Position, target: Position) -> int:
        return abs(target.x - origin.x) + abs(target.y - origin.y) 

    # Get the nearest teleport from the bot
    def get_nearest_teleport(self, curr:Position, teleports: List[GameObject]) -> Position:
        min_distance = float('inf')
        nearest_position = None

        for tel in teleports:
            # Get distance data
            distance = self.get_distance(curr, tel.position)
            
            # Minimum Comparation
            if distance < min_distance:
                min_distance = distance
                nearest_position = tel.position
                
        return nearest_position
    
    # GEt the distance between bot and diamond by using teleport
    def get_distance_diamond_bot_by_teleport(self, curr: Position, diamond: Position, teleport: Position) -> int:
        return self.get_distance(curr, teleport) + self.get_distance(teleport, diamond)
    
    # Get the nearest diamond from the bot using teleport
    def get_nearest_diamond_by_teleport(self, curr: Position, diamonds: List[GameObject], teleports: List[GameObject]) -> Position:
        min_distance = float('inf')
        nearest_teleport = None

        for diamond in diamonds:
            for tel in teleports:
                # Get distance data
                distance = self.get_distance_diamond_bot_by_teleport(curr, diamond.position, tel.position)
                
                # Minimum Comparation
                if distance < min_distance:
                    min_distance = distance
                    nearest_teleport = tel.position
                
        return nearest_teleport
    
    