import os
import subprocess
from time import sleep
from pyautogui import press, hotkey, keyDown, keyUp
from enum import Enum
import pyperclip

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
        self.state = None
        self.window_id = None
        self._get_inertia_window()

        self.get_specific()


    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        sleep(10)
        subprocess.run(
            ['kill', f'{self.ipid}']
        )
    def _get_inertia_window(self) -> None:
        if os.environ.get("XDG_SESSION_TYPE") != 'x11':
            raise EnvironmentError("This script must be run in an X11 session")
        self.ipid = str(subprocess.Popen(["sgt-inertia"]).pid)
        sleep(self.delays)
        while True:
            result = subprocess.run(
                ["xdotool", "search", "--pid", self.ipid], # "--class", "Inertia"],
                capture_output=True,
                text=True,
                check=True
            )
            window_ids = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            print(f"{window_ids=}")
            for win_id in window_ids:
                sleep(self.delays)
                subprocess.run(
                    ["xdotool", "windowactivate", win_id],
                    check=True
                )
                sleep(self.delays)
                result = subprocess.run(
                    ["xdotool", "getactivewindow"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                window_id = result.stdout.strip()
                if window_id == win_id:
                    self.window_id = window_id
                    return
        raise RuntimeError(f"Can't set window_id, {window_ids=}, {self.window_id}")


    def _activate_inertia_window(self):

        sleep(self.delays)
        subprocess.run(
            ["xdotool", "windowactivate", self.window_id],
            check=True
        )
        result = subprocess.run(
            ["xdotool", "getactivewindow"],
            capture_output=True,
            text=True,
            check=True
        )
        window_id = result.stdout.strip()
        if window_id != self.window_id:
            raise RuntimeError(f"window id: {window_id} != {self.window_id}")

    def new_game(self) -> None:
        self._activate_inertia_window()
        press('N')

    def get_specific(self) -> str:
        self._activate_inertia_window()
        sleep(self.delays)
        keyDown('altleft')
        keyDown('g')
        keyUp('altleft')
        keyUp('g')
        press('Down')
        press('Down')
        press('Enter')
        hotkey('ctrlleft', 'c')
        self.state = pyperclip.paste()
        print(f'Copied {self.state}')
        press('Enter')

    def set_game(self, game: str) -> None:
        self._activate_inertia_window()

    def move(self, direction: Moves) -> None:
        self._activate_inertia_window()
        press(direction.value)

    def check_state(self) -> State:
        self._activate_inertia_window()

if __name__ == "__main__":
    with InertiaRemote() as inertia:
        pass
