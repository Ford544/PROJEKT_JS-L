from functools import partial
from pathlib import Path
import time

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QPainter, QPen, QColor

from ..game.game import Game
from ..profiles.profile_ import Profile
from ..profiles.profile_manager import ProfileManager
from .gui_board import GUIBoard


class MainMenu(QFrame):

    window : QMainWindow

    quick_start_button : QPushButton
    new_game_button : QPushButton
    profiles_button : QPushButton

    profile_name_banner : QLabel
    
    def __init__(self, parent, window):
    
        super().__init__(parent)
        self.window = window


        main_layout = QHBoxLayout()
        
        button_layout = QVBoxLayout()

        button_layout.addStretch()
        self.quick_start_button = QPushButton("Quick start")
        self.quick_start_button.clicked.connect(self.quick_start_button_effect)
        button_layout.addWidget(self.quick_start_button)

        self.new_game_button = QPushButton("New game")
        self.new_game_button.clicked.connect(self.new_game_button_effect)
        button_layout.addWidget(self.new_game_button)

        self.profiles_button = QPushButton("Profiles")
        self.profiles_button.clicked.connect(self.profiles_button_effect)
        button_layout.addWidget(self.profiles_button)
        button_layout.addStretch()

        self.profile_name_banner = QLabel()
        self.profile_name_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_profile_name_message()
        button_layout.addWidget(self.profile_name_banner)
        

        main_layout.addStretch(stretch=1)
        main_layout.addLayout(button_layout,stretch=1)
        main_layout.addStretch(stretch=1)

        self.setLayout(main_layout)
        self.setStyleSheet('background-color: #338888;')

    def quick_start_button_effect(self):
        self.window.quick_game()

    def profiles_button_effect(self):
        self.window.enter_profiles_menu()

    def new_game_button_effect(self):
        self.window.enter_new_game_menu()

    def set_profile_name_message(self):
        if self.window.manager.active_profile is not None:
            self.profile_name_banner.setText(f"Welcome, {self.window.manager.active_profile.name}!")
        else:
            self.profile_name_banner.setText(f"Welcome!")
        

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

class ProfileManagerMenu(QFrame):

    window : QMainWindow
    manager : ProfileManager
    profile_list : QListWidget
    name_field : QLineEdit
    choose_button : QPushButton
    add_button : QPushButton
    remove_button : QPushButton
    return_button : QPushButton
    stat_labels : dict[str,QLabel]



    def __init__(self, parent, window : QMainWindow, manager : ProfileManager):
        super().__init__(parent)
        self.window = window
        self.manager = manager

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        self.profile_list = QListWidget()
        self.profile_list.itemSelectionChanged.connect(self.profile_list_selection_change_effect)
        self.load_data()
        
        self.name_field = QLineEdit()
        button_layout = QHBoxLayout()
        self.choose_button = QPushButton("Choose")
        self.choose_button.clicked.connect(self.choose_button_effect)
        self.add_button = QPushButton("Create profile")
        self.add_button.clicked.connect(self.add_profile)
        self.remove_button = QPushButton("Remove profile")
        self.remove_button.clicked.connect(self.remove_profile)
        self.return_button = QPushButton("Back")
        self.return_button.clicked.connect(self.return_button_effect)
        button_layout.addWidget(self.choose_button, stretch=1)
        button_layout.addStretch(stretch = 1)
        button_layout.addWidget(self.add_button, stretch=1)
        button_layout.addStretch(stretch = 1)
        button_layout.addWidget(self.remove_button, stretch=1)
        button_layout.addStretch(stretch=1)
        button_layout.addWidget(self.return_button, stretch=1)


        left_layout.addWidget(self.profile_list)
        left_layout.addWidget(self.name_field)
        left_layout.addLayout(button_layout)

        right_layout = QVBoxLayout()

        self.stat_labels = {}
        self.stat_labels["total_games"] = QLabel()
        self.stat_labels["wins"] = QLabel()
        self.stat_labels["losses"] = QLabel()
        self.stat_labels["win_ratio"] = QLabel()
        self.clear_stats()
        for label in self.stat_labels.values():
            #print(label)
            right_layout.addWidget(label)

        if manager.active_profile is not None:
            self.profile_list.setCurrentItem(self.profile_list.findItems(self.manager.active_profile.name,Qt.MatchFlag.MatchExactly)[0])

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def load_data(self) -> None:
        self.profile_list.clear()
        for profile in self.manager.profiles:
            self.profile_list.addItem(profile.name)

    def clear_stats(self) -> None:
        self.stat_labels["total_games"].setText(f"Total games played: -")
        self.stat_labels["wins"].setText(f"Games won: -")
        self.stat_labels["losses"].setText(f"Games lost: -")
        self.stat_labels["win_ratio"].setText(f"Win ratio: -")

    #enable/disable buttons?
    def profile_list_selection_change_effect(self) -> None:
        selected = self.profile_list.currentItem()
        print(selected.text())
        if selected is not None:
            profile = self.manager.get_profile(selected.text())
            if profile is not None:
                self.stat_labels["total_games"].setText(f"Total games played: {profile.games}")
                self.stat_labels["wins"].setText(f"Games won: {profile.wins}")
                self.stat_labels["losses"].setText(f"Games lost: {profile.losses}")
                if profile.win_ratio == -1:
                    percentage = "-"
                else:
                    percentage = f"{int(profile.win_ratio * 100)}%"
                self.stat_labels["win_ratio"].setText(f"Win ratio: {percentage}")
            else:
                self.clear_stats()
        else:
            self.clear_stats()

    def choose_button_effect(self):
        selected = self.profile_list.currentItem()
        profile = self.manager.get_profile(selected.text())
        if profile is not None:
            self.manager.active_profile = profile
            self.window.go_to_menu()
    
    def add_profile(self):
        text = self.name_field.text().strip()
        if text:
            if not self.manager.add_profile(text):
                QMessageBox.warning(self, "Input Error", "Please enter a valid item.")
            else:
                self.load_data()
            self.name_field.clear()


    def remove_profile(self):
        selected = self.profile_list.currentItem()
        if selected is not None:
            self.manager.remove_profile(selected.text())
            self.load_data()

    def return_button_effect(self):
        self.window.go_to_menu()

