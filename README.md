# Wordsworth
Analysis of two-player pencil-and-paper game "Wordsworth".

For more information, see ["Almost everything to know about Wordsworth"](https://ollybritton.com/blog/wordsworth) on my website.

## Install
To install, clone the repository and install all depedencies:

```sh
pip install -r requirements.txt
```

## Usage
To run a game:

```sh
python main.py play --strategy-1 [name] --strategy-2 [name]
```

To play against a strategy on paper:

```sh
python main.py human-vs-ai --strategy [name]
```

To run a tournament (a series of matches between many strategies):

```sh
python main.py tournament --rounds [rounds] --strategy [name] --strategy [name] --strategy [name] ...
```

To run a match (a series of games between two strategies):

```sh
python main.py match --rounds [rounds] --strategy-1 [name] --strategy-2 [name]
```

## Available strategies
- `Random`: pick letters and positions randomly
- `EnglishRandom`: pick letters and positions randomly but according to their distribution in dictionaries
- `Sleepy`: repeatedly pick "Z"
- `ThinkRight`: play the words "THINK" and then "RIGHT", then play randomly
- `Expectimax`: use the expectimax algorithm
- `MonteCarloTreeSearch-easy`: use MCTS with 3 seconds of thinking time
- `MonteCarloTreeSearch-medium`: use MCTS with 15 seconds of thinking time
- `MonteCarloTreeSearch-hard`: use MCTS with 45 seconds of thinking time
- `MonteCarloTreeSearch-very-hard`: use MCTS with 90 seconds of thinking time

## `board/`
Contains the `Board` class for representing the state of a game.

## `strategies/`
Implement a `Strategy` class. A strategy is a pair of two functions:

- `strategy_move_pick_char(board : Board) -> (char, i, j)`: Given this `board`, pick a character to place at position `(i, j)`.
- `strategy_move_given_char(board : Board, char) -> (i, j)`: Given this `board` and this letter `char`, find a position `(i, j)` for which to place it.

(This definition does mean that strategies which model their opponent's board can't be implemented).

To implement a new strategy:

- Implement in `strategies/` (see e.g. [`strategies/expectimax.py`](strategies/expectimax.py))
- Add it to `strategies/__init__.py`
- Add it to the list here on the README
- It will then be available as an option to the main program

## Data
- `data/5-letter-words.txt` is Donald Knuth's public domain collection of five letter words.
- `data/4-letter-words.txt` comes from here: <https://gist.github.com/paulcc/3799331>
- `data/3-letter-words.txt` comes from here: <https://github.com/hzlzh/Domain-Name-List/blob/master/3-letter-words.txt>