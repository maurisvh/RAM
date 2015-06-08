import Element
import Timer
import Color
import random

M_KESTREL = 0
M_SKELETON = 1
M_TROLL = 2
M_ANDROID = 3
M_JELLY = 4
M_SALAMANDER = 5
M_TINY_UFO = 6
M_MINOTAUR = 7
M_PROGRAM_BUG = 8
M_WITCH = 9
M_GHOST = 10
M_SOLDIER = 11
M_ATTRACTOR = 12
M_TURRET = 13
M_ELF = 14
M_GOLDEN_DRAGON = 15

appearance = {
    M_KESTREL: ('K', Color.WHITE),
    M_SKELETON: ('Z', Color.LIGHTGRAY),
    M_TROLL: ('T', Color.BROWN),
    M_ANDROID: ('A', Color.CYAN),
    M_JELLY: ('J', Color.LIGHTGREEN),
    M_SALAMANDER: ('S', Color.LIGHTRED),
    M_TINY_UFO: ('U', Color.LIGHTCYAN),
    M_MINOTAUR: ('M', Color.RED),
    M_PROGRAM_BUG: ('B', Color.YELLOW),
    M_WITCH: ('@', Color.MAGENTA),
    M_GHOST: ('W', Color.DARKGRAY),
    M_SOLDIER: ('@', Color.LIGHTBLUE),
    M_ATTRACTOR: ('8', Color.CYAN),
    M_TURRET: ('8', Color.DARKGRAY),
    M_ELF: ('E', Color.LIGHTGREEN),
    M_GOLDEN_DRAGON: ('D', [Color.YELLOW, Color.LIGHTRED, Color.WHITE]),
}

class Monster:
    def __init__(self, kind, flags, pos, hp):
        self.kind = kind
        self.flags = flags
        self.pos = pos
        self.hp = hp

    def color(self):
        col = appearance[self.kind][1]
        if isinstance(col, list):
            col = random.choice(col)
        return col

    def char(self):
        return appearance[self.kind][0]


