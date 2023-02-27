"""Module containing game logic"""
import random
from enum import Enum
from collections import Counter, defaultdict
from math import inf as infinity

from loggers import board_logger, ai_logger


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
        self.winning_span = []

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

    def get_state(self) -> BoardState:
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
        """ Plays a square (of `self.get_current_player()`) in the specified
        `row`/`column`.

        Attempts to play a square for the specified `row`/`column`. If the
        square is playable, assigns the value of `self.get_current_player()`
        to that square.

        """
        current_val = self.board[row][column]
        if current_val is not None:
            error_text = f'Attempted to select a non-empty cell {row}x{column}'
            board_logger.error(error_text)
            board_logger.debug(str(self))
            raise InvalidMoveError(error_text)
        self.board[row][column] = self.get_current_player()

    def get_current_player(self):
        """ Returns the Player whose turn it currently is. """
        board_logger.debug('Get current player')
        ret = Player.PLAYER_X
        square_counter = Counter()
        [square_counter.update(row) for row in self.board]
        board_logger.debug('Square counter:')
        board_logger.debug(square_counter)
        x_count = square_counter[Player.PLAYER_X]
        o_count = square_counter[Player.PLAYER_O]
        if x_count > o_count:
            ret = Player.PLAYER_O
        board_logger.debug('Get current player: %s', ret.value)
        board_logger.debug(str(self))
        return ret

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

    def make_best_move(self):
        board_logger.debug('Make best move')
        state = self.get_state()
        if state is not BoardState.PLAYING:
            board_logger.warning('Attempt to make best move in non playing state')
            return

        player = self.get_current_player()
        opponent = Player.get_foe(player)

        # win or block
        for row_num in range(3):
            row = self.board[row_num]
            counter = Counter(row)
            board_logger.debug('Row counter %s: %s', row_num, counter)
            # if there is one empty spot on this row, grab it!
            if ((counter[player] == 2 and counter[opponent] == 0) or
               (counter[opponent] == 2 and counter[player] == 0)):
                board_logger.debug('Found a span with one empty spot. Grabbing it.')
                for col_num in range(3):
                    cell_val = self.board[row_num][col_num]
                    if cell_val is None:
                        self.board[row_num][col_num] = player

        for col_num in range(3):
            col = self.board[0][col_num], self.board[1][col_num], self.board[2][col_num]
            counter = Counter(col)
            board_logger.debug('Column counter %s: %s', col_num, counter)
            # if there is one empty spot on this column, grab it!
            if ((counter[player] == 2 and counter[opponent] == 0) or
               (counter[opponent] == 2 and counter[player] == 0)):
                board_logger.debug('Found a span with one empty spot. Grabbing it.')
                for row_num in range(3):
                    cell_val = self.board[row_num][col_num]
                    if cell_val is None:
                        self.board[row_num][col_num] = player

        # if a corner is available, take it
        corner_cells = ((0, 0), (0, 2), (2, 0), (2, 2))
        for cell in corner_cells:
            if self.board[cell[0]][cell[1]] is None:
                board_logger.debug('Taking a corner cell.')
                self.board[cell[0]][cell[1]] = player
                return

        # if the center is available, take it
        if self.board[1][1] is None:
            board_logger.debug('Taking the center cell.')
            self.board[1][1] = player
            return

        # if an edge is available, take it
        edge_cells = ((1, 0), (0, 1), (2, 1), (1, 2))
        for cell in edge_cells:
            if self.board[cell[0]][cell[1]] is None:
                board_logger.debug('Taking an edge cell.')
                self.board[cell[0]][cell[1]] = player
                return

        raise InvalidMoveError('No moves available')

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
