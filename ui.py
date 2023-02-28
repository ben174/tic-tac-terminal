"""Module containing terminal UI"""
from textual.app import App, ComposeResult, RenderResult
from textual import events, log
from textual.binding import Binding
from textual.containers import Container, Horizontal, Grid
from textual.reactive import reactive
from textual.widget import Widget
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer, Input

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
        yield Static(" Windows ", id="title")
        yield Static("Help screen")
        yield Static("Press escape to close.[blink]_[/]", id="any-key")

class StatsScreen(Screen):
    BINDINGS = [
                   ("escape", "app.pop_screen", "Pop screen"),
                   ("q", "app.pop_screen", "Pop screen")
               ]
    who = reactive("Paul")
    name = reactive("Paul")
    count = reactive(0)
    is_cool = reactive(True)

    def compose(self) -> ComposeResult:
        yield Static(" Windows ", id="title")
        yield Static(f"Error goes here: {self.who}")
        yield Static("Press any key to continue [blink]_[/]", id="any-key")

    def on_mount(self) -> None:
        self.name = "stats mounted"


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
        # yield Static(BANNER, id="header-label")
        with Container(id="game-container"):
            with Container(id="cells-container"):
                for row_num in range(3):
                    for col_num in range(3):
                        yield Button(id=f'cell-{row_num}-{col_num}')
            with Container(id="status-container"):
                yield Static("Wins: ", id="wins-label")
                yield Static("Game: ", id="status-label")

        yield Footer()

    def on_key(self, event: events.Key) -> None:
        """Called when the user presses a key."""
        key = event.key
        if key.isdecimal():
            index = int(key) - 1
            log("LOGLOG")
            log(index=index)
            print(index)
            row = index // 3
            col = index % 3
            button_id = f'#cell-{row}-{col}'
            log('Pressing button id:')
            log(button_id)
            self.query_one(button_id, Button).press()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        log('test')
        log(locals())
        log(event.button)
        # event.button.add_class('selected')
        # event.button.styles.background = 'red'
        log('button split')
        log(event.button.id.split('-')[1:])
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
            #todo: bell
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
        self.query_one('#wins-label').update('Winner: ' + winner)

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

stats_screen = StatsScreen()
board_screen = BoardScreen()
help_screen = HelpScreen()

class TicTacTerminalApp(App):
    """Tic-Tac-Terminal UI"""
    CSS_PATH = 'ui.css'
    TITLE = 'Tic-Tac-Terminal'
    SUB_TITLE = 'A terminal-based tic-tac-toe app by Ben Friedland'

    SCREENS = {
        'stats': stats_screen,
        'board': board_screen,
        'help': help_screen,
    }

    BINDINGS = [
        Binding(key='s', action='push_screen(\'stats\')', description='Show Stats'),
        Binding(key='h', action='push_screen(\'help\')', description='Show Help'),
        Binding(key='q', action='app.quit', description='Quit'),
        Binding(key='r', action='restart', description='Restart Game'),
    ]


    def __init__(self):
        self.counter = 0
        super().__init__()

    def on_mount(self) -> None:
        """Occurs after initial layout is performed."""
        stats_screen.who = '-'
        self.push_screen('board')

    def action_restart(self):
        game.new_game()
        board_screen.draw_board()


if __name__ == "__main__":
    TicTacTerminalApp().run()
