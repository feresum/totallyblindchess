# Pokey, by Brilliand
# https://codegolf.stackexchange.com/a/195188/30688
# Revision of 2019-11-02 04:11:05Z

#! /usr/bin/python

import sys
import random
import math

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
sendmove(((4,1),(4,2)))
captures = ([m for m in captures if not (4,1) in m]
         + [((x,2),(x+1,3)) for x in range(7)]
         + [((x+1,2),(x,3)) for x in range(7)])
for m in captures:
    sendmove(m)
sendmove(((3,0),(5,2)))
captures = ([m for m in captures if not (3,0) in m and not m[0] == (5,2)]
         + [((4,0),(3,1))])
for m in captures:
    sendmove(m)
sendmove(((6,0),(7,2)))
captures = ([m for m in captures if not (6,0) in m]
         + [((4,0),(3,1))])
for m in captures:
    sendmove(m)
sendmove(((7,2),(6,4)))
captures = (captures
         + [((5,2),(5,6))])
for m in captures:
    sendmove(m)
sendmove(((7,1),(7,3)))
sendmove(((7,1),(7,2)))
sendmove(((7,2),(7,3)))
captures = ([m for m in captures if not (7,1) in m and not (7,2) in m]
         + [((7,0),(7,3))]
         + [((x,3),(x+1,4)) for x in range(7)]
         + [((x+1,3),(x,4)) for x in range(7)])
for m in captures:
    sendmove(m)
sendmove(((7,3),(7,4)))
captures = ([m for m in captures if not (7,3) in m]
         + [((7,0),(7,6))]
         + [((x,4),(x+1,5)) for x in range(7)]
         + [((x+1,4),(x,5)) for x in range(7)])
for m in captures:
    sendmove(m)
sendmove(((7,4),(7,5)))
captures = ([m for m in captures if not (7,4) in m]
         + [((x,5),(x+1,6)) for x in range(7)]
         + [((x+1,5),(x,6)) for x in range(7)])
for m in captures:
    sendmove(m)
sendmove(((7,5),(7,6)))
for m in long_safe_move((7,0), (0,1), 6):
    sendmove(m)
captures = ([m for m in captures if not (7,5) in m and not (5,6) in m]
         + [((x,6),(x+1,7)) for x in range(7)]
         + [((x+1,6),(x,7)) for x in range(7)])
for m in captures:
    sendmove(m)
sendmove(((5,2),(7,4)))
sendmove(((7,4),(7,6)))
captures = ([m for m in captures if not (7,4) in m]
         + [((6,4),(7,6))])
for m in captures:
    sendmove(m)
sendmove(((7,6),(7,7)))
captures = [m for m in captures if not (7,6) in m]
for m in captures:
    sendmove(m)
sendmove(((5,6),(6,5)))
captures = [m for m in captures if not (5,6) in m]
for m in captures:
    sendmove(m)
sendmove(((6,5),(7,6)))
sendmove(((7,6),(7,7)))
for m in captures:
    sendmove(m)
for m in long_safe_move((7,7), (-1,0), 7):
    sendmove(m)
for m in captures:
    sendmove(m)
for m in long_safe_move((7,6), (-1,0), 7):
    sendmove(m)
for m in captures:
    sendmove(m)
sendmove(((5,2),(3,0)))
sendmove(((7,4),(3,0)))
def zombiemarch():
    colorder = list(range(8))
    random.shuffle(colorder)
    roworder = [6,5,4,3,2,1]
    for col in colorder:
        for row in roworder:
            if col >= 1:
                yield ((col,row), (col-1,row+1))
            if col >= 1:
                yield ((col,row), (col-1,row+1))
            yield ((col,row), (col,row+1))
captures = list(zombiemarch())
for m in captures:
    sendmove(m)
