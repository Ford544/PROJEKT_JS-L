from functools import partial
from pathlib import Path
import time

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QPainter, QPen, QColor

from ..consts import WIDTH,HEIGHT
from ..game.game import Game
from ..profiles.profile_ import Profile
from ..profiles.profile_manager import ProfileManager
from .gui_board import GUIBoard


class MainMenu(QWidget):


    window : QMainWindow

    start_button : QPushButton
    
    def __init__(self, parent, window):
    
        super().__init__(parent)
        self.window = window


        main_layout = QHBoxLayout()
        
        button_layout = QVBoxLayout()

        self.start_button = QPushButton("Quick start")
        self.start_button.clicked.connect(self.quick_start_button_effect)
        button_layout.addWidget(self.start_button)

        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.setStyleSheet('background-color: #338888;')

    def quick_start_button_effect(self):
        self.window.start_game()

class GameView(QWidget):

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

        main_layout = QVBoxLayout()

        self.banner = QLabel(self)
        self.banner.setText("Hey")
        self.banner.setFixedSize(720,20)
        self.banner.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.banner)

        button_layout = QHBoxLayout()

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_button_effect)
        button_layout.addWidget(self.reset_button)

        self.return_button = QPushButton("Return")
        self.return_button.clicked.connect(self.return_button_effect)
        button_layout.addWidget(self.return_button)

        main_layout.addLayout(button_layout)
        
        self.board = GUIBoard(self,self.game)
        main_layout.addWidget(self.board)

        self.setMinimumSize(QSize(760, 660))
        self.setStyleSheet('background-color: #338888;')
        self.setLayout(main_layout)

    def reset_button_effect(self):
        self.game.restart()
        self.game.play()

    def return_button_effect(self):
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

        


class MainWindow(QMainWindow):

    #this is probably unneeded
    open : bool
    
    stack : QStackedWidget
    main_menu : MainMenu
    game_view : GameView
    
    def __init__(self,game):
        super().__init__()

        self.open = True

        self.stack = QStackedWidget()

        #self.setMinimumSize(QSize(760, 660))

        self.setStyleSheet('background-color: #338888;')
        
        self.main_menu = MainMenu(self.stack, self)
        self.stack.addWidget(self.main_menu)
        self.game_view = GameView(self.stack, self, game)
        self.stack.addWidget(self.game_view)
        self.setCentralWidget(self.stack)

    def update(self):
        self.main_menu.update()
        self.game_view.update()

    def closeEvent(self, event):
        self.open = False
        print("I just got closed")
        super().closeEvent(event)

    def start_game(self):
        self.stack.setCurrentWidget(self.game_view)
        self.game_view.game.play()

    def go_to_menu(self):
        self.stack.setCurrentWidget(self.main_menu)

    @property
    def tiles(self):
        return self.game_view.tiles
    
    def enable_tiles(self):
        return self.game_view.enable_tiles()
    
    def disable_tiles(self):
        return self.game_view.disable_tiles()
    
    def set_banner_text(self, text):
        self.game_view.set_banner_text(text)                

class GUI:

    app : QApplication
    window : MainWindow
    profile_manager : ProfileManager

    def init(self):
        self.app = QApplication([])
        self.app.setStyle('Fusion')
        self.game = Game(self)
        self.profile_manager = ProfileManager(Path("profiles"))
        self.window = MainWindow(self.game)
        self.window.show()

        self.window.update()
        #self.game.play()
        self.run()
    
    def run(self):
        if self.window.open:
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
    
    def set_banner_text(self, text):
        return self.window.set_banner_text(text)


if __name__ == "__main__":
    gui = GUI()
    gui.init()
