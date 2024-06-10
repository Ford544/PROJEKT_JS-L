from abc import ABC, abstractmethod


class Player(ABC):

    name : str

    def __init__(self, game, name : str) -> None:
        self.game = game
        self.name = name

    @abstractmethod
    def pass_control(self) -> bool:
        pass