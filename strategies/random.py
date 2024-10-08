import random
from .strategy import Strategy


def random_pick_char(board):
    return random.choice(board.possible_moves())


def random_given_char(board, char):
    possible = board.possible_moves()
    possible_with_char = []

    for move in possible:
        if move[0] == char:
            possible_with_char.append(move)

    return random.choice(possible_with_char)


StrategyRandom = Strategy(
    "Random",
    "Pick letters and positions randomly",
    random_pick_char,
    random_given_char,
)
