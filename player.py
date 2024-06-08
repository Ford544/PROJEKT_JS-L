from abc import ABC, abstractmethod


class Player(ABC):

    name : str

    def __init__(self, game, name : str) -> None:
        self.game = game
        self.name = name

    @abstractmethod
    def make_move(self):
        pass