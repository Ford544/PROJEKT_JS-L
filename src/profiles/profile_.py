class Profile:
    name : str
    wins : int
    losses : int
    draws : int

    def __init__(self, name : str):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.draws = 0
        
    def register_win(self) -> None:
        self.wins += 1

    def register_loss(self) -> None:
        self.losses += 1
    
    def register_draw(self) -> None:
        self.draws += 1
  
    @property
    def games(self) -> int:
        return self.wins + self.losses + self.draws

    @property
    def win_ratio(self) -> float:
        if self.games == 0:
            return -1
        return self.wins / self.games