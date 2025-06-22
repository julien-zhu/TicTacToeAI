# Tic-tac-toe in terminal

Inspired by [Sebastian Lague's video on minimax and alpha-beta pruning](https://www.youtube.com/watch?v=l-hh51ncgDI) and [Kylie Ying's video on implementing minimax on Tic Tac Toe](https://www.youtube.com/watch?v=fT3YWCKvuQE).

Requires Python version >= 3.10

## Run the script
Run the file using Python like `python3 main.py` / `python main.py` or `./main.py`

## How to play
At startup :
- choose who plays for `X`. In the terminal, type `1` for a human, `2` for a weak computer and `3` for a strong computer. Then press `Enter`.
- choose who plays for `O`. In the terminal, type `1` for a human, `2` for a weak computer and `3` for a strong computer. Then press `Enter`.


Then place your inputs with by typing a number from `1` to `9` then press `Enter`. Each input is mapped to the grid like a numpad keyboard like this:
```
7 8 9
4 5 6
1 2 3
```

Available cells are displayed with a dot `.`.


## Computers implementation

The "weak computer" plays moves at random following a uniform distribution.

The "strong computer" plays using the minimax algorithm without depth (implemented with alpha-beta pruning for faster computing speed), and will chose the fastest way to win. In theory, since tic tac toe is a solved game, winning against the computer is impossible, the best is to tie.
