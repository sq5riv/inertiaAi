from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ..game.inertia import Moves, Inertia, GameState


@dataclass
class WalkState:
    game_state: str
    number_of_diamonds: int
    move_to: Optional[Moves] = None
    moves_to_check: list[Moves] = field(default_factory=lambda: [Moves.E, Moves.W, Moves.S, Moves.N, Moves.NE, Moves.SE,
                                                                 Moves.SW, Moves.SE])
class States(Enum):
    FORWARD = 'F'
    BACK = 'B'
    WIN = 'W'
    STACK = 'S'

class Walk:
    def __init__(self, board:str):
        self.board = board
        self.steps: list[WalkState] = []
        self._set_start()

    def _set_start(self):
        num_diamonds = Inertia(self.board).get_gem_number()
        self.steps.append(WalkState(self.board, num_diamonds))

    def __call__(self):
        self.resolve()

    def resolve(self):
        okgo = True
        state = States.FORWARD
        while okgo:
            if state == States.FORWARD:
                state = self.forward()
            elif state == States.BACK:
                state = self.backward()
            elif state == States.WIN:
                state = self.win()
                okgo = False
            elif state == States.STACK:
                state = self.stack()
                okgo = False

    def forward(self) -> States:
        if len(self.steps) == 0:
            return States.STACK
        step = self.steps[-1]
        if len(step.moves_to_check) == 0:
            return States.BACK
        move = step.moves_to_check.pop(-1)
        game = Inertia(step.game_state)
        game_dict = game.move(move)
        if game_dict['state'] == GameState.WIN:
            return States.WIN
        elif game_dict['state'] == GameState.END:
            return States.FORWARD
        elif game_dict['state'] == GameState.GO:
            # ToDo add stack check.
            self.steps.append(WalkState(game_state = self.board, number_of_diamonds=game_dict['actual_gems']))
            return States.FORWARD
        return States.FORWARD


    def backward(self) -> States:
        self.steps.pop(-1)
        return States.FORWARD
    def stack(self) -> States:
        return True
    def win(self) -> States:
        return True
