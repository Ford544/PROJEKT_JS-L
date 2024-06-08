import time

from player import Player

class HumanPlayer(Player):
    def make_move(self):
        print("human makes move")
        self.game.gui.window.await_inputs()
