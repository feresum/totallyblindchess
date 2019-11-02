# Blunt Instrument, by ymbirtt
# https://codegolf.stackexchange.com/a/195108/30688
# Revision of 2019-11-01 20:31:04Z

#! /usr/bin/python

import sys
import random

_, color, seed = sys.argv[:3]

random.seed(seed)

colnames = "abcdefgh"
rownames = "12345678" if color == "w" else "87654321"
ENEMY_KING = (4, 7)

def coord2code((col, row)):
    return colnames[col] + rownames[row];

def buildmoves((col, row)):
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

def distance_to_square(coords1, coords2):
    x1, y1 = coords1
    x2, y2 = coords2
    return max(abs(x2-x1), abs(y2-y1))

def sort_key(move):
    from_, to_ = move
    # Our favourite moves are ones that land us on top of the enemy king
    # After that, we like moves that make us closer to the enemy king
    # After that, we like moves that take us a long way from where we started
    # After that, we like moves that move pieces that are a long way from the enemy king
    # After that, we pick at random!
    gained_ground = distance_to_square(from_, ENEMY_KING) - distance_to_square(to_, ENEMY_KING)
    return (distance_to_square(to_, ENEMY_KING), -gained_ground, -distance_to_square(from_, to_), -distance_to_square(from_, ENEMY_KING), random.randint(0, 999999))

def cowardly_filter(move):
    from_, to_ = move
    # Remove all moves that move more than 2 spaces away from the enemy king
    # Eliminate moves that gain no ground with probability 12/16
    # Eliminate moves that lose 1 space with probability 14/16
    # Eliminate moves that lose 2 spaces with probability 15/16
    # I pulled these numbers from my backside and don't know if they're actually good.

    gained_ground = distance_to_square(from_, ENEMY_KING) - distance_to_square(to_, ENEMY_KING)
    if gained_ground > 0:
        return True
    if gained_ground < -2:
        return False
    fudge_factor = random.randint(0, 16)
    # I tried to figure out a nice mathsy way of doing this but it's half past 8 and I want to play Dragon Age.
    if gained_ground == 0 and fudge_factor > 11:
        return True
    if gained_ground == -1 and fudge_factor > 13:
        return True
    if gained_ground ==  -2 and fudge_factor > 14:
        return True
    return False


def gen_all_valid_moves():
    for row in range(8):
        for col in range(8):
            for to in buildmoves((row, col)):
                yield ((row, col), to)

movelist = list(gen_all_valid_moves())

movelist.sort(key=sort_key)

# movelist = [(coord2code(a), coord2code(b)) for (a,b) in all_valid_moves]

while True:
    for (a, b) in filter(cowardly_filter, movelist):
        print coord2code(a), coord2code(b)
