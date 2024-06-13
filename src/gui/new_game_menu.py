from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ..consts import CAPTURING_OPTIONAL, CAPTURING_OBLIGATORY, MAXIMUM_CAPTURING_OBLIGATORY, BRAZILIAN, POLISH, AMERICAN, CANADIAN, RUSSIAN


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


    def __init__(self, parent, window : QMainWindow):

        super().__init__(parent)
        self.window = window

        main_layout = QHBoxLayout()

        menu_layout = QVBoxLayout()

        user1_layout = QVBoxLayout()
        user1_button_layout = QHBoxLayout()

        self.profile_player_radio_group = QButtonGroup()
        #this isn't mean to be visible, it only serves as the third option for profile player radio group
        neither_profile_radio = QRadioButton()
        self.profile_player_radio_group.addButton(neither_profile_radio)
        self.profile_player_radio_group.setId(neither_profile_radio,0)
        neither_profile_radio.setHidden(True)

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
        user1_profile_radio = QRadioButton("Profile player")
        self.profile_player_radio_group.addButton(user1_profile_radio)
        self.profile_player_radio_group.setId(user1_profile_radio,1)
        user1_profile_radio.setHidden(True)

        user1_layout.addWidget(self.user1_name_input)
        user1_layout.addLayout(user1_button_layout)
        user1_layout.addWidget(user1_profile_radio)

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
        user2_profile_radio = QRadioButton("Profile player")
        self.profile_player_radio_group.addButton(user2_profile_radio)
        self.profile_player_radio_group.setId(user2_profile_radio,2)
        user2_profile_radio.setHidden(True)

        user1_profile_radio.setChecked(True)

        user2_layout.addWidget(self.user2_name_input)
        user2_layout.addLayout(user2_button_layout)
        user2_layout.addWidget(user2_profile_radio)

        self.user1_radio_group.buttonToggled.connect(self.player_mode_change)
        self.user2_radio_group.buttonToggled.connect(self.player_mode_change)

        self.ruleset_radio_group = QButtonGroup()
        ruleset_layout = QHBoxLayout()
        brazilian_ruleset_radio = QRadioButton("Brazilian")
        self.ruleset_radio_group.addButton(brazilian_ruleset_radio)
        self.ruleset_radio_group.setId(brazilian_ruleset_radio, BRAZILIAN)
        ruleset_layout.addWidget(brazilian_ruleset_radio)
        polish_ruleset_radio = QRadioButton("Polish/International")
        self.ruleset_radio_group.addButton(polish_ruleset_radio)
        self.ruleset_radio_group.setId(polish_ruleset_radio, POLISH)
        ruleset_layout.addWidget(polish_ruleset_radio)
        american_ruleset_radio = QRadioButton("American/English")
        self.ruleset_radio_group.addButton(american_ruleset_radio)
        self.ruleset_radio_group.setId(american_ruleset_radio, AMERICAN)
        ruleset_layout.addWidget(american_ruleset_radio)
        canadian_ruleset_radio = QRadioButton("Canadian")
        self.ruleset_radio_group.addButton(canadian_ruleset_radio)
        self.ruleset_radio_group.setId(canadian_ruleset_radio, CANADIAN)
        ruleset_layout.addWidget(canadian_ruleset_radio)
        russian_ruleset_radio = QRadioButton("Russian")
        self.ruleset_radio_group.addButton(russian_ruleset_radio)
        self.ruleset_radio_group.setId(russian_ruleset_radio, RUSSIAN)
        ruleset_layout.addWidget(russian_ruleset_radio)
        # custom_ruleset_radio = QRadioButton("Custom")
        # self.ruleset_radio_group.addButton(custom_ruleset_radio)
        # self.ruleset_radio_group.setId(custom_ruleset_radio, RUSSIAN)
        # ruleset_layout.addWidget(custom_ruleset_radio)
        self.ruleset_radio_group.buttonToggled.connect(self.ruleset_change)

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
        size12_button = QRadioButton("12x12")
        self.size_radio_group.addButton(size12_button)
        self.size_radio_group.setId(size12_button, 12)
        size_layout.addWidget(size12_button)
        size8_button.setChecked(True)

        settings_layout = QVBoxLayout()

        self.capturing_obligatory_radio_group = QButtonGroup()
        capturing_optional_radio = QRadioButton("Capturing optional")
        self.capturing_obligatory_radio_group.addButton(capturing_optional_radio)
        self.capturing_obligatory_radio_group.setId(capturing_optional_radio, CAPTURING_OPTIONAL)
        capturing_obligatory_radio = QRadioButton("Capturing obligatory")
        self.capturing_obligatory_radio_group.addButton(capturing_obligatory_radio)
        self.capturing_obligatory_radio_group.setId(capturing_obligatory_radio, CAPTURING_OBLIGATORY)
        maximum_capturing_obligatory_radio = QRadioButton("Maximum capturing obligatory")
        self.capturing_obligatory_radio_group.addButton(maximum_capturing_obligatory_radio)
        self.capturing_obligatory_radio_group.setId(maximum_capturing_obligatory_radio,MAXIMUM_CAPTURING_OBLIGATORY)
        maximum_capturing_obligatory_radio.setChecked(True)

        capturing_obligatory_layout = QHBoxLayout()
        capturing_obligatory_layout.addWidget(capturing_optional_radio)
        capturing_obligatory_layout.addWidget(capturing_obligatory_radio)
        capturing_obligatory_layout.addWidget(maximum_capturing_obligatory_radio)

        self.pieces_capturing_backwards_checkbox = QCheckBox("Pieces capturing backwards")

        self.flying_kings_checkbox = QCheckBox("Flying kings")

        self.mid_jump_crowning_checkbox = QCheckBox("Mid-jump crowning")

        settings_layout.addLayout(capturing_obligatory_layout)
        settings_layout.addWidget(self.pieces_capturing_backwards_checkbox)
        settings_layout.addWidget(self.flying_kings_checkbox)
        settings_layout.addWidget(self.mid_jump_crowning_checkbox)

        brazilian_ruleset_radio.setChecked(True)

        start_button = QPushButton("Start game")
        start_button.clicked.connect(self.start_button_effect)

        menu_layout.addWidget(neither_profile_radio)
        menu_layout.addLayout(user1_layout)
        menu_layout.addLayout(user2_layout)
        menu_layout.addLayout(ruleset_layout)
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
        self.window.start_game(self.size_radio_group.checkedId(), self.capturing_obligatory_radio_group.checkedId(), 
                               self.pieces_capturing_backwards_checkbox.isChecked(), 
                               self.flying_kings_checkbox.isChecked(), self.mid_jump_crowning_checkbox.isChecked(), 
                               self.user1_radio_group.checkedId(), self.user1_name_input.text(), 
                               self.user2_radio_group.checkedId(),self.user2_name_input.text(), 
                               self.profile_player_radio_group.checkedId())
        
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

    def ruleset_change(self):
        ruleset = self.ruleset_radio_group.checkedId()
        if ruleset == BRAZILIAN:
            self.size_radio_group.button(8).click()
            self.capturing_obligatory_radio_group.button(MAXIMUM_CAPTURING_OBLIGATORY).setChecked(True)
            self.pieces_capturing_backwards_checkbox.setChecked(True)
            self.flying_kings_checkbox.setChecked(True)
            self.mid_jump_crowning_checkbox.setChecked(False)
        elif ruleset == POLISH:
            self.size_radio_group.button(10).click()
            self.capturing_obligatory_radio_group.button(MAXIMUM_CAPTURING_OBLIGATORY).setChecked(True)
            self.pieces_capturing_backwards_checkbox.setChecked(True)
            self.flying_kings_checkbox.setChecked(True)
            self.mid_jump_crowning_checkbox.setChecked(False)
        elif ruleset == AMERICAN:
            self.size_radio_group.button(8).click()
            self.capturing_obligatory_radio_group.button(CAPTURING_OBLIGATORY).setChecked(True)
            self.pieces_capturing_backwards_checkbox.setChecked(False)
            self.flying_kings_checkbox.setChecked(False)
            self.mid_jump_crowning_checkbox.setChecked(False)
        elif ruleset == CANADIAN:
            self.size_radio_group.button(12).click()
            self.capturing_obligatory_radio_group.button(MAXIMUM_CAPTURING_OBLIGATORY).setChecked(True)
            self.pieces_capturing_backwards_checkbox.setChecked(True)
            self.flying_kings_checkbox.setChecked(True)
            self.mid_jump_crowning_checkbox.setChecked(False)
        elif ruleset == RUSSIAN:
            self.size_radio_group.button(8).click()
            self.capturing_obligatory_radio_group.button(CAPTURING_OBLIGATORY).setChecked(True)
            self.pieces_capturing_backwards_checkbox.setChecked(True)
            self.flying_kings_checkbox.setChecked(True)
            self.mid_jump_crowning_checkbox.setChecked(True)


