"""Module containing terminal UI"""
from textual.app import App, ComposeResult
from textual import events, log
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer

from banners import BANNER
from game import Game, GameOutcome
from board import BoardState, Player
from board import InvalidMoveError


class HelpScreen(Screen):
    BINDINGS = [
                   ("escape", "app.pop_screen", "Pop screen"),
                   ("q", "app.pop_screen", "Pop screen")
               ]

    def compose(self) -> ComposeResult:
        yield Static(BANNER, id="header-label")
        yield Static('Simple terminal tic-tac-toe game by Ben Friedland')
        yield Static("Press escape to close.[blink]_[/]")


class BoardScreen(Screen):
    """Main game screen"""
    TITLE = 'Tic-Tac-Terminal'
    SUB_TITLE = 'A terminal-based tic-tac-toe app by Ben Friedland'

    def __init__(self):
        super().__init__()

    def on_mount(self) -> None:
        """Occurs after initial layout is performed."""
        self.draw_board()

    def compose(self) -> ComposeResult:
        """Draws initial layout."""
        yield Header()
        with Container(id="game-container"):
            with Container(id="cells-container"):
                for row_num in range(3):
                    for col_num in range(3):
                        yield Button(id=f'cell-{row_num}-{col_num}')
            with Container(id="status-container"):
                yield Static("Winner: ", id="winner-label")
                yield Static("Game: ", id="status-label")
                yield Static("Stats:", id="stats-label")
                yield Static("Wins:", id="win-count-label")
                yield Static("Losses:", id="lose-count-label")
                yield Static("Ties:", id="tie-count-label")
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        """Parse numeric keys and translate to a cell."""
        key = event.key
        if key.isdecimal():
            index = int(key) - 1
            row = index // 3
            col = index % 3
            button_id = f'#cell-{row}-{col}'
            self.query_one(button_id, Button).press()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        board_state = game.board.get_state()
        if board_state is not BoardState.PLAYING:
            log('Attempt to move when game is not running')
            return

        row, col = (int(i) for i in event.button.id.split('-')[1:])
        log(f'Select cell: {row}x{col}')
        try:
            game.board.select_cell(row, col)
        except InvalidMoveError:
            log('Invalid move, dummy')
            return

        board_state = game.board.get_state()
        if board_state is BoardState.FINISHED:
            winner = game.board.get_winner()
            if winner is Player.PLAYER_X:
                game.outcomes[GameOutcome.WIN] += 1
            elif winner is Player.PLAYER_O:
                game.outcomes[GameOutcome.LOSE] += 1
        elif board_state is BoardState.CATS_GAME:
            game.outcomes[GameOutcome.CATS_GAME] += 1
        else:
            game.board.make_best_move()
        self.draw_board()

    def draw_board(self):
        """ Draws the updated board."""
        game_state = game.board.get_state().value
        winner = game.board.get_winner()

        if winner is not None:
            winner = winner.value
        else:
            winner = '-'
        self.query_one('#status-label').update('Game Status: ' + game_state)
        self.query_one('#winner-label').update('Winner: ' + winner)

        win_count = str(game.outcomes[GameOutcome.WIN])
        lose_count = str(game.outcomes[GameOutcome.LOSE])
        tie_count = str(game.outcomes[GameOutcome.CATS_GAME])

        self.query_one('#win-count-label').update(f'Wins: {win_count}')
        self.query_one('#lose-count-label').update(f'Losses: {lose_count}')
        self.query_one('#tie-count-label').update(f'Ties: {tie_count}')

        for row_num in range(3):
            for col_num in range(3):
                cell = game.board.board[row_num][col_num]
                button = self.query_one(f'#cell-{row_num}-{col_num}')
                button.remove_class('win')
                button.label = cell.value if cell is not None else '-'
                if cell is None:
                    button.remove_class('player-X')
                    button.remove_class('player-O')
                elif cell == Player.PLAYER_X:
                    button.remove_class('player-O')
                    button.add_class('player-X')
                    button.text = 'poop'
                elif cell == Player.PLAYER_O:
                    button.remove_class('player-X')
                    button.add_class('player-O')

        if game.board.get_state() == BoardState.FINISHED:
            game.board.get_winner().value
            log('Winner')


game = Game()
board_screen = BoardScreen()
help_screen = HelpScreen()


class TicTacTerminalApp(App):
    """Tic-Tac-Terminal UI"""
    CSS_PATH = 'ui.css'
    TITLE = 'Tic-Tac-Terminal'
    SUB_TITLE = 'A terminal-based tic-tac-toe app by Ben Friedland'

    SCREENS = {
        'board': board_screen,
        'help': help_screen,
    }

    BINDINGS = [
        Binding(key='h', action='push_screen(\'help\')', description='Help'),
        Binding(key='q', action='app.quit', description='Quit'),
        Binding(key='r', action='restart', description='Restart Game'),
    ]

    def __init__(self):
        super().__init__()

    def on_mount(self) -> None:
        """Occurs after initial layout is performed."""
        self.push_screen('board')

    def action_restart(self):
        game.new_game()
        board_screen.draw_board()


if __name__ == "__main__":
    TicTacTerminalApp().run()
