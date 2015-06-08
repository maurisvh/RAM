import curses
from Board import Board
import Color
import Element
import Item
from constants import *
from messages import msg, messages
import memory
import random

# Screen dimensions.

# AAAAbbbbbbbb
# AAAAbbBBBBbb  A = status / ram window
# AAAAbbBBBBbb  B = game window (centered)
# AAAAbbBBBBbb  C = message window
# AAAAbbBBBBbb
# AAAAbbbbbbbb
# CCCCCCCCCCCC
# CCCCCCCCCCCC

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
WIN_STATUS_WIDTH = 40
WIN_TEXT_HEIGHT = 6

# Align everything else.
WIN_STATUS_X = 0
WIN_STATUS_Y = 0
WIN_TEXT_X = 0
WIN_TEXT_WIDTH = SCREEN_WIDTH
WIN_STATUS_HEIGHT = SCREEN_HEIGHT - WIN_TEXT_HEIGHT
WIN_TEXT_Y = WIN_STATUS_HEIGHT
WIN_GAME_BOX_X = WIN_STATUS_WIDTH
WIN_GAME_BOX_Y = WIN_STATUS_Y
WIN_GAME_BOX_WIDTH = SCREEN_WIDTH - WIN_STATUS_WIDTH
WIN_GAME_BOX_HEIGHT = WIN_STATUS_HEIGHT
WIN_GAME_Y = (WIN_GAME_BOX_HEIGHT - Board.HEIGHT) // 2
WIN_GAME_X = (WIN_GAME_BOX_WIDTH - Board.WIDTH) // 2

win_status = None
win_game = None
win_text = None

def update_status(player):
    caption_colour = Color.DARKGRAY
    value_colour = Color.LIGHTGRAY
    win_status.addstr(0, 0, '!', Color.BLACK)

    def ratio_color(r):
        if r > 0.8:
            return Color.LIGHTGRAY
        elif r > 0.6:
            return Color.GREEN
        elif r > 0.4:
            return Color.YELLOW
        elif r > 0.2:
            return Color.RED
        else:
            return Color.LIGHTRED

    def sign_color(x):
        if x > 0:
            return Color.GREEN
        elif x < 0:
            return Color.RED
        else:
            return Color.LIGHTGRAY

    def writes_value(caption, value):
        def show(y, x):
            win_status.addstr(y, x, caption, caption_colour)
            win_status.addstr(str(value), value_colour)
        return show

    def writes_ratio(caption, value, maximum):
        def show(y, x):
            win_status.addstr(y, x, caption, caption_colour)
            rc = ratio_color(value / maximum)
            win_status.addstr(str(value), rc)
            win_status.addstr('/{0}'.format(maximum), caption_colour)
        return show

    def show_name(y, x):
        win_status.addstr(y, x, player.char() + ' ', player.color())
        win_status.addstr(player.name_str, Color.LIGHTCYAN)

    show_hp = writes_ratio('HP: ',player.hp, player.maxhp)
    show_tp = writes_ratio('TP: ',player.tp, player.maxtp)
    show_dlvl = writes_value('Depth: ', player.dlvl)
    show_xl   = writes_value('Exp: ',   player.xl)
    show_def  = writes_value('Def: ',  player.defense)

    def show_apt(element):
        def show(y, x):
            caption = Element.name(element).capitalize() + ': '
            win_status.addstr(y, x, caption, caption_colour)
            apt = player.aptitude[element]
            win_status.addstr(str(apt), sign_color(apt))
        return show

    m = WIN_STATUS_WIDTH // 2 - 1
    hud = [
        (show_name, show_xl),
        (show_hp,   show_tp),
        (show_def,  show_dlvl),
        (show_apt(Element.METAL), show_apt(Element.ACID)),
        (show_apt(Element.FIRE),  show_apt(Element.ELEC)),
    ]

    for y, row in enumerate(hud, 1):
        fL, fR = row
        if fL: fL(y, 2)
        if fR: fR(y, 2 + m)

    if player.show_ram:
        ram_y = y + 3
        ram_width = 8 * 4 + 3
        ram_x = (WIN_STATUS_WIDTH - ram_width) // 2
        for i in range(0x40):
            y = ram_y + i // 8
            x = ram_x + (i % 8 + 1) * 4 + 1
            try:
                byte = memory.read_memory(player, i)
            except NotImplementedError:
                byte = random.randint(0, 255)
            attr = Color.CYAN
            if i == player.address:
                attr = Color.LIGHTGRAY | curses.A_REVERSE
            win_status.addstr(y, x, "{:02X}".format(byte), attr)
        for i in range(8):
            attr = Color.BLUE
            if player.address & 0b000111 == i:
                attr |= curses.A_REVERSE
            win_status.addstr(ram_y - 1, ram_x + (i + 1) * 4,
                              "{:03b}".format(i), attr)
            attr = Color.MAGENTA
            if player.address & 0b111000 == i << 3:
                attr |= curses.A_REVERSE
            win_status.addstr(ram_y + i, ram_x,
                              "{:03b}".format(i), attr)
        win_status.move(ram_y + 8, ram_x)
        win_status.clrtoeol()
        win_status.addstr(memory.address_name(player.address), Color.LIGHTBLUE)
    else:
        item_y = y + 2
        for i in range(8):
            y = item_y + i
            item = player.inventory[i]
            line = item.compressed_name() if item.kind else 'nothing'
            num_color = Color.LIGHTBLUE if item.kind else Color.DARKGRAY
            line_color = item.color() if item.kind else Color.DARKGRAY
            win_status.addstr(y, 2, '{0} '.format(i + 1), num_color)
            win_status.addstr(line, line_color)

    win_status.refresh()

