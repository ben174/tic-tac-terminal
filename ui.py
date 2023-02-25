"""Module containing terminal UI"""
from textual.app import App, ComposeResult
from textual import events, log
from textual.containers import Container
from textual.widgets import Button, Static, Header, Footer

from banners import BANNER
from board import Board, BoardState, Player
from board import InvalidMoveError


class TicTacTerminalApp(App):
    """Tic-Tac-Terminal UI"""
    CSS_PATH = 'ui.css'
    TITLE = 'Tic-Tac-Terminal'
    SUB_TITLE = 'A terminal-based tic-tac-toe app by Ben Friedland'

    def __init__(self):
        super().__init__()
        game_layout = [
            [Player.PLAYER_X, Player.PLAYER_O, None],
            [Player.PLAYER_X, Player.PLAYER_O, None],
            [Player.PLAYER_X, Player.PLAYER_X, None],
        ]
        game_layout = None
        self.board = Board(game_layout, ai=True)

    def on_mount(self) -> None:
        """Occurs after initial layout is performed."""
        self.draw_board()

    def compose(self) -> ComposeResult:
        """Draws initial layout."""
        yield Container(
            Header(),
            Static(BANNER, id="header-label"),
            Button(" ", id="cell-0-0"),
            Button(" ", id="cell-0-1"),
            Button(" ", id="cell-0-2"),
            Button(" ", id="cell-1-0"),
            Button(" ", id="cell-1-1"),
            Button(" ", id="cell-1-2"),
            Button(" ", id="cell-2-0"),
            Button(" ", id="cell-2-1"),
            Button(" ", id="cell-2-2"),
            Footer(),
            id="calculator",
        )

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
            self.query_one(f"#cell-{row}-{col}", Button).press()
        elif key == "q":
            #TODO: quit app
            log.warning('todo: quit app')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        log('test')
        log(locals())
        log(event.button)
        # event.button.add_class('selected')
        # event.button.styles.background = 'red'
        log('button split')
        log(event.button.id.split('-')[1:])
        row, col = (int(i) for i in event.button.id.split('-')[1:])
        try:
            self.board.select_cell(row, col)
            self.draw_board()
        except InvalidMoveError:
            log('Invalid move, dummy')

    def draw_board(self):
        """ Draws the updated board."""
        for row_num in range(3):
            for col_num in range(3):
                cell = self.board.board[row_num][col_num]
                button = self.query_one(f'#cell-{row_num}-{col_num}')
                button.remove_class('win')
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

        if self.board.state == BoardState.FINISHED:
            log('Winner')
            log(self.board.winning_span)

            for cell in self.board.winning_span:
                button = self.query_one(f'#cell-{cell[0]}-{cell[1]}')
                button.addClass('win')

            self.board = Board()
            self.draw_board()


if __name__ == "__main__":
    TicTacTerminalApp().run()
