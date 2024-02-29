from typing import List, Dict
import threading
from game.models import GameObject, Board
class Processor(threading.Thread):
    def __init__(self, bot:GameObject , board: Board):
        super().__init__()
        self.bot = bot
        self.board = board
        self.processed = False

    def run(self):
        self.process()

    def process(self):
        # Fungsi utama
        pass
