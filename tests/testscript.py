from enum import Enum
from json import dumps
from random import choices, choice
from game.inertia import Inertia, Moves


def main() -> None:
    d = {1:{2: 3, 5: 6}}
    print(max(d.get(1, 0).values()))


if __name__ == '__main__':
    main()
