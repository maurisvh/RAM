import curses

import Color
from Player import Player
from messages import messages
import memory
import view

def main(stdscr):
    """Starts the game."""
    curses.initscr()
    Color.initialize()

    player = Player()
    # memory.write_memory(player, memory.addr_player_appearance, 41)
    # memory.write_memory(player, memory.addr_player_appearance, 41+64)
    # for i, line in enumerate(messages):
    #     stdscr.addstr(i, 0, line[0])
    # stdscr.addstr(9, 9, player.char, player.color)
    view.update_screen(stdscr)

if __name__ == '__main__':
    curses.wrapper(main)
