# 10x8:gbwwgmwmgbbgbgmswmsssmsbSwgbsmgwggmbbwswssbmwmwmmbbwmgwsswmggmsssmswbggbwgwgbbsm
from enum import Enum
from json import dumps

class FieldType(Enum):
    GEM = 'g'
    BOLD = 'b'
    BALL = 'B'
    START = 'S'
    MINE = 'm'
    WALL = 'w'
    STOP = 's'

class Moves(Enum):
    SW = 1
    S = 2
    SE = 3
    W = 4
    E = 6
    NW = 7
    N = 8
    NE = 9

class Inertia:
    def __init__(self, board: str) -> None:
        self.width, self.height, self.board = self._board_decode(board)
        self.gems_max = self.board.count('g')
        self.actual_gems = self.gems_max
        self.field = self.width * self.height
        self.coord_set = set()
        self.last_coors_set_len = 0
        self.dead_end = 0

    @staticmethod
    def _board_decode(board: str) -> tuple[int, int, str]:
        xy, board = board.split(":")
        x, y = xy.split("x")
        x, y = int(x), int(y)
        if x * y != len(board):
            raise ValueError(f"Invalid board: {board}")
        return int(x), int(y), board

    def _check_down(self, coord: int) -> bool:
        print(f'{coord} + {self.width} < {self.field}')
        return coord + self.width < self.field

    def _check_left(self, coord: int) -> bool:
        return coord % self.width != 0

    def _check_right(self, coord: int) -> bool:
        return coord % self.width != self.width - 1

    def _check_state(self) -> str:
        self.actual_gems = self.board.count('g')
        state = 'GO'
        if len(self.coord_set) != self.last_coors_set_len:
            self.dead_end = 0
        else:
            self.dead_end += 1
        if self.dead_end >= self.gems_max:
            state = 'END'
        if 'S' not in self.board and 'B' not in self.board:
            state = 'END'
        if 'g' not in self.board:
            state = 'WIN'


        return  dumps({'state': state, 'actual_gems': self.actual_gems, 'max_gems': self.gems_max, 'map': self.board})

    def _check_top(self, coord: int) -> bool:
        return coord - self.width >= 0

    @staticmethod
    def _move_ball(old_coord: int, new_coord: int, board: list[str]) -> list[str]:
        if board[old_coord] == FieldType.BALL.value:
            board[old_coord] = FieldType.BOLD.value
        if board[old_coord] == FieldType.START.value:
            board[old_coord] = FieldType.STOP.value
        if board[new_coord] == FieldType.BOLD.value or board[new_coord] == FieldType.GEM.value:
            board[new_coord] = FieldType.BALL.value
        if board[new_coord] == FieldType.STOP.value:
            board[new_coord] = FieldType.START.value
        return board

    def _move_exec(self, old_coord: int, new_coord: int, last_move: Moves) -> None:
        board = list(self.board)
        print(f'move {old_coord} to {new_coord}, {last_move} with {board[new_coord]}, {board}')
        match board[new_coord]:
            case FieldType.GEM.value | FieldType.BOLD.value:
                self.board = ''.join(self._move_ball(old_coord, new_coord, board))
                self.move(last_move)
            case FieldType.STOP.value:
                self.board = ''.join(self._move_ball(old_coord, new_coord, board))

            case FieldType.WALL.value:
                pass
            case FieldType.MINE.value:
                print(f'{new_coord=} -> {last_move=}')
                board = self._move_ball(old_coord, new_coord, board)
                board[new_coord] = FieldType.BOLD.value
                self.board = ''.join(board)
        self.coord_set.add(old_coord)

    def get_human_board(self) -> str:
        board = list(self.board)
        for coord in range(len(board), 0, -self.width):
            board.insert(coord, '\n')
        return ''.join(board)


    def move(self, move: Moves) -> str:
        coord = self.board.find('S')
        if coord == -1:
            coord = self.board.find('B')
        if coord == -1:
            raise EOFError("Game ended")
        match move:
            case Moves.SW:
                if self._check_down(coord) and self._check_left(coord):
                    self._move_exec(coord, coord + self.width - 1, Moves.SW)
            case Moves.S:
                if self._check_down(coord):
                    self._move_exec(coord, coord + self.width, Moves.S)
            case Moves.SE:
                if self._check_down(coord) and self._check_right(coord):
                    self._move_exec(coord, coord + self.width + 1, Moves.SE)
            case Moves.E:
                if self._check_right(coord):
                    self._move_exec(coord, coord + 1, Moves.E)
            case Moves.NE:
                if self._check_right(coord) and self._check_top(coord):
                    self._move_exec(coord, coord - self.width + 1, Moves.NE)
            case Moves.N:
                if self._check_top(coord):
                    self._move_exec(coord, coord - self.width, Moves.N)
            case Moves.NW:
                if self._check_top(coord) and self._check_left(coord):
                    self._move_exec(coord, coord - self.width - 1, Moves.NW)
            case Moves.W:
                if self._check_left(coord):
                    self._move_exec(coord, coord - 1, Moves.W)

        return self._check_state()

