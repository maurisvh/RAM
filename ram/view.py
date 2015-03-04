import curses
from constants import *

# Screen dimensions.

# AAAABBBBBBBB
# AAAABBBBBBBB  A = status / ram window
# AAAABBBBBBBB  B = game window (centered)
# AAAABBBBBBBB  C = message window
# AAAABBBBBBBB
# AAAABBBBBBBB
# CCCCCCCCCCCC
# CCCCCCCCCCCC

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
WIN_STATUS_WIDTH = 25
WIN_TEXT_HEIGHT = 6

# Align everything else.
WIN_STATUS_X = 0
WIN_STATUS_Y = 0
WIN_TEXT_X = 0
WIN_TEXT_WIDTH = SCREEN_WIDTH
WIN_STATUS_HEIGHT = SCREEN_HEIGHT - WIN_TEXT_HEIGHT
WIN_TEXT_Y = WIN_STATUS_HEIGHT
WIN_GAME_X = WIN_STATUS_WIDTH
WIN_GAME_Y = WIN_STATUS_Y
WIN_GAME_WIDTH = SCREEN_WIDTH - WIN_STATUS_WIDTH
WIN_GAME_HEIGHT = WIN_STATUS_HEIGHT

def update_screen(stdscr):
    win_status = curses.newwin(WIN_STATUS_HEIGHT, WIN_STATUS_WIDTH,
                               WIN_STATUS_Y, WIN_STATUS_X)
    win_game = curses.newwin(WIN_GAME_HEIGHT, WIN_GAME_WIDTH,
                             WIN_GAME_Y, WIN_GAME_X)
    win_text = curses.newwin(WIN_TEXT_HEIGHT, WIN_TEXT_WIDTH,
                             WIN_TEXT_Y, WIN_TEXT_X)

    HL, VL = curses.ACS_HLINE, curses.ACS_VLINE
    UL, UR = curses.ACS_ULCORNER, curses.ACS_URCORNER
    LL, LR = curses.ACS_LLCORNER, curses.ACS_LRCORNER
    SP = ord(' ')

    win_status.border(VL, VL, HL, HL, UL, UR, curses.ACS_LTEE)
    win_status.refresh()
    win_game.border(VL, VL, HL, HL, UL, UR, LL, curses.ACS_RTEE)
    win_game.refresh()
    win_text.border(VL, VL, SP, HL, VL, VL)
    win_text.refresh()
    win_text.getch()
