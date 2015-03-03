import curses
from constants import *

def update_screen(stdscr):
    win_status = curses.newwin(WIN_STATUS_HEIGHT, WIN_STATUS_WIDTH,
                               WIN_STATUS_Y, WIN_STATUS_X)
    win_game = curses.newwin(WIN_GAME_HEIGHT, WIN_GAME_WIDTH,
                             WIN_GAME_Y, WIN_GAME_X)
    win_text = curses.newwin(WIN_TEXT_HEIGHT, WIN_TEXT_WIDTH,
                             WIN_TEXT_Y, WIN_TEXT_X)


