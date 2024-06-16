import socket
from _thread import *
import pickle
import time

from .utils import encode

class ClientInterface:

    server : socket.socket
    ip : str
    port : int


    def __init__(self, ip : str, port : int, game):
        print(ip)
        print(port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.game = game

    def connect(self):
        print(self.addr)
        try:
            print("we're about to connect...")
            self.server.connect(self.addr)
            print("connected")
            return pickle.loads(self.server.recv(4096))
        except error as e:
            print(e)
            return None
        
    def send_select(self, x : int, y : int):
        return self.send(encode(x,y))

    def send(self, data : str):
        try:
            self.server.send(str.encode(data))
            return pickle.loads(self.server.recv(4096))
        except:
            return None
        
    def update_loop(self, remote_color : int): 
        board,selected = self.send("get")
        self.game.board = board
        self.game.selected = selected
        while board.active_player == remote_color and not self.game.paused:
            time.sleep(0.1)
            response = self.send("get")
            print("client received: ", response)
            board, selected = response
            self.game.board = board
            self.game.selected = selected
            self.game.gui.update()
        print("loop over, enabling tiles")
        self.game.enable_tiles()


    def run_update_loop(self, remote_color : int):
        start_new_thread(self.update_loop, (remote_color,))