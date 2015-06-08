import curses
import sys

import Color
from Board import make_dungeon
from Player import Player
from messages import messages, msg
from util import move_keys
import memory
import view

def perform(player, dungeon, c):
    """Return true if a successful move was made."""
    level = dungeon[player.dlvl]
    if chr(c) in move_keys:
        dx, dy = move_keys[chr(c)]
        return player.step(level, dx, dy)
    elif chr(c) == 'Q':
        msg('Really quit?')
        sys.exit()
    elif chr(c) in '<>':
        feat = level[player.pos]
        if feat not in '<>':
            msg("You don't see any stairs here.")
            return False
        d = player.dlvl_delta
        if feat == '<':
            d *= -1
        goal = (player.dlvl + d) & 0xFF
        player.dlvl = goal
        if feat == '<':
            msg('You take the stairs up to level {0}.'.format(goal))
            player.pos = dungeon[goal].stairs_down
        else:
            msg('You take the stairs down to level {0}.'.format(goal))
            player.pos = dungeon[goal].stairs_up
        return True
    elif chr(c) == '(':
        player.address = (player.address - 1) & 0x3F
        return False
    elif chr(c) == ')':
        player.address = (player.address + 1) & 0x3F
        return False
    elif chr(c) == '+':
        v = memory.read_memory(player, player.address)
        memory.write_memory(player, player.address, (v + 1) & 0xFF)
    elif chr(c) == '-':
        v = memory.read_memory(player, player.address)
        memory.write_memory(player, player.address, (v - 1) & 0xFF)

def main(stdscr):
    """Starts the game."""
    curses.initscr()
    curses.curs_set(1) # invisible
    Color.initialize()

    player = Player()
    dungeon = make_dungeon()
    player.pos = dungeon[0].stairs_up

    view.init_screen(stdscr)
    while True:
        view.update_screen(stdscr, player, dungeon)
        perform(player, dungeon, stdscr.getch())

if __name__ == '__main__':
    curses.wrapper(main)
