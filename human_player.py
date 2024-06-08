import time

from player import Player

class HumanPlayer(Player):
    def make_move(self):
        self.game.enable_tiles()
        while not self.game.turn_over:
            self.game.gui.processEvents()
            time.sleep(0.01)
