from game.inertia import Inertia, Moves

TEST_BOARD = "3x3:bbbgSwmbb"
def tst():
    game = Inertia(TEST_BOARD)
    print(game.get_human_board())
    game.move(Moves.SW)
    print(game.get_human_board())


def main() -> None:
    tst()


if __name__ == '__main__':
    main()
