from abc import ABC, abstractmethod


class Player(ABC):

    name : str
    profile : bool

    def __init__(self, game, name : str, profile : bool) -> None:
        self.game = game
        self.name = name
        self.profile = profile

    #this method should return False if the whole move is executed in one call
    #                          True if the game should pause the game and wait for the move (the player took control)
    @abstractmethod
    def pass_control(self) -> bool:
        pass