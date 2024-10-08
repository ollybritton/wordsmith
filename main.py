from board import Board
from strategies import StrategyRandom


def play_versus(strategy_1, strategy_2):
    board_1 = Board()
    board_2 = Board()
    current_player = 1

    while not (board_1.game_over() and board_2.game_over()):
        if current_player == 1:
            char, i, j = strategy_1.move_pick_char(board_1)
            board_1 = board_1.move(char, i, j)

            char, i, j = strategy_2.move_given_char(board_2, char)
            board_2 = board_2.move(char, i, j)

            current_player = 2

        elif current_player == 2:
            char, i, j = strategy_2.move_pick_char(board_2)
            board_2 = board_2.move(char, i, j)

            char, i, j = strategy_1.move_given_char(board_1, char)
            board_1 = board_1.move(char, i, j)

            current_player = 1

    return board_1, board_2


def match_versus(strategy_1, stragey_2, rounds):
    total_score_1 = 0
    total_wins_1 = 0

    total_score_2 = 0
    total_wins_2 = 0

    for _ in range(rounds):
        board_1, board_2 = play_versus(StrategyRandom, StrategyRandom)

        score_1, _ = board_1.score()
        score_2, _ = board_2.score()

        total_score_1 += score_1
        total_score_2 += score_2

        if score_1 > score_2:
            total_wins_1 += 1
        elif score_1 < score_2:
            total_wins_2 += 1
        else:
            # No one wins in a draw
            pass

    avg_score_1 = total_score_1 / rounds
    win_rate_1 = total_wins_1 / rounds

    avg_score_2 = total_score_2 / rounds
    win_rate_2 = total_wins_2 / rounds

    return (
        avg_score_1,
        win_rate_1,
        avg_score_2,
        win_rate_2,
    )


def main():
    strategy_1 = StrategyRandom
    strategy_2 = StrategyRandom

    rounds = 100

    avg_score_1, win_rate_1, avg_score_2, win_rate_2 = match_versus(
        strategy_1,
        strategy_2,
        rounds,
    )

    print("\n"*10)

    print(f"Rounds: {rounds}")
    print(f"Strategy 1 win rate: {win_rate_1*100:.2f}%")
    print(f"Strategy 2 win rate: {win_rate_2*100:.2f}%")
    print(f"Strategy 1 avg score: {avg_score_1:.2f}")
    print(f"Strategy 2 avg score: {avg_score_2:.2f}")


if __name__ == "__main__":
    main()
