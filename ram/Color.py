import curses

# We need to call curses.initscr before we can initialize these.
def initialize():
    curses.init_pair(1, curses.COLOR_BLUE,    curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN,   curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN,    curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED,     curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_YELLOW,  curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE,   curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK,   curses.COLOR_BLACK)

def define_colors(stdscr):
    global BLACK, BLUE, GREEN, CYAN, RED, MAGENTA, BROWN, LIGHTGRAY
    global DARKGRAY, LIGHTBLUE, LIGHTGREEN, LIGHTCYAN, LIGHTRED
    global LIGHTMAGENTA, YELLOW, WHITE

    BLACK        = curses.color_pair(8)
    BLUE         = curses.color_pair(1)
    GREEN        = curses.color_pair(2)
    CYAN         = curses.color_pair(3)
    RED          = curses.color_pair(4)
    MAGENTA      = curses.color_pair(5)
    BROWN        = curses.color_pair(6)
    LIGHTGRAY    = curses.color_pair(7)
    DARKGRAY     = curses.color_pair(8) | curses.A_BOLD
    LIGHTBLUE    = curses.color_pair(1) | curses.A_BOLD
    LIGHTGREEN   = curses.color_pair(2) | curses.A_BOLD
    LIGHTCYAN    = curses.color_pair(3) | curses.A_BOLD
    LIGHTRED     = curses.color_pair(4) | curses.A_BOLD
    LIGHTMAGENTA = curses.color_pair(5) | curses.A_BOLD
    YELLOW       = curses.color_pair(6) | curses.A_BOLD
    WHITE        = curses.color_pair(7) | curses.A_BOLD

curses.wrapper(define_colors)
