     .---. .-. .---.  .---.  .--.   .---.
    {_   _}| |/  ___}{_   _}/ {} \ /  ___}
      | |  | |\     }  | | /  /\  \\     }
      `-'  `-' `---'   `-' `-'  `-' `---'
     .---. .----..----. .-.   .-..-..-. .-.  .--.  .-.
    {_   _}| {_  | {}  }|  `.'  || ||  `| | / {} \ | |
      | |  | {__ | .-. \| |\ /| || || |\  |/  /\  \| `--.
      `-'  `----'`-' `-'`-' ` `-'`-'`-' `-'`-'  `-'`----'"""

[![Tic-Tac-Terminal](https://github.com/ben174/tic-tac-terminal/actions/workflows/python-package.yml/badge.svg)](https://github.com/ben174/tic-tac-terminal/actions/workflows/python-package.yml)

# Tic-Tac-Terminal
Tic-Tac-Toe in the terminal. A game by Ben Friedland (www.bugben.com)

## Features

### Separation of concerns:

Consists of three main modules:

- **`board.py`** - The game logic
- **`ai.py`** - AI for playing against the computer
- **`ui.py`** - A fancy curses-style UI to play the game in your console
- **`tests/board.py`** - Thorough testing of the entire game module

### Graceful exception handling:

Dedicated `Exception` classes to alert to invalid board conditions or moves.

### Rigorous testing and CI pipeline:

Full coverage of the board module to ensure nothing breaks. GitHub workflow to test on each commit.


## Usage

### Run from the command line:

```bash
pip install -r requirements.txt
python ui.py
```


### Use the `Board` module directly

```python
def test_win():
    """ Plays a standard game, ensuring the PLAYING state remains
    until the game is finished.
    """
    board = Board()

    # X: X - -
    #    - - -
    #    - - - 
    board.select_cell(0, 0)

    # O: X - -
    #    O - -
    #    - - -
    board.select_cell(1, 0)

    # X: X X -
    #    O - -
    #    - - - 
    board.select_cell(0, 1)

    # O: X X -
    #    O O -
    #    - - - 
    board.select_cell(1, 1)
    assert board.state == BoardState.PLAYING

    # X: X X X -- Finish Him!
    #    O O -
    #    - - - 
    board.select_cell(0, 2)
    assert board.state == BoardState.FINISHED
```

## License

[MIT © Ben Friedland](../LICENSE)
