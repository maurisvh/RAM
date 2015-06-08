import random

def coinflip():
    return bool(random.randint(0, 1))

compass = [(-1, -1), ( 0, -1), (+1, -1),
           (-1,  0),           (+1,  0),
           (-1, +1), ( 0, +1), (+1, +1)]

orthogonal = compass[1::2]

move_keys = {
    '7': (-1, -1), '8': ( 0, -1), '9': (+1, -1),
    'y': (-1, -1), 'k': ( 0, -1), 'u': (+1, -1),
    '4': (-1,  0),                '6': (+1,  0),
    'h': (-1,  0),                'l': (+1,  0),
    '1': (-1, +1), '2': ( 0, +1), '3': (+1, +1),
    'b': (-1, +1), 'j': ( 0, +1), 'n': (+1, +1),
}

def nth(n):
    i = 0 if 10 <= n <= 19 else n % 10
    return str(n) + 'th st nd rd th th th th th th'.split()[i]

def pos2int(n):
    return n[0] + n[1] * 19
