import time

from .player import Player

class HumanPlayer(Player):

    def pass_control(self) -> bool:
        self.game.gui.enable_tiles()
        return True
