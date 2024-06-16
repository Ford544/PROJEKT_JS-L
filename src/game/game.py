from PySide6.QtCore import *
from PySide6.QtWidgets import *

from ..board.piece import Piece
from ..board.board import Board
from .player import Player
from .human_player import HumanPlayer
from .random_player import RandomPlayer
from .minimax_player import MinimaxPlayer
from.remote_player import RemotePlayer
from ..profiles.profile_manager import ProfileManager
from ..network.server import Server
from ..network.client_interface import ClientInterface
from ..consts import BLACK,WHITE,MAXIMUM_CAPTURING_OBLIGATORY, DRAW

class Game:

    board : Board
    selected : Piece
    white_player : Player
    black_player : Player
    manager : ProfileManager
    paused : bool
    server : Server | None
    interface : ClientInterface | None

    def __init__(self, gui, manager : ProfileManager, size : int = 8, 
                 capturing_obligatory : int = MAXIMUM_CAPTURING_OBLIGATORY, pieces_capturing_backwards : bool = True, 
                 flying_kings : bool = True, mid_jump_crowning : bool = False, player1_mode : int = -2, 
                 player1_name : str = "Player1", player2_mode : int = 2, player2_name : str = "Player2", 
                 profile_player : int = 1):
        #player modes:
        # -4 - client
        # -3 - remote (server)
        # -2 - human
        # 0 - random ai
        # n = 1,2,3,... - minimax with depth n

        #profile player:
        #0 - neither
        #1 - white
        #2 - black
       self.configure(size, capturing_obligatory, pieces_capturing_backwards, flying_kings, mid_jump_crowning, 
                      player1_mode, player1_name, player2_mode, player2_name, profile_player)
       self.selected = None
       self.gui = gui
       self.manager = manager
       self.paused = False
       self.server = None
       self.interface = None

    def play(self) -> None: 
        while self.board.winner == 0 and not self.paused:
            if self.board.active_player == WHITE:
                self.gui.set_banner_text(f"{self.white_player.name}'s (WHITE) TURN")
                if self.white_player.pass_control():
                    return
            else:
                self.gui.set_banner_text(f"{self.black_player.name}'s (BLACK) TURN")
                if self.black_player.pass_control():
                    return
            self.gui.processEvents()
        if self.board.winner == BLACK:
            self.gui.set_banner_text(f"{self.black_player.name} has won!")
            self.register_game(self.black_player)
        elif self.board.winner == WHITE:
            self.gui.set_banner_text(f"{self.white_player.name} has won!")
            self.register_game(self.white_player)
        elif self.board.winner == DRAW:
            self.gui.set_banner_text(f"Game ends in draw!")
            self.register_game(None)

    #an information about waiting for connection?
    def host(self, port) -> bool:
        self.server = Server(port,self)
        if self.server.set_up():
            print("server is all set up")
            self.server.run()
            return True
        else:
            print("server failed to get off the ground")
            return False
        
    def join(self, ip : str, port : int, name : str) -> bool:
        self.interface = ClientInterface(ip, port, self)
        response = self.interface.connect()
        if response is not None:
            color, remote_name = response
            color = int(color)
            if color == BLACK:
                self.white_player = HumanPlayer(self, name, True)
                self.black_player = RemotePlayer(self, remote_name, False, BLACK)
            else:
                self.white_player = RemotePlayer(self, remote_name, False, WHITE)
                self.black_player = HumanPlayer(self, name, True)
            board, selected = self.interface.send("get")
            self.board = board
            self.selected = selected

    def end(self):
        if self.interface is not None:
            self.interface.close()
            self.interface = None
        if self.server is not None:
            self.server.closed = True
            self.server.shut_down()
            self.server = None

    def restart(self) -> None:
        self.board.set_up()
        self.selected = None

    def configure(self, size : int, capturing_obligatory : int, pieces_capturing_backwards : bool, flying_kings : bool, 
                mid_jump_crowning : bool, player1_mode : int, player1_name : str, player2_mode : str, 
                player2_name : int, profile_player : int) -> None:
        self.board = Board(size, capturing_obligatory, pieces_capturing_backwards, flying_kings, mid_jump_crowning)
        white_profile = False
        black_profile = False
        if profile_player == 1:
            white_profile = True
        if profile_player == 2:
            black_profile = True
        self.white_player = self.make_player(player1_mode, player1_name, white_profile, True)
        self.black_player = self.make_player(player2_mode, player2_name, black_profile, False)
        self.server = None
        self.interface = None
        
    def make_player(self, mode : int, name : str, profile : bool, white : bool) -> Player:
       if white: color = WHITE
       else: color = BLACK
       match mode:
           case -3:
               return RemotePlayer(self, name, profile, color)
           case -2:
               return HumanPlayer(self,name, profile)
           case 0:
               return RandomPlayer(self,name, profile)
           case n:
               return MinimaxPlayer(self, name, profile, n, white)
              

    def select(self, x : int, y : int) -> bool:
        if self.interface is not None:
            try:
                self.interface.send_select(x,y)
                board, selected = self.interface.send("get")
                self.board = board
                self.selected = selected
            except:
                print("connection lost")
        else:
            target = self.board.get_piece(x,y)
            if target is None:
                if self.selected is not None:
                    if self.board.move(self.selected,x,y):
                        if self.board.has_valid_moves(self.selected):
                            self.mark_selected(self.selected)
                        else:
                            self.mark_selected(None)
                            return True
                        self.gui.update()

            elif target.color == self.board.active_player:
                self.mark_selected(target)
            return False

    def mark_selected(self, target : Piece) -> None:
        self.selected = target
        self.gui.update()

    def register_game(self, winner : Player | None) -> None:
        if winner is None:
            self.manager.register_draw()
        elif winner.profile:
            self.manager.register_win()
        else:
            self.manager.register_loss()

    @property
    def selected_tile(self) -> tuple[int,int] | None:
        if self.selected is None: return None
        return self.selected.x,self.selected.y
    
    @property
    def selected_valid_moves(self) -> list[tuple[int,int]]:
        if self.selected is None: return []
        if not self.selected in self.board.valid_moves.keys(): return []
        return [move.first_step for move in self.board.valid_moves[self.selected]]
    
    @property
    def marked_tiles(self) -> list[tuple[int,int]]:
        return self.board.marked
    
    def enable_tiles(self) -> None:
        self.gui.enable_tiles()

    def disable_tiles(self) -> None:
        self.gui.disable_tiles()

