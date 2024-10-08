import numpy as np

ALPHABET = np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
WORDS_5 = []
WORDS_4 = []
WORDS_3 = []

with open("data/5-letter-words.txt", "r") as f:
    WORDS_5 = f.read().split("\n")

with open("data/4-letter-words.txt", "r") as f:
    WORDS_4 = f.read().split("\n")

with open("data/3-letter-words.txt", "r") as f:
    WORDS_3 = f.read().split("\n")


def score_word(word):
    word = word.lower()

    if word in WORDS_5:
        return 10, word

    if word[0:4] in WORDS_4:
        return 4, word[0:4]

    if word[1:5] in WORDS_4:
        return 4, word[1:5]

    if word[0:3] in WORDS_3:
        return 3, word[0:3]

    if word[1:4] in WORDS_3:
        return 3, word[1:4]

    if word[2:5] in WORDS_5:
        return 3, word[2:5]

    return 0, ""


class Board:
    def __init__(self, state=None):
        # TODO initial state?

        state = np.zeros((5, 5), dtype=str) if state is None else state
        self.state = state

    def move(self, char, i, j):
        if self.state[i][j] != "":
            raise ValueError("already occupied")

        new_board = self.copy()
        new_board.state[i][j] = char

        return new_board

    def possible_moves(self):
        I, J = (self.state == "").nonzero()
        return list(zip(
            ALPHABET.repeat(I.size),
            np.tile(I, 26),
            np.tile(J, 26),
        ))

    def copy(self):
        return Board(np.copy(self.state))

    def game_over(self):
        return (self.state != "").all()

    def score(self):
        total = 0
        words = []

        # Horizontally
        score, word = score_word("".join(self.state[0]))
        total += score
        if score != 0:
            words.append(word)

        score, word = score_word("".join(self.state[1]))
        total += score
        if score != 0:
            words.append(word)

        score, word = score_word("".join(self.state[2]))
        total += score
        if score != 0:
            words.append(word)

        score, word = score_word("".join(self.state[3]))
        total += score
        if score != 0:
            words.append(word)

        score, word = score_word("".join(self.state[4]))
        total += score
        if score != 0:
            words.append(word)

        # Vertically
        score, word = score_word("".join(self.state[:, 0]))
        total += score
        if score != 0:
            words.append(word)

        score, word = score_word("".join(self.state[:, 1]))
        total += score
        if score != 0:
            words.append(word)

        score, word = score_word("".join(self.state[:, 2]))
        total += score
        if score != 0:
            words.append(word)

        score, word = score_word("".join(self.state[:, 3]))
        total += score
        if score != 0:
            words.append(word)

        score, word = score_word("".join(self.state[:, 4]))
        total += score
        if score != 0:
            words.append(word)

        return total, words

    def __str__(self):
        out = ""

        for i in range(5):
            out += "-" * 31 + "\n"
            out += "|  " + "  |  ".join([" "] * 5) + "  |\n"
            out += "|  " + "  |  ".join([" " if x == "" else x for x in self.state[i]]) + "  |\n"
            out += "|  " + "  |  ".join([" "] * 5) + "  |\n"

        out += "-" * 31 + "\n"

        return out
