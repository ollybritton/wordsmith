import random
from .strategy import Strategy


THINK_RIGHT_POSITIONS = [
    ("T", 0, 0),
    ("H", 0, 1),
    ("I", 0, 2),
    ("N", 0, 3),
    ("K", 0, 4),
    ("R", 1, 0),
    ("I", 1, 1),
    ("G", 1, 2),
    ("H", 1, 3),
    ("T", 1, 4),
]


def think_right_pick_char(board):
    for char, i, j in THINK_RIGHT_POSITIONS:
        if board.state[i][j] != char:
            assert board.state[i][j] == ""
            return (char, i, j)

    return random.choice(board.possible_moves)


def think_right_given_char(board, char):
    return (char,) + board.possible_positions[-1]


StrategyThinkRight = Strategy(
    "ThinkRight",
    "Put the letters for 'think' and 'right', and then pick randomly",
    think_right_pick_char,
    think_right_given_char,
)
