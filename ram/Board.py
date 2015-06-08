from constants import *
from util import coinflip, compass, orthogonal
from string import ascii_uppercase

import Color
from Item import Item

import curses
import random
from los import sight_lines

# 5 bits char (down from '@'), 3 bits col (up from darkblue)
door_appearance = 0b10101101
# 5 bits char (down from '@'), 3 bits col (up from darkgray)
wall_appearance = 0b11101111
# 3 bits col (up from darkblue)
floor_color = 0b000

# Tiles are:
#  .  floor
#  +  closed door (can change)
# (\  open door)
#  #  wall (can change)
#  <  stairs up
#  >  stairs down
# 012345 switches

solids = '#+012345'

class Board:
    WIDTH = 19
    HEIGHT = 13

    def __init__(self, depth, des):
        self.depth = depth

        self.tiles = {}
        self.discovered = set()
        stairs_positions = set()
        open_positions = set()

        # Parse board description string.
        des = des.strip().split('\n')

        if coinflip():
            # Vertical mirroring
            des = des[::-1]
        if coinflip():
            # Horizontal mirroring
            des = [line[::-1] for line in des]

        des = ''.join(des)
        assert len(des) == Board.WIDTH * Board.HEIGHT

        # Replace ABCD groups with walls/floors randomly.
        for c in ascii_uppercase:
            if c not in des:
                break
            des = des.replace(c, random.choice('.#'))

        for i, c in enumerate(des):
            # Don't always generate doors.
            y, x = divmod(i, Board.WIDTH)
            pos = (x, y)
            if c == '+' and random.random() < 0.1:
                c = '.'
            if c == '<':
                stairs_positions.add(pos)
                c = '.'
            if c == '.':
                open_positions.add(pos)
            self.tiles[pos] = c

        assert len(stairs_positions) >= 2
        assert len(open_positions) >= 6

        up, down = random.sample(stairs_positions, 2)
        self.stairs_up   = up
        self.stairs_down = down
        self.tiles[up]   = '<'
        self.tiles[down] = '>'
        open_positions.remove(up)
        open_positions.remove(down)

        self.monsters = [None for n in range(MAX_MONSTERS)]
        num_mons = min(MAX_MONSTERS, random.randint(1, 2) + depth // 2)
        for i in range(num_mons):
            # TODO make monsters
            self.monsters[i] = None

        # Map from position to item.
        self.items = {}

        # TODO scale this
        num_items = 3
        for i in range(num_items):
            [p] = random.sample(open_positions, 1)
            open_positions.remove(p)
            self.items[p] = Item.generate(depth)

        # Place switches on some walls we can definitely reach.
        for i in range(3):
            [p] = random.sample(open_positions, 1)
            x, y = p
            for dx, dy in orthogonal:
                pos = (x + dx, y + dy)
                if pos not in self.tiles:
                    continue
                if self[pos] == '#':
                    self.tiles[pos] = random.choice('012345')
                    break

    def __getitem__(self, v):
        """Index the board, using a position as an integer (indexing in row
        order) or a tuple (x, y)."""
        return self.tiles[v]

    def __str__(self):
        w = Board.WIDTH
        h = Board.HEIGHT
        return '\n'.join(''.join(self.tiles[i*w:(i+1)*w]) for i in range(h))

    def char_at(self, player, pos):
        feat = self[pos]
        if pos == player.pos:
            return player.char()
        elif pos not in self.discovered:
            return ' '
        elif pos in self.items:
            return self.items[pos].char()
        elif feat == '#':
            return '#'
        elif feat == '.':
            return '.'
        elif feat == '+':
            return '+'
        else:
            return feat

    def color_at(self, player, pos):
        feat = self[pos]
        if pos == player.pos:
            return player.color()
        elif not self.los(player.pos, pos):
            if pos in self.discovered:
                return Color.DARKGRAY
            else:
                return Color.BLACK
        # XXX Mega Hack
        self.discovered.add(pos)
        if pos in self.items:
            return self.items[pos].color()
        elif feat == '#':
            return Color.RED
        elif feat == '.':
            return Color.LIGHTGRAY
        elif feat in "'+":
            return Color.WHITE
        elif feat in '<>':
            return Color.LIGHTCYAN
        elif feat.isdigit():  # switch
            bit = 1 << int(feat)
            attr = Color.BLUE if int(feat) < 3 else Color.MAGENTA
            if player.address & bit:
                attr |= curses.A_BOLD
            return attr

    def los(self, p1, p2):
        """Can (x1, y1) see (x2, y2)?"""
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > 3 or abs(dy) > 3:
            return False
        for l in sight_lines:
            if (dx, dy) not in l:
                continue
            for (px, py) in l:
                if (px, py) == (dx, dy):
                    return True
                if self[x1+px, y1+py] in solids:
                    break
        return False

def make_dungeon():
    # Parse level layouts
    descs = []
    for line in open('maps.txt'):
        try:
            int(line)
            descs.append('')
        except ValueError:
            descs[-1] += line

    # Pick all level layouts
    layouts = []
    while len(layouts) < 0x100:
        needed = 0x100 - len(layouts)
        layouts += random.sample(descs, min(len(descs), needed))

    dungeon = {i: Board(i, l) for i, l in enumerate(layouts)}
    return dungeon
