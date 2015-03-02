from spell import Spell
from element import Element

# 00 = Player appearance.
#      top 3 bits = color
#      bottom 5 bits is character, counting down from ascii '@'
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
addr_mon_pos   = {0x11: 0, 0x14: 1, 0x17: 2, 0x1A: 3, 0x1D: 4}
addr_mon_hp    = {0x12: 0, 0x15: 1, 0x18: 2, 0x1B: 3, 0x1E: 4}

# 1F = Spell memory (8 bits)
#
addr_spell_memory = 0x1F

# 20-23 = identification
addr_identify = {0x20: 0, 0x21: 8, 0x22: 16, 0x23: 24}

# 24-27 = timers
addr_timers = {0x24: Timer.poison, 0x25: Timer.haste,
              0x26: Timer.charge, 0x27: Timer.protect}

# 28-2F = inventory
addr_inventory = {0x28+i: i for i in range(8)}

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

def read_memory(addr):
    global player

    if addr == addr_player_appearance:
        return player.appearance_byte
    elif addr in addr_player_name:
        return player.name[addr - 1]
    elif addr in addr_mon_flags:
        raise NotImplementedError()
    elif addr in addr_mon_pos:
        raise NotImplementedError()
    elif addr in addr_mon_hp:
        raise NotImplementedError()
    elif addr == addr_spell_memory:
        return player.spell_memory_byte
    elif addr in addr_identify:
        raise NotImplementedError()
    elif addr in addr_timers:
        timer = addr_timers[addr]
        return player.timers[timer]
    elif addr in addr_inventory:
        raise NotImplementedError()
    elif addr == addr_door_appearance:
        raise NotImplementedError()
    elif addr == addr_wall_appearance:
        raise NotImplementedError()
    elif addr == addr_floor_color:
        raise NotImplementedError()
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
        return player.pos
    elif addr == addr_player_dlvl:
        return player.dlvl
    elif addr == addr_player_metal_acid:
        return (player.aptitude[Element.metal] << 4) \
              | player.aptitude[Element.acid]
    elif addr == addr_player_fire_elec:
        return (player.aptitude[Element.fire] << 4) \
              | player.aptitude[Element.elec]

def write_memory(addr, value):
    global player

    if addr == addr_player_appearance:
        pass
    elif addr in addr_player_name:
        pass
    elif addr in addr_mon_flags:
        pass
    elif addr in addr_mon_pos:
        pass
    elif addr in addr_mon_hp:
        pass
    elif addr == addr_spell_memory:
        pass
    elif addr in addr_identify:
        pass
    elif addr in addr_timers:
        pass
    elif addr in addr_inventory:
        pass
    elif addr == addr_door_appearance:
        pass
    elif addr == addr_wall_appearance:
        pass
    elif addr == addr_floor_color:
        pass
    elif addr == addr_dlvl_delta:
        pass
    elif addr == addr_timer_delta:
        pass
    elif addr == addr_damage_offset:
        pass
    elif addr == addr_text_sync:
        pass
    elif addr == addr_player_hp:
        pass
    elif addr == addr_player_tp:
        pass
    elif addr == addr_player_xl_def:
        pass
    elif addr == addr_player_pos:
        pass
    elif addr == addr_player_dlvl:
        pass
    elif addr == addr_player_metal_acid:
        pass
    elif addr == addr_player_fire_elec:
        pass

# Spells:
# 0 zero
# 1 increment
# 2 set rightmost zero bit
# 3 copy next
# 4 add 0x9D
# 5 reverse
# 6 choose lower byte
# 7 choose upper byte

def cast_spell(spell):
    global player
    addr = player.address
    assert 0x00 <= addr <= 0x3F

    if spell is Spell.ONE:
        write_memory(addr, 0x01)
    elif spell is Spell.CLO:
        v = read_memory(addr)
        mask = 0x7F
        while mask and v & mask == v:
            mask >>= 1
        v &= mask
        write_memory(addr, v)
    elif spell is Spell.INC:
        v = read_memory(addr)
        write_memory(addr, (v + 1) & 0xFF)
    elif spell is Spell.CPN:
        v = read_memory((addr + 1) & 0x3F)
        write_memory(addr, v)
    elif spell is Spell.A9D:
        v = read_memory(addr)
        write_memory(addr, (v + 0x9D) & 0xFF)
    elif spell is Spell.REV:
        v = read_memory(addr)
        v = ((v & 0xF0) >> 4) | ((v & 0x0F) << 4)
        v = ((v & 0xCC) >> 2) | ((v & 0x33) << 2)
        v = ((v & 0xAA) >> 1) | ((v & 0x55) << 1)
        write_memory(addr, v)
    elif spell is Spell.WLN:
        raise NotImplementedError()
    elif spell is Spell.WHN:
        raise NotImplementedError()
