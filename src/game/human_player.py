import time

from .player import Player

class HumanPlayer(Player):

    def pass_control(self) -> bool:
        print("human makes move")
        self.game.gui.enable_tiles()
        return True
