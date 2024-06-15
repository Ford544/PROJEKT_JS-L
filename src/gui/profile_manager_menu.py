from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ..profiles.profile_manager import ProfileManager


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
        self.stat_labels["draws"] = QLabel()
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
        self.stat_labels["draws"].setText("Draws: -")
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
                self.stat_labels["draws"].setText(f"Draws: {profile.draws}")
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