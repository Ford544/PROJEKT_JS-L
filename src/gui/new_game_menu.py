from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ..consts import CAPTURING_OPTIONAL, CAPTURING_OBLIGATORY, MAXIMUM_CAPTURING_OBLIGATORY, BRAZILIAN, POLISH, AMERICAN, CANADIAN, RUSSIAN, MENU_STYLE

class NewGameMenu(QFrame):

    window : QMainWindow

    user1_name_input : QLineEdit
    user1_radio_group : QButtonGroup
    user2_name_input : QLineEdit
    user2_radio_group : QButtonGroup
    ruleset_radio_group : QButtonGroup
    size_radio_group : QButtonGroup
    capturing_obligatory_radio_group : QButtonGroup
    profile_player_radio_group  : QButtonGroup
    pieces_capturing_backwards_checkbox : QCheckBox
    flying_kings_checkbox : QCheckBox
    mid_jump_crowning_checkbox : QCheckBox
    start_button : QPushButton
    host_button : QPushButton


    def __init__(self, parent, window : QMainWindow):

        super().__init__(parent)
        self.window = window

        main_layout = QHBoxLayout()

        menu_layout = QVBoxLayout()

        menu_frame = QFrame()
        menu_frame.setLayout(menu_layout)
        menu_frame.setStyleSheet(MENU_STYLE)

        user1_layout = QVBoxLayout()
        user1_button_layout = QHBoxLayout()

        self.profile_player_radio_group = QButtonGroup()
        #this isn't mean to be visible, it only serves as the third option for profile player radio group
        neither_profile_radio = QRadioButton()
        self.profile_player_radio_group.addButton(neither_profile_radio)
        self.profile_player_radio_group.setId(neither_profile_radio,0)
        neither_profile_radio.setHidden(True)

        self.user1_name_input = QLineEdit()
        self.user1_radio_group = QButtonGroup()

        self.make_radio_button("Human", self.user1_radio_group, -2, user1_button_layout)
        self.make_radio_button("Random AI", self.user1_radio_group, 0, user1_button_layout)
        self.make_radio_button("Weak AI", self.user1_radio_group, 2, user1_button_layout)
        self.make_radio_button("Strong AI", self.user1_radio_group, 3, user1_button_layout)
        self.make_radio_button("Remote", self.user1_radio_group, -4, user1_button_layout)
        self.user1_radio_group.button(-2).setChecked(True)
        
        user1_layout.addWidget(self.user1_name_input)
        user1_layout.addLayout(user1_button_layout)

        self.make_radio_button("Profile player", self.profile_player_radio_group, 1, user1_layout)
        self.profile_player_radio_group.button(1).setHidden(True)

        user2_layout = QVBoxLayout()
        user2_button_layout = QHBoxLayout()

        self.user2_name_input = QLineEdit()
        self.user2_name_input.setText("AI")
        self.user2_radio_group = QButtonGroup()
        
        self.make_radio_button("Human", self.user2_radio_group, -2, user2_button_layout)
        self.make_radio_button("Random AI", self.user2_radio_group, 0, user2_button_layout)
        self.make_radio_button("Weak AI", self.user2_radio_group, 2, user2_button_layout)
        self.make_radio_button("Strong AI", self.user2_radio_group, 3, user2_button_layout)
        self.make_radio_button("Remote", self.user2_radio_group, -4, user2_button_layout)
        self.user2_radio_group.button(2).setChecked(True)

        user2_layout.addWidget(self.user2_name_input)
        user2_layout.addLayout(user2_button_layout)
        
        self.make_radio_button("Profile player", self.profile_player_radio_group, 2, user2_layout)
        self.profile_player_radio_group.button(2).setHidden(True)

        self.profile_player_radio_group.button(1).setChecked(True)

        self.user1_radio_group.buttonToggled.connect(self.player_mode_change)
        self.user2_radio_group.buttonToggled.connect(self.player_mode_change)

        self.ruleset_radio_group = QButtonGroup()
        ruleset_layout = QHBoxLayout()

        self.make_radio_button("Brazilian", self.ruleset_radio_group, BRAZILIAN, ruleset_layout)
        self.make_radio_button("Polish/International", self.ruleset_radio_group, POLISH, ruleset_layout)
        self.make_radio_button("American/British", self.ruleset_radio_group, AMERICAN, ruleset_layout)
        self.make_radio_button("Canadian", self.ruleset_radio_group, CANADIAN, ruleset_layout)
        self.make_radio_button("Russian", self.ruleset_radio_group, RUSSIAN, ruleset_layout)
        self.ruleset_radio_group.buttonToggled.connect(self.ruleset_change)

        size_layout = QHBoxLayout()
        self.size_radio_group = QButtonGroup()

        self.make_radio_button("8x8", self.size_radio_group, 8, size_layout)
        self.make_radio_button("10x10", self.size_radio_group, 10, size_layout)
        self.make_radio_button("12x12", self.size_radio_group, 12, size_layout)
        self.size_radio_group.button(8).setChecked(True)

        settings_layout = QVBoxLayout()

        capturing_obligatory_layout = QHBoxLayout()
        self.capturing_obligatory_radio_group = QButtonGroup()

        self.make_radio_button("Capturing optional", self.capturing_obligatory_radio_group, CAPTURING_OPTIONAL, capturing_obligatory_layout)
        self.make_radio_button("Capturing obligatory", self.capturing_obligatory_radio_group, CAPTURING_OBLIGATORY, capturing_obligatory_layout)
        self.make_radio_button("Maximum capturing optional", self.capturing_obligatory_radio_group, MAXIMUM_CAPTURING_OBLIGATORY, capturing_obligatory_layout)
        self.capturing_obligatory_radio_group.button(MAXIMUM_CAPTURING_OBLIGATORY).setChecked(True)

        self.pieces_capturing_backwards_checkbox = QCheckBox("Pieces capturing backwards")

        self.flying_kings_checkbox = QCheckBox("Flying kings")

        self.mid_jump_crowning_checkbox = QCheckBox("Mid-jump crowning")

        settings_layout.addLayout(capturing_obligatory_layout)
        settings_layout.addWidget(self.pieces_capturing_backwards_checkbox)
        settings_layout.addWidget(self.flying_kings_checkbox)
        settings_layout.addWidget(self.mid_jump_crowning_checkbox)

        self.ruleset_radio_group.button(BRAZILIAN).setChecked(True)

        nav_buttons_layout = QHBoxLayout()

        self.start_button = QPushButton("Start game")
        self.start_button.clicked.connect(self.start_button_effect)

        return_button = QPushButton("Back")
        return_button.clicked.connect(self.return_button_effect)

        self.host_button = QPushButton("Host game")
        self.host_button.clicked.connect(self.host_button_effect)
        self.host_button.setDisabled(True)

        nav_buttons_layout.addWidget(self.start_button, stretch=1)
        nav_buttons_layout.addStretch(stretch=1)
        nav_buttons_layout.addWidget(self.host_button)
        nav_buttons_layout.addStretch(stretch=1)
        nav_buttons_layout.addWidget(return_button,stretch=1)        

        menu_layout.addWidget(neither_profile_radio)
        menu_layout.addLayout(user1_layout)
        menu_layout.addLayout(user2_layout)
        menu_layout.addLayout(ruleset_layout)
        menu_layout.addLayout(size_layout)
        menu_layout.addLayout(settings_layout)
        menu_layout.addLayout(nav_buttons_layout)

        main_layout.addStretch(stretch=1)
        main_layout.addWidget(menu_frame)
        main_layout.addStretch(stretch=1)

        self.setLayout(main_layout)

        self.setStyleSheet('QFrame { background-color: #338888; }')

        self.set_up()

    def set_up(self) -> None:
        if self.window.manager.active_profile is not None:
            human_name = self.window.manager.active_profile.name
        else:
            human_name = "Human"
        self.user1_name_input.setText(human_name)

    def start_button_effect(self) -> None:
        if self.user1_name_input.text() == "":
            return
        if self.user2_name_input.text() == "":
            return
        self.window.start_game(self.size_radio_group.checkedId(), self.capturing_obligatory_radio_group.checkedId(), 
                               self.pieces_capturing_backwards_checkbox.isChecked(), 
                               self.flying_kings_checkbox.isChecked(), self.mid_jump_crowning_checkbox.isChecked(), 
                               self.user1_radio_group.checkedId(), self.user1_name_input.text(), 
                               self.user2_radio_group.checkedId(),self.user2_name_input.text(), 
                               self.profile_player_radio_group.checkedId())
        
    def host_button_effect(self) -> None:
        if self.user1_name_input.text() == "":
            return
        if self.user2_name_input.text() == "":
            return
        port, ok = QInputDialog.getInt(self, "Host game", "Choose port", 52000, 49152, 65535)
        if ok:
            self.window.host_game(self.size_radio_group.checkedId(), self.capturing_obligatory_radio_group.checkedId(), 
                                self.pieces_capturing_backwards_checkbox.isChecked(), 
                                self.flying_kings_checkbox.isChecked(), self.mid_jump_crowning_checkbox.isChecked(), 
                                self.user1_radio_group.checkedId(), self.user1_name_input.text(), 
                                self.user2_radio_group.checkedId(),self.user2_name_input.text(), 
                                self.profile_player_radio_group.checkedId(), port)
        
    def return_button_effect(self) -> None:
        self.window.go_to_menu()
        
    def player_mode_change(self) -> None:
        user1_mode = self.user1_radio_group.checkedId()
        user2_mode = self.user2_radio_group.checkedId()
        if user1_mode >= 0 and user2_mode >= 0:
            self.profile_player_radio_group.button(0).setChecked(True)
            self.profile_player_radio_group.button(1).setHidden(True)
            self.profile_player_radio_group.button(2).setHidden(True)
        if user1_mode == -2 and user2_mode >= 0:
            self.profile_player_radio_group.button(1).setChecked(True)
            self.profile_player_radio_group.button(1).setHidden(True)
            self.profile_player_radio_group.button(2).setHidden(True)
        if user1_mode >= 0 and user2_mode == -2:
            self.profile_player_radio_group.button(2).setChecked(True)
            self.profile_player_radio_group.button(1).setHidden(True)
            self.profile_player_radio_group.button(2).setHidden(True)
        if user1_mode == -2 and user2_mode == -2:
            self.profile_player_radio_group.button(1).setChecked(True)
            self.profile_player_radio_group.button(1).setHidden(False)
            self.profile_player_radio_group.button(2).setHidden(False)
        if user1_mode == -4:
            self.profile_player_radio_group.button(2).setChecked(True)
            self.profile_player_radio_group.button(1).setHidden(True)
            self.profile_player_radio_group.button(2).setHidden(True)
            self.user2_radio_group.button(-2).setChecked(True)
            self.host_button.setDisabled(False)
            self.start_button.setDisabled(True)
        elif user2_mode == -4:
            self.profile_player_radio_group.button(1).setChecked(True)
            self.profile_player_radio_group.button(1).setHidden(True)
            self.profile_player_radio_group.button(2).setHidden(True)
            self.user1_radio_group.button(-2).setChecked(True)
            self.host_button.setDisabled(False)
            self.start_button.setDisabled(True)
        else:
            self.host_button.setDisabled(True)
            self.start_button.setDisabled(False)

    def ruleset_change(self) -> None:
        ruleset = self.ruleset_radio_group.checkedId()
        if ruleset == BRAZILIAN:
            self.apply_ruleset(8, MAXIMUM_CAPTURING_OBLIGATORY, True, True, False)
        elif ruleset == POLISH:
            self.apply_ruleset(10, MAXIMUM_CAPTURING_OBLIGATORY, True, True, False)
        elif ruleset == AMERICAN:
            self.apply_ruleset(8, CAPTURING_OBLIGATORY, False, False, False)
        elif ruleset == CANADIAN:
            self.apply_ruleset(12, MAXIMUM_CAPTURING_OBLIGATORY, True, True, False)
        elif ruleset == RUSSIAN:
            self.apply_ruleset(8, CAPTURING_OBLIGATORY, True, True, True)

    def apply_ruleset(self, size : int, capturing_obligatory : int, capturing_backwards : bool, flying_kings : bool, 
                      mid_jump_crowning : bool) -> None:
        self.size_radio_group.button(size).click()
        self.capturing_obligatory_radio_group.button(capturing_obligatory).setChecked(True)
        self.pieces_capturing_backwards_checkbox.setChecked(capturing_backwards)
        self.flying_kings_checkbox.setChecked(flying_kings)
        self.mid_jump_crowning_checkbox.setChecked(mid_jump_crowning)

    def make_radio_button(self, text : str, group : QButtonGroup, id : int, layout : QLayout) -> None:
        radio = QRadioButton(text)
        group.addButton(radio)
        group.setId(radio, id)
        layout.addWidget(radio)