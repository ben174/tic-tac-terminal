import logging
from enum import Enum
from collections import Counter


logging.basicConfig(filename='game.log', level=logging.DEBUG, force=True)


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


class Board:
    '''
    A class to hold the stateful Tic-Tac-Toe board, including the
    current board layout, the state of the board, and the current
    move.

    '''

    def __init__(self):
        logging.info('Game start')
        self.board = [[None]*3 for i in range(3)]
        self.current_player = Player.PLAYER_X
        self.state = BoardState.PLAYING

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
        logging.debug('Checking diagonal (\\): %s', diag_f)
        logging.debug('Checking diagonal (/): %s', diag_b)

        # do the check
        clear_row_found = False
        for span_name, span in spans.items():
            span_count = Counter(span)
            logging.debug('Checking span: %s - %s', span_name, span)

            # check if at least one span isn't blocked
            if (span_count[Player.PLAYER_O] == 0 or
               span_count[Player.PLAYER_X] == 0):
                logging.debug('Found a span which is clear for win: %s', span)
                clear_row_found = True

            if (span_count[Player.PLAYER_O] == 3 or
               span_count[Player.PLAYER_X] == 3):
                logging.info('Winner, winner, chicken dinner.')
                logging.info(span_count)
                win_count += 1

        if not clear_row_found:
            logging.info('Cat\'s game')
            return BoardState.CATS_GAME

        # if win, ensure exactly one win
        if win_count == 1:
            logging.info('Found one win')
            return BoardState.FINISHED
        if win_count > 1:
            logging.error('Invalid board state (multiple wins)')
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
            raise InvalidMoveError('Attempted to select a non-empty cell')
        self.board[row][column] = self.current_player
        self.state = self.check_state()
        if self.state == BoardState.PLAYING:
            # only toggle current_player if the self.state is still PLAYING
            self.current_player = (Player.PLAYER_O
                                   if self.current_player == Player.PLAYER_X
                                   else Player.PLAYER_X)
            logging.debug('Setting player: %s', self.current_player.value)

    def __repr__(self):
        ret = ''
        for row in self.board:
            for cell in row:
                if not cell:
                    ret += '-'
                else:
                    ret += cell.value
            ret += '\n'
        return ret


class MultipleWinError(Exception):
    """ An exception which is thrown when the board has invalid state containing
    more than one win.

    """


class InvalidMoveError(Exception):
    """ An exception which is thrown when the an invalid move attempt is made
    (selecting an already-occupied square.

    """
