from color import Color

messages = []

def msg(s, col=Color.lightgray):
    messages.append((s, col))
