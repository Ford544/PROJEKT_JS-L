import PySide6
from functools import partial
import time

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

    def __init__(self,game):
        super().__init__()

        self.game = game
        self.open = True

        self.setFixedSize(QSize(720, 660))

        main_layout = QVBoxLayout()

        self.banner = QLabel(self)
        self.banner.setText("Hey")
        self.banner.setFixedSize(720,20)
        self.banner.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.banner)
        
        self.board = GUIBoard(self,game)
        main_layout.addWidget(self.board)

        self.setLayout(main_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def update(self):
        self.board.update()

    def closeEvent(self, event):
        self.open = False
        print("I just got closed")
        super().closeEvent(event)
        

    def await_inputs(self):
        self.enable_tiles()
        while not self.game.turn_over and self.open:
            self.game.gui.processEvents()
            time.sleep(0.01)

    @property
    def tiles(self):
        return self.board.tiles
    
    @property
    def enable_tiles(self):
        return self.board.enable_tiles
    
    @property
    def disable_tiles(self):
        return self.board.disable_tiles


class GUIBoard(QFrame):

    def __init__(self, parent, game):
        super().__init__(parent)
        
        self.game = game
        self.tiles = []
        self.tiles_enabled = False

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

    def enable_tiles(self):
        self.tiles_enabled = True

    def disable_tiles(self):
        self.tiles_disabled = False

    def update(self):
        #draw pieces
        print("updajtuje borda")
        for i in range(HEIGHT):
            for j in range(WIDTH):
                contents = self.game.board.get_piece(i,j)
                tile = self.tiles[i][j]
                #print(f"{i}:{j}: {contents}")

                if i % 2 == j % 2:
                    if (i,j) == self.game.selected_tile:
                        tile.setStyleSheet(f'background-color: {SELECTED_WHITE_TILE_COLOR}')
                    else:
                        tile.setStyleSheet(f'background-color: {WHITE_TILE_COLOR}')
                else:
                    if (i,j) == self.game.selected_tile:
                        tile.setStyleSheet(f'background-color: {SELECTED_BROWN_TILE_COLOR}')
                    else:
                        tile.setStyleSheet(f'background-color: {BROWN_TILE_COLOR}')

                marked = self.game.marked_tiles
                valid_moves = self.game.selected_valid_moves

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
                    if (contents.x,contents.y) in marked:
                        tile.marked = True
                    else:
                        tile.marked = False
                if (tile.x, tile.y) in valid_moves:
                    tile.valid_move = True
                else:
                    tile.valid_move = False
                tile.update()



class Tile(QLabel):

    clicked = Signal()

    x : int
    y : int
    marked : bool
    valid_move : bool

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

            #TODO make kings distinct visually
            if self.content == WHITE_PIECE or self.content == WHITE_KING:
                qcolor = QColor(255, 255, 255)
            if self.content == BLACK_PIECE or self.content == BLACK_KING:
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
            #this is a simple way to disable tile clicking, but it's probably not the best one
            #we may want some alternate event to happen when the disabled board is clicked after all
            if self.parent().tiles_enabled:
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

    def processEvents(self):
        self.app.processEvents()

    @property
    def enable_tiles(self):
        return self.window.enable_tiles

    @property
    def disable_tiles(self):
        return self.window.disable_tiles


        
