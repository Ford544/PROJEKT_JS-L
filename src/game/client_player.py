from .player import Player

class ClientPlayer(Player):
    
    def pass_control(self) -> bool:
        return True