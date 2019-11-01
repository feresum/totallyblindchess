# Backline, by Spitemaster
# https://codegolf.stackexchange.com/a/195132/30688
# Revision of 2019-11-01 03:13:44Z

#! /usr/bin/python3

import random
import sys

_, colour, seed = sys.argv[:3]
random.seed(seed)

files = "abcdefgh"

def colour_move(start, end, flip):
    if colour == "w":
        return (7 - start[0] if flip else start[0], start[1]), (7 - end[0] if flip else end[0], end[1])
    else:
        return (7 - start[0] if flip else start[0], 7 - start[1]), (7 - end[0] if flip else end[0], 7 - end[1])

def stringify_move(start, end):
    return f"{files[start[0]]}{start[1] + 1} {files[end[0]]}{end[1] + 1} q"

# This guarantees that if the piece is not taken, it reaches the final square as quickly as possible.
def safely_make_long_move(start, end):
    file_change = end[0] - start[0]
    rank_change = end[1] - start[1]
    used_squares = [start]
    while used_squares[-1][0] != end[0] or used_squares[-1][1] != end[1]:
        used_squares.append((used_squares[-1][0] + (1 if file_change > 0 else (-1 if file_change < 0 else 0)), used_squares[-1][1] + (1 if rank_change > 0 else (-1 if rank_change < 0 else 0))))
    for i in range(len(used_squares) - 1):
        for j in reversed(range(i + 1, len(used_squares))):
            yield (used_squares[i]), (used_squares[j])
    yield None

def rook_attack(p):
    flip = p == "h"
    # Move pawn forward two spaces.
    yield stringify_move(*colour_move((0, 1), (0, 3), flip))
    track = [(0,0), (0,2), (1,2), (1,7), (0,7), (7,7), (7,6), (1,6), (1,2), (0,2), (0,0)]
    for i in range(len(track) - 1):
        move_gen = safely_make_long_move(track[i], track[i+1])
        while True:
            move = next(move_gen)
            if move:
                yield stringify_move(*colour_move(*move, flip))
            else:
                break
    yield None

def bishop_attack(p):
    flip = p == "f"
    # Move pawn forward two spaces.
    yield stringify_move(*colour_move((3, 1), (3, 2), flip))
    track = [(2,0), (3,1), (2,2), (7,7), (6,6), (5,7), (4,6), (3,7), (2,6), (1,7), (0,6), (2,4), (1,3), (3,1), (2,0)]
    for i in range(len(track) - 1):
        move_gen = safely_make_long_move(track[i], track[i+1])
        while True:
            move = next(move_gen)
            if move:
                yield stringify_move(*colour_move(*move, flip))
            else:
                break
    yield None

def queen_attack(p):
    flip = False
    # Move pawn forward two spaces.
    yield stringify_move(*colour_move((4, 1), (4, 2), flip))
    track = [(3,0), (7,4), (7,7), (0,7), (0,5), (7,5), (7,4), (4,1)]
    for i in range(len(track) - 1):
        move_gen = safely_make_long_move(track[i], track[i+1])
        while True:
            move = next(move_gen)
            if move:
                yield stringify_move(*colour_move(*move, flip))
            else:
                break
    yield None

def knight_attack(p):
    flip = p == "g"
    # Move pawn forward two spaces.
    track = [(1,0), (2,2), (1,4), (2,6), (0,7), (1,5), (3,6), (5,7), (6,5), (7,7), (5,6), (3,7), (1,6), (2,4), (0,3), (2,2), (1,0)]
    for i in range(len(track) - 1):
        yield stringify_move(*colour_move(track[i], track[i+1], flip))
    yield None

# Just Everything's code:
colnames = "abcdefgh"
rownames = "12345678" if colour == "w" else "87654321"

def coord2code(col, row):
    return colnames[int(col)] + rownames[int(row)]

def buildmoves(col, row):
    # Knight moves
    for x in (1, 2, -2, -1):
        if x+col >= 0 and x+col <= 7:
            for y in (2/x, -2/x):
                if y+row >= 0 and y+row <= 7:
                    yield (x+col, y+row)
    # Bishop moves
    for x in range(1,8):
        if col+x <= 7:
            if row+x <= 7:
                yield (col+x, row+x)
            if row-x >= 0:
                yield (col+x, row-x)
        if col-x >= 0:
            if row+x <= 7:
                yield (col-x, row+x)
            if row-x >= 0:
                yield (col-x, row-x)
    # Rook moves
    for x in range(1,8):
        if col+x <= 7:
            yield (col+x, row)
        if col-x >= 0:
            yield (col-x, row)
        if row+x <= 7:
            yield (col, row+x)
        if row-x >= 0:
            yield (col, row-x)

def allmoves():
    for row in range(8):
        for col in range(8):
            for to in buildmoves(row, col):
                yield ((row, col), to)

movelist = [(coord2code(*a), coord2code(*b)) for (a,b) in allmoves()]
random.shuffle(movelist)

# Avoid Scholar
print("g2 g3")
print("g7 g6")

# Choose random piece to attempt to kill the enemy with.
used_piece = ["a", "b", "c", "d", "f", "g", "h"]
random.shuffle(used_piece)
while True:
    # Try to kill off their pieces by sending one piece at a time in to attack
    for p in used_piece:
        if p in ["a", "h"]:
            move_gen = rook_attack(p)
        elif p in ["b", "g"]:
            move_gen = knight_attack(p)
        elif p in ["c", "f"]:
            move_gen = bishop_attack(p)
        elif p == "d":
            move_gen = queen_attack(p)
        while True:
            move = next(move_gen)
            if move:
                print(move)
            else:
                break
    # Break out of possible checks by trying every possible move once.

    for (a, b) in movelist:
        print(a, b, "q")
