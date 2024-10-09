import random
from .strategy import Strategy


def random_pick_char(board):
    return random.choice(board.possible_moves)


def random_given_char(board, char):
    return (char,) + random.choice(board.possible_positions)


StrategyRandom = Strategy(
    "Random",
    "Pick letters and positions randomly",
    random_pick_char,
    random_given_char,
)
