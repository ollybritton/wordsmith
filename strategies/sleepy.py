from .strategy import Strategy


def sleepy_pick_char(board):
    return ("Z",) + board.possible_positions[0]


def sleepy_given_char(board, char):
    return (char,) + board.possible_positions[-1]


StrategySleepy = Strategy(
    "Sleepy",
    "Put Zs at the start, and the other player's letters at the end",
    sleepy_pick_char,
    sleepy_given_char,
)
