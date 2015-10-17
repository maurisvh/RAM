import Color
import Element

import curses
import random
import re

CHAR_WEAPON = '/'
CHAR_BODY_ARMOR = '['
CHAR_NECKLACE = '"'
CHAR_FOOD = '*'
CHAR_MISC = '$'
CHAR_ARTIFACT = '&'

fruits = list(range(0x05, 0x08))
pills = list(range(0x08, 0x10))

NO_ITEM = 0x00
CROWBAR = 0x01
VOLCANIC_SHARD = 0x02
TASER = 0x03
JELLY_GUN = 0x04
FULL_HP_FRUIT = fruits[0]
FULL_TP_FRUIT = fruits[1]
HALF_HP_FRUIT = fruits[2]
CHARGE_PILL = pills[0]
XP_UP_PILL = pills[1]
HASTE_PILL = pills[2]
IDENTIFY_PILL = pills[3]
XP_DOWN_PILL = pills[4]
POISON_PILL = pills[5]
PROTECT_PILL = pills[6]
TORMENT_PILL = pills[7]
THICK_SWEATER = 0x10
BALLISTIC_VEST = 0x11
DRAGON_SCALE_MAIL = 0x12
TITANIUM_NECKLACE = 0x13
RUSTY_NECKLACE = 0x14
CRIMSON_NECKLACE = 0x15
GLOWING_NECKLACE = 0x16
UNHOLY_NECKLACE = 0x17
WAND_OF_DEATH = 0x18
MANUAL = 0x19
GUIDEBOOK = 0x1A
CORRUPTOR = 0x1B
OFFSETTER = 0x1C
COPIER = 0x1D
PALANTIR = 0x1E
GOLDEN_CANDLE = 0x1F

weapons = [CROWBAR, VOLCANIC_SHARD, TASER, JELLY_GUN]
body_armors = [THICK_SWEATER, BALLISTIC_VEST, DRAGON_SCALE_MAIL]
necklaces = [TITANIUM_NECKLACE, RUSTY_NECKLACE, CRIMSON_NECKLACE,
             GLOWING_NECKLACE, UNHOLY_NECKLACE]
consumables = [FULL_HP_FRUIT, FULL_TP_FRUIT, HALF_HP_FRUIT, CHARGE_PILL,
               XP_UP_PILL, HASTE_PILL, IDENTIFY_PILL, XP_DOWN_PILL, POISON_PILL,
               PROTECT_PILL, TORMENT_PILL, WAND_OF_DEATH, MANUAL, GUIDEBOOK,
               CORRUPTOR, OFFSETTER, COPIER]

identified = set()


class Item:
    def __init__(self, byte):
        self.byte = byte

    @staticmethod
    def generate(depth):
        depth = min(20, depth)
        weights = [
            (CROWBAR, 10),
            (VOLCANIC_SHARD, 7 + depth),
            (TASER, 4 + 2 * depth),
            (JELLY_GUN, 1 + 3 * depth),
            (FULL_HP_FRUIT, 10 - depth // 2),
            (FULL_TP_FRUIT, 10 - depth // 2),
            (HALF_HP_FRUIT, 20 - depth // 2),
            (CHARGE_PILL, 6),
            (XP_UP_PILL, 4),
            (HASTE_PILL, 6),
            (IDENTIFY_PILL, 12),
            (XP_DOWN_PILL, 8),
            (POISON_PILL, 8),
            (PROTECT_PILL, 6),
            (TORMENT_PILL, 4),
            (THICK_SWEATER, 8),
            (BALLISTIC_VEST, 6 + depth),
            (DRAGON_SCALE_MAIL, 2 * depth),
            (TITANIUM_NECKLACE, 3),
            (RUSTY_NECKLACE, 3),
            (CRIMSON_NECKLACE, 3),
            (GLOWING_NECKLACE, 3),
            (UNHOLY_NECKLACE, 3),
            (WAND_OF_DEATH, 1),
            (MANUAL, 1),
            (GUIDEBOOK, 1 if depth > 10 else 0),
            (CORRUPTOR, 1 if depth > 10 else 0),
            (OFFSETTER, 1 if depth > 10 else 0),
            (COPIER, 1 if depth > 10 else 0),
        ]

        item = Item(0)
        gen_kind = None
        w = random.randrange(sum(n for x, n in weights))
        for gen_kind, n in weights:
            w -= n
            if w <= 0:
                break

        item.kind = gen_kind

        p_cursed = 1.0 if gen_kind == UNHOLY_NECKLACE else 0.1
        if item.is_equip() and random.random() < p_cursed:
            item.cursed = True
        if item.is_equip() and random.random() < 0.15:
            item.enchanted = True

        return item

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
        max_len = 30
        if len(name) <= max_len:
            return name
        repls = [('(equipped)', '(eq)'),
                 ('necklace', 'neckl.'),
                 ('dragon scale ', 'drag.sc.'),
                 ('ballistic ', 'ball.'),
                 ('volcanic ', 'volc.'),
                 ('enchanted', 'ench'),
                 ('cursed', 'crsd')]
        for a, b in repls:
            name = name.replace(a, b)
            if len(name) <= max_len: return name
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
