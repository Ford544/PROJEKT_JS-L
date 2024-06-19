import time

from .player import Player


class RemotePlayer(Player):

    color : int

    def __init__(self, game, name : str, profile : bool, color : int):
        super().__init__(game, name, profile)
        self.color = color

    def pass_control(self) -> bool:
        if self.game.interface is not None:
            #print("server player turn")
            try:
                board,selected = self.game.interface.send("get")
                self.game.board = board
                self.game.selected = selected
                time.sleep(0.05)
                self.game.gui.update()
            except:
                print("connection lost")
                self.game.paused = True
            return False
        else:
            return True