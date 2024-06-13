class Profile:
    name : str
    stats : dict[str,int]

    def __init__(self, name : str):
        self.name = name

        #initialize stats here
        self.stats = {"wins" : 0,
                      "losses" : 0}
        
    def register_win(self) -> None:
        self.stats["wins"] += 1

    def register_loss(self) -> None:
        self.stats["losses"] += 1

    @property
    def wins(self):
        return self.stats["wins"]
    
    @property
    def losses(self) -> int:
        return self.stats["losses"]
    
    @property
    def games(self) -> int:
        return self.wins + self.losses

    @property
    def win_ratio(self) -> float:
        if self.games == 0:
            return -1
        return self.wins / self.games