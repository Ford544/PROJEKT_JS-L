import time

from .player import Player

class ClientPlayer(Player):
    
    def pass_control(self) -> bool:
        print("waiting for client player")
        self.game.board, self.game.selected = self.game.server.get_state()
        time.sleep(0.05)
        #needed?
        self.game.gui.update()
        return False