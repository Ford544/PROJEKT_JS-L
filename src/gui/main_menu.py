from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ..consts import MENU_STYLE

class MainMenu(QFrame):

    window : QMainWindow

    quick_start_button : QPushButton
    new_game_button : QPushButton
    profiles_button : QPushButton
    join_button : QPushButton
    profile_name_banner : QLabel
    
    def __init__(self, parent, window : QMainWindow):
    
        super().__init__(parent)
        self.window = window

        banner = QLabel("Checkers")
        banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner.setStyleSheet("QLabel { font-size: 20pt }")

        main_layout = QHBoxLayout()
        
        button_layout = QVBoxLayout()

        central_frame = QFrame()
        central_frame.setLayout(button_layout)
        central_frame.setStyleSheet(MENU_STYLE)

        button_layout.addWidget(banner)
        button_layout.addStretch()
        self.quick_start_button = QPushButton("Quick start")
        self.quick_start_button.clicked.connect(self.quick_start_button_effect)
        button_layout.addWidget(self.quick_start_button)

        self.new_game_button = QPushButton("New game")
        self.new_game_button.clicked.connect(self.new_game_button_effect)
        button_layout.addWidget(self.new_game_button)

        self.join_button = QPushButton("Join")
        self.join_button.clicked.connect(self.join_button_effect)
        button_layout.addWidget(self.join_button)

        self.profiles_button = QPushButton("Profiles")
        self.profiles_button.clicked.connect(self.profiles_button_effect)
        button_layout.addWidget(self.profiles_button)
        button_layout.addStretch()

        self.profile_name_banner = QLabel()
        self.profile_name_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_profile_name_message()
        button_layout.addWidget(self.profile_name_banner)
        
        main_layout.addStretch(stretch=1)
        main_layout.addWidget(central_frame,stretch=1)
        main_layout.addStretch(stretch=1)

        self.setLayout(main_layout)
        self.setStyleSheet('background-color: #338888;')

    def quick_start_button_effect(self) -> None:
        self.window.quick_game()

    def profiles_button_effect(self) -> None:
        self.window.enter_profiles_menu()

    def new_game_button_effect(self) -> None:
        self.window.enter_new_game_menu()

    def join_button_effect(self):
        self.window.connect_to_game()

    def set_profile_name_message(self) -> None:
        if self.window.manager.active_profile is not None:
            self.profile_name_banner.setText(f"Welcome, {self.window.manager.active_profile.name}!")
        else:
            self.profile_name_banner.setText(f"Welcome!")