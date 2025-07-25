from game.inertia import Inertia, Moves
from random import choice
from json import loads

game = Inertia("3x3:bbbgSwmbb")

def main() -> None:
    moves = 0
    while True:
        state = loads(game.move(choice(list(Moves))))

        if state['state'] == 'WIN':
            print('Win')
            break
        if state['state'] == 'END':
            print('Loose')
            break
        print(f"Move: {moves=}")
        moves+=1

if __name__ == '__main__':
    main()
