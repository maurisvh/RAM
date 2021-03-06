import Board
import Spell
import Element
import Timer
import Item
import Color

from messages import msg
from util import nth, pos2int

# 00 = Player appearance.
#      bottom 3 bits = color
#      top 5 bits is character, counting down from ascii '@'
#
addr_player_appearance = 0x00

# 01-0F = Player name. Zero terminated
#
addr_player_name = range(0x01, 0x10)

# 10-12 = Monster 1 flags, pos, hp.
# 13-15 = Monster 2 flags, pos, hp.
# 16-18 = Monster 3 flags, pos, hp.
# 19-1B = Monster 4 flags, pos, hp.
# 1C-1E = Monster 5 flags, pos, hp.
addr_mon_flags = {0x10: 0, 0x13: 1, 0x16: 2, 0x19: 3, 0x1C: 4}
addr_mon_pos = {0x11: 0, 0x14: 1, 0x17: 2, 0x1A: 3, 0x1D: 4}
addr_mon_hp = {0x12: 0, 0x15: 1, 0x18: 2, 0x1B: 3, 0x1E: 4}

# 1F = Spell memory (8 bits)
#
addr_spell_memory = 0x1F

# 20-23 = identification
addr_identify = {0x20: 0, 0x21: 8, 0x22: 16, 0x23: 24}

# 24-27 = timers
addr_timers = {0x24: Timer.POISON, 0x25: Timer.HASTE,
               0x26: Timer.CHARGE, 0x27: Timer.PROTECT}

# 28-2F = inventory
addr_inventory = {0x28 + i: i for i in range(8)}

# 30 = door appearance
addr_door_appearance = 0x30

# 31 = wall appearance
addr_wall_appearance = 0x31

# 32 = floor color
addr_floor_color = 0x32

# 33 = z delta       (signed)
addr_dlvl_delta = 0x33

# 34 = timer delta   (signed)
addr_timer_delta = 0x34

# 35 = damage offset (signed)
addr_damage_offset = 0x35

# 36 = ?
# 37 = ? (should mess things up very hard)

# 38 = "text sync" (causes glitches when set high)
addr_text_sync = 0x38

# 39 = Player HP (capped by XL).
addr_player_hp = 0x39

# 3A = Player TP (capped by XL).
addr_player_tp = 0x3A

# 3B = high nibble: XL 0-15
#      low nibble: Def 0-15
addr_player_xl_def = 0x3B

# 3C = position (y + 19*x)
addr_player_pos = 0x3C

# 3D = dlvl
addr_player_dlvl = 0x3D

# 3E = metal (hi) acid (lo) res
addr_player_metal_acid = 0x3E

# 3F = fire (hi) elec (lo) res
addr_player_fire_elec = 0x3F


def address_name(addr):
    assert 0 <= addr < 0x40
    if addr == addr_player_appearance:
        return 'player appearance'
    elif addr in addr_player_name:
        return 'player name ({0} letter)'.format(nth(addr))
    elif addr in addr_mon_flags:
        letter = 'ABCDE'[addr_mon_flags[addr]]
        return 'monster {0} flags'.format(letter)
    elif addr in addr_mon_pos:
        letter = 'ABCDE'[addr_mon_pos[addr]]
        return 'monster {0} position'.format(letter)
    elif addr in addr_mon_hp:
        letter = 'ABCDE'[addr_mon_hp[addr]]
        return 'monster {0} hp'.format(letter)
    elif addr == addr_spell_memory:
        return 'spell memory'
    elif addr in addr_identify:
        return 'identification bits'
    elif addr in addr_timers:
        timer = addr_timers[addr]
        return '{0} timer'.format(timer)
    elif addr in addr_inventory:
        slot = addr_inventory[addr] + 1
        return 'item {0}'.format(slot)
    elif addr == addr_door_appearance:
        return 'door appearance'
    elif addr == addr_wall_appearance:
        return 'wall appearance'
    elif addr == addr_floor_color:
        return 'floor color'
    elif addr == addr_dlvl_delta:
        return 'depth delta'
    elif addr == addr_timer_delta:
        return 'timer delta'
    elif addr == addr_damage_offset:
        return 'damage offset'
    elif addr == addr_text_sync:
        return 'text signal sync'
    elif addr == addr_player_hp:
        return 'player hp'
    elif addr == addr_player_tp:
        return 'player tp'
    elif addr == addr_player_xl_def:
        return 'player exp/defense'
    elif addr == addr_player_pos:
        return 'player position'
    elif addr == addr_player_dlvl:
        return 'dungeon level'
    elif addr == addr_player_metal_acid:
        return 'metal/acid aptitude'
    elif addr == addr_player_fire_elec:
        return 'fire/elec aptitude'
    else:
        return '(UNIMPLEMENTED)'


