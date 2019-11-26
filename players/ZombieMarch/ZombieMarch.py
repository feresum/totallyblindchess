# Zombie March, by Brilliand
# https://codegolf.stackexchange.com/a/195059/30688
# Revision of 2019-10-30 07:00:24Z

#! /usr/bin/python

import sys
import random

_, color, seed = sys.argv[:3]

random.seed(seed)

moveorder = [(2, 2), (1, 1), (0, 2), (0, 1), (1, 2), (2, 1), (2, 0), (1, 0)]
moveorder7 = [(4, 0), (3, 0), (2, 0), (1, 0), (0, -4), (0, -3), (0, -2), (0, -1), (4, -4), (3, -3), (2, -2), (1, -1), (1, -2), (2, -1)]
colorder = random.sample([2, 3, 4, 5], 4) + random.sample([0, 1, 6, 7], 4)
roworder = [1, 2, 3, 4, 5, 6, 7, 0]

colnames = "abcdefgh"
rownames = "12345678" if color == "w" else "87654321"

def buildmoves((col, row), (x, y)):
    if row+y > 7 or row+y < 0:
        return
    if x == 0:
        yield (col, row+y)
        return
    if col < 4:
        if col+x <= 7:
            yield (col+x, row+y)
        if col-x >= 0:
            yield (col-x, row+y)
    else:
        if col-x >= 0:
            yield (col-x, row+y)
        if col+x <= 7:
            yield (col+x, row+y)

def coord2code((col, row)):
    return colnames[col] + rownames[row];

# Some fixed behavior (counter foolsmate)
print coord2code((6, 1)), coord2code((6, 2))
print coord2code((4, 1)), coord2code((4, 3))
print coord2code((3, 1)), coord2code((3, 3))
print coord2code((6, 2)), coord2code((7, 3))
print coord2code((3, 3)), coord2code((2, 4))

iter = 0
while True:
    iter += 1
    for row in roworder:
        for move in (moveorder if row*(1+iter*random.random()/10)<7 else random.sample(moveorder7, 8)):
            for col in colorder:
                for to in buildmoves((col, row), move):
                    print coord2code((col, row)), coord2code(to)
