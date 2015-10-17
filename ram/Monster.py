import Element
import Timer
import Color
import random

# We need to do this in a very C-like way for memory poke-y stuff to work. :<
M_KESTREL = 0
M_SKELETON = 1
M_TROLL = 2
M_ANDROID = 3
M_JELLY = 4
M_SALAMANDER = 5
M_TINY_UFO = 6
M_MINOTAUR = 7
M_GLITCH = 8
M_WITCH = 9
M_GHOST = 10
M_SOLDIER = 11
M_ATTRACTOR = 12
M_TURRET = 13
M_ELF = 14
M_GOLDEN_DRAGON = 15


def glitch_name(recursed=False):
    # Try to generate something believably glitchy, not just garbage.
    which = random.randint(1, 6)
    if which == 1:
        return ' ' * random.randint(3, 8)
    elif which == 2:
        c = random.randint(33, 55)
        return ''.join(chr(c + i) for i in range(random.randint(6, 10)))
    elif which == 3:
        c1 = random.randint(33, 55)
        c2 = random.randint(33, 55)
        return (chr(c1) + chr(c2)) * random.randint(3, 6)
    elif which == 4:
        if recursed:
            return chr(random.randint(33, 55)) * random.randint(3, 12)
        n1 = glitch_name(recursed=True)
        n2 = glitch_name(recursed=True)
        return (n1 + n2)[:random.randint(10, 12)]
    elif which == 5 or which == 6:
        # look like item/monster names
        name = random.choice(['strel#sk', '#tro///', 'ndroidThe',
                              'jjeellll', 'amanderYou', 'UFO\", \"', 'in((aur',
                              'itch#wi', '    /gh', ' s o\\\\\\\\', '8',
                              'Welcome to',
                              'You try to', 'EelfDgold', 'Suddenly,',
                              'The dungeon',
                              'ERROR:%d' % random.randint(-128, 127),
                              'anium neckla',
                              'on scale mail#ta', 'It s', '  The', '/*'])
        name = list(name)
        for i in range(random.randint(1, 5)):
            name.insert(random.randrange(len(name)),
                        chr(random.randint(33, 35)))
            if random.randrange(0, 1) == 1:
                del name[random.randrange(len(name))]
        return ''.join(name)


class Monster:
    appearance = {
        M_KESTREL: ('K', Color.WHITE),
        M_SKELETON: ('Z', Color.LIGHTGRAY),
        M_TROLL: ('T', Color.BROWN),
        M_ANDROID: ('A', Color.CYAN),
        M_JELLY: ('J', Color.LIGHTGREEN),
        M_SALAMANDER: ('S', Color.LIGHTRED),
        M_TINY_UFO: ('U', Color.LIGHTCYAN),
        M_MINOTAUR: ('M', Color.RED),
        M_GLITCH: ('B', [Color.YELLOW, Color.LIGHTMAGENTA]),
        M_WITCH: ('@', Color.MAGENTA),
        M_GHOST: ('W', Color.DARKGRAY),
        M_SOLDIER: ('@', Color.LIGHTBLUE),
        M_ATTRACTOR: ('8', Color.CYAN),
        M_TURRET: ('8', Color.DARKGRAY),
        M_ELF: ('E', Color.LIGHTGREEN),
        M_GOLDEN_DRAGON: ('D', [Color.YELLOW, Color.LIGHTRED, Color.WHITE]),
    }

    name_table = {
        M_KESTREL: 'kestrel',
        M_SKELETON: 'skeleton',
        M_TROLL: 'troll',
        M_ANDROID: 'android',
        M_JELLY: 'jelly',
        M_SALAMANDER: 'salamander',
        M_TINY_UFO: 'tiny UFO',
        M_MINOTAUR: 'minotaur',
        M_GLITCH: None,
        M_WITCH: 'witch',
        M_GHOST: 'ghost',
        M_SOLDIER: 'soldier',
        M_ATTRACTOR: 'attractor',
        M_TURRET: 'turret',
        M_ELF: 'elf',
        M_GOLDEN_DRAGON: 'golden dragon',
    }

    gen_range = {
        M_KESTREL: (1, 4),
        M_SKELETON: (1, 5),
        M_TROLL: (2, 6),
        M_ANDROID: (3, 7),
        M_JELLY: (4, 8),
        M_SALAMANDER: (5, 9),
        M_TINY_UFO: (6, 10),
        M_MINOTAUR: (8, 15),
        M_GLITCH: (0, 0),  # only in glitch world
        M_WITCH: (11, 16),
        M_GHOST: (13, 19),
        M_SOLDIER: (14, 20),
        M_ATTRACTOR: (15, 20),
        M_TURRET: (15, 20),
        M_ELF: (1, 0),  # don't generate
        M_GOLDEN_DRAGON: (20, 255),
    }

    max_hp = {
        M_KESTREL: 6,
        M_SKELETON: 8,
        M_TROLL: 20,
        M_ANDROID: 15,
        M_JELLY: 13,
        M_SALAMANDER: 18,
        M_TINY_UFO: 16,
        M_MINOTAUR: 40,
        M_GLITCH: 15,
        M_WITCH: 24,
        M_GHOST: 35,
        M_SOLDIER: 45,
        M_ATTRACTOR: 50,
        M_TURRET: 60,
        M_ELF: 40,
        M_GOLDEN_DRAGON: 200,
    }

    # If not passed flags/hp, calculate a starting value.
    def __init__(self, kind, pos, flags=None, hp=None):
        if flags is None:
            flags = 0x00
        if hp is None:
            hp = Monster.max_hp[kind]

        self.kind = kind
        self.flags = flags
        self.pos = pos
        self.hp = hp

    @classmethod
    def generate(cls, depth, pos):
        opts = []
        for kind, (lo, hi) in Monster.gen_range.items():
            if lo <= depth <= hi:
                opts.append(kind)

        return cls(random.choice(opts), pos)

    def color(self):
        col = Monster.appearance[self.kind][1]
        if isinstance(col, list):
            col = random.choice(col)
        return col

    def char(self):
        return Monster.appearance[self.kind][0]

    def name(self):
        return Monster.name_table[self.kind] or glitch_name()
