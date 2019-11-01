Controller and players for [Totally Blind Chess](https://codegolf.stackexchange.com/questions/195032) robot tournament.

## Dependencies
- Python ≥ 3.5.2
- Dependencies for any bots you wish to run:
    - `example` and `Scholar`: gcc (or another C compiler)
    - `ZombieMarch`, `JustEverything`, `BluntInstrument` and `Prickly`: Python 2
    - `Backline`: Python 3.6

## Setting up your player

Suppose you want to create a player named `foo`. Create the directory `players/foo` and write the
source file(s) therein. Then create an entry with the key `"foo"` in [players.json](players.json)
with the commands to run, and optionally, build, your program.

## Controller usage

- `python3 controller.py build` runs the build command for all players. You should run this before either of the other commands.
- `python3 controller.py check` checks that the players produce valid and consistent output.
- `python3 controller.py fight --parallelism=4` starts a tournament with unlimited rounds, 4 concurrent games, and one instance of each player.

For more details on flags, see `controller.py --help` and `controller.py fight --help`.

The `build` and `check` commands exit upon encountering the first error. `fight`, on the other hand,
forfeits misbehaving processes. So it's a good idea to validate your bot with `check` before starting a tournament.

## Interpreting controller output

This is the ouput for a tournament with `--players=example,example,example` and `--cycles=2`:

```Seed: 3764704884103223436
example/2            example/1            B f   64
example/0            example/2            W c   48
example/2            example/0            W f   30
example/1            example/0            B f   40
example/0            example/1            B f   12
example/1            example/2            W f   19
==================Standings after 1 cycle:==================
  example/2                2
  example/0                4
  example/1                6
============================================================
example/0            example/2            W f   29
example/2            example/0            B f   20
example/2            example/1            B f   29
example/0            example/1            W f   65
example/1            example/0            B f   29
example/1            example/2            W f   77
=================Standings after 2 cycles:==================
  example/2                2
  example/1               10
  example/0               12
============================================================
```

One line is logged to stderr for each completed game. The columns are white player, black player,
result, method of result, method and number of moves.
__Result__ is `B` for black win, `W` for white win, or `D` for draw.
__Method of result__ is `c` for checkmate, `s` for stalemate, `m` for draw by 100-move
rule, `f` for forfeit by 2000 consecutive illegal moves, `i` for invalid output (which
may be caused by the program crashing), `h` for forfeit due to taking too long to output
anything, or `e` for forfeit by process failing to start.

After each double round robin cycle, the current standings are printed to stdout. Players receive 2
points for a win and 1 point for a draw.

If the `--move-log` option is provided, the moves of each game are logged to the given file.
