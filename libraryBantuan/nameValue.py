from collections import namedtuple
import pygame
class FileName:
    MATRIX      = 'data/matrix.bahaya'
    HIGH_SCORE  = 'data/hs.bahaya'
    SCORE       = 'data/s.bahaya'
    UNDO_IMG    = 'assets/img/undo.png'
    RESTART_IMG = 'assets/img/restart.png'

class Move:
    UP    = [1, 0, 0, 0]
    RIGHT = [0, 1, 0, 0]
    DOWN  = [0, 0, 1, 0]
    LEFT  = [0, 0, 0, 1]

# Saya pakai vscode extension "Color highlight", supaya bisa kasi nama Nama rgb dan kelihatan warnanya di vscode
def RGB(r, g, b): 
    return (r, g, b)

class Color:
    BACKGROUND = RGB(248,248,238)
    BOARD = RGB(187,173,160)

pygame.font.init()
Data = namedtuple('Data', ('value', 'color', 'text'))
CELL_DATA = [
    Data(1,      RGB(205,193,180), pygame.font.SysFont(name='woff', size=80).render(" ", True, RGB(119,110,101))),
    Data(2,      RGB(238,228,218), pygame.font.SysFont(name='woff', size=80).render("2", True, RGB(119,110,101))),
    Data(4,      RGB(238,225,201), pygame.font.SysFont(name='woff', size=80).render("4", True, RGB(119,110,101))),
    Data(8,      RGB(243,178,122), pygame.font.SysFont(name='woff', size=80).render("8", True, RGB(249,246,242))),
    Data(16,     RGB(246,150,100), pygame.font.SysFont(name='woff', size=75).render("16", True, RGB(249,246,242))),
    Data(32,     RGB(247,124,95),  pygame.font.SysFont(name='woff', size=75).render("32", True, RGB(249,246,242))),
    Data(64,     RGB(247,95,59),   pygame.font.SysFont(name='woff', size=75).render("64", True, RGB(249,246,242))),
    Data(128,    RGB(237,201,80),  pygame.font.SysFont(name='woff', size=50).render("128", True, RGB(249,246,242))),
    Data(256,    RGB(237,204,98),  pygame.font.SysFont(name='woff', size=50).render("256", True, RGB(249,246,242))),
    Data(512,    RGB(237,200,80),  pygame.font.SysFont(name='woff', size=50).render("512", True, RGB(249,246,242))),
    Data(1024,   RGB(237,197,63),  pygame.font.SysFont(name='woff', size=40).render("1024", True, RGB(249,246,242))),
    Data(2048,   RGB(237,194,45),  pygame.font.SysFont(name='woff', size=50).render("2048", True, RGB(249,246,242))),
    Data(4096,   RGB(239,103,108), pygame.font.SysFont(name='woff', size=50).render("4096", True, RGB(249,246,242))),
    Data(8192,   RGB(236,77,88),   pygame.font.SysFont(name='woff', size=50).render("8192", True, RGB(249,246,242))),
    Data(16384,  RGB(226,67,56),   pygame.font.SysFont(name='woff', size=50).render("16384", True, RGB(249,246,242))),
    Data(32768,  RGB(113,180,213), pygame.font.SysFont(name='woff', size=50).render("32768", True, RGB(249,246,242))),
    Data(65536,  RGB(92,160,222),  pygame.font.SysFont(name='woff', size=50).render("65536", True, RGB(249,246,242))),
    Data(131072, RGB(33,124,190),  pygame.font.SysFont(name='woff', size=50).render("131072", True, RGB(249,246,242))),
]