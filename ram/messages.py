from color import Color

messages = []

def msg(s, col=None):
    if col is None:
        col = Color.lightgray
    messages.append((s, col))
