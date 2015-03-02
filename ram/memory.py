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
#
# 38 = "text sync" (causes glitches when set high)
addr_text_sync = 0x38

# 39 = Player HP (capped by XL).
addr_player_hp = 0x39

# 3A = Player TP (capped by XL).
addr_player_tp = 0x39

# 3B = high nibble: XL 0-15
#      low nibble: Def 0-15
addr_player_xl_def = 0x3a

# 3C = position (y + 19*x)
#
# 3D = dlvl
#
# 3E = metal (hi) acid (lo) res
#
# 3F = fire (hi) elec (lo) res


# Spells:
# 0 zero
# 1 increment
# 2 set rightmost zero bit
# 3 copy next
# 4 add 0x9D
# 5 reverse
# 6 choose lower byte
# 7 choose upper byte

