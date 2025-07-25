import os
import subprocess
from time import sleep
from pyautogui import press
from enum import Enum

class Moves(Enum):
    SW = 'num1'
    S = 'num2'
    SE = 'num3'
    W = 'num4'
    E = 'num6'
    NW = 'num7'
    N = 'num8'
    NE = 'num9'

class State(Enum):
    GO = 'Gems'
    WIN = 'Win'
    DEAD = 'Dead'

class InertiaRemote:
    def __init__(self, delays = 1):
        self.delays = delays # delay between moves
        if os.environ.get("XDG_SESSION_TYPE") != 'x11':
            raise EnvironmentError("This script must be run in an X11 session")
        self.ipid = subprocess.Popen(["sgt-inertia"]).pid
        sleep(1)
        print('bbb')
        for m in ['num1', 'num2', 'num3', 'num4', 'num6']:
            press(m)
            sleep(1)
        print('end')

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def new_game(self) -> None:
        pass

    def get_specific(self) -> str:
        pass

    def set_game(self, game: str) -> None:
        pass

    def move(self, direction: Moves) -> None:
        pass

    def check_state(self) -> State:
        pass

    def win_activate(self) -> bool:
        pass
if __name__ == "__main__":
    with InertiaRemote() as inertia:
        pass
