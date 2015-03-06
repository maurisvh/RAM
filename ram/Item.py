import Color
import Element

import curses
import random
CHAR_WEAPON     = '/'
CHAR_BODY_ARMOR = '['
CHAR_NECKLACE   = '"'
CHAR_FOOD       = '*'
CHAR_MISC       = '$'
CHAR_ARTIFACT   = '&'

weapons     = []
body_armors = []
necklaces   = []
consumables = []

class Flag:
    def __init__(self, where):
        self.where = where
    def __rsub__(self, num):
        self.where.append(num); return num
w, b, n, c = map(Flag, (weapons, body_armors, necklaces, consumables))

fruits = f = list(range(0x05, 0x08))
random.shuffle(fruits)
pills = p = list(range(0x08, 0x10))
random.shuffle(pills)

NO_ITEM           = 0x00;     THICK_SWEATER     = 0x10 -b
CROWBAR           = 0x01 -w;  BALLISTIC_VEST    = 0x11 -b
VOLCANIC_SHARD    = 0x02 -w;  DRAGON_SCALE_MAIL = 0x12 -b
TASER             = 0x03 -w;  TITANIUM_NECKLACE = 0x13 -n
JELLY_GUN         = 0x04 -w;  RUSTY_NECKLACE    = 0x14 -n
FULL_HP_FRUIT     = f[0] -c;  CRIMSON_NECKLACE  = 0x15 -n
FULL_TP_FRUIT     = f[1] -c;  GLOWING_NECKLACE  = 0x16 -n
HALF_HP_FRUIT     = f[2] -c;  UNHOLY_NECKLACE   = 0x17 -n
CHARGE_PILL       = p[0] -c;  WAND_OF_DEATH     = 0x18 -c
XP_UP_PILL        = p[1] -c;  MANUAL            = 0x19 -c
HASTE_PILL        = p[2] -c;  GUIDEBOOK         = 0x1A -c
IDENTIFY_PILL     = p[3] -c;  CORRUPTOR         = 0x1B -c
XP_DOWN_PILL      = p[4] -c;  OFFSETTER         = 0x1C -c
POISON_PILL       = p[5] -c;  COPIER            = 0x1D -c
PROTECT_PILL      = p[6] -c;  PALANTIR          = 0x1E
TORMENT_PILL      = p[7] -c;  GOLDEN_CANDLE     = 0x1F
del f, p, Flag, w, b, n, c
######################################################################