class NewGameMenu(QFrame):

    window : QMainWindow

    user1_name_input : QLineEdit
    user1_radio_group : QButtonGroup
    user2_name_input : QLineEdit
    user2_radio_group : QButtonGroup
    size_radio_group : QButtonGroup
    capturing_obligatory_checkbox : QCheckBox

    def __init__(self, parent, window : QMainWindow):

        super().__init__(parent)
        self.window = window

        main_layout = QHBoxLayout()

        menu_layout = QVBoxLayout()

        user1_layout = QVBoxLayout()
        user1_button_layout = QHBoxLayout()

        self.user1_name_input = QLineEdit()
        if window.manager.active_profile is not None:
            human_name = window.manager.active_profile.name
        else:
            human_name = "Human"
        self.user1_name_input.setText(human_name)
        self.user1_radio_group = QButtonGroup()
        human_radio = QRadioButton("Human")
        self.user1_radio_group.addButton(human_radio)
        self.user1_radio_group.setId(human_radio, -2)
        user1_button_layout.addWidget(human_radio)
        random_radio = QRadioButton("Random AI")
        self.user1_radio_group.addButton(random_radio)
        self.user1_radio_group.setId(random_radio, 0)
        user1_button_layout.addWidget(random_radio)
        weak_radio = QRadioButton("Weak AI")
        self.user1_radio_group.addButton(weak_radio)
        self.user1_radio_group.setId(weak_radio, 2)
        user1_button_layout.addWidget(weak_radio)
        strong_radio = QRadioButton("Strong AI")
        self.user1_radio_group.addButton(strong_radio)
        self.user1_radio_group.setId(strong_radio, 3)
        user1_button_layout.addWidget(strong_radio)
        human_radio.setChecked(True)
        #checkbox for profile player?

        user1_layout.addWidget(self.user1_name_input)
        user1_layout.addLayout(user1_button_layout)

        user2_layout = QVBoxLayout()
        user2_button_layout = QHBoxLayout()

        self.user2_name_input = QLineEdit()
        self.user2_name_input.setText("AI")
        self.user2_radio_group = QButtonGroup()
        human_radio = QRadioButton("Human")
        self.user2_radio_group.addButton(human_radio)
        self.user2_radio_group.setId(human_radio, -2)
        user2_button_layout.addWidget(human_radio)
        random_radio = QRadioButton("Random AI")
        self.user2_radio_group.addButton(random_radio)
        self.user2_radio_group.setId(random_radio, 0)
        user2_button_layout.addWidget(random_radio)
        weak_radio = QRadioButton("Weak AI")
        self.user2_radio_group.addButton(weak_radio)
        self.user2_radio_group.setId(weak_radio, 2)
        user2_button_layout.addWidget(weak_radio)
        strong_radio = QRadioButton("Strong AI")
        self.user2_radio_group.addButton(strong_radio)
        self.user2_radio_group.setId(strong_radio, 3)
        user2_button_layout.addWidget(strong_radio)
        weak_radio.setChecked(True)
        #checkbox for profile player?

        user2_layout.addWidget(self.user2_name_input)
        user2_layout.addLayout(user2_button_layout)

        size_layout = QHBoxLayout()

        self.size_radio_group = QButtonGroup()
        size8_button = QRadioButton("8x8")
        self.size_radio_group.addButton(size8_button)
        self.size_radio_group.setId(size8_button, 8)
        size_layout.addWidget(size8_button)
        size10_button = QRadioButton("10x10")
        self.size_radio_group.addButton(size10_button)
        self.size_radio_group.setId(size10_button, 10)
        size_layout.addWidget(size10_button)
        size8_button.setChecked(True)

        settings_layout = QVBoxLayout()
        self.capturing_obligatory_checkbox = QCheckBox("Capturing obligatory")
        self.capturing_obligatory_checkbox.setChecked(True)

        settings_layout.addWidget(self.capturing_obligatory_checkbox)

        start_button = QPushButton("Start game")
        start_button.clicked.connect(self.start_button_effect)

        menu_layout.addLayout(user1_layout)
        menu_layout.addLayout(user2_layout)
        menu_layout.addLayout(size_layout)
        menu_layout.addLayout(settings_layout)
        menu_layout.addWidget(start_button)

        main_layout.addStretch(stretch=1)
        main_layout.addLayout(menu_layout)
        main_layout.addStretch(stretch=1)

        self.setLayout(main_layout)

    def start_button_effect(self) -> None:
        if self.user1_name_input.text() == "":
            return
        if self.user2_name_input.text() == "":
            return
        self.window.start_game(self.size_radio_group.checkedId(), self.capturing_obligatory_checkbox.isChecked(),
                              self.user1_radio_group.checkedId(),self.user1_name_input.text(),
                              self.user2_radio_group.checkedId(),self.user2_name_input.text())
        



        

        
            
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
        self.manager.save()
        super().closeEvent(event)

    def quick_game(self):
        if self.manager.active_profile is None:
            human_name = "Human"
        else:
            human_name = self.manager.active_profile.name
        self.start_game(8, True, -2, human_name, 3, "SI")

    def start_game(self, size : int, capturing_obligatory : bool, player1_mode : int, player1_name : str, 
                  player2_mode : int, player2_name :str):
        self.game_view.game.configure(size,capturing_obligatory,player1_mode,player1_name,player2_mode,player2_name)
        self.stack.setCurrentWidget(self.game_view)
        self.game_view.board.set_up()
        self.game_view.game.play()

    def go_to_menu(self):
        self.main_menu.set_profile_name_message()
        self.stack.setCurrentWidget(self.main_menu)

    def enter_profiles_menu(self):
        self.profile_menu.load_data()
        self.stack.setCurrentWidget(self.profile_menu)

    def enter_new_game_menu(self):
        self.stack.setCurrentWidget(self.new_game_menu)

    def configure(self, size : int, capturing_obligatory : bool, player1_mode : int, player1_name : str, 
                  player2_mode : int, player2_name :str) -> None:
        self.game_view.game.configure(size,capturing_obligatory,player1_mode,player1_name,player2_mode,player2_name)

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
    #unneeded?
    manager : ProfileManager

    def init(self):
        self.app = QApplication([])
        self.app.setStyle('Fusion')
        self.manager = ProfileManager(Path("profiles"))
        self.manager.load()
        self.game = Game(self,self.manager)
        self.window = MainWindow(self.game, self.manager)
        self.window.show()

        self.window.update()
        #self.game.play()
        self.run()
    
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
    
    def set_banner_text(self, text):
        return self.window.set_banner_text(text)


if __name__ == "__main__":
    gui = GUI()
    gui.init()
