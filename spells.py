class Spell:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

Spell.ONE = Spell('ONE',
    'Writes 0x01 to the selected address.')
Spell.CLO = Spell('CLO',
    'Clear the leftmost 1 bit of the target value.')
Spell.INC = Spell('INC',
    'Increment the target value, wrapping from 0xFF to 0x00 on overflow.')
Spell.CPN = Spell('CPN',
    'Set the target value to that of the byte after it in memory, '
    'cycling from 0x3F back to 0x00.')
Spell.A9D = Spell('A9D',
    'Add 0x9D to the target value, wrapping on overflow. In decimal, this '
    'is 157 (unsigned) or -99 (signed).')
Spell.REV = Spell('REV',
    'Reverses the bits of the target value.')
Spell.WLN = Spell('WLN',
    'Rewrite the lower nibble of the target value freely.')
Spell.WHN = Spell('WHN',
    'Rewrite the higher nibble of the target value freely.')

