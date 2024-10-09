# flake8: noqa

import click

import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

from board import Board

from strategies import (
    STRATEGY_LOOKUP,
)


def play(strategy_1, strategy_2, verbose=False):
    """
    Play one game between two strategies, and return the final board of each player.
    """

    if verbose:
        print(f"Game: <{strategy_1.name}> vs <{strategy_2.name}>")

    board_1 = Board()
    board_2 = Board()
    current_player = 1

    while not (board_1.game_over() and board_2.game_over()):
        if verbose:
            print("")
            print(f"\tBoard for <{strategy_1.name}>:")
            print("\t" + "\n\t".join(str(board_1).split("\n")))
            print(f"\tBoard for <{strategy_2.name}>:")
            print("\t" + "\n\t".join(str(board_2).split("\n")))
            print("")

        if current_player == 1:
            if verbose:
                print(f"\tTo move: {strategy_1.name}")

            char, i, j = strategy_1.move_pick_char(board_1)
            board_1 = board_1.move(char, i, j)

            if verbose:
                print(f"\t- {strategy_1.name} picks '{char}', and places at position ({i}, {j})")
                print(f"\t- {strategy_2.name} thinking of a response...")

            char, i, j = strategy_2.move_given_char(board_2, char)
            board_2 = board_2.move(char, i, j)

            if verbose:
                print(f"\t- {strategy_2.name} places '{char}' at position ({i}, {j})")

            current_player = 2

        elif current_player == 2:
            if verbose:
                print(f"\tTo move: {strategy_2.name}")

            char, i, j = strategy_2.move_pick_char(board_2)
            board_2 = board_2.move(char, i, j)

            if verbose:
                print(f"\t- {strategy_2.name} picks '{char}', and places at position ({i}, {j})")
                print(f"\t- {strategy_1.name} thinking of a response...")

            char, i, j = strategy_1.move_given_char(board_1, char)
            board_1 = board_1.move(char, i, j)

            if verbose:
                print(f"\t- {strategy_1.name} places '{char}' at position ({i}, {j})")

            current_player = 1

        if verbose:
            print("")
            print("\t" + "..."*4)
            print("")

    return board_1, board_2


def match(strategy_1, strategy_2, rounds, verbose=False):
    """
    Return statistics for a match between two strategies (i.e. a series of games), where
    `rounds` is the number of games to play.

    Returned are:

        avg_score_1,
        win_rate_1,
        avg_score_2,
        win_rate_2,
    """

    if verbose:
        print(f"Match: <{strategy_1.name}> vs <{strategy_2.name}>, {rounds} rounds")
        print("")

    total_score_1 = 0
    total_wins_1 = 0

    total_score_2 = 0
    total_wins_2 = 0

    for i in range(rounds):
        board_1, board_2 = play(strategy_1, strategy_2)

        score_1, words_1 = board_1.score()
        score_2, words_2 = board_2.score()

        if score_1 > score_2:
            total_wins_1 += 1
            board_1_winner = "(winner)"
            board_2_winner = ""
        elif score_1 < score_2:
            total_wins_2 += 1
            board_1_winner = ""
            board_2_winner = "(winner)"
        else:
            board_1_winner = "(draw)"
            board_2_winner = "(draw)"
            pass

        if verbose:
            print(f"\tGame ({i+1}/{rounds}): <{strategy_1.name}> and <{strategy_2.name}>")
            print("\tScore: ", score_1, words_1, board_1_winner)
            print("\tScore: ", score_2, words_2, board_2_winner)
            print("")

        total_score_1 += score_1
        total_score_2 += score_2

    avg_score_1 = total_score_1 / rounds
    win_rate_1 = total_wins_1 / rounds

    avg_score_2 = total_score_2 / rounds
    win_rate_2 = total_wins_2 / rounds

    if verbose:
        print("\nMatch over!")
        print(f"- <{strategy_1.name}> avg score: {avg_score_1:.2f}")
        print(f"- <{strategy_1.name}> win rate: {win_rate_1*100:.2f}")
        print(f"- <{strategy_2.name}> avg score: {avg_score_2:.2f}")
        print(f"- <{strategy_2.name}> win rate: {win_rate_2*100:.2f}")

    return (
        avg_score_1,
        win_rate_1,
        avg_score_2,
        win_rate_2,
    )


def tournament(strategies, rounds, verbose=False):
    """
    Pitch N strategies against one another for k rounds. A total of N^2 * k games will
    be played.
    """

    if verbose:
        print("Tournament:", " | ".join([strategy.name for strategy in strategies]), f"(rounds: {rounds})")
        print("")

    avg_scores = np.zeros((len(strategies), len(strategies)))
    avg_win_rates = np.zeros((len(strategies), len(strategies)))

    for i, strategy_1 in enumerate(strategies):
        for j, strategy_2 in enumerate(strategies):
            if verbose:
                print(f"Match: <{strategy_1.name}> vs <{strategy_2.name}>")
                print("")

            avg_score_1, win_rate_1, avg_score_2, win_rate_2 = match(
                strategy_1,
                strategy_2,
                rounds,
                verbose=False
            )

            if verbose:
                print(f"- <{strategy_1.name}> avg score: {avg_score_1:.2f}")
                print(f"- <{strategy_1.name}> win rate: {win_rate_1*100:.2f}")
                print("")

            avg_scores[i][j] = avg_score_1
            avg_win_rates[i][j] = win_rate_1

    return avg_scores, avg_win_rates


