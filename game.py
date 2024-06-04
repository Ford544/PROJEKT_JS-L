from PySide6.QtCore import *
from PySide6.QtWidgets import *

from piece import Piece
from board import Board
from gui import MainWindow,GUI

class Game:
    def __init__(self):
       self.board = Board()
       self.selected = None
       self.gui = GUI()
       self.gui.init(self)
       self.gui.run()

    def select(self, x, y):
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

    def mark_selected(self, target):
        print("selecting")
        self.selected = target
        if target == None:
            self.gui.set_selected(None)
            self.gui.set_valid_moves([])
        else:
            self.gui.set_selected((target.x,target.y))
            self.gui.set_valid_moves([move.first_step for move in self.board.valid_moves[target]])
        self.gui.update()


Game()