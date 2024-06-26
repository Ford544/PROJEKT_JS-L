import random
import time

from .player import Player

#implemented for testing purposes, but can be used in the final version

class RandomPlayer(Player):

    def pass_control(self) -> bool:
        valid_moves = []
        
        for piece,moves in self.game.board.valid_moves.items():
            for move in moves:
                valid_moves.append((piece,move))
        piece,move = random.choice(valid_moves)
        self.game.select(piece.x, piece.y)
        for x,y in move.steps:
            self.game.gui.processEvents()
            self.game.select(x,y)
            time.sleep(0.25)
        return False
        
