from .strategy import Strategy

import random
import numpy as np
from datetime import datetime

# Code primarily adapted from: https://ai-boson.github.io/mcts/

PROGRESS_BAR = True


class Node:
    def __init__(self, chance_node, char, c_param=1.0, time=45, board=None,
                 parent=None, parent_action=None):
        self.board = board
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = dict()

        self._total_score = 0
        self._total_trials = 0

        self.chance_node = chance_node
        self.char = char

        self._untried_actions = self.untried_actions()

        self.c_param = c_param
        self.time = time

    def untried_actions(self):
        if not self.chance_node:
            self._untried_actions = self.board.possible_moves
        else:
            self._untried_actions = [
                (self.char,) + pos for pos in self.board.possible_positions
            ]

        random.shuffle(self._untried_actions)
        return self._untried_actions

    def q(self):
        return self._total_score

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_board = self.board.move(*action)

        chance = not self.chance_node
        char = "" if self.char != "" else action[0]

        child_node = Node(
            chance,
            char,
            self.c_param,
            self.time,
            next_board,
            parent=self,
            parent_action=action,
        )
        self.children.append(child_node)

        return child_node

    def is_terminal_node(self):
        return self.board.game_over()

    def rollout(self):
        current_rollout_state = self.board

        while not current_rollout_state.game_over():
            possible_moves = current_rollout_state.possible_moves
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(*action)

        return current_rollout_state.score()

    def backpropagate(self, result):
        score, _ = result

        self._number_of_visits += 1
        self._total_score += score

        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param):
        choices_weights = [
            (c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n()))
            for c in self.children
        ]

        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self

        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child(self.c_param)

        return current_node

    def best_action(self):
        start = datetime.now()

        while (datetime.now() - start).seconds < self.time:
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)

    def is_game_over(self):
        return self.board.game_over()

    def game_result(self):
        return self.board.score()

    def move(self, action):
        self.chance_node = not self.chance_node
        self.char = "" if self.char != "" else action[0]

        self.board = self.board.move(*action)


def mcts_strategy(c_param, time):
    def mcts_pick_char(board):
        root = Node(False, "", c_param, time, board)

        return root.best_action().parent_action

    def mcts_given_char(board, char):
        root = Node(True, char, c_param, time, board)

        return root.best_action().parent_action

    return mcts_pick_char, mcts_given_char


StrategyMCTSEasy = Strategy(
    "MonteCarloTreeSearch-easy",
    "Use the Monte-Carlo tree search algorithm (thinks for 3 seconds)",
    *mcts_strategy(c_param=1.414, time=3),
)

StrategyMCTSMedium = Strategy(
    "MonteCarloTreeSearch-medium",
    "Use the Monte-Carlo tree search algorithm (thinks for 15 seconds)",
    *mcts_strategy(c_param=1.414, time=15),
)

StrategyMCTSHard = Strategy(
    "MonteCarloTreeSearch-hard",
    "Use the Monte-Carlo tree search algorithm (thinks for 45 seconds)",
    *mcts_strategy(c_param=1.414, time=45),
)

StrategyMCTSVeryHard = Strategy(
    "MonteCarloTreeSearch-very-hard",
    "Use the Monte-Carlo tree search algorithm (thinks for 90 seconds)",
    *mcts_strategy(c_param=1.414, time=90),
)
