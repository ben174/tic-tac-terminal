import ai
import logging


logging.basicConfig(filename='game.log', level=logging.DEBUG, force=True)

HORIZONTAL_WIN_O = [
    ['O', 'O', 'O'],
    [None, None, None],
    [None, None, None],
]

VERTICAL_WIN_X = [
    ['X', 'O', 'O'],
    ['X', None, None],
    ['X', None, None],
]

DIAG_WIN_X = [
    ['X', 'O', 'O'],
    ['X', 'X', None],
    ['X', None, 'X'],
]

DIAG_WIN_O = [
    ['X', 'O', 'O'],
    ['X', 'O', None],
    ['O', None, 'X'],
]

CATS_GAME = [
    ['X', 'O', 'X'],
    ['X', 'O', 'O'],
    ['O', 'X', 'X'],
]

VERTICAL_WIN_X = [
    ['X', 'X', None],
    ['X', 'O', None],
    ['X', None, None],
]

BEST_MOVE_O = [
    ['X', 'X', None],
    ['X', 'O', None],
    ['O', None, None],
]



def test_ai_check_horizontal():
    assert ai.check_winner(HORIZONTAL_WIN_O) == 'O'

def test_ai_check_vertical():
    assert ai.check_winner(VERTICAL_WIN_X) == 'X'

def test_ai_check_diag():
    assert ai.check_winner(DIAG_WIN_O) == 'O'
    assert ai.check_winner(DIAG_WIN_X) == 'X'

def test_ai_cats_game():
    assert ai.check_winner(CATS_GAME) == 'cats'


def test_ai_best_move():
    move = ai.get_best_move(BEST_MOVE_O)
    logging.warning('best move done')
    logging.warning(move)
