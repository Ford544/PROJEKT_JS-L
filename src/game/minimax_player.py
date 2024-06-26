import copy
import random
import time

from ..board.board import Board, Move
from ..consts import WHITE, BLACK, DRAW
from ..board.piece import Piece
from .player import Player

class MinimaxPlayer(Player):

    depth : int
    white : bool

    def __init__(self, game, name : str, profile : bool, depth : int, white : bool):
        super().__init__(game,name, profile)
        self.depth = depth
        self.white = white

    def pass_control(self) -> bool:

        self.counter = 0
        
        _, best_moves = self.minimax(self.game.board, self.depth, self.white, float("-inf"), float("+inf"))

        #if there are multiple moves with the same score, pick a random one
        piece, move = random.choice(best_moves)
        
        self.game.select(piece.x, piece.y)
        self.game.gui.processEvents()

        for x,y in move.steps:
            self.game.gui.processEvents()
            self.game.select(x,y)
            time.sleep(0.25)
        
        return False
    
    #return the best move score and a list of moves with that score
    def minimax(self, board : Board, level : int, max_ : bool, alpha : float, beta : float) -> tuple[float, list[tuple[Piece, Move]]]:
        value = self.evaluate_board(board)
        if level == 0 or value == float("+inf") or value == float("-inf"):
            self.counter += 1
            return value, None
        best_moves = []
        if max_:
            current_maximum = float("-inf")   
            for piece,moves in board.valid_moves.items():
                for move in moves:
                    value,_ = self.minimax(self.simulate_move(board,piece,move), level - 1, not max_, alpha, beta)
                    if value == current_maximum:
                        best_moves.append((piece, move))
                    if value > current_maximum:
                        current_maximum = value
                        best_moves = [(piece, move)]

                    alpha = max(alpha, current_maximum)
                    if alpha >= beta:
                        return current_maximum, best_moves
                    
            return current_maximum, best_moves
        else:
            current_minimum = float("+inf")
            for piece,moves in board.valid_moves.items():
                for move in moves:
                    value,_ = self.minimax(self.simulate_move(board,piece,move), level - 1, not max_, alpha, beta)
                    if value == current_minimum:
                        best_moves.append((piece,move))
                    if value < current_minimum:
                        current_minimum = value
                        best_moves = [(piece, move)]

                    beta = min(beta, current_minimum)
                    if alpha >= beta:
                        return current_minimum, best_moves
                    
            return current_minimum, best_moves
            
        
    #white maximizes, black minimizes
    def evaluate_board(self, board : Board) -> float:
        if board.winner == WHITE:
            return float("+inf")
        if board.winner == BLACK:
            return float("-inf")
        if board.winner == DRAW:
            return 0.
        return float(board.whites - board.blacks + 0.5*board.white_kings - 0.5*board.black_kings)
    
    #get copy of the board after executing a particular move sequence
    def simulate_move(self, board : Board , piece : Piece, move : Move) -> Board:

        new_board = copy.deepcopy(board)

        piece = new_board.get_piece(piece.x, piece.y)
        new_board.execute_full_move(piece, move)

        return new_board