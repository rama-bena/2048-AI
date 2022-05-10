from collections import namedtuple

Point = namedtuple('Point', ('x', 'y'))

class Move:
    UP    = [1, 0, 0, 0]
    RIGHT = [0, 1, 0, 0]
    DOWN  = [0, 0, 1, 0]
    LEFT  = [0, 0, 0, 1]

# Saya pakai vscode extension "Color highlight", supaya bisa kasi nama Nama rgb dan kelihatan warnanya di vscode
def RGB(r, g, b): 
    return (r, g, b)

Data = namedtuple('Data', ('value', 'color', 'text_color', 'text_size'))

CELL_DATA = [
    Data(1,      RGB(205,193,180), RGB(119,110,101), 80),
    Data(2,      RGB(238,228,218), RGB(119,110,101), 80),
    Data(4,      RGB(238,225,201), RGB(119,110,101), 80),
    Data(8,      RGB(243,178,122), RGB(249,246,242), 80),
    Data(16,     RGB(246,150,100), RGB(249,246,242), 75),
    Data(32,     RGB(247,124,95),  RGB(249,246,242), 75),
    Data(64,     RGB(247,95,59),   RGB(249,246,242), 75),
    Data(128,    RGB(237,201,80),  RGB(249,246,242), 50),
    Data(256,    RGB(237,204,98),  RGB(249,246,242), 50),
    Data(512,    RGB(237,200,80),  RGB(249,246,242), 50),
    Data(1024,   RGB(237,197,63),  RGB(249,246,242), 40),
    Data(2048,   RGB(237,194,45),  RGB(249,246,242), 40),
    Data(4096,   RGB(239,103,108), RGB(249,246,242), 40),
    Data(8192,   RGB(236,77,88),   RGB(249,246,242), 40),
    Data(16384,  RGB(226,67,56),   RGB(249,246,242), 40),
    Data(32768,  RGB(113,180,213), RGB(249,246,242), 40),
    Data(65536,  RGB(92,160,222),  RGB(249,246,242), 40),
    Data(131072, RGB(33,124,190),  RGB(249,246,242), 40),
]

class Color:
    BACKGROUND = RGB(248,248,238)
    BOARD = RGB(187,173,160)