class Item:
    def __init__(self, byte):
        self.byte = byte

    @property
    def kind(self):
        return self.byte >> 3
    @property
    def enchanted(self):
        return self.byte & 0x80
    @property
    def equipped(self):
        return self.byte & 0x40
    @property
    def cursed(self):
        return self.byte & 0x20

    def is_weapon(self):
        return self.kind in weapons
    def is_body_armor(self):
        return self.kind in body_armors
    def is_necklace(self):
        return self.kind in necklaces
    def is_consumable(self):
        return self.kind in consumables
    def is_pill(self):
        return self.kind in pills
    def is_fruit(self):
        return self.kind in fruits

    def kind_name(self):
        if self.kind == NO_ITEM:
            return 'null'
        elif self.kind == CROWBAR:
            return 'crowbar'
        elif self.kind == VOLCANIC_SHARD:
            return 'volcanic shard'
        elif self.kind == TASER:
            return 'taser'
        elif self.kind == JELLY_GUN:
            return 'jelly gun'
        elif self.kind == fruits[0]:
            return 'akebi'
        elif self.kind == fruits[1]:
            return 'shikuwasa'
        elif self.kind == fruits[2]:
            return 'yuzu'
        elif self.kind == CHARGE_PILL:
            return 'charge pill'
        elif self.kind == XP_UP_PILL:
            return 'experience pill'
        elif self.kind == HASTE_PILL:
            return 'speed pill'
        elif self.kind == IDENTIFY_PILL:
            return 'knowledge pill'
        elif self.kind == XP_DOWN_PILL:
            return 'inexperience pill'
        elif self.kind == POISON_PILL:
            return 'poison pill'
        elif self.kind == PROTECT_PILL:
            return 'protection pill'
        elif self.kind == TORMENT_PILL:
            return 'radioactive pill'
        elif self.kind == THICK_SWEATER:
            return 'thick sweater'
        elif self.kind == BALLISTIC_VEST:
            return 'ballistic vest'
        elif self.kind == DRAGON_SCALE_MAIL:
            return 'dragon scale mail'
        elif self.kind == TITANIUM_NECKLACE:
            return 'titanium necklace'
        elif self.kind == RUSTY_NECKLACE:
            return 'rusty necklace'
        elif self.kind == CRIMSON_NECKLACE:
            return 'crimson necklace'
        elif self.kind == GLOWING_NECKLACE:
            return 'glowing necklace'
        elif self.kind == UNHOLY_NECKLACE:
            return 'unholy necklace'
        elif self.kind == WAND_OF_DEATH:
            return 'wand of death'
        elif self.kind == MANUAL:
            return 'manual'
        elif self.kind == GUIDEBOOK:
            return 'guidebook'
        elif self.kind == CORRUPTOR:
            return 'corruptor'
        elif self.kind == OFFSETTER:
            return 'offsetter'
        elif self.kind == COPIER:
            return 'copier'
        elif self.kind == PALANTIR:
            return 'palantir'
        elif self.kind == GOLDEN_CANDLE:
            return 'golden candle'

    def color(self):
        if self.is_pill():
            return Color.WHITE
        elif self.kind == NO_ITEM:
            return curses.A_REVERSE
        elif self.kind == CROWBAR:
            return Color.LIGHTGRAY
        elif self.kind == VOLCANIC_SHARD:
            return Color.LIGHTRED
        elif self.kind == TASER:
            return Color.LIGHTCYAN
        elif self.kind == JELLY_GUN:
            return Color.LIGHTGREEN
        elif self.kind == fruits[0]:
            return Color.MAGENTA
        elif self.kind == fruits[1]:
            return Color.LIGHTGREEN
        elif self.kind == fruits[2]:
            return Color.YELLOW
        elif self.kind == THICK_SWEATER:
            return Color.MAGENTA
        elif self.kind == BALLISTIC_VEST:
            return Color.CYAN
        elif self.kind == DRAGON_SCALE_MAIL:
            return Color.GREEN
        elif self.kind == TITANIUM_NECKLACE:
            return Color.LIGHTGRAY
        elif self.kind == RUSTY_NECKLACE:
            return Color.BROWN
        elif self.kind == CRIMSON_NECKLACE:
            return Color.RED
        elif self.kind == GLOWING_NECKLACE:
            return Color.YELLOW
        elif self.kind == UNHOLY_NECKLACE:
            return Color.DARKGRAY
        elif self.kind == WAND_OF_DEATH:
            return Color.BLUE
        elif self.kind == MANUAL:
            return Color.BROWN
        elif self.kind == GUIDEBOOK:
            return Color.YELLOW
        elif self.kind == CORRUPTOR:
            return Color.LIGHTRED
        elif self.kind == OFFSETTER:
            return Color.LIGHTMAGENTA
        elif self.kind == COPIER:
            return Color.LIGHTBLUE
        elif self.kind == PALANTIR:
            return random.choice([Color.LIGHTBLUE, Color.BLUE,
                                  Color.LIGHTCYAN, Color.CYAN])
        elif self.kind == GOLDEN_CANDLE:
            return random.choice([Color.LIGHTRED, Color.YELLOW,
                                  Color.BROWN, Color.WHITE])

    def char(self):
        if self.is_weapon() or self.kind == WAND_OF_DEATH:
            return CHAR_WEAPON
        elif self.is_body_armor():
            return CHAR_BODY_ARMOR
        elif self.is_necklace():
            return CHAR_NECKLACE
        elif self.is_pill() or self.is_fruit():
            return CHAR_FOOD
        elif self.kind == PALANTIR or self.kind == GOLDEN_CANDLE:
            return CHAR_ARTIFACT
        else:
            return CHAR_MISC

