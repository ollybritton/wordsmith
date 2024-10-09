from tqdm import tqdm

from .strategy import Strategy
from .english_random import random_char_with_dist

# Number of trials to make of random play in order to evaluate position
ROLLOUT_TRIALS = 2


class Node:
    def __init__(self, board):
        self.board = board

    @property
    def options(self):
        return [Node(self.board.move(*move)) for move in self.board.possible_moves]


def evaluate(board, trials):
    """
    Heuristic evaluation of the value of a board.
    """

    total_score = 0

    for _ in range(trials):
        feasible_board = board.copy()

        for i, j in board.possible_positions:
            char = random_char_with_dist()
            feasible_board.move(char, i, j)

        score, _ = feasible_board.score()
        total_score += score

    return total_score / trials


def expectimax(depth, node, is_max):
    if depth >= 1:
        return evaluate(node.board, ROLLOUT_TRIALS)

    if len(node.options) == 0:
        return node.board.score()

    options = node.options

    if is_max:
        return max([expectimax(depth+1, option, False) for option in options])
    else:
        # Assumes all outcomes are equally likely
        return sum(
            [expectimax(depth+1, option, True) for option in options]
        ) / len(options)


def expectimax_pick_char(board):
    best_move = None
    best_score = None

    # Start from depth 1 here since the search space is larger by a factor of 26
    for move in tqdm(board.possible_moves):
        root = Node(board.move(*move))
        score = expectimax(1, root, True)

        if best_score is None:
            best_score = score
            best_move = move
        elif score > best_score:
            best_score = score
            best_move = move

    return best_move


def expectimax_given_char(board, char):
    best_move = None
    best_score = None

    # Start from depth 0 here since the search space is smaller by a factor of 26
    for i, j in tqdm(board.possible_positions):
        root = Node(board.move(char, i, j))
        score = expectimax(0, root, True)

        if best_score is None:
            best_score = score
            best_move = (char, i, j)
        elif score > best_score:
            best_score = score
            best_move = (char, i, j)

    return best_move


StrategyExpectimax = Strategy(
    "Expectimax",
    "Choose moves which look best over average of some outcomes",
    expectimax_pick_char,
    expectimax_given_char,
)
