import pathlib
import pickle

from .profile_ import Profile

class ProfileManager:
    
    active_profile : Profile
    profiles : list[Profile]
    path : pathlib.Path

    def __init__(self, path):
        self.path = path
        self.load()

    def load(self):
        if self.path.is_file():
            f = open(self.path, 'rb')
            tmp_dict = pickle.load(f)
            f.close()          

            self.__dict__.update(tmp_dict) 


    def save(self):
        f = open(self.path, 'wb')
        pickle.dump(self.__dict__, f)
        f.close()