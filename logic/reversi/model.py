from typing import List

from logic.reversi.stone import ReversiStone
from logic.reversi.player import ReversiPlayer
from logic.reversi.state import ReversiState


class ReversiModel:
    def __init__(self):
        """
        初期化
        """
        # 変数初期化
        self.__current_player_color: ReversiPlayer = ReversiPlayer.BLACK
        self.__current_state: ReversiState = ReversiState.PLAYING
        self.__previous_i_put: int = 0
        self.__previous_i_flips: List[int] = []
        self.__previous_i_candidates: List[int] = []
        self.__board: List[ReversiStone] = [ReversiStone.EMPTY] * 100

        # 初期の石を配置
        self.__board[44] = ReversiStone.WHITE
        self.__board[45] = ReversiStone.BLACK
        self.__board[54] = ReversiStone.BLACK
        self.__board[55] = ReversiStone.WHITE

        # 壁を配置
        for i in range(10):
            self.__board[i] = ReversiStone.WALL
            self.__board[90 + i] = ReversiStone.WALL
            self.__board[10 * i] = ReversiStone.WALL
            self.__board[10 * i + 9] = ReversiStone.WALL

        # 初期の候補を探索
        current_player_color = self.__current_player_color
        self.__search_candidates(current_player_color)

    @property
    def current_board(self) -> List[ReversiStone]:
        return self.__board

    @property
    def current_player_color(self) -> ReversiPlayer:
        return self.__current_player_color

    @property
    def previous_i_put(self) -> int:
        return self.__previous_i_put

    @property
    def previous_i_flips(self) -> List[int]:
        return self.__previous_i_flips

    @property
    def previous_i_candidates(self) -> List[int]:
        return self.__previous_i_candidates

    @property
    def current_state(self) -> ReversiState:
        return self.__current_state

    def can_put(self, i_board: int) -> bool:
        """
        盤面のi_boardに現在のプレイヤーの石を置けるかどうか
        置けるならTrue、置けなければFalseを返す
        """
        # 候補以外なら空のリストを返す
        if self.__board[i_board] == ReversiStone.CANDIDATE:
            return True
        else:
            return False

    def put(self, i_board: int) -> None:
        """
        盤面のi_boardに現在のプレイヤーの石を置き、敵のプレイヤーの石をひっくり返す
        """
        # 石を置き、ひっくり返す
        current_player_color = self.__current_player_color
        self.__flip_stones(i_board, current_player_color)

        # 次のプレイヤーが石を置ける候補を探す
        next_player_color = self.__get_reverse_player_color(self.__current_player_color)
        is_find_candidate = self.__search_candidates(next_player_color)

        # 候補が見つかったので、次は反対の色のプレイヤーのターン
        if is_find_candidate:
            self.__current_player_color = next_player_color
            return

        # 候補が見つからなかったので、反対の色のターンはスキップされ、同じプレイヤーの候補を再検索する
        is_find_candidate = self.__search_candidates(current_player_color)

        # 候補が見つかったので、次も自分のターン
        if is_find_candidate:
            self.__current_player_color = current_player_color
            return

        # どちらの色の候補も見つからなかったのでゲーム終了
        self.__current_state = ReversiState.FINISHED
        return

    def __flip_stones(self, i_board: int, player_color: ReversiPlayer) -> None:
        """
        盤面の i_board に player_color の石を置き、敵のプレイヤーの石をひっくり返す
        """

        # 相手の色
        enemy_player_color = self.__get_reverse_player_color(player_color)

        # ひっくり返されるマスのリスト
        i_flips = []

        # 方向パラメータ
        UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
        RIGHT_UP, RIGHT_DOWN, LEFT_UP, LEFT_DOWN = (
            RIGHT + UP,
            RIGHT + DOWN,
            LEFT + UP,
            LEFT + DOWN,
        )

        # 8方向を走査
        for i_unit in (RIGHT, RIGHT_UP, UP, LEFT_UP, LEFT, LEFT_DOWN, DOWN, RIGHT_DOWN):
            # ひっくり返す候補
            i_flips_temp = []

            # 置いた石の隣が敵の石でなければ次へ
            i_check = i_board + i_unit
            if self.__board[i_check].name != enemy_player_color.name:
                continue

            # 敵の石である限り、unit方向に進み続ける
            while self.__board[i_check].name == enemy_player_color.name:
                i_flips_temp.append(i_check)
                i_check += i_unit

            # 敵の石のあとが自分の石なら置けることが確定
            if self.__board[i_check].name == player_color.name:
                i_flips += i_flips_temp

        # 石を置き、ひっくり返す
        self.__board[i_board] = getattr(ReversiStone, player_color.name)
        for i_flip in i_flips:
            self.__board[i_flip] = getattr(ReversiStone, player_color.name)
        self.__previous_i_put = i_board
        self.__previous_i_flips = i_flips

    def __get_reverse_player_color(
        self, current_player_color: ReversiPlayer
    ) -> ReversiPlayer:
        """
        現在のプレイヤーと反対のプレイヤーを取得
        """
        if current_player_color == ReversiPlayer.BLACK:
            return ReversiPlayer.WHITE
        else:
            return ReversiPlayer.BLACK

    def __search_candidates(self, next_player_color: ReversiPlayer) -> bool:
        """
        次のターンの人が置ける場所探索する
        次のターンの人が置ける場所があればTrue、なければFalseを返す
        """
        # 現在の候補を空に
        for i, stone_kind in enumerate(self.__board.copy()):
            if stone_kind == ReversiStone.CANDIDATE:
                self.__board[i] = ReversiStone.EMPTY

        # 次の候補を探す
        i_candidates = []
        for i, _ in enumerate(self.__board.copy()):
            if self.__is_candidate(i, next_player_color):
                i_candidates.append(i)

        # 候補を反映させる
        for i_candidate in i_candidates:
            self.__board[i_candidate] = ReversiStone.CANDIDATE
        self.__previous_i_candidates = i_candidates

        if i_candidates:
            return True
        else:
            return False

    def __is_candidate(self, i_board: int, player_color: ReversiPlayer) -> bool:
        """
        盤面の i_board に player_color の石を置けるかどうか
        置けるならTrue、置けなければFalseを返す
        """

        # 空以外なら置けないことが確定
        if self.__board[i_board] != ReversiStone.EMPTY:
            return False

        # 相手のカラー
        enemy_player_color = self.__get_reverse_player_color(player_color)

        # 方向パラメータ
        UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
        RIGHT_UP, RIGHT_DOWN, LEFT_UP, LEFT_DOWN = (
            RIGHT + UP,
            RIGHT + DOWN,
            LEFT + UP,
            LEFT + DOWN,
        )

        # 8方向を走査
        for i_unit in (RIGHT, RIGHT_UP, UP, LEFT_UP, LEFT, LEFT_DOWN, DOWN, RIGHT_DOWN):
            # 置いた石の隣が敵の石でなければ次へ
            i_check = i_board + i_unit
            if self.__board[i_check].name != enemy_player_color.name:
                continue

            # 敵の石である限り、unit方向に進み続ける
            while self.__board[i_check].name == enemy_player_color.name:
                i_check += i_unit

            # 敵の石のあとが自分の石なら置けることが確定
            if self.__board[i_check].name == player_color.name:
                return True

        # 全方向探索してもひっくり返せる石が見つからなければ置けないことが確定
        return False