@click.group()
def cli():
    pass


@cli.command("tournament")
@click.option("--strategy", "strategy_names", help="Strategies to play against one another.", multiple=True)
@click.option("--rounds", help="Number of rounds.", default=2)
def command_tournament(strategy_names, rounds):
    strategies = [STRATEGY_LOOKUP[s] for s in strategy_names]
    scores, rates = tournament(strategies, int(rounds), verbose=True)

    scores_df = pd.DataFrame(
        scores,
        index=[s.name for s in strategies],
        columns=[s.name for s in strategies],
    )

    rates_df = pd.DataFrame(
        rates,
        index=[s.name for s in strategies],
        columns=[s.name for s in strategies],
    )

    print(scores_df)
    print(rates_df)

    fig, axes = plt.subplots(2, figsize=(10, 7))

    fig.suptitle("Tournament: " + " | ".join([strategy.name for strategy in strategies]) + f" (rounds: {rounds})")

    sn.heatmap(scores_df, annot=True, ax=axes[0]).set(title="Avg score of vertical player")
    sn.heatmap(rates_df, annot=True, ax=axes[1]).set(title="Avg win rate of vertical player")

    plt.show()


@cli.command("match")
@click.option("--strategy-1", "strategy_1_name", help="Strategy going first.")
@click.option("--strategy-2", "strategy_2_name", help="Strategy going second.")
@click.option("--rounds", help="Number of rounds")
def command_match(strategy_1_name, strategy_2_name, rounds):
    strategy_1 = STRATEGY_LOOKUP[strategy_1_name]
    strategy_2 = STRATEGY_LOOKUP[strategy_2_name]

    match(strategy_1, strategy_2, int(rounds), verbose=True)


@cli.command("play")
@click.option("--strategy-1", "strategy_1_name", help="Strategy going first.")
@click.option("--strategy-2", "strategy_2_name", help="Strategy going second.")
def command_play(strategy_1_name, strategy_2_name):
    """
    Play a game between two strategies.
    """

    strategy_1 = STRATEGY_LOOKUP[strategy_1_name]
    strategy_2 = STRATEGY_LOOKUP[strategy_2_name]

    board_1, board_2 = play(strategy_1, strategy_2, verbose=True)

    print("\n--------- GAME OVER ---------\n")

    print(f"Board for <{strategy_1.name}>")
    print(board_1)
    board_1_score, board_1_words = board_1.score()
    print(f"Score: {board_1_score}")
    print(f"Words: {board_1_words}")
    print("")

    print(f"Board for <{strategy_2.name}>")
    print(board_2)
    board_2_score, board_2_words = board_2.score()
    print(f"Score: {board_2_score}")
    print(f"Words: {board_2_words}")
    print("")

    if board_1_score > board_2_score:
        print(f"Winner: {strategy_1.name}")
    elif board_1_score == board_2_score:
        print("Winner: Draw!")
    elif board_1_score < board_2_score:
        print(f"Winner: {strategy_2.name}")


@cli.command("human-vs-ai")
@click.option("--strategy", "strategy_name", help="Strategy to play against")
@click.option("--go-second", default=False)
def command_human_vs_ai(strategy_name, go_second):
    strategy = STRATEGY_LOOKUP[strategy_name]

    # 1 is the human
    # 2 is the AI

    board_1 = Board()
    board_2 = Board()
    current_player = 2 if go_second else 1

    while not board_2.game_over():
        print(board_2)

        print("............")
        if current_player == 1:
            print("\nPlease make your move on paper and enter the letter you chose:")
            char = input(">>> ").upper()

            print("Computer is thinking...")

            char, i, j = strategy.move_given_char(board_2, char)
            board_2 = board_2.move(char, i, j)

            print("Okay.")
            print("")

            current_player = 2

        elif current_player == 2:
            print("\nComputer is thinking of a letter...")
            char, i, j = strategy.move_pick_char(board_2)
            board_2 = board_2.move(char, i, j)

            print("The computer has chosen:", char)
            print("Make your move on paper and press enter.")
            input("")

            current_player = 1

    print("Game over!")

    print(f"Board for computer:")
    print(board_2)
    board_2_score, board_2_words = board_2.score()
    print(f"Score: {board_2_score}")
    print(f"Words: {board_2_words}")
    print("")


if __name__ == "__main__":
    cli()