def read_memory(player, addr):
    if addr == addr_player_appearance:
        return player.appearance_byte
    elif addr in addr_player_name:
        return player.name[addr - addr_player_name[0]]
    elif addr in addr_mon_flags:
        raise NotImplementedError()
    elif addr in addr_mon_pos:
        raise NotImplementedError()
    elif addr in addr_mon_hp:
        raise NotImplementedError()
    elif addr == addr_spell_memory:
        return player.spell_memory_byte
    elif addr in addr_identify:
        v = 0
        offset = addr_identify[addr]
        for i in range(offset, offset + 8):
            v <<= 1
            if i in Item.identified:
                v |= 1
        return v
    elif addr in addr_timers:
        timer = addr_timers[addr]
        return player.timers[timer]
    elif addr in addr_inventory:
        return player.inventory[addr_inventory[addr]].byte
    elif addr == addr_door_appearance:
        return Board.door_appearance
    elif addr == addr_wall_appearance:
        return Board.wall_appearance
    elif addr == addr_floor_color:
        return Board.floor_color
    elif addr == addr_dlvl_delta:
        return player.dlvl_delta
    elif addr == addr_timer_delta:
        return player.timer_delta
    elif addr == addr_damage_offset:
        return player.damage_offset
    elif addr == addr_text_sync:
        return player.text_sync
    elif addr == addr_player_hp:
        return player.hp
    elif addr == addr_player_tp:
        return player.tp
    elif addr == addr_player_xl_def:
        return (player.xl << 4) | player.defense
    elif addr == addr_player_pos:
        return pos2int(player.pos)
    elif addr == addr_player_dlvl:
        return player.dlvl
    elif addr == addr_player_metal_acid:
        return (player.aptitude[Element.METAL] << 4) \
               | player.aptitude[Element.ACID]
    elif addr == addr_player_fire_elec:
        return (player.aptitude[Element.FIRE] << 4) \
               | player.aptitude[Element.ELEC]
    elif addr == 0x36 or addr == 0x37:
        raise NotImplementedError
    else:
        raise ValueError


def describe_player(byte):
    col = [
        'white', 'yellow', 'pink', 'red',
        'cyan', 'green', 'blue', 'gray',
    ][byte & 0x07]
    noun = [
        'at sign', 'question mark',
        'angle bracket', 'equals sign',
        'angle bracket', 'semicolon',
        'colon', 'nine',
        'eight', 'seven',
        'six', 'five',
        'four', 'three',
        'two', 'one',
        'zero', 'slash',
        'dot', 'dash',
        'comma', 'plus',
        'asterisk', 'parenthesis',
        'parenthesis', 'apostrophe',
        'ampersand', 'percent sign',
        'dollar sign', 'pound sign',
        'quotation mark', 'exclamation point',
    ][byte >> 3]
    return col, noun


def bits(n):
    """Return a list of set bits in n, e.g. bits(0b11001) == [0, 3, 4]"""
    res = []
    i = 0
    while n > 0:
        if n & 1:
            res.append(i)
        n >>= 1
        i += 1
    return res


