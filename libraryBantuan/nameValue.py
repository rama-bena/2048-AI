from collections import namedtuple

Point = namedtuple('Point', ('x', 'y'))

class Move:
    UP    = [1, 0, 0, 0]
    RIGHT = [0, 1, 0, 0]
    DOWN  = [0, 0, 1, 0]
    LEFT  = [0, 0, 0, 1]

class Color:
    SCREEN = (187,173,160)
    
    BLOCK_1 = (205,193,180)
    BLOCK_2 = (238,228,218)
    BLOCK_4 = (238,225,201)
    BLOCK_8 = (243,178,122)
    BLOCK_16 = (246,150,100)
    BLOCK_32 = (247,124,95)
    BLOCK_64 = (247,95,59)
    BLOCK_128 = (237,201,80)
    BLOCK_256 = (237,204,98)
    BLOCK_512 = (237,201,80)
    BLOCK_1024 = (237,197,63)
    # BLOCK_2048 = 

    TEXT_1 = (119,110,101)
    TEXT_2 = (119,110,101)
    TEXT_4 = (119,110,101)
    TEXT_8 = (249,246,242)
    TEXT_16 = (249,246,242)
    TEXT_32 = (249,246,242)
    TEXT_64 = (249,246,242)

