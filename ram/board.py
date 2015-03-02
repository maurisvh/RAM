from constants import *
from util import coinflip

import random

# Tiles are:
#  .  floor
#  +  closed door
# (\  open door)
#  #  wall
#  <  stairs up
#  >  stairs down

class Board:
    WIDTH = 19
    HEIGHT = 13

    def __init__(self, depth, des):
        self.tiles = []
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

        # This is sort of a hack?
        for c in 'ABCDEFGHIJKLMNOP':
            des = des.replace(c, random.choice('.#'))
        for pos, c in enumerate(des):
            # Don't always generate doors.
            if c == '+' and random.random() < 0.1:
                c = '.'
            if c == '<':
                stairs_positions.add(pos)
                c = '.'
            if c == '.':
                open_positions.add(pos)
            self.tiles.append(c)

        assert len(stairs_positions) >= 2
        assert len(open_positions) >= 6

        up_pos, down_pos = random.sample(stairs_positions, 2)
        self.tiles[up_pos] = '<'
        self.tiles[down_pos] = '>'
        self.monsters = [None for n in range(MAX_MONSTERS)]

        # Map from position to item.
        self.items = {}

        # TODO: generate items, linking

    def __getitem__(self, v):
        """Index the board, using a position as an integer (indexing in row
        order) or a tuple (x, y)."""
        if isinstance(v, tuple):
            x, y = v
            return self[y * Board.WIDTH + x]
        else:
            return self.tiles[v]

    def __str__(self):
        w = Board.WIDTH
        h = Board.HEIGHT
        return '\n'.join(''.join(self.tiles[i*w:(i+1)*w]) for i in range(h))

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
