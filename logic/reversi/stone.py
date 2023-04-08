from enum import Enum, auto


class ReversiStone(Enum):
    EMPTY = auto()  # 空
    BLACK = auto()  # 黒
    WHITE = auto()  # 白
    WALL = auto()  # 壁
    CANDIDATE = auto()  # 候補
