# Just Everything, by Brilliand
# https://codegolf.stackexchange.com/a/195064/30688
# Revision of 2019-10-30 21:07:12Z

#! /usr/bin/python

import sys
import random

_, color, seed = sys.argv[:3]

random.seed(seed)

colnames = "abcdefgh"
rownames = "12345678" if color == "w" else "87654321"

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

def allmoves():
    for row in range(8):
        for col in range(8):
            for to in buildmoves((row, col)):
                yield ((row, col), to)

movelist = [(coord2code(a), coord2code(b)) for (a,b) in allmoves()]
random.shuffle(movelist)

while True:
    for (a, b) in movelist:
        print a, b
