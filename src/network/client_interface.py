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
        print(f"sending select {(x,y)}")
        return self.send(encode(x,y))

    def send(self, data : str):
        try:
            self.server.send(str.encode(data))
            return pickle.loads(self.server.recv(4096))
        except:
            return None
        
    def close(self):
        print("closing connection (client)")
        self.server.close()