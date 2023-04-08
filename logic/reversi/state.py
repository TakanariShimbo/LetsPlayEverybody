from enum import Enum, auto


class ReversiState(Enum):
    PLAYING = auto()  # プレイ中
    FINISHED = auto()  # 終了済
