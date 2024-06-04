import PySide6
from functools import partial

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QPainter, QPen, QColor

import consts
from consts import WIDTH,HEIGHT

#those are for display purposes and distinct from constants in consts.py, which are meant for logic
EMPTY = 0
WHITE_PIECE = 2
WHITE_KING = 3
BLACK_PIECE = 4
BLACK_KING = 5
MOVE = 6

#colors
WHITE_TILE_COLOR = "#EEEEEE"
SELECTED_WHITE_TILE_COLOR = "#AAAAAA"
BROWN_TILE_COLOR = "#B58863"
SELECTED_BROWN_TILE_COLOR = "#855843"


class MainWindow(QMainWindow):

    @property
    def tiles(self):
        return self.board.tiles

    def __init__(self,game):
        super().__init__()

        self.game = game

        self.setFixedSize(QSize(720, 640))

        main_layout = QHBoxLayout()
        self.board = GUIBoard(self,game)
        main_layout.addWidget(self.board)

        self.setLayout(main_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def update(self):
        self.board.update()


class GUIBoard(QFrame):
    def __init__(self, parent, game):
        super().__init__(parent)
        
        self.game = game
        self.tiles = []
        self.selected = None
        self.valid_moves = []

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        for row in range(HEIGHT):
            self.tiles.append([])
            for col in range(WIDTH):
                square = Tile(self,row,col)
                square.clicked.connect(partial(game.select,row,col))
                if row % 2 == col % 2:
                    square.setStyleSheet(f'background-color: {WHITE_TILE_COLOR}')
                else:
                    square.setStyleSheet(f'background-color: {BROWN_TILE_COLOR}')
                self.layout.addWidget(square, row, col)
                self.tiles[-1].append(square)

    def update(self):
        #draw pieces
        for i in range(HEIGHT):
            for j in range(WIDTH):
                contents = self.game.board.get_piece(i,j)
                tile = self.tiles[i][j]
                #print(f"{i}:{j}: {contents}")

                if i % 2 == j % 2:
                    if (i,j) == self.selected:
                        tile.setStyleSheet(f'background-color: {SELECTED_WHITE_TILE_COLOR}')
                    else:
                        tile.setStyleSheet(f'background-color: {WHITE_TILE_COLOR}')
                else:
                    if (i,j) == self.selected:
                        tile.setStyleSheet(f'background-color: {SELECTED_BROWN_TILE_COLOR}')
                    else:
                        tile.setStyleSheet(f'background-color: {BROWN_TILE_COLOR}')

                if contents is None:
                    tile.content = EMPTY
                else:
                    if contents.color == consts.WHITE:
                        if contents.is_king:
                            tile.content = WHITE_KING
                        else:  
                            tile.content = WHITE_PIECE
                    else:
                        if contents.is_king:
                            tile.content = BLACK_KING
                        else:  
                            tile.content = BLACK_PIECE
                    #print(self.game.board.marked)
                    if (contents.x,contents.y) in self.game.board.marked:
                        tile.marked = True
                    else:
                        tile.marked = False
                print(self.valid_moves)
                if (tile.x, tile.y) in self.valid_moves:
                    tile.valid_move = True
                else:
                    tile.valid_move = False
                tile.update()



class Tile(QLabel):

    clicked = Signal()

    def __init__(self,parent, x, y):
        super().__init__(parent)
        self.content = EMPTY
        self.x = x
        self.y = y
        self.marked = False
        self.valid_move = False
        

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        center = rect.center()
        if self.content != EMPTY:
            if self.content == WHITE_PIECE:
                qcolor = QColor(255, 255, 255)
            if self.content == BLACK_PIECE:
                qcolor = QColor(0, 0, 0)   
            pen = QPen(qcolor, 3, Qt.SolidLine)
            qp.setPen(pen)
           
            
            radius = min(rect.width(), rect.height()) // 3 - pen.width() // 3
            qp.drawEllipse(center, radius, radius)
            radius = min(rect.width(), rect.height()) // 4 - pen.width() // 4
            qp.drawEllipse(center, radius, radius)

            #tilt 45 degrees
            if self.marked:
                pen = QPen(QColor(255, 0, 0), 5, Qt.SolidLine)
                qp.setPen(pen)
                
                qp.drawLine(center.x() - radius, center.y(), center.x() + radius, center.y())
                qp.drawLine(center.x(), center.y() - radius, center.x(), center.y() + radius)

        if self.valid_move:
            qp.setBrush(QColor(0, 255, 0))
            qp.drawEllipse(center, 10, 10)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

class GUI:

    def init(self,game):
        self.app = QApplication([])

        self.window = MainWindow(game)
        self.window.show()

        self.window.update()

        for row in self.window.tiles:
            for cell in row:
                print(cell.content,end="")
            print()
    
    def run(self):
        self.app.exec()

    def update(self):
        self.window.update()

    def set_selected(self, piece):
        self.window.board.selected = piece

    def set_valid_moves(self, valid_moves):
        self.window.board.valid_moves = valid_moves


        
