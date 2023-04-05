from abc import ABC, abstractmethod

from logic.reversi.controller import ReversiPlayer, ReversiController
    

class Room(ABC):
    def __init__(self, room_name: str) -> None:
        self.__room_name = room_name
        self.__players = {}

    @property
    def room_name(self) -> str:
        return self.__room_name

    @property
    def players(self):
        return self.__players

    @property
    @abstractmethod
    def game_name(self) -> str:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def is_full(self) -> bool:
        pass


class ReversiRoom(Room):
    def __init__(self, room_name: str) -> None:
        super().__init__(room_name)
        self.__controller = ReversiController()

    @property
    def controller(self) -> ReversiController:
        return self.__controller

    @property
    def game_name(self) -> str:
        return "reversi"

    def is_empty(self) -> bool:
        return len(self.players) == 0

    def is_full(self) -> bool:
        return len(self.players) == 2
    
    def add_player(self, player_color: ReversiPlayer, session_id: str) -> None:
        self.players[player_color] = session_id

    def remove_player(self, player_color: ReversiPlayer) -> None:
        del self.players[player_color]

    def get_empty_player_color(self) -> ReversiPlayer:
        return ({ReversiPlayer.BLACK, ReversiPlayer.WHITE} - set(self.players.keys())).pop()
