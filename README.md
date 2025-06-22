# Tic-tac-toe in terminal

Inspirated by [Sebastian Lague's video on minimax and alpha-beta pruning](https://www.youtube.com/watch?v=l-hh51ncgDI) and [Kylie Ying's video on implementing minimax on Tic Tac Toe](https://www.youtube.com/watch?v=fT3YWCKvuQE).

Requires Python version >= 3.10

## How to play
At startup, choose if players (`X` and `O`) are human or computers.

Then place your inputs with numpad keyboard. 

The cells of the 3x3 grid are key binded to this:
```
7 8 9
4 5 6
1 2 3
```

(just like a standard numpad keyboard).

## Computers implementation

The "weak computer" plays moves at random following a uniform distribution.

The "strong computer" plays using the minimax algorithm without depth (implemented with alpha-beta pruning for faster computing speed), and will chose the fastest way to win. In theory, since tic tac toe is a solved game, winning against the computer is impossible, the best is to tie.