import curses

import Color
from Player import Player
from messages import messages
import memory

def init_color_pairs():
    """Initializes color pairs for curses."""
    # These numbers are used by Color.blue, etc.
    curses.init_pair(1, curses.COLOR_BLUE,    curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN,   curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN,    curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED,     curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_YELLOW,  curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE,   curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK,   curses.COLOR_BLACK)

def main(stdscr):
    """Starts the game."""
    curses.initscr()
    init_color_pairs()
    Color.initialize()

    player = Player()
    memory.write_memory(player, memory.addr_player_appearance, 41)
    for i, line in enumerate(messages):
        stdscr.addstr(i, 1, line[0])
        stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)
