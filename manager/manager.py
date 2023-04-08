from manager.user import ReversiUser
from manager.room import ReversiRoom


class RoomUserManager:
    """
    共通
    """

    def __init__(self):
        self.__room_dict = {}
        self.__user_dict = {}

    def get_user(self, session_id: str):
        return self.__user_dict.get(session_id)

    def remove_user(self, session_id: str):
        user = self.get_user(session_id)

        if type(user) == ReversiUser:
            self.__remove_reversi_user(session_id)

    def __remove_user(self, session_id):
        del self.__user_dict[session_id]

    def get_room(self, room_name: str):
        return self.__room_dict.get(room_name)

    def remove_room(self, room_name: str):
        room = self.__room_dict.get(room_name)

        if type(room) == ReversiRoom:
            self.___remove_reversi_room(room_name)

    def __remove_room(self, room_name):
        del self.__room_dict[room_name]

    @property
    def room_name_list(self):
        return list(self.__room_dict.keys())

    @property
    def room_dict(self):
        _room_dict = {}
        for name, room in self.__room_dict.items():
            _room_dict[name] = room.game_name
        return _room_dict

    def is_exists_room(self, room_name: str) -> bool:
        if room_name in self.room_name_list:
            return True
        else:
            return False

    """
    リバーシ
    """

    def create_reversi_room(self, room_name: str) -> ReversiRoom:
        room = ReversiRoom(room_name)
        self.__room_dict[room_name] = room
        return room

    def create_reversi_user_and_assign_to_room(
        self, session_id: str, room_name: str, player_color: str
    ) -> None:
        user = self.__create_reversi_user(session_id, room_name, player_color)
        self.__assign_to_reversi_room(room_name, user.player_color, session_id)

    def __create_reversi_user(self, session_id, room_name, player_color):
        user = ReversiUser(session_id, room_name, player_color)
        self.__user_dict[session_id] = user
        return user

    def __assign_to_reversi_room(self, room_name, player_color, session_id):
        room = self.get_room(room_name)
        room.add_player(player_color, session_id)

    def __remove_reversi_user(self, session_id: str) -> None:
        user = self.get_user(session_id)
        room = self.get_room(user.room_name)

        self.__remove_user(session_id)
        room.remove_player(user.player_color)

    def ___remove_reversi_room(self, room_name: str) -> None:
        room = self.__room_dict.get(room_name)

        for session_id in room.players.values():
            self.remove_reversi_user(session_id)
        self.__remove_room(room_name)
