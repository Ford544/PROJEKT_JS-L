from dataclasses import dataclass

from .piece import Piece
from ..consts import BLACK, WHITE

class Move:

    steps : list[tuple[int]]
    jumped : list[tuple[int]]

    def __init__(self, steps : list[tuple[int]] = [], jumped : list[tuple[int]] = []):
        self.steps = steps
        self.jumped = jumped

    def pop(self) -> bool:
        if len(self.steps) == 0:
            return False
        self.steps = self.steps[1:]
        if len(self.jumped) != 0:
            self.jumped = self.jumped[1:]
        if len(self.steps) == 0:
            return False
        return True
    
    @property
    def first_step(self) -> tuple[int] | None:
        if len(self.steps) == 0:
            return None
        return self.steps[0]
    
    @property
    def first_jumped(self) -> tuple[int] | None:
        if len(self.jumped) == 0:
            return None
        return self.jumped[0]

    def __str__(self) -> str:
        return f"Move object (steps={self.steps} jumped={self.jumped})"

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, o):
        return Move(self.steps + o.steps, self.jumped + o.jumped)

class Board:

    size : int
    #those two are currently redundand, as they always equal to size and each other
    #they're kept for the sake of potential extendability (we may potentially want to add some strange
    #rule variant with non-square board)
    width : int
    height : int
    capturing_obligatory : bool

    board : list[list[Piece | None]]
    pieces : list[Piece]
    valid_moves : dict[Piece, list[Move]]
    active_player : int
    marked : list[tuple[int]]

    def __init__(self, size, capturing_obligatory):
        self.size = size
        self.width = size
        self.height = size
        self.capturing_obligatory = capturing_obligatory
        self.set_up()


    def set_up(self) -> None:
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.pieces = []
        for row in range(self.size):
            for col in range(self.size):
                piece = self.starting_location_piece(row,col)
                if piece != None:
                    self.pieces.append(piece)
                    self.board[row][col] = piece
        self.valid_moves = {}
        self.active_player = WHITE
        self.marked = []

        self.update_valid_moves(self.active_player)

    def starting_location_piece(self, row : int, col : int) -> Piece | None:
        if row < self.size / 2 - 1 and row % 2 != col % 2:
            return Piece(row,col,WHITE)
        if row >= self.size / 2 + 1 and row % 2 != col % 2:
            return Piece(row,col,BLACK)
        return None
    
    @property
    def whites(self) -> int:
        counter = 0
        for piece in self.pieces:
            if piece.color == WHITE: counter += 1
        return counter
    
    @property
    def blacks(self) -> int:
        return len(self.pieces) - self.whites
    
    @property
    def winner(self) -> int:
        if self.blacks == 0:
            return WHITE
        if self.whites == 0:
            return BLACK
        if self.no_valid_moves():
            return -1*self.active_player
        return 0
    
    def no_valid_moves(self) -> bool:
        for moves in self.valid_moves.values():
            if len(moves) > 0: return False
        return True
    
    def get_piece(self, x : int, y : int) -> Piece | None:
        return self.board[x][y]
    
    def update_valid_moves(self, turn : int) -> None:
        longest_jump_length = 0
        
        for piece in self.pieces:
            if piece.color == turn:
                self.valid_moves[piece] = self.get_valid_piece_moves(piece)
                for move in self.valid_moves[piece]:
                    longest_jump_length = max(longest_jump_length,len(move.jumped))
        
        if self.capturing_obligatory:
            self.valid_moves = {piece : list(filter(lambda move : len(move.jumped) == longest_jump_length, moves)) for piece, moves in self.valid_moves.items()}
        
        
    
    def get_valid_piece_moves(self, piece : Piece) -> list[Move]:
        return self.get_piece_moves(piece.x,piece.y,piece,[])

    def get_piece_moves(self, start_x : int, start_y : int, piece : Piece, jumped : list[tuple[int]]) -> list[Move]:
        moves = []
        for vector in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            moves = moves + self.check_diagonal(start_x,start_y,piece,vector,jumped)
        return moves


    def check_diagonal(self, start_x : int, start_y : int, piece : Piece, vector : tuple[int], jumped : list[tuple[int]]) -> list[Move]:
        moves = []
        jumps = []
        potential_jumped = []
        previous = None
        #get next tile on the diagonal
        tile = (start_x + vector[0],start_y + vector[1])
            #if out of bound, terminate
        if tile[0] < 0 or tile[0] >= self.height:
            return moves
        if tile[1] < 0 or tile[1] >= self.width:
            return moves
        #only consider moving (without jumping) if didn't jump yet AND the vector goes forward or the piece is a king
        if jumped == [] and (vector[0] == piece.color or piece.is_king):
            #if the tile's empty, move is possible 
            #the second condition is because it should be possible to return to the same spot
            if (self.board[tile[0]][tile[1]] is None) or (tile == (piece.x,piece.y)):
                moves.append(Move(steps=[tile]))
        previous = self.board[tile[0]][tile[1]]
        tile = (tile[0] + vector[0], tile[1] + vector[1])
        while 0 <= tile[0] < self.height and 0 <= tile[1] < self.width:
            #if we encountered a piece of our own color, we cannot move further
            if self.board[tile[0]][tile[1]] is not None and self.board[tile[0]][tile[1]].color == piece.color:
                break
            #if we jumped already in this iteration, encountering another piece ends the iteration
            if previous is not None and self.board[tile[0]][tile[1]] is not None:
                break
            #a king can move to further empty tiles
            if (jumped == []) and (previous is None) and (piece.is_king) and (self.board[tile[0]][tile[1]] is None or (tile == (piece.x,piece.y))):
                moves.append(Move(steps=[tile]))
            #jumping
            #there must have been an enemy piece before; whether the piece is a king
            #or not is irrelevant at this stage, as a non-king will not progress past
            #the first loop anyway
            if (previous is not None) and (previous.color != piece.color) and (self.board[tile[0]][tile[1]] is None or tile == (piece.x,piece.y)) and ((previous.x,previous.y) not in jumped):
                jumps.append(tile)
                potential_jumped.append((previous.x, previous.y))
            #if not king, we need not consider tiles further away than two
            if not piece.is_king:
                break
            #update previous and tile
            if self.board[tile[0]][tile[1]] is not None:
                previous = self.board[tile[0]][tile[1]]
            tile = (tile[0] + vector[0], tile[1] + vector[1])
        #recursively look for further moves for all jumps
        for jump,captured in zip(jumps,potential_jumped):
            further_moves = self.get_piece_moves(jump[0], jump[1], piece, jumped+[captured])
            moves.append(Move(steps=[jump],jumped=[captured]))
            for further_move in further_moves:
                moves.append(Move(steps=[jump],jumped=[captured]) + further_move)
        
        return moves
    
    #return True if move was executed, and False if it wasn't (because it was invalid)
    def move(self, piece : Piece, x : int, y : int) -> bool:
        if self.is_valid_move(piece, x, y):
            self.board[piece.x][piece.y] = None
            self.board[x][y] = piece
            piece.x, piece.y = x, y
            self.prune_valid_moves(piece, x, y)
            #if the move sequence is over
            if self.valid_moves == {}:

                #make king
                if piece.color == WHITE and x == self.height - 1:
                    piece.is_king = True
                if piece.color == BLACK and x == 0:
                    piece.is_king = True

                self.active_player *= -1
                for marked_piece in self.marked:
                    self.remove(marked_piece)
                self.marked = []
                self.update_valid_moves(self.active_player)
            return True
        return False
    
    def execute_full_move(self, piece : Piece, move : Move) -> None:
        for x, y in move.steps:
            self.move(piece, x, y)


    #remove piece at the coordinates
    def remove(self, coords : tuple[int]) -> None:
        x,y = coords
        if self.board[x][y] != None:
            self.pieces.remove(self.board[x][y])
        self.board[x][y] = None 

    def prune_valid_moves(self, piece : Piece, x : int, y : int) -> None:
        new_moves = []
        for move in self.valid_moves[piece]:
            if move.first_step == (x,y):
                jumped = move.first_jumped
                if (jumped is not None) and (jumped not in self.marked):
                    self.marked.append(jumped)                
                if move.pop():
                    new_moves.append(move)
        self.valid_moves = {}
        if len(new_moves) > 0:
            self.valid_moves[piece] = new_moves

    def is_valid_move(self, piece : Piece, x : int, y : int) -> bool:
        if piece not in self.valid_moves.keys():
            return False
        for move in self.valid_moves[piece]:
            if move.first_step == (x,y):
                return True
        return False

    def is_valid_tile(self, x : int, y : int) -> bool:
        return (0 <= x < self.height) and (0 <= y < self.width)
    
    def has_valid_moves(self, piece : Piece) -> bool:
        return piece in self.valid_moves.keys() and len(self.valid_moves[piece]) > 0 

#TESTING
if __name__ == "__main__":
    b = Board()
    for i in range(b.height):
        for j in range(b.width):
            b.board[i][j] = None
    b.board[0][1] = Piece(0,1,WHITE)
    b.board[0][1].is_king = True
    b.board[3][4] = Piece(3,4,BLACK)
    b.board[5][4] = Piece(5,4,BLACK)