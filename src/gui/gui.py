from pathlib import Path

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ..game.game import Game
from ..profiles.profile_manager import ProfileManager
from .main_window import MainWindow

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
