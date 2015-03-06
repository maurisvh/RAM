METAL = 'metal'
ACID = 'acid'
FIRE = 'fire'
ELEC = 'elec'

def name(element, verbose=False):
    if element == METAL:
        return 'metal'
    elif element == ACID:
        return 'acid'
    elif element == FIRE:
        return 'fire'
    elif element == ELEC:
        return 'electricity' if verbose else 'elec'
    else:
        raise ValueError('expected Element')
