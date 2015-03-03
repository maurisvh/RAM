import Color

messages = []

def msg(s, col=None):
    if col is None:
        col = Color.LIGHTGRAY
    messages.append((s, col))