def update_map(player, dungeon):
    board = dungeon[player.dlvl]
    for y in range(Board.HEIGHT):
        for x in range(Board.WIDTH):
            # XXX TERA-HACK: this has side effects that char_at relies on.
            # Otherwise I'd have to call los() twice.
            col = board.color_at(player, (x, y))
            win_game.insstr(y, x, board.char_at(player, (x, y)), col)
    win_game.refresh()

def prompt(s, col=None):
    msg(s, col)
    view.update_text()

def update_text():
    for m, col in messages:
        win_text.scroll(1)
        win_text.insstr(WIN_TEXT_HEIGHT - 1, 0, m, col)
    del messages[:]
    win_text.refresh()

def init_screen(stdscr):
    global win_status, win_game, win_text
    win_status = curses.newwin(WIN_STATUS_HEIGHT, WIN_STATUS_WIDTH,
                               WIN_STATUS_Y, WIN_STATUS_X)
    win_game_box = curses.newwin(WIN_GAME_BOX_HEIGHT, WIN_GAME_BOX_WIDTH,
                                 WIN_GAME_BOX_Y, WIN_GAME_BOX_X)
    win_game = win_game_box.derwin(Board.HEIGHT, Board.WIDTH,
                                   WIN_GAME_Y, WIN_GAME_X)
    win_text = curses.newwin(WIN_TEXT_HEIGHT, WIN_TEXT_WIDTH,
                             WIN_TEXT_Y, WIN_TEXT_X)
    win_text.scrollok(True)

    for y in range(WIN_GAME_BOX_HEIGHT):
        for x in range(WIN_GAME_BOX_WIDTH):
            win_game_box.insstr(y, x, '#', Color.DARKGRAY)
    win_game_box.refresh()
    win_game.clear()
    win_game.refresh()

def update_screen(stdscr, player, dungeon):
    update_status(player)
    update_text()
    update_map(player, dungeon)
    stdscr.move(player.pos[1] + WIN_GAME_Y, player.pos[0] + WIN_GAME_X + WIN_GAME_BOX_X)
