import unittest

from board import Board, MultipleWinException, InvalidMoveException


def test_single_cell_no_win():
    '''
    Ensures a win is not awarded if there is a row which contains
    an empty cell.
    '''
    board = Board()
    board.board[0][1] = 'X'
    print()
    print(board)

def test_mixed_row():
    '''
    Ensures a win is not awarded if a row contains an X and an O
    '''
    pass

def test_row_win():
    '''
    Ensures a win is awarded when a row (and only one row) is complete.
    '''
    #TODO: Test each row
    pass

def test_column_win():
    '''
    Ensures a win is awarded when a row (and only one row) is complete.
    '''
    #TODO: Test each column
    pass

def test_diagonal_win():
    '''
    Ensures a win is awarded when a diagonal (or reverse-diagonal)
    is complete.
    '''
    #TODO: Test each diagonal front
    #TODO: Test each diagonal back
    pass

def test_cats_game():
    '''
    Ensures the BoardState is set to CATS_GAME when a unwinnable
    board state is reached.
    '''
    pass

def test_multiple_win_error():
    return
    with pytest.raises(
    # s = 'hello world'
    # .assertEqual(s.split(), ['hello', 'world'])
    # check that s.split fails when the separator is not a string
    # with .assertRaises(TypeError):
        s.split(2)

def test_finished_board_has_correct_winner():
    '''
    Ensures a winning board has the `current_player` set correctly.
    '''
    pass

def test_select_cell_toggles_player():
    '''
    Ensures a using the `select_cell` method of the Board
    '''
    pass
