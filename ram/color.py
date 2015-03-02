import curses

class Color:
    "Defines curses attributes for each possible foreground color."

    # We need to call curses.initscr before we can initialize these.
    @staticmethod
    def initialize():
        Color.blue         = curses.color_pair(1)
        Color.green        = curses.color_pair(2)
        Color.cyan         = curses.color_pair(3)
        Color.red          = curses.color_pair(4)
        Color.magenta      = curses.color_pair(5)
        Color.brown        = curses.color_pair(6)
        Color.lightgray    = curses.color_pair(7)
        Color.darkgray     = curses.color_pair(8) | curses.A_BOLD
        Color.lightblue    = curses.color_pair(1) | curses.A_BOLD
        Color.lightgreen   = curses.color_pair(2) | curses.A_BOLD
        Color.lightcyan    = curses.color_pair(3) | curses.A_BOLD
        Color.lightred     = curses.color_pair(4) | curses.A_BOLD
        Color.lightmagenta = curses.color_pair(5) | curses.A_BOLD
        Color.yellow       = curses.color_pair(6) | curses.A_BOLD
        Color.white        = curses.color_pair(7) | curses.A_BOLD
