from logic.reversi.controller import ReversiPlayer


class User:
    def __init__(self, session_id: str, room_name: str) -> None:
        self.__session_id = session_id
        self.__room_name = room_name
        
    @property
    def session_id(self) -> str:
        return self.__session_id
    
    @property
    def room_name(self) -> str:
        return self.__room_name
    

class ReversiUser(User):
    def __init__(self, session_id: str, room_name: str, player_color: str) -> None:
        super().__init__(session_id, room_name)
        self.__player_color = getattr(ReversiPlayer, player_color)

    @property
    def player_color(self) -> ReversiPlayer:
        return self.__player_color