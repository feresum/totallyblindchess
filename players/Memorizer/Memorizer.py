# Memorizer, by famous1622
# https://codegolf.stackexchange.com/a/195288/30688
# Revision of 2019-11-04 18:49:14Z

import sys
import random
from functools import lru_cache


board = [
    [{"R"},{"K"},{"B"},{"Q"},{"k"},{"B"},{"K"},{"R"}],
    [{"P"},{"P"},{"P"},{"P"},{"P"},{"P"},{"P"},{"P"}],
    [set(),set(),set(),set(),set(),set(),set(),set()],
    [set(),set(),set(),set(),set(),set(),set(),set()],
    [set(),set(),set(),set(),set(),set(),set(),set()],
    [set(),set(),set(),set(),set(),set(),set(),set()],
    [set(),set(),set(),set(),set(),set(),set(),set()],
    [set(),set(),set(),set(),set(),set(),set(),set()]]

_, color, seed = sys.argv[:3]
random.seed(seed)

pawns = [(i,j) for i in range(8) for j in range(4)]

colnames = "abcdefgh" if color == "w" else "hgfedcba"
rownames = "12345678" if color == "w" else "87654321"

def coord2code(col, row):
    return colnames[col] + rownames[row]

def move(col1, row1, col2, row2):
    if (col1, row1) not in pawns and 0 <= col2 <= 8 and 0 <= row2 <= 8:
        pass
    try:
        print(" ".join((coord2code(col1, row1),coord2code(col2, row2),"q")))
        for type in board[row1][col1]:
            if (col2,row2) in getmoves(col1,row1,(type,)):
                board[row2][col2].add(type)
            if "P" in board[row2][col2] and row2 == 8:
                board[row2][col2].add("Q")
        pawns.append((col2,row2))
    except IndexError:
        pass

def pawncapture(col, row):
    if random.getrandbits(1):
        move(col, row, col+1, row+1)
        move(col, row, col-1, row+1)
    else:
        move(col, row, col+1, row+1)
        move(col, row, col-1, row+1)

def spycheckmove(col1, row1, col2, row2):
    move(col1,row1,col2,row2)
    move(col2,row2,col1,row1)

def protect_middle(adventure = True):
    move(4,3,3,4)
    move(3,3,4,4)
    move(2,2,3,3)
    pawncapture(4,4)
    pawncapture(3,3)
    pawncapture(2,2)
    pawncapture(5,2)
    spycheckmove(2,2,3,4)
    move(2,1,2,2)
    spycheckmove(5,2,4,4)
    move(5,1,5,2)

@lru_cache()
def getmoves(col, row, piece_types):
    return list(buildmoves(col, row, piece_types))

def buildmoves(col, row, piece_types):
    if "K" in piece_types:
        # Knight moves
        for x in (1, 2, -2, -1):
            if x+col >= 0 and x+col <= 7:
                for y in (2//x, -2//x):
                    if y+row >= 0 and y+row <= 7:
                        yield (x+col, y+row)

    if "P" in piece_types:
        yield (col+1,row+1)
        yield (col+1,row+1)
        yield (col-1,row+1)
        yield (col-1,row+1)
        yield (col+1,row+1)
        yield (col+1,row+1)
        yield (col-1,row+1)
        yield (col-1,row+1)
        yield (col+1,row+1)
        yield (col+1,row+1)
        yield (col-1,row+1)
        yield (col,  row+1)
        yield (col,  row+1)

    if "k" in piece_types:
        yield (col+1,row)
        yield (col-1,row)
        yield (col, row+1)
        yield (col, row-1)
        yield (col-1, row-1)
        yield (col-1, row+1)
        yield (col+1, row-1)
        yield (col-1, row+1)        
        yield (col+1,row)
        yield (col-1,row)
        yield (col, row+1)
        yield (col, row-1)
        yield (col-1, row-1)
        yield (col-1, row+1)
        yield (col+1, row-1)
        yield (col-1, row+1)

    if "B" in piece_types or "Q" in piece_types:
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

    if "R" in piece_types or "Q" in piece_types:
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

move(4,1,4,3)
protect_middle()
move(4,0,4,1)
move(4,1,4,2)
move(3,1,3,3)
protect_middle()
move(1,0,2,2)
protect_middle()
move(6,0,5,2)
protect_middle()

while True:
    a = random.choice(pawns)
    piecetypes = board[a[1]][a[0]]
    if not piecetypes:
        continue
    b = random.choice(getmoves(a[0],a[1],tuple(piecetypes)))
    move(a[0], a[1], b[0], b[1])
