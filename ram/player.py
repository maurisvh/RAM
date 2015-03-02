from actor import Actor
from element import Element
from timer import Timer

class Player(Actor):
    def __init__(self):
        self.pos = None
        self.dlvl = None

        # Fake a zero-terminated string.
        self.name = 'test'
        self.name = [ord(c) for c in name[:14].ljust(15, '\0')]

        # 0 to 255
        self.hp = 10
        # 0 to 255
        self.tp = 10
        # 0 (death) to 15
        self.xl = 1
        # 0 (no defense) to 15
        self.defense = 1

        self.appearance_byte = 0
        self.display_byte = 0
        self.spell_memory_byte = 0

        # Elemental aptitudes (-8 to 7)
        self.aptitude = {
            Element.metal: 0,
            Element.acid:  0,
            Element.fire:  0,
            Element.elec:  0,
        }

        # Timers (0 to 255)
        self.timers = {
            Timer.poison:  0,
            Timer.haste:   0,
            Timer.charge:  0,
            Timer.protect: 0,
        }

        # Currently selected address in memory
        self.address = 0

    @property
    def maxhp(self):
        # TODO
        return 10

    @property
    def maxtp(self):
        # TODO
        return 10