captures = [m for m in captures if not m[0][1] == 1]
def jitter(tiles):
    fromset = set()
    for (a,b) in tiles:
        fromset.add(b)
    for (a,b) in fromset:
        if a>0:
            yield ((a,b), (a-1,b))
        if a<7:
            yield ((a,b), (a+1,b))
        if a>0:
            if b>0:
                yield ((a,b), (a-1,b-1))
            if b<7:
                yield ((a,b), (a-1,b+1))
        if a<7:
            if b>0:
                yield ((a,b), (a+1,b-1))
            if b<7:
                yield ((a,b), (a+1,b+1))
        if b>0:
            yield ((a,b), (a,b-1))
        if b<7:
            yield ((a,b), (a,b+1))
kingescape = list(jitter({((4,0),(4,0))}))
for m in captures:
    sendmove(m)
for m in captures:
    sendmove(m)
for m in kingescape:
    sendmove(m)
kingescape = list(jitter(kingescape))
for m in captures:
    sendmove(m)
for m in captures:
    sendmove(m)
for m in kingescape:
    sendmove(m)
kingescape = list(jitter(kingescape))
for m in captures:
    sendmove(m)
for m in captures:
    sendmove(m)
for m in kingescape:
    sendmove(m)
kingescape = list(jitter(kingescape))
for m in captures:
    sendmove(m)
for m in captures:
    sendmove(m)
for m in kingescape:
    sendmove(m)
for m in long_safe_move((7,7), (-1,0), 7):
    sendmove(m)
for m in captures:
    sendmove(m)
sendmove(((0,7),(2,5)))
for i in range(2):
    for m in long_safe_move((0+3*i,6), (1,0), 3):
        sendmove(m)
    for m in long_safe_move((1+3*i,7), (1,0), 3):
        sendmove(m)
    for m in long_safe_move((2+3*i,5), (1,0), 3):
        sendmove(m)
    kingescape = list(jitter(kingescape))
    for m in kingescape:
        sendmove(m)
sendmove(((7,7),(6,6)))
for m in long_safe_move((7,0), (0,1), 5):
    sendmove(m)
for i in range(3):
    for m in long_safe_move((6-2*i,6), (0,-1), 2):
        sendmove(m)
    for m in long_safe_move((7-2*i,5), (0,-1), 2):
        sendmove(m)
kingescape = list(jitter(kingescape))
for m in kingescape:
    sendmove(m)

def allmovegroups():
    # Knight moves
    for row in range(8):
        for col in range(8):
            for x in (1, 2, -2, -1):
                if x+col >= 0 and x+col <= 7:
                    for y in (2/x, -2/x):
                        if y+row >= 0 and y+row <= 7:
                            yield [((col, row),(x+col, y+row))]
                        else:
                            # Move knights away from edges
                            yield [((col, row),(int(math.copysign(x,4-col))+col, int(math.copysign(y,4-row))+row))]
    # Bishop moves
    for i in range(8):
        yield long_safe_move((0,i), (1,1), 7)
        yield long_safe_move((7,i), (-1,1), 7)
        yield long_safe_move((0,i), (1,-1), 7)
        yield long_safe_move((7,i), (-1,-1), 7)
        if i != 0:
            yield long_safe_move((i,0), (1,1), 7)
            yield long_safe_move((i,7), (1,-1), 7)
        if i != 7:
            yield long_safe_move((i,0), (-1,1), 7)
            yield long_safe_move((i,7), (-1,-1), 7)
    # Rook moves
    for i in range(8):
        yield long_safe_move((0,i), (1,0), 7)
        yield long_safe_move((7,i), (-1,0), 7)
        yield long_safe_move((i,0), (0,1), 7)
        yield long_safe_move((i,7), (0,-1), 7)

movegrouplist = [a for a in allmovegroups()]
random.shuffle(movegrouplist)

def allmoves():
    for movegroup in movegrouplist:
        for move in movegroup:
            yield move
movelist = list(allmoves())

while True:
    for (a, b) in movelist:
        print coord2code(a), coord2code(b)
