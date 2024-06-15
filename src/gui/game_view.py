from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ..game.game import Game
from .gui_board import GUIBoard
from ..consts import MENU_STYLE

class GameView(QFrame):

    window : QMainWindow
    game : Game

    reset_button : QPushButton
    return_button : QPushButton
    banner : QLabel
    board : GUIBoard

    def __init__(self, parent, window, game):

        super().__init__(parent)

        self.window = window
        self.game = game

        main_layout = QHBoxLayout()

        central_layout = QVBoxLayout()
        central_frame = QFrame()
        central_frame.setLayout(central_layout)
        central_frame.setStyleSheet(MENU_STYLE)

        self.banner = QLabel(self)
        self.banner.setText("Hey")
        self.banner.setFixedSize(720,20)
        self.banner.setAlignment(Qt.AlignCenter)
        central_layout.addWidget(self.banner)

        button_layout = QHBoxLayout()

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_button_effect)
        
        self.return_button = QPushButton("Return")
        self.return_button.clicked.connect(self.return_button_effect)

        button_layout.addWidget(self.reset_button)
        button_layout.addStretch(stretch=1)
        button_layout.addWidget(self.return_button)

        central_layout.addLayout(button_layout)
        
        self.board = GUIBoard(self,self.game)
        central_layout.addWidget(self.board)

        self.left_spacing = QSpacerItem(0,0)
        self.right_spacing = QSpacerItem(0,0)
        main_layout.addStretch()
        main_layout.addWidget(central_frame)
        main_layout.addStretch()

        self.setMinimumSize(QSize(760, 660))
        self.setStyleSheet('QFrame { background-color: #338888; }')
        self.setLayout(main_layout)

    def reset_button_effect(self):
        self.game.restart()
        self.game.play()

    def return_button_effect(self):
        self.game.paused = True
        self.window.go_to_menu()

    def set_banner_text(self, text):
        self.banner.setText(text)
        self.update()

    @property
    def tiles(self):
        return self.board.tiles
    
    def enable_tiles(self):
        self.board.enable_tiles()
    
    def disable_tiles(self):
        self.board.disable_tiles()
    
    def update(self):
        self.board.update()
