from PySide6.QtCore import *
from PySide6.QtWidgets import *

from piece import Piece
from board import Board
from gui import MainWindow,GUI

class Game:
    board : Board
    selected : Piece
    gui : GUI

    def __init__(self):
       self.board = Board()
       self.selected = None
       self.gui = GUI()
       self.gui.init(self)
       self.gui.run()

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

        elif target.color == self.board.active_player:
            self.mark_selected(target)

    def mark_selected(self, target : Piece):
        self.selected = target
        self.gui.update()

    @property
    def selected_tile(self):
        if self.selected is None: return None
        return self.selected.x,self.selected.y
    
    @property
    def selected_valid_moves(self):
        if self.selected is None: return []
        return [move.first_step for move in self.board.valid_moves[self.selected]]
    
    @property
    def marked_tiles(self):
        return self.board.marked


Game()