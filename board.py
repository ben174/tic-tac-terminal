"""Module containing game logic"""
from enum import Enum
from collections import Counter
from math import inf as infinity

from loggers import board_logger, ai_logger


HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

class BoardState(Enum):
    '''
    Play state of the Board.

    '''
    PLAYING = 'Playing'
    FINISHED = 'Finished'
    CATS_GAME = 'Cat\'s Game'


class Player(Enum):
    '''
    Players (X and O)

    '''

    PLAYER_X = 'X'
    PLAYER_O = 'O'

    @classmethod
    def get_foe(cls, player):
        """ Returns the opposing `Player` for the specified `player`
        """
        foe = 'X' if player.value == 'O' else 'O'
        return cls(foe)


class Board:
    """ A class to hold the stateful Tic-Tac-Toe board, including the
    current board layout, the state of the board, and the current
    move.
    """

    def __init__(self):
        """ Creates a new instance of the Board class, optionally
        accepting a current board state. """
        board_logger.info('Game start')
        self.board = [
            [None]*3 for i in range(3)
        ]
        self.current_player = Player.PLAYER_X
        self.winning_span = []
        self.state = BoardState.PLAYING
        self.moves = []

    def undo(self):
        """ Undo the last move."""
        row, col = self.moves.pop()
        if row is not None and col is not None:
            board_logger.debug('Undoing last move: %sx%s', row, col)
            board_logger.debug('Board before:')
            board_logger.debug(str(self))
            self.board[row][col] = None
            board_logger.debug('Board after:')
            board_logger.debug(str(self))
            self.last_selected = (None, None)
        else:
            board_logger.error('Attempt to UNDO when no move has been made.')

    def get_winner(self):
        """ Find winner on board."""
        spans = {}

        # check each row and column
        for i in range(3):
            row = self.board[i]
            spans[f'row {i}'] = row
            col = self.board[0][i], self.board[1][i], self.board[2][i]
            spans[f'col {i}'] = col

        # check diagonal front and back
        diag_f = self.board[0][0], self.board[1][1], self.board[2][2]
        diag_b = self.board[0][2], self.board[1][1], self.board[2][0]
        spans['diag f'] = diag_f
        spans['diag b'] = diag_b
        board_logger.debug('Checking diagonal (\\): %s', diag_f)
        board_logger.debug('Checking diagonal (/): %s', diag_b)

        for span_name, span in spans.items():
            span_count = Counter(span)
            board_logger.debug('Checking span: %s - %s', span_name, span)
            if (span_count[Player.PLAYER_O] == 3 or
               span_count[Player.PLAYER_X] == 3):
                winner = Player.PLAYER_O if span_count[Player.PLAYER_O] > 0 else Player.PLAYER_X
                board_logger.info('Winner: %s', winner)
                return winner

    def check_state(self) -> BoardState:
        """ Check board for a win condition or errors.

        Checks the board for win conditions in rows, columns and diagonal.
        Also checks the board for invalid states (multiple wins), or a
        Cat's Game (tie game).

        :returns:
            A BoardState with the current state of the board.
        """
        win_count = 0
        spans = {}

        # check each row and column
        for i in range(3):
            row = self.board[i]
            spans[f'row {i}'] = row
            col = self.board[0][i], self.board[1][i], self.board[2][i]
            spans[f'col {i}'] = col

        # check diagonal front and back
        diag_f = self.board[0][0], self.board[1][1], self.board[2][2]
        diag_b = self.board[0][2], self.board[1][1], self.board[2][0]
        spans['diag f'] = diag_f
        spans['diag b'] = diag_b
        board_logger.debug('Checking diagonal (\\): %s', diag_f)
        board_logger.debug('Checking diagonal (/): %s', diag_b)

        # do the check
        clear_row_found = False
        for span_name, span in spans.items():
            span_count = Counter(span)
            board_logger.debug('Checking span: %s - %s', span_name, span)

            # check if at least one span isn't blocked
            if (span_count[Player.PLAYER_O] == 0 or
               span_count[Player.PLAYER_X] == 0):
                board_logger.debug(
                   'Found a span which is clear for win: %s', span
                )
                clear_row_found = True

            if (span_count[Player.PLAYER_O] == 3 or
               span_count[Player.PLAYER_X] == 3):
                board_logger.info('Winner, winner, chicken dinner.')
                board_logger.info(span_count)
                self.winning_span = span_name
                win_count += 1

        if not clear_row_found:
            board_logger.info('Cat\'s game')
            return BoardState.CATS_GAME

        # if win, ensure exactly one win
        if win_count == 1:
            board_logger.info('Found one win')
            return BoardState.FINISHED
        if win_count > 1:
            board_logger.error('Invalid board state (multiple wins)')
            board_logger.debug(str(self))
            raise MultipleWinError()

        return BoardState.PLAYING

    def select_cell(self, row, column):
        """ Plays a square (of `self.current_player`) in the specified `row`/`column`.

        Attempts to play a square for the specified `row`/`column`. If the
        square is playable, assigns the value of `self.current_player` to that
        square.
        Then, `self.check_win()` is called to set the new `BoardState` value
        and toggle the player (if the game is still in progress).

        :returns:
            A BoardState with the current state of the board.

        """
        current_val = self.board[row][column]
        if current_val is not None:
            error_text = f'Attempted to select a non-empty cell {row}x{column}'
            board_logger.error(error_text)
            board_logger.debug(str(self))
            raise InvalidMoveError(error_text)
        self.board[row][column] = self.current_player
        self.moves.append((row, column))
        self.state = self.check_state()
        if self.state == BoardState.PLAYING:
            # only toggle current_player if the self.state is still PLAYING
            self.current_player = Player.get_foe(self.current_player)
            # if self.current_player == Player.PLAYER_O and self.enable_ai:
            #    grid = self.board_to_grid()
            #    board_logger.info(grid)
            #    move = ai.get_best_move(grid)
            #    board_logger.info('AI selected best move %s', move)
            #    self.select_cell(move[0], move[1])
            board_logger.debug('Setting player: %s', self.current_player.value)

    def get_available_squares(self) -> [(int, int)]:
        """ Returns a list of coordinates for empty squares on the board.
        """
        ret = []
        for row_num in range(3):
            for col_num in range(3):
                if self.board[row_num][col_num] is None:
                    ret.append((row_num, col_num))
        board_logger.debug('Get available squares:')
        board_logger.debug(self.board)
        board_logger.debug(ret)
        return ret

	def wins(self, state, player):
		"""
		This function tests if a specific player wins. Possibilities:
		* Three rows    [X X X] or [O O O]
		* Three cols    [X X X] or [O O O]
		* Two diagonals [X X X] or [O O O]
		:param state: the state of the current board
		:param player: a human or a computer
		:return: True if the player wins
		"""
		win_state = [
			[state[0][0], state[0][1], state[0][2]],
			[state[1][0], state[1][1], state[1][2]],
			[state[2][0], state[2][1], state[2][2]],
			[state[0][0], state[1][0], state[2][0]],
			[state[0][1], state[1][1], state[2][1]],
			[state[0][2], state[1][2], state[2][2]],
			[state[0][0], state[1][1], state[2][2]], [state[2][0], state[1][1], state[0][2]],
		]
		if [player, player, player] in win_state:
			return True
		else:
			return False



    def get_board_state(self):
        ret = []
        for row in self.board:
            row_vals = []
            for cell in row:
                val = 0
                if cell == Player.PLAYER_O:
                    val = COMP
                if cell == Player.PLAYER_X:
                    val = HUMAN
                row_vals.append(val)
            ret.append(row_vals)
        return ret

    def make_best_move(self):
        depth = len(self.get_available_squares())
        winner = self.get_winner()

        if depth == 0 or winner is not None:
            board_logger.error('Make best move when game is done.')
            return

        state = self.get_board_state()

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax(state, depth, COMP)
            x, y = move[0], move[1]

        board_logger.error("BEEEEEST MOVE")
        board_logger.error(x)
        board_logger.error(y)


    def minimax(self, state, depth, player):
        """
        AI function that choice the best move
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if player == COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        winner = self.get_winner()
        if depth == 0 or winner is not None:
            if winner == COMP:
                score = 1
            elif winner == HUMAN:
                score = -1
            else:
                score = 0
            return [-1, -1, score]

        for cell in self.empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

    def empty_cells(self, state):
        """
        Each empty cell will be added into cells' list
        :param state: the state of the current board
        :return: a list of empty cells
        """
        cells = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])

        return cells


    '''
    def make_best_move(self):
        """ Makes the best move using recurison (MiniMax algorithm).
        """
        board_logger.debug('Make best move')
        best_score = float('-inf')
        best_move = None
        for move in self.get_available_squares():
            row, col = move
            self.select_cell(row, col)
            score = self.minimax(False, Player.PLAYER_O)
            self.undo()
            if score > best_score:
                best_score = score
                best_move = move
        board_logger.debug('Selecting best move: %s', best_move)
        self.board.select_cell(best_move)

    def minimax(self, max_turn, maximizer):
        """ Implementation of minimax algorithm to determine best move. """
        state = self.check_state()
        if state is BoardState.CATS_GAME:
            return 0
        if state is BoardState.FINISHED:
            winner = self.get_winner()
            return 1 if winner == maximizer else -1

        scores = []
        available_squares = self.get_available_squares()
        for move in available_squares:
            row, col = move
            board_logger.debug('Minimax selecting available square: %s', move)
            board_logger.debug('Board:')
            board_logger.debug(str(self))
            board_logger.debug('Available Squares:')
            board_logger.debug(available_squares)
            self.select_cell(row, col)
            scores.append(self.minimax(not max_turn, maximizer))
            self.undo()
        return max(scores) if max_turn else min(scores)

    '''

    def __repr__(self):
        ret = 'Board State:\n'
        for row in self.board:
            for cell in row:
                if not cell:
                    ret += '-'
                else:
                    ret += cell.value
            ret += '\n'
        ret += '\n\n'
        return ret


class MultipleWinError(Exception):
    """ An exception which is thrown when the board has invalid state containing
    more than one win.

    """


class InvalidMoveError(Exception):
    """ An exception which is thrown when the an invalid move attempt is made
    (selecting an already-occupied square.

    """
