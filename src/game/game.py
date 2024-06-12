from PySide6.QtCore import *
from PySide6.QtWidgets import *

from ..board.piece import Piece
from ..board.board import Board
from .player import Player
from .human_player import HumanPlayer
from .random_player import RandomPlayer
from .minimax_player import MinimaxPlayer
from ..profiles.profile_manager import ProfileManager
from ..consts import BLACK,WHITE

class Game:
    board : Board
    selected : Piece
    white_player : Player
    black_player : Player
    manager : ProfileManager

    def __init__(self, gui, manager):
       
       self.board = Board()
       self.selected = None
       self.gui = gui
       self.manager = manager

       self.white_player = HumanPlayer(self, "human")
       self.black_player = MinimaxPlayer(self, "si", 2, False)
       self.active_player = 1 

    def play(self):
        while self.board.winner == 0:
            if self.board.active_player == WHITE:
                self.gui.set_banner_text("WHITE'S TURN")
                if self.white_player.pass_control():
                    return
            else:
                self.gui.set_banner_text("BLACK'S TURN")
                if self.black_player.pass_control():
                    return
            self.gui.processEvents()
        if self.board.winner == BLACK:
            self.gui.set_banner_text("Black has won!")
            self.register_game(self.black_player)
        elif self.board.winner == WHITE:
            self.gui.set_banner_text("White has won!")
            self.register_game(self.white_player)

    def restart(self):
        self.board.set_up()
        self.selected = None

    def select(self, x : int, y : int):
        target = self.board.get_piece(x,y)
        if target is None:
            if self.selected is not None:
                if self.board.move(self.selected,x,y):
                    if self.board.has_valid_moves(self.selected):
                        self.mark_selected(self.selected)
                    else:
                        self.mark_selected(None)
                    self.gui.update()
                    print(f"moved to {(x,y)}")

        elif target.color == self.board.active_player:
            self.mark_selected(target)
            print(f"selected {(x,y)}")

    def mark_selected(self, target : Piece) -> None:
        self.selected = target
        self.gui.update()

    def register_game(self, player : Player) -> None:
        if isinstance(player,HumanPlayer):
            self.manager.register_win()
        else:
            self.manager.register_loss()

    @property
    def selected_tile(self):
        if self.selected is None: return None
        return self.selected.x,self.selected.y
    
    @property
    def selected_valid_moves(self):
        if self.selected is None: return []
        if not self.selected in self.board.valid_moves.keys(): return []
        return [move.first_step for move in self.board.valid_moves[self.selected]]
    
    @property
    def marked_tiles(self):
        return self.board.marked
    
    def enable_tiles(self):
        self.gui.enable_tiles()

    def disable_tiles(self):
        self.gui.disable_tiles()

