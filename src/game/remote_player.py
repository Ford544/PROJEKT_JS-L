from .player import Player


class RemotePlayer(Player):

    color : int

    def __init__(self, game, name : str, profile : bool, color : int):
        super().__init__(game, name, profile)
        self.color = color

    def pass_control(self) -> bool:
        print("remote player activating")
        if self.game.interface is not None:
            self.game.interface.run_update_loop(self.color)
        return True