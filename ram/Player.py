from Actor import Actor
import Element
import Timer
import Color
import Item
import memory

import random
import sys

class Player(Actor):
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

        self.inventory = [Item.Item(random.randint(0, 255)) for i in range(8)]
        #self.inventory[0].kind = Item.CROWBAR
        #self.inventory[0] = Item.Item(0xFF)
        #self.equip(0)

        [Item.Item(i).compressed_name() for i in range(8, 256)]

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
        sys.stderr.write(repr(s) + '\n')
        while True:
            c = self.read_memory(p)
            if c == 0:
                return ''.join(s)
            s.append(chr(c))
            p += 1

    @property
    def color(self):
        c = self.appearance_byte & 0x07
        return [Color.WHITE, Color.YELLOW, Color.LIGHTMAGENTA,
                Color.LIGHTRED, Color.LIGHTCYAN, Color.LIGHTGREEN,
                Color.LIGHTBLUE, Color.DARKGRAY][c]

    @property
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
