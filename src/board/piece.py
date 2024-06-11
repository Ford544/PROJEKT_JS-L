from ..consts import WHITE, BLACK, BOARD_SIZE

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

    def __str__(self):
        if self.color == WHITE:
            return f"{self.x},{self.y},white"
        else:
            return f"{self.x},{self.y},black"
        
    def __repr__(self):
        if self.color == BLACK:
            return f"{self.x},{self.y},white"
        else:
            return f"{self.x},{self.y},black"
        
    def get_forward_tiles(self):
        tiles = []
        if 0 <= self.x + self.color < BOARD_SIZE:
            if self.y > 0:
                tiles.append((self.x + self.color, self.y - 1))
            if self.y < BOARD_SIZE - 1:
                tiles .append((self.x + self.color,self.y + 1))