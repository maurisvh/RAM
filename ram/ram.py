import curses

import Color
from Board import make_dungeon
from Player import Player
from messages import messages
import memory
import view

def main(stdscr):
    """Starts the game."""
    curses.initscr()
    curses.curs_set(0) # invisible
    Color.initialize()

    player = Player()
    dungeon = make_dungeon()
    player.pos = dungeon[0].stairs_up

    view.update_screen(stdscr, player, dungeon)

if __name__ == '__main__':
    curses.wrapper(main)
