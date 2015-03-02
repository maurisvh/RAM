import curses

class Color:
    "Defines curses attributes for each possible foreground color."
    blue         = curses.color_pair(1)
    green        = curses.color_pair(2)
    cyan         = curses.color_pair(3)
    red          = curses.color_pair(4)
    magenta      = curses.color_pair(5)
    brown        = curses.color_pair(6)
    lightgray    = curses.color_pair(7)
    darkgray     = curses.color_pair(8) | curses.A_BOLD
    lightblue    = curses.color_pair(1) | curses.A_BOLD
    lightgreen   = curses.color_pair(2) | curses.A_BOLD
    lightcyan    = curses.color_pair(3) | curses.A_BOLD
    lightred     = curses.color_pair(4) | curses.A_BOLD
    lightmagenta = curses.color_pair(5) | curses.A_BOLD
    yellow       = curses.color_pair(6) | curses.A_BOLD
    white        = curses.color_pair(7) | curses.A_BOLD
