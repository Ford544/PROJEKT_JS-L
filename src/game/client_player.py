import time

from .player import Player

#represents the remote client player from the perspective of the server

class ClientPlayer(Player):
    
    def pass_control(self) -> bool:
        self.game.board, self.game.selected = self.game.server.get_state()
        time.sleep(0.05)
        self.game.gui.update()
        return False