"""Module containing computer AI"""
from loggers import ai_logger


SCORES = {
  'X': 10,
  'O': -10,
  'cats': 0,
  None: 0,
}
POSITIVE_INFINITY = float('inf')
NEGATIVE_INFINITY = float('-inf')


def check_winner(grid, depth=0):
    ai_logger.debug('%sCheck Winner, Grid:', ' '*depth)
    ai_logger.debug(grid)

    winner = None

    for row_num in range(3):
        row = grid[row_num]
        if None not in row and len(set(row)) == 1:
            winner = row[0]

    for col_num in range(3):
        col = grid[0][col_num], grid[1][col_num], grid[2][col_num]
        if None not in col and len(set(col)) == 1:
            winner = col[0]
    diag_f = grid[0][0], grid[1][1], grid[2][2]
    if None not in diag_f and len(set(diag_f)) == 1:
        winner = diag_f[0]
    diag_b = grid[2][0], grid[1][1], grid[0][2]
    if None not in diag_b and len(set(diag_b)) == 1:
        winner = diag_b[0]

    open_spots = 0
    for row in grid:
        for cell in row:
            if cell is None:
                open_spots += 1

    if winner is None and open_spots == 0:
        return 'cats'
    ai_logger.debug('%sReturning %s', ' '*depth, winner)
    return winner


def mini_max(grid, depth, maximize):
    winner = check_winner(grid)

    if winner is not None:
        ai_logger.info('%sMINIMAX (winner) returning: %s, depth: %s, maximize: %s', ' '*depth, SCORES[winner], depth, maximize)
        return SCORES[winner]

    best_score = NEGATIVE_INFINITY if maximize else POSITIVE_INFINITY
    for row_num in range(3):
        for col_num in range(3):
            if grid[row_num][col_num] is None:
                grid[row_num][col_num] = 'O' if maximize else 'X'
                score = mini_max(grid, depth+1, not maximize)
                grid[row_num][col_num] = None
                if maximize:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)
    ai_logger.info('%sMINIMAX (maximize) returning: %s, depth: %s, maximize: %s', ' '*depth, best_score, depth, maximize)
    return best_score


def get_best_move(grid):
    best_score = NEGATIVE_INFINITY
    move = None

    for row_num in range(3):
        for col_num in range(3):
            if grid[row_num][col_num] is None:
                grid[row_num][col_num] = 'O'
                score = mini_max(grid, 0, False)
                grid[row_num][col_num] = None
                if score > best_score:
                    best_score = score
                    move = (row_num, col_num)
    return move

'''
function minimax(board, depth, isMaximizing) {
let result = checkWinner();
if (result !== null) {
  return scores[result];
}

if (isMaximizing) {
  let bestScore = -Infinity;
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      // Is the spot available?
      if (board[i][j] == '') {
        board[i][j] = ai;
        let score = minimax(board, depth + 1, false);
        board[i][j] = '';
        bestScore = max(score, bestScore);
      }
    }
  }
  return bestScore;
} else {
  let bestScore = Infinity;
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      // Is the spot available?
      if (board[i][j] == '') {
        board[i][j] = human;
        let score = minimax(board, depth + 1, true);
        board[i][j] = '';
        bestScore = min(score, bestScore);
      }
    }
  }
  return bestScore;
}
}
function bestMove() {
// AI to make its turn

let bestScore = -Infinity;
let move;
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    // Is the spot available?
    if (board[i][j] == '') {
      board[i][j] = ai;
      let score = minimax(board, 0, false);
      board[i][j] = '';
      if (score > bestScore) {
        bestScore = score;
        move = { i, j };
      }
    }
  }
}
board[move.i][move.j] = ai;
currentPlayer = human;
}

let scores = {
X: 10,
O: -10,
tie: 0
};


'''
