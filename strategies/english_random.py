import random
from .strategy import Strategy

# Distribution of letters in English dictionaries, from:
# https://en.wikipedia.org/wiki/Letter_frequency
ENGLISH_DIST = [
    ("E", 0.1100),
    ("S", 0.0870),
    ("I", 0.0860),
    ("A", 0.0780),
    ("R", 0.0730),
    ("N", 0.0720),
    ("T", 0.0670),
    ("O", 0.0610),
    ("L", 0.0530),
    ("C", 0.0400),
    ("D", 0.0380),
    ("U", 0.0330),
    ("G", 0.0300),
    ("P", 0.0280),
    ("M", 0.0270),
    ("H", 0.0230),
    ("B", 0.0200),
    ("Y", 0.0160),
    ("F", 0.0140),
    ("V", 0.0100),
    ("K", 0.0097),
    ("W", 0.0091),
    ("Z", 0.0044),
    ("X", 0.0027),
    ("J", 0.0021),
    ("Q", 0.0019),
]


def random_char_with_dist():
    unif = random.random()
    sum = 0

    for char, freq in ENGLISH_DIST:
        sum += freq

        if unif < sum:
            return char


def english_random_pick_char(board):
    return (random_char_with_dist(),) + random.choice(board.possible_positions)


def english_random_given_char(board, char):
    return (char,) + random.choice(board.possible_positions)


StrategyEnglishRandom = Strategy(
    "EnglishRandom",
    "Pick letters according to their relative frequency in English dictionaries",
    english_random_pick_char,
    english_random_given_char,
)
