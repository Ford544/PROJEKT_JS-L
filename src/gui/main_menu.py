from PySide6.QtWidgets import *
from PySide6.QtCore import *

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