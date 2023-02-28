"""Module orchestrating game flow, including AI and stats."""
from enum import Enum

from loggers import game_logger
from board import Board

class GameOutcome(Enum):
    WIN = 'Win'
    LOSE = 'Lose'
    CATS_GAME = 'Cat\'s Game'


class GameDifficulty(Enum):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    IMPOSSIBLE = 'Impossible'

    def __repr__(self):
        return self.value


class Game:
    def __init__(self, ai=True):
        game_logger.debug('Initializing new game')
        self.board = Board()
        self.difficulty = GameDifficulty.IMPOSSIBLE
        self.ai = ai
        self.outcomes = {
            GameOutcome.WIN: 0,
            GameOutcome.LOSE: 0,
            GameOutcome.CATS_GAME: 0,
        }

    def new_game(self, ai=True, difficulty=GameDifficulty.IMPOSSIBLE):
        self.board = Board()

    def get_state(self):
        return self.board.get_state()
