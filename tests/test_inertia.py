import pytest
from unittest.mock import patch, MagicMock
from game.inertia import Inertia, Moves, FieldType

# Test data: 3x3 board with a gem and ball
TEST_BOARD = "3x3:bbbgSbbbb"  # Just an example board
TEST_BOARD2 = "3x3:bbbgSwmbb"  # Just an example board with mine and wall

def test_board_decode():
    inertia = Inertia(TEST_BOARD)
    assert inertia.width == 3
    assert inertia.height == 3
    assert inertia.board == "bbbgSbbbb"

def test_check_state_win():
    board = TEST_BOARD
    game = Inertia(board)
    # Simulate a state with no gems
    game.board = game.board.replace("g", "b")
    result = game._check_state()
    assert '"state": "WIN"' in result

def test_check_state_end_by_no_start_or_ball():
    board = TEST_BOARD
    game = Inertia(board)
    game.board = board.replace("S", "b").replace("B", "b")
    result = game._check_state()
    assert '"state": "END"' in result

def test_check_state_dead_end_triggers_end():
    board = TEST_BOARD
    game = Inertia(board)
    game.dead_end = game.gems_max  # simulate dead end
    game.last_coors_set_len = len(game.coord_set)
    result = game._check_state()
    assert '"state": "END"' in result

def test_move_game_ended():
    game = Inertia("3x3:bbbgbbbbb")
    with pytest.raises(EOFError):
        game.move(Moves.E)


def test_invalid_board():
    with pytest.raises(ValueError):
        Inertia(TEST_BOARD[:-1])

def test_walking():
    game = Inertia(TEST_BOARD)

    game.move(Moves.N)
    game.move(Moves.SW)
    game.move(Moves.NE)
    game.move(Moves.W)
    game.move(Moves.SE)
    game.move(Moves.NW)
    game.move(Moves.S)
    game.move(Moves.E)
    assert game.board == 'bbbbsbbbB'

def test_mine():
    game = Inertia(TEST_BOARD2)
    game.move(Moves.SW)
    assert game.board == 'bbbgswbbb'

