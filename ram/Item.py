import Color
import Element

import curses
import random
import re

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

identified = set()

class Item:
    def __init__(self, byte):
        self.byte = byte

    @property
    def kind(self):
        return self.byte >> 3
    @kind.setter
    def kind(self, value):
        self.byte = (self.byte & 0b00000111) | (value << 3)
    @property
    def enchanted(self):
        return self.byte & 0b100
    @enchanted.setter
    def enchanted(self, value):
        self.byte = (self.byte & ~0b100) | (int(value) << 2)
    @property
    def equipped(self):
        return self.byte & 0b010
    @equipped.setter
    def equipped(self, value):
        self.byte = (self.byte & ~0b010) | (int(value) << 1)
    @property
    def cursed(self):
        return self.byte & 0b001
    @cursed.setter
    def cursed(self, value):
        self.byte = (self.byte & ~0b001) | (int(value) << 0)

    def is_weapon(self):
        return self.kind in weapons
    def is_body_armor(self):
        return self.kind in body_armors
    def is_necklace(self):
        return self.kind in necklaces
    def is_equip(self):
        return self.is_weapon() or self.is_body_armor() \
               or self.is_necklace()
    def is_consumable(self):
        return self.kind in consumables
    def is_pill(self):
        return self.kind in pills
    def is_fruit(self):
        return self.kind in fruits
    def known(self):
        return self.kind in identified

    def kind_name(self):
        if self.kind == NO_ITEM:
            raise ValueError
        elif self.kind == CROWBAR:
            return 'crowbar'
        elif self.kind == VOLCANIC_SHARD:
            return 'volcanic shard'
        elif self.kind == TASER:
            return 'taser'
        elif self.kind == JELLY_GUN:
            return 'jelly gun'
        elif self.kind == FULL_HP_FRUIT and self.known():
            return 'full-healing fruit'
        elif self.kind == FULL_TP_FRUIT and self.known():
            return 'energizing fruit'
        elif self.kind == HALF_HP_FRUIT and self.known():
            return 'healing fruit'
        elif self.kind == fruits[0]:
            return 'akebi'
        elif self.kind == fruits[1]:
            return 'shikuwasa'
        elif self.kind == fruits[2]:
            return 'yuzu'
        elif self.kind == CHARGE_PILL and self.known():
            return 'charge pill'
        elif self.kind == XP_UP_PILL and self.known():
            return 'experience pill'
        elif self.kind == HASTE_PILL and self.known():
            return 'speed pill'
        elif self.kind == IDENTIFY_PILL and self.known():
            return 'knowledge pill'
        elif self.kind == XP_DOWN_PILL and self.known():
            return 'inexperience pill'
        elif self.kind == POISON_PILL and self.known():
            return 'poison pill'
        elif self.kind == PROTECT_PILL and self.known():
            return 'protection pill'
        elif self.kind == TORMENT_PILL and self.known():
            return 'radioactive pill'
        elif self.kind in pills:
            descs = ['round', 'tiny', 'diamond', 'oblong',
                     'soft', 'hard', 'wide', 'translucent']
            return descs[pills.index(self.kind)] + ' pill'
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

    def name(self, article=None):
        s = self.kind_name()
        if self.is_equip():
            if self.enchanted:
                s = 'enchanted ' + s
            if self.equipped:
                s += ' (equipped)'
        if self.cursed and not self.is_fruit():
            s = 'cursed ' + s
        if article == '':
            return s
        elif article is not None:
            return article + ' ' + s
        elif s[0].lower() in 'aeiou':
            return 'an ' + s
        else:
            return 'a ' + s

    def compressed_name(self):
        name = self.name('')
        if len(name) <= 30: return name
        name = name.replace('(equipped)', '(eq)')
        if len(name) <= 30: return name
        name = name.replace(r'necklace', 'neckl.')
        if len(name) <= 30: return name
        name = name.replace(r'dragon scale ', 'drag.s.')
        if len(name) <= 30: return name
        name = name.replace(r'ballistic ', 'ball.')
        if len(name) <= 30: return name
        name = name.replace(r'volcanic ', 'volc.')
        if len(name) <= 30: return name
        name = name.replace(r'enchanted', 'ench')
        if len(name) <= 30: return name
        name = name.replace(r'cursed', 'crsd')
        if len(name) <= 30: return name
        raise ValueError(name)

    def color(self):
        if self.is_pill():
            return Color.WHITE
        elif self.kind == NO_ITEM:
            raise ValueError
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
        if self.kind == NO_ITEM:
            raise ValueError
        elif self.is_weapon() or self.kind == WAND_OF_DEATH:
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

    def defense(self):
        if self.kind == THICK_SWEATER:
            return 2
        elif self.kind == BALLISTIC_VEST:
            return 4
        elif self.kind == DRAGON_SCALE_MAIL:
            return 6
        else:
            return 0

    def element_bonus(self, element):
        me, ac, fi, el = (Element.METAL, Element.ACID,
                          Element.FIRE, Element.ELEC)
        if self.kind == THICK_SWEATER:
            v = {me: 0, ac: 0, fi: 2, el: -2}
        elif self.kind == BALLISTIC_VEST:
            v = {me: 2, ac: -2, fi: 0, el: 0}
        elif self.kind == DRAGON_SCALE_MAIL:
            v = {me: 0, ac: 2, fi: -2, el: 0}
        elif self.kind == TITANIUM_NECKLACE:
            v = {me: 3, ac: -1, fi: -1, el: -1}
        elif self.kind == RUSTY_NECKLACE:
            v = {me: -1, ac: 3, fi: -1, el: -1}
        elif self.kind == CRIMSON_NECKLACE:
            v = {me: -1, ac: -1, fi: 3, el: -1}
        elif self.kind == GLOWING_NECKLACE:
            v = {me: -1, ac: -1, fi: -1, el: 3}
        elif self.kind == RUSTY_NECKLACE:
            v = {me: -3, ac: -3, fi: -3, el: -3}
        else:
            v = {me: 0, ac: 0, fi: 0, el: 0}
        return v[element]

