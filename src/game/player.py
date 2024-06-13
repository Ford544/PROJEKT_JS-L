from abc import ABC, abstractmethod


class Player(ABC):

    name : str
    profile : bool

    def __init__(self, game, name : str, profile : bool) -> None:
        self.game = game
        self.name = name
        self.profile = profile

    @abstractmethod
    def pass_control(self) -> bool:
        pass