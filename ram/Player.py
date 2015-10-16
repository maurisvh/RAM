import Element
import Timer
import Color
import Item
import memory
from messages import msg

import random
import sys

class Player:
    def __init__(self):
        self.pos = None
        self.dlvl = 0

        # Fake a zero-terminated string.
        name = 'test'
        self.name = [ord(c) for c in name[:14].ljust(15, '\0')]

        # 0 to 255
        self.hp = 10
        # 0 to 255
        self.tp = 10
        # 0 (death) to 15
        self.xl = 1
        # -8 (no defense) to 7
        self.defense = 0

        # Elemental aptitudes (-8 to 7)
        self.aptitude = {
            Element.METAL: 0,
            Element.ACID:  0,
            Element.FIRE:  0,
            Element.ELEC:  0,
        }

        self.inventory = [Item.Item.generate(0) for i in range(8)]
        #self.inventory[0].kind = Item.CROWBAR
        #self.inventory[0] = Item.Item(0xFF)
        #self.equip(0)

        self.appearance_byte = 0
        self.display_byte = 0
        self.spell_memory_byte = 0

        # Timers (0 to 255)
        self.timers = {
            Timer.POISON:  0,
            Timer.HASTE:   0,
            Timer.CHARGE:  0,
            Timer.PROTECT: 0,
        }

        # Currently selected address in memory
        self.address = 0

        self.dlvl_delta = 0x01
        self.timer_delta = 0xFF
        self.damage_offset = 0x00
        self.text_sync = 0x00

        # Interface
        self.show_ram = False

    def read_memory(self, p):
        return memory.read_memory(self, p)

    def write_memory(self, p, value):
        return memory.write_memory(self, p, value)

    @property
    def name_str(self):
        # Simulate buffer overflows.
        s = []; p = memory.addr_player_name[0]
        while True:
            c = self.read_memory(p)
            if c == 0:
                return ''.join(s)
            s.append(chr(c))
            p += 1

    def color(self):
        c = self.appearance_byte & 0x07
        return [Color.WHITE, Color.YELLOW, Color.LIGHTMAGENTA,
                Color.LIGHTRED, Color.LIGHTCYAN, Color.LIGHTGREEN,
                Color.LIGHTBLUE, Color.DARKGRAY][c]

    def char(self):
        c = self.appearance_byte >> 3
        return chr(ord('@') - c)

    @property
    def maxhp(self):
        # TODO
        return 10

    @property
    def maxtp(self):
        # TODO
        return 10

    def equip(self, index):
        item = self.inventory[index]
        assert item is not None
        assert not item.equipped

        def remove_obj(self, obj):
            obj.equipped = False
            for element in self.aptitude:
                self.aptitude[element] -= obj.element_bonus(element)
            self.defense -= obj.defense()

        for j, o in enumerate(self.inventory):
            if index == j:
                continue
            if item.is_weapon() and o.is_weapon() and o.equipped:
                msg('You unwield {0}.'.format(o.name('your')))
                remove_obj(self, o)
            elif item.is_necklace() and o.is_necklace() and o.equipped:
                msg('You remove {0}.'.format(o.name('your')))
                remove_obj(self, o)
            elif item.is_body_armor() and o.is_body_armor() and o.equipped:
                msg('You take off {0}.'.format(o.name('your')))
                remove_obj(self, o)

        item.equipped = True
        for element in self.aptitude:
            self.aptitude[element] += item.element_bonus(element)
        self.defense += item.defense()

    def move(self, level, pos):
        self.pos = pos
        feat = level[pos]
        item = level.items.get(pos)
        if item:
            msg('You see here {0}.'.format(item.name()))
        if feat in '<>':
            d = self.dlvl_delta
            if feat == '<':
                d *= -1
            goal = (self.dlvl + d) & 0xFF
            if feat == '<' and goal == 0xFF:
                msg('There is a staircase to level {0} here.'.format(goal))
            else:
                msg('There is a staircase leading out of the dungeon here.')

    def step(self, level, dx, dy):
        """Return whether a turn was passed."""
        x, y = self.pos
        goal = (x + dx, y + dy)
        feat = level[goal]
        if feat == '+':
            level.tiles[goal] = "'"
            msg('You open the door.')
            return True
        elif feat.isdigit():
            bit = 1 << int(feat)
            new_state = 'off' if self.address & bit else 'on'
            msg('You turn the BIT{0} switch {1}.'.format(feat, new_state))
            self.address ^= bit
            return True
        elif feat == '#':
            return False
        else:
            self.move(level, goal)
            return True
