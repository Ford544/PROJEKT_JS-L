class Profile:
    name : str
    stats : dict[str,int]

    def __init__(self, name):
        self.name = name

        #initialize stats here
        self.stats = {}