from pathlib import Path

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ..game.game import Game
from ..profiles.profile_manager import ProfileManager
from .main_window import MainWindow

class GUI:

    app : QApplication
    game : Game
    window : MainWindow
    manager : ProfileManager

    def init(self):
        self.app = QApplication([])
        self.manager = ProfileManager(Path("profiles"))
        self.manager.load()
        self.game = Game(self,self.manager)
        self.window = MainWindow(self.game, self.manager)
        self.window.show()

        self.window.update()
        self.run()
    
    def run(self) -> None:
        self.app.exec()

    def update(self) -> None:
        self.window.update()

    def processEvents(self):
        self.app.processEvents()

    def enable_tiles(self):
        return self.window.enable_tiles()

    def disable_tiles(self):
        return self.window.disable_tiles()
    
    def set_banner_text(self, text : str) -> None:
        return self.window.set_banner_text(text)