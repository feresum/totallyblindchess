# Prickly, by Brilliand
# https://codegolf.stackexchange.com/a/195147/30688
# Revision of 2019-11-01 10:45:08Z

#! /usr/bin/python

import sys
import random

_, color, seed = sys.argv[:3]

random.seed(seed)

colnames = "abcdefgh"
rownames = "12345678" if color == "w" else "87654321"

def coord2code((col, row)):
    return colnames[col] + rownames[row];

def sendmove((a, b)):
    print coord2code(a), coord2code(b)

def long_safe_move(start, step, length):
    a,b = start
    x,y = step
    i = 0
    while i < length:
        m_start = (a+x*i,b+y*i)
        j = length
        while j > i:
            m_end = (a+x*j,b+y*j)
            if m_end[0] >= 0 and m_end[0] <= 7 and m_end[1] >= 0 and m_end[1] <= 7:
                yield (m_start, m_end)
            j -= 1
        i += 1

captures = ([((x,1),(x+1,2)) for x in range(7)]
         + [((x+1,1),(x,2)) for x in range(7)]
         + [((0,0),(0,1)), ((1,0),(3,1)), ((2,0),(1,1)), ((2,0),(3,1))]
         + [((7,0),(7,1)), ((6,0),(4,1)), ((5,0),(6,1)), ((5,0),(4,1))]
         + [((3,0),(2,1)), ((3,0),(3,1)), ((3,0),(4,1)), ((4,0),(5,1))])
captures.remove(((3,1),(4,2)))
captures.remove(((4,1),(3,2)))
sendmove(((6,1),(6,2)))
captures = [m for m in captures if not (6,1) in m]
for m in captures:
    sendmove(m)
sendmove(((6,0),(5,2)))
captures = ([m for m in captures if not (6,0) in m]
         + [((5,2),(7,1)), ((5,2),(3,1))]
         + [((x,2),(x+1,3)) for x in range(7)]
         + [((x+1,2),(x,3)) for x in range(7)])
for m in captures:
    sendmove(m)
sendmove(((5,0),(6,1)))
captures = ([m for m in captures if not (5,0) in m]
         + [((6,1),(5,2))])
for m in captures:
    sendmove(m)
sendmove(((4,0),(6,0)))
captures = ([m for m in captures if not (4,0) in m]
         + [((5,0),(5,1)), ((6,0),(5,1)), ((6,0),(6,1)), ((6,0),(7,1)), ((6,0),(5,0))]
         + [((x,3),(x+1,4)) for x in range(7)]
         + [((x+1,3),(x,4)) for x in range(7)])
for m in captures:
    sendmove(m)
sendmove(((1,1),(1,2)))
captures = [m for m in captures if not (1,1) in m]
for m in captures:
    sendmove(m)
sendmove(((1,0),(2,2)))
captures = ([m for m in captures if not (1,0) in m]
         + [((2,2),(0,1)), ((2,2),(4,1))]
         + [((x,4),(x+1,5)) for x in range(7)]
         + [((x+1,4),(x,5)) for x in range(7)])
for m in captures:
    sendmove(m)
sendmove(((2,0),(1,1)))
captures = ([m for m in captures if not (2,0) in m]
         + [((1,1),(2,2))]
         + [((x,5),(x+1,6)) for x in range(7)]
         + [((x+1,5),(x,6)) for x in range(7)])
for m in captures:
    sendmove(m)
for m in captures:
    sendmove(m)
sendmove(((3,1),(3,3)))
sendmove(((3,2),(3,3)))
captures = ([m for m in captures if not (3,1) in m and not (3,2) in m]
         + [((5,2),(3,3))]
         + [((x,6),(x+1,7)) for x in range(7)]
         + [((x+1,6),(x,7)) for x in range(7)])
for m in captures:
    sendmove(m)
for m in captures:
    sendmove(m)
sendmove(((4,1),(4,3)))
sendmove(((4,2),(4,3)))
captures = ([m for m in captures if not (4,1) in m and not (4,2) in m]
         + [((2,2),(4,3))])
for m in captures:
    sendmove(m)
for i in range(8):
    sendmove(((i,6),(i,7)))
for m in captures:
    sendmove(m)
sendmove(((3,3),(3,4)))
captures = ([m for m in captures if not (3,3) in m]
         + [((2,2),(3,4))])
for m in captures:
    sendmove(m)
sendmove(((4,3),(4,4)))
captures = ([m for m in captures if not (3,3) in m]
         + [((5,2),(4,4)), ((5,2),(3,3)), ((2,2),(4,3))])
for m in captures:
    sendmove(m)
captures = [m for m in captures if not (2,2) in m and not (5,2) in m and not (1,1) in m and not (6,1) in m]
for m in long_safe_move((0,7), (1,0), 7):
    sendmove(m)
for m in captures:
    sendmove(m)
for m in long_safe_move((7,7), (-1,0), 7):
    sendmove(m)
for m in captures:
    sendmove(m)
for m in long_safe_move((1,1), (1,1), 6):
    sendmove(m)
captures = [m for m in captures if not (1,1) in m]
for m in captures:
    sendmove(m)
for m in long_safe_move((6,1), (-1,1), 6):
    sendmove(m)
captures = [m for m in captures if not (6,1) in m]
for m in captures:
    sendmove(m)
sendmove(((2,1),(2,3)))
sendmove(((2,2),(2,3)))
captures = [m for m in captures if not (2,1) in m and not (2,2) in m]
for m in captures:
    sendmove(m)

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

movelist = [(a,b) for (a,b) in allmoves()]
random.shuffle(movelist)

for (a, b) in movelist:
    if a[1] != 7:
        print coord2code(a), coord2code(b)

for i in range(8):
    sendmove(((i,7),(i,6)))
for i in range(7):
    sendmove(((i,7),(7,i)))
for i in range(1,8):
    sendmove(((i,7),(0,7-i)))
for m in captures:
    sendmove(m)
for m in long_safe_move((0,6), (1,0), 6):
    sendmove(m)
for m in captures:
    sendmove(m)
sendmove(((6,6),(6,7)))
sendmove(((5,6),(5,5)))
sendmove(((4,6),(4,4)))
for m in captures:
    sendmove(m)
for (a, b) in movelist:
    if a[1] < 4 and b[1] < 4:
        print coord2code(a), coord2code(b)
for i in range(3):
    for m in long_safe_move((7-2*i,6), (-1,0), 2):
        sendmove(m)
    for m in long_safe_move((6-2*i,7), (-1,0), 2):
        sendmove(m)
    for m in long_safe_move((5-2*i,5), (-1,0), 2):
        sendmove(m)
    for m in long_safe_move((4-2*i,4), (-1,0), 2):
        sendmove(m)
    for m in captures:
        sendmove(m)

while True:
    for (a, b) in movelist:
        print coord2code(a), coord2code(b)
