import socket
from _thread import *
import pickle

from .utils import encode

#this class handles communication with the server from the client side

class ClientInterface:

    server : socket.socket
    ip : str
    port : int


    def __init__(self, ip : str, port : int, game):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.game = game

    def connect(self):
        try:
            self.server.connect(self.addr)
            #print("connected")
            return pickle.loads(self.server.recv(4096))
        except error as e:
            print(e)
            return None
        
    def send_select(self, x : int, y : int):
        #print(f"sending select {(x,y)}")
        return self.send(encode(x,y))

    def send(self, data : str):
        try:
            self.server.send(str.encode(data))
            return pickle.loads(self.server.recv(4096))
        except:
            return None
        
    def close(self):
        #print("closing connection (client)")
        self.server.close()