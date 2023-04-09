from typing import List, Tuple

from logic.reversi.model import ReversiStone, ReversiPlayer, ReversiModel


class ReversiController:
    def __init__(self):
        """
        初期化
        """
        self.__model: ReversiModel = ReversiModel()
        self.__previous_board: List[ReversiStone] = self.__model.current_board.copy()

    def can_put(self, x: int, y: int) -> bool:
        """
        (x, y)に石を置けるかどうか
        """
        x += 1
        y += 1
        return self.__model.can_put(10 * y + x)

    def put(self, x: int, y: int) -> None:
        """
        (x, y)に石を置く
        """
        self.__previous_board = self.__model.current_board.copy()

        x += 1
        y += 1
        self.__model.put(10 * y + x)

    @property
    def current_board_str(self) -> Tuple[Tuple[str, ...], ...]:
        """
        盤面を返す
        盤面には[x][y]でアクセスする
        """
        board_str = [stone_kind.name for stone_kind in self.__model.current_board]
        bd = [board_str[10 * i + 1 : 10 * i + 9] for i in range(1, 9)]
        return tuple(zip(*bd))

    @property
    def previous_board_str(self) -> Tuple[Tuple[str, ...], ...]:
        """
        一手前の盤面を返す
        盤面には[x][y]でアクセスする
        """
        previous_board_str = [
            stone_kind.name if stone_kind != ReversiStone.CANDIDATE else "EMPTY"
            for stone_kind in self.__previous_board
        ]
        bd = [previous_board_str[10 * i + 1 : 10 * i + 9] for i in range(1, 9)]
        return tuple(zip(*bd))

    @property
    def previous_xy_put(self) -> List[int]:
        """
        石を置いた座標を返す
        """
        y = int(self.__model.previous_i_put / 10)
        x = int(self.__model.previous_i_put - 10 * y)
        return [x - 1, y - 1]

    @property
    def previous_xy_flips(self) -> List[List[int]]:
        """
        ひっくり返す石群の座標を返す
        """
        xy_flips = []
        for i_flip in self.__model.previous_i_flips:
            y = int(i_flip / 10)
            x = int(i_flip - 10 * y)
            xy_flips.append([x - 1, y - 1])
        return xy_flips

    @property
    def previous_xy_candidates(self) -> List[List[int]]:
        """
        候補の石群の座標を返す
        """
        xy_candidates = []
        for i_candidate in self.__model.previous_i_candidates:
            y = int(i_candidate / 10)
            x = int(i_candidate - 10 * y)
            xy_candidates.append([x - 1, y - 1])
        return xy_candidates

    @property
    def current_player_color(self) -> ReversiPlayer:
        """
        現在のプレイヤーを ReversiPlayer で返す
        """
        return self.__model.current_player_color

    @property
    def current_player_color_str(self) -> str:
        """
        現在のプレイヤーを str で返す
        """
        return self.__model.current_player_color.name

    @property
    def black_stone_count(self) -> int:
        """
        現在の黒石の数
        """
        return self.__model.current_board.count(ReversiStone.BLACK)

    @property
    def white_stone_count(self) -> int:
        """
        現在の白石の数
        """
        return self.__model.current_board.count(ReversiStone.WHITE)

    @property
    def current_state_str(self) -> str:
        """
        現在の状態
        """
        return self.__model.current_state.name
