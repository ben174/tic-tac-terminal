"""Module tests for Board"""

import pytest

from loggers import board_logger
from board import Board, BoardState, Player
from board import MultipleWinError, InvalidMoveError


def test_single_cell_no_win():
    """ Ensures a win is not awarded if there is a row which contains
    an empty cell.
    """
    board = Board()
    board.select_cell(0, 1)
    assert board.state == BoardState.PLAYING


def test_win():
    """ Plays a standard game, ensuring the PLAYING state remains
    until the game is finished.
    """
    board = Board()

    # X: X - -
    #    - - -
    #    - - -
    board.select_cell(0, 0)

    # O: X - -
    #    O - -
    #    - - -
    board.select_cell(1, 0)

    # X: X X -
    #    O - -
    #    - - -
    board.select_cell(0, 1)

    # O: X X -
    #    O O -
    #    - - -
    board.select_cell(1, 1)
    assert board.state == BoardState.PLAYING

    # X: X X X -- Finish Him!
    #    O O -
    #    - - -
    board.select_cell(0, 2)
    assert board.state == BoardState.FINISHED


def test_ai():
    """ Plays a standard game, against AI
    TODO: this should be an entire module
    """
    board = Board()

    # X: X - -
    #    - - -
    #    - - -
    board.select_cell(0, 0)

    board.make_best_move()
    board_logger.info(board.board)

    return

    # O: X - -
    #    O - -
    #    - - -
    board.select_cell(1, 0)

    # X: X X -
    #    O - -
    #    - - -
    board.select_cell(0, 1)

    # O: X X -
    #    O O -
    #    - - -
    board.select_cell(1, 1)
    assert board.state == BoardState.PLAYING

    # X: X X X -- Finish Him!
    #    O O -
    #    - - -
    board.select_cell(0, 2)
    assert board.state == BoardState.FINISHED


def test_player_toggle():
    """ Ensures the current player is toggled after each move.
    """
    board = Board()
    assert board.current_player == Player.PLAYER_X
    board.select_cell(0, 0)
    assert board.current_player == Player.PLAYER_O
    board.select_cell(0, 1)
    assert board.current_player == Player.PLAYER_X


def test_mixed_row():
    """ Ensures a win is not awarded if a row contains an X and an O
    """
    board = Board()

    # X: X - -
    board.select_cell(0, 0)

    # O: X O -
    board.select_cell(0, 1)

    # X: X O X
    board.select_cell(0, 2)
    assert board.state == BoardState.PLAYING


def test_row_win():
    """ Ensures a win is awarded when a row (and only one row)
    is complete.
    """
    for i in range(3):
        board = Board()
        board.board[i] = [Player.PLAYER_X] * 3
        assert board.check_state() == BoardState.FINISHED


def test_col_win():
    """ Ensures a win is awarded when a column (and only one column)
    is complete.
    """
    for i in range(3):
        board = Board()
        board.board[0][i], board.board[1][i], board.board[2][i] = (
            [Player.PLAYER_O] * 3)
        assert board.check_state() == BoardState.FINISHED


def test_diagonal_win():
    """ Ensures a win is awarded when a diagonal (or reverse-diagonal)
    is complete.
    """
    # Diagonal: \
    board = Board()
    for i in range(3):
        board.board[i][i] = Player.PLAYER_O
    assert board.check_state() == BoardState.FINISHED

    # Diagonal: /
    board = Board()
    board.board[2][0], board.board[1][1], board.board[0][2] = (
        [Player.PLAYER_O] * 3)
    assert board.check_state() == BoardState.FINISHED


def test_cats_game():
    """ Ensures the BoardState is set to CATS_GAME when a unwinnable
    board state is reached.
    """
    board = Board()

    # Construct an unwinnable game:
    # O X O
    # X O -
    # X O X
    board.board[0] = Player.PLAYER_O, Player.PLAYER_X, Player.PLAYER_O
    board.board[1] = Player.PLAYER_X, Player.PLAYER_O, None
    board.board[2] = Player.PLAYER_X, Player.PLAYER_O, Player.PLAYER_X
    assert board.check_state() == BoardState.CATS_GAME


def test_multiple_win_error():
    """ Ensures a MultipleWinError exception is generated if the board
    contains multiple wins.
    """
    with pytest.raises(MultipleWinError):
        board = Board()
        board.board[0] = [Player.PLAYER_X] * 3
        board.board[1] = [Player.PLAYER_O] * 3
        board.check_state()


def test_invalid_move_error():
    """ Ensures an InvalidMoveError exception is generated if an attempt
    is made to move on an already-occupied square.
    """
    with pytest.raises(InvalidMoveError):
        board = Board()
        board.select_cell(0, 1)
        board.select_cell(0, 1)
