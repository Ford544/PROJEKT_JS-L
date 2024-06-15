from ..consts import WHITE

class Piece:
    x : int
    y : int
    color : int
    is_king : bool

    def __init__(self, x : int, y : int, color : int):
        self.x = x
        self.y = y
        self.color = color
        self.is_king = False

    def __str__(self) -> str:
        if self.color == WHITE:
            return f"{self.x},{self.y},white"
        else:
            return f"{self.x},{self.y},black"