def write_memory(player, addr, value):
    assert 0x00 <= value <= 0xFF

    if addr == addr_player_appearance:
        old_col, old_noun = describe_player(player.appearance_byte)
        col, noun = describe_player(value)
        if old_col == col:
            if old_noun == noun:
                msg('You feel momentarily different.')
            else:
                # Dirty hack, but sufficient.
                article = 'an' if noun[0] in 'ae' else 'a'
                msg('You turn into {0} {1}!'.format(article, noun))
        elif old_noun == noun:
            msg('You turn {0}!'.format(col))
        else:
            msg('You turn into a {0} {1}!'.format(col, noun))
        player.appearance_byte = value

    elif addr in addr_player_name:
        idx = addr - addr_player_name[0]
        player.name[idx] = value

    elif addr in addr_mon_flags:
        raise NotImplementedError()
    elif addr in addr_mon_pos:
        raise NotImplementedError()
    elif addr in addr_mon_hp:
        raise NotImplementedError()

    elif addr == addr_spell_memory:
        old = player.spell_memory_byte
        for i in bits(old & ~value):
            sp = Spell.spells[i].name
            msg('You forget how to cast {0}.'.format(sp), Color.RED)
        for i in bits(value & ~old):
            sp = Spell.spells[i].name
            msg('You learn how to cast {0}.'.format(sp), Color.CYAN)
        player.spell_memory_byte = value

    elif addr in addr_identify:
        offset = addr_identify[addr]
        old = 0
        for i in range(offset, offset + 8):
            old <<= 1
            if i in Item.identified:
                old |= 1
        lose = old & ~value
        gain = value & ~old

        if lose and gain:
            msg('Your knowledge of items shifts around.', Color.MAGENTA)
        elif lose:
            msg('Your knowledge of items grows weaker.', Color.RED)
        elif gain:
            msg('Your knowledge of items grows stronger.', Color.GREEN)

        for i in bits(lose):
            Item.identified.remove(i + offset)
        for i in bits(gain):
            Item.identified.add(i + offset)

    elif addr in addr_timers:
        t = addr_timers[addr]
        old = player.timers[t]
        if t is Timer.POISON:
            if value > old:
                if old == 0:
                    msg('You feel poisoned.', Color.RED)
                else:
                    msg('You feel even more poisoned.', Color.RED)
            elif value < old:
                if value == 0:
                    msg('You feel better.', Color.RED)
                else:
                    msg('You feel less poisoned.')
        elif t is Timer.HASTE:
            if value > old:
                if old == 0:
                    msg('You feel fast!', Color.GREEN)
                else:
                    msg('You feel even faster!', Color.GREEN)
            elif value < old:
                if value == 0:
                    msg('Your speed returns to normal.', Color.RED)
                else:
                    msg('You feel slower.', Color.RED)
        elif t is Timer.CHARGE:
            if value > old:
                if old == 0:
                    msg('You feel strong!', Color.GREEN)
                else:
                    msg('You feel even stronger!', Color.GREEN)
            elif value < old:
                if value == 0:
                    msg('Your strength returns to normal.', Color.RED)
                else:
                    msg('You feel weaker.', Color.RED)
        elif t is Timer.PROTECT:
            if value > old:
                if old == 0:
                    msg('You feel protected!', Color.GREEN)
                else:
                    msg('You feel even more protected!', Color.GREEN)
            elif value < old:
                if value == 0:
                    msg('Your defenses return to normal.', Color.RED)
                else:
                    msg('You feel more vulnerable.', Color.RED)
        player.timers[t] = value

    elif addr in addr_inventory:
        i = addr_inventory[addr]
        old = player.inventory[i]
        new = Item.Item(value)

        # TODO: talk about what happens to equipment status?
        if old.kind == Item.NO_ITEM and new.kind != Item.NO_ITEM:
            msg('You suddenly have {0}!'.format(new.name()), Color.CYAN)
        elif new.kind == Item.NO_ITEM:
            msg('{0} suddenly disappears!'.format(old.name('Your')),
                Color.RED)
        elif old.kind == new.kind and old.byte != new.byte:
            msg('{0} looks different.'.format(old.name('Your')),
                Color.CYAN)
        else:
            msg('{0} changes into {1}!'.format(old.name('Your'),
                                               new.name()), Color.CYAN)
    elif addr == addr_door_appearance:
        # Probably implement LOS first
        raise NotImplementedError()
    elif addr == addr_wall_appearance:
        raise NotImplementedError()
    elif addr == addr_floor_color:
        raise NotImplementedError()
    elif addr == addr_dlvl_delta:
        raise NotImplementedError()
    elif addr == addr_timer_delta:
        raise NotImplementedError()
    elif addr == addr_damage_offset:
        raise NotImplementedError()
    elif addr == addr_text_sync:
        raise NotImplementedError()
    elif addr == addr_player_hp:
        raise NotImplementedError()
    elif addr == addr_player_tp:
        raise NotImplementedError()
    elif addr == addr_player_xl_def:
        raise NotImplementedError()
    elif addr == addr_player_pos:
        raise NotImplementedError()
    elif addr == addr_player_dlvl:
        raise NotImplementedError()
    elif addr == addr_player_metal_acid:
        raise NotImplementedError()
    elif addr == addr_player_fire_elec:
        raise NotImplementedError()


# Spells:
# 0 zero
# 1 increment
# 2 set rightmost zero bit
# 3 copy next
# 4 add 0x9D
# 5 reverse
# 6 choose lower byte
# 7 choose upper byte

def cast_spell(player, spell):
    addr = player.address
    assert 0x00 <= addr <= 0x3F

    if spell is Spell.ONE:
        write_memory(player, addr, 0x01)
    elif spell is Spell.CLO:
        v = read_memory(player, addr)
        mask = 0x7F
        while mask and v & mask == v:
            mask >>= 1
        v &= mask
        write_memory(player, addr, v)
    elif spell is Spell.INC:
        v = read_memory(player, addr)
        write_memory(player, addr, (v + 1) & 0xFF)
    elif spell is Spell.CPN:
        v = read_memory(player, (addr + 1) & 0x3F)
        write_memory(player, addr, v)
    elif spell is Spell.A9D:
        v = read_memory(player, addr)
        write_memory(player, addr, (v + 0x9D) & 0xFF)
    elif spell is Spell.REV:
        v = read_memory(player, addr)
        v = ((v & 0xF0) >> 4) | ((v & 0x0F) << 4)
        v = ((v & 0xCC) >> 2) | ((v & 0x33) << 2)
        v = ((v & 0xAA) >> 1) | ((v & 0x55) << 1)
        write_memory(player, addr, v)
    elif spell is Spell.WLN:
        raise NotImplementedError()
    elif spell is Spell.WHN:
        raise NotImplementedError()
