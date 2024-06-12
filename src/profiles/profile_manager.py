import pathlib
import pickle

from .profile_ import Profile

class ProfileManager:
    
    active_profile : Profile
    profiles : dict[str,Profile]
    path : pathlib.Path

    def __init__(self, path):
        self.path = path
        self.active_profile = None
        self.profiles_dict = {}
        self.load()

    def load(self) -> bool:
        if self.path.is_file():
            try:
                f = open(self.path, 'rb')
                tmp_dict = pickle.load(f)
                f.close()          
                self.__dict__.update(tmp_dict)
                return True
            except:
                return False
        return False

    def save(self) -> bool:
        try:
            f = open(self.path, 'wb')
            pickle.dump(self.__dict__, f)
            f.close()
            return True
        except:
            return False

    def get_profile(self, name : str) -> Profile | None:
        if name in self.profiles_dict.keys():
            return self.profiles_dict[name]
        return None
    
    def add_profile(self, name : str) -> bool:
        if self.get_profile(name) is not None:
            return False
        self.profiles_dict[name] = Profile(name)
        if self.active_profile is None:
            self.active_profile = self.profiles_dict[name]
        return True
    
    def remove_profile(self, name : str) -> bool:
        if name in self.profiles_dict.keys():
            del self.profiles_dict[name]
            if self.active_profile.name == name:
                self.active_profile = None
            return True
        return False
    
    def register_win(self):
        if self.active_profile is not None:
            self.active_profile.register_win()

    def register_loss(self):
        if self.active_profile is not None:
            self.active_profile.register_loss()
    
    @property
    def profiles(self) -> list[Profile]:
        return self.profiles_dict.values()
