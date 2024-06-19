import socket
from _thread import *
import pickle

from .utils import decode
from ..game.game import HumanPlayer
from ..consts import BLACK, WHITE

class Server:

    ip : str
    port : int
    socket_ : socket.socket
    closed : bool

    def __init__(self, port : int, game):
        self.ip = self.get_ip()
        print(self.ip)
        print(port)
        self.port = port
        self.game = game
        self.closed = False

    def set_up(self) -> bool:
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.socket_)
        try:
            print((self.ip, self.port))
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
        print("starting thread")
        start_new_thread(self.wait_for_conn, tuple())
    
    def listen(self, conn):
        if isinstance(self.game.white_player, HumanPlayer):
            conn.send(pickle.dumps((WHITE,self.game.white_player.name)))
        else:
            conn.send(pickle.dumps((BLACK,self.game.black_player.name)))
        while not self.closed:
            try:
                data = conn.recv(4096).decode()
                #print("server received: ", data)
                if data != "get":
                    coords = decode(data)
                    if coords is not None: 
                        x,y = coords
                        print(f"receiving coords: {(x,y)}")
                    if self.game.select(x,y):
                        self.game.enable_tiles()
                    
                conn.send(pickle.dumps((self.game.board, self.game.selected)))
            except:
                break

        print("Lost connection")
        conn.close()

    def wait_for_conn(self): 
        try:
            conn, addr = self.socket_.accept()
            print("Connected to:", addr)
            self.listen(conn)
        except error as e:
            print("wait_for_conn has a problem: ", e)

    def shut_down(self):
        print("closing connection (server)")
        self.socket_.close()