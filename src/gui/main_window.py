from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ..profiles.profile_manager import ProfileManager
from .main_menu import MainMenu
from .game_view import GameView
from .profile_manager_menu import ProfileManagerMenu
from .new_game_menu import NewGameMenu


class MainWindow(QMainWindow):

    stack : QStackedWidget
    main_menu : MainMenu
    game_view : GameView
    profile_menu : ProfileManagerMenu
    new_game_menu : NewGameMenu
    manager : ProfileManager
    
    def __init__(self,game, manager):
        super().__init__()

        self.stack = QStackedWidget()
        self.manager = manager

        #self.setMinimumSize(QSize(760, 660))

        #self.setStyleSheet('background-color: #338888;')
        
        self.main_menu = MainMenu(self.stack, self)
        self.stack.addWidget(self.main_menu)
        self.game_view = GameView(self.stack, self, game)
        self.stack.addWidget(self.game_view)
        self.profile_menu = ProfileManagerMenu(self.stack, self, manager)
        self.stack.addWidget(self.profile_menu)
        self.new_game_menu = NewGameMenu(self.stack, self)
        self.stack.addWidget(self.new_game_menu)

        self.setCentralWidget(self.stack)

    def update(self):
        self.main_menu.update()
        self.game_view.update()

    def closeEvent(self, event):
        self.game_view.game.paused = True
        self.manager.save()
        super().closeEvent(event)

    def quick_game(self) -> None:
        if self.manager.active_profile is None:
            human_name = "Human"
        else:
            human_name = self.manager.active_profile.name
        self.start_game(8, True, -2, human_name, 3, "SI", 1)

    def start_game(self, size : int, capturing_obligatory : bool, player1_mode : int, player1_name : str, 
                  player2_mode : int, player2_name : str, profile_player : int) -> None:
        self.game_view.game.configure(size,capturing_obligatory,player1_mode,player1_name,player2_mode,player2_name, profile_player)
        self.stack.setCurrentWidget(self.game_view)
        self.game_view.board.set_up()
        self.game_view.game.paused = False
        self.game_view.game.play()

    def go_to_menu(self) -> None:
        self.main_menu.set_profile_name_message()
        self.stack.setCurrentWidget(self.main_menu)

    def enter_profiles_menu(self) -> None:
        self.profile_menu.load_data()
        self.stack.setCurrentWidget(self.profile_menu)

    def enter_new_game_menu(self) -> None:
        self.stack.setCurrentWidget(self.new_game_menu)

    def configure(self, size : int, capturing_obligatory : bool, player1_mode : int, player1_name : str, 
                  player2_mode : int, player2_name :str) -> None:
        self.game_view.game.configure(size,capturing_obligatory,player1_mode,player1_name,player2_mode,player2_name)

    
    def enable_tiles(self):
        return self.game_view.enable_tiles()
    
    def disable_tiles(self):
        return self.game_view.disable_tiles()
    
    def set_banner_text(self, text):
        self.game_view.set_banner_text(text)