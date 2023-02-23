from enum import Enum


class BoardState(Enum):
    '''
    Play state of the Board.

    '''
    PLAYING = 'Playing'
    FINISHED = 'Finished'
    CATS_GAME = 'Cat\'s Game'
    INVALID = 'Invalid'


class Player(Enum):
    '''
    Players (X and O)

    '''

    X = 'X'
    O = 'O'



class Board:
    '''
    A class to hold the stateful Tic-Tac-Toe board, including the
    current board layout, the state of the board, and the current
    move.

    '''

    def __init__(self):
        self.board = [[None]*3 for i in range(3)]
        self.current_player = Player.X
        self.state = BoardState.PLAYING

    def check_win(self):
        """ Check board for a win condition.

        Checks the board for win conditions in rows, columns and diagonal.
        Also checks the board for invalid states (multiple wins), or a
        Cat's Game (tie game).

        :returns:
            A BoardState with the current state of the board.

        """
        win_count = 0
        win_cell = None
        for i in range(3):
            print('i', i)
            row = self.board[i]
            print('row', row)
            print(set(row))
            print()
            col = self.board[0][i], self.board[1][i], self.board[2][i]
            print('col', col)
            print(set(col))
            print()
            print()
            # if self.board[i][0]

            # if self.board[i][0] ==

        #TODO: raise exception based on win_count, also set self.state = 'INVALID'
        #TODO: if game is finished set self.state = 'FINISHED'
        #TODO: check cats game ?
        # if len(set(row)) == 2 for all rows and cols and diagonals

    def select_cell(self, row, column):
        current_val = self.board[row][column]
        if current_val is not None:
            raise InvalidMoveException('Attempted to select a non-empty cell')
        self.board[row][column] = self.current_player
        if self.check_win() == BoardState.PLAYING:

            # only toggle current_player if the self.state is still PLAYING
            self.current_player = Player.O if self.current_player == Player.X else Player.X

    def __str__(self):
        ret = ''
        for row in self.board:
            for cell in row:
                if not cell:
                    ret += '-'
                else:
                    ret += cell
            ret += '\n'
        return ret


class MultipleWinException(Exception):
    pass

class InvalidMoveException(Exception):
    pass
