import socket
from _thread import *
import pickle

from .utils import decode
from ..game.client_player import ClientPlayer
from ..consts import BLACK, WHITE

#this class is used to coordinate a network game
#the host creates an instance of this class which keeps track of the game state
#both players get synchronise their internal game states with this class
#(the client side player over the network, the server side player directly)

class Server:

    ip : str
    port : int
    socket_ : socket.socket
    closed : bool
    client_player : ClientPlayer

    def __init__(self, port : int, board, selected, white_name, black_name, host_color, client_player):
        self.ip = self.get_ip()
        self.port = port
        self.board = board
        self.selected = selected
        self.white_name = white_name
        self.black_name = black_name
        self.host_color = host_color
        self.client_player = client_player
        self.closed = False

    def set_up(self) -> bool:
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket_.bind((self.ip, self.port))
        except socket.error as e:
            return False
        self.socket_.listen(1)
        return True

    def get_ip(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def run(self):
        start_new_thread(self.wait_for_conn, tuple())
    
    #this is meant to run as a thread and handle communication incoming from the client
    def listen(self, conn):
        #tell the client which color the host has chosen and what is their player name
        if self.host_color == WHITE:
            conn.send(pickle.dumps((WHITE,self.white_name)))
        else:
            conn.send(pickle.dumps((BLACK,self.black_name)))
        while not self.closed:
            #there are three kinds of communications the client may send:
            #-get, which is just asking for the game state
            #-a pair of numbers, which is the client's selection
            #-a string starting with name=, which contains the client's player name
            try:
                data = conn.recv(4096).decode()
                if data != "get":
                    coords = decode(data)
                    if coords is not None: 
                        x,y = coords
                        self.select(x,y)                
                    elif data[0:5] == "name=":
                        self.client_player.name = data[5:]

                conn.send(pickle.dumps((self.board, self.selected)))
            except:
                break

        #print("Lost connection")
        conn.close()

    def wait_for_conn(self): 
        try:
            conn, addr = self.socket_.accept()
            self.listen(conn)
        except error as e:
            pass
            #print("wait_for_conn has a problem: ", e)

    def shut_down(self):
        self.socket_.close()

    #internal server select; it does not need to handle display and is thus simpler than game.select
    def select(self, x : int, y : int) -> None:
        target = self.board.get_piece(x,y)
        if target is None:
            if self.selected is not None:
                if self.board.move(self.selected,x,y):
                    if not self.board.has_valid_moves(self.selected):
                        self.selected = None
        elif target.color == self.board.active_player:
            self.selected = target
        return False
    
    def get_state(self):
        return self.board, self.selected