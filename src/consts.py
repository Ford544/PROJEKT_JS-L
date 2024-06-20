#player/piece colors, also game results
WHITE = 1
BLACK = -1
DRAW = -2

DRAW_MOVE_THRESHOLD = 40

#rule codes
CAPTURING_OPTIONAL = 0
CAPTURING_OBLIGATORY = 1
MAXIMUM_CAPTURING_OBLIGATORY = 2

#rulesets
BRAZILIAN = 0
POLISH = 1
AMERICAN = 2
CANADIAN = 3
RUSSIAN = 4

MENU_STYLE = "QFrame{ background-color: #AAAAAA; border: 2px solid #CCCCCC; border-radius: 6px; font-size: 12pt}" + "QPushButton{ background-color: #777777; border: 2px solid #888888; border-radius: 5px; font-size: 12pt }" + "QPushButton:hover { background-color: #888888 }" + "QPushButton:disabled { background-color: #BBBBBB}" + "QLabel { border: 0px none}"