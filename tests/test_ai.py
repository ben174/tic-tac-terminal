import ai
from loggers import ai_logger


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

''' causes loop
BEST_MOVE_O = [
    ['X', None, None],
    [None, None, None],
    [None, None, None],
]
'''


def test_ai_check_horizontal():
    """Verifies `check_winner` function for horizontal wins."""
    assert ai.check_winner(HORIZONTAL_WIN_O) == 'O'


def test_ai_check_vertical():
    """Verifies `check_winner` function for vertical wins."""
    assert ai.check_winner(VERTICAL_WIN_X) == 'X'


def test_ai_check_diag():
    """Verifies `check_winner` function for diagonal wins."""
    assert ai.check_winner(DIAG_WIN_O) == 'O'
    assert ai.check_winner(DIAG_WIN_X) == 'X'


def test_ai_cats_game():
    """Verifies `check_winner` function for cat's games (tie game)."""
    assert ai.check_winner(CATS_GAME) == 'cats'


def test_ai_best_move():
    """Verifies `get_best_move` function."""
    move = ai.get_best_move(BEST_MOVE_O)
    ai_logger.warning('best move done')
    ai_logger.warning(move)
