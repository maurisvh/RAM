import Color
import Element

import random

class Item:
    color = Color.LIGHTMAGENTA; char = '?'
    base_name = 'dummy'
    def __init__(self, enchanted, equipped, cursed):
        self.enchanted = enchanted
        self.equipped = equipped
        self.cursed = cursed
    @property
    def name(self):
        s = base_name
        if self.enchanted:
            s = 'enchanted ' + s
        if self.cursed:
            s = 'cursed ' + s
        return s

    @property
    def a_name(self):
        s = self.name
        if s[0].lower() in 'aeiou':
            return 'an ' + s
        else:
            return 'a ' + s

class Equippable(Item):
    @property
    def name(self):
        s = Item.name(self)
        if self.equipped:
            s += ' (in use)'
        return s

class Weapon(Equippable):
    color = Color.LIGHTMAGENTA; char = '/'
    base_dmg = 0
    element = None

class RangedWeapon(Weapon):
    pass

class Armor(Equippable):
    color = Color.LIGHTMAGENTA; char = '['
    defense = 0
    aptitude = {Element.METAL: 0, Element.ACID: 0,
                Element.FIRE: 0, Element.ELEC: 0}

class Necklace(Armor):
    char = '"'
    aptitude = {Element.METAL: 0, Element.ACID: 0,
                Element.FIRE: 0, Element.ELEC: 0}

class Consumable(Item):
    char = '*'

class Device(Consumable):
    char = '$'

class Artifact(Item):
    char = '&'

######################################################################

class Crowbar(Weapon):
    base_name = 'crowbar'
    color = Color.DARKGRAY
    base_dmg = 3
    element = Element.METAL

class VolcanicShard(Weapon):
    base_name = 'volcanic shard'
    color = Color.LIGHTRED
    base_dmg = 5
    element = Element.FIRE

class Taser(Weapon):
    base_name = 'taser'
    color = Color.LIGHTBLUE
    base_dmg = 6
    element = Element.ELEC

class JellyGun(RangedWeapon):
    base_name = 'jelly gun'
    color = Color.LIGHTGREEN
    base_dmg = 3
    element = Element.ACID

class ThickSweater(Armor):
    base_name = 'thick sweater'
    color = Color.MAGENTA
    defense = 3
    aptitude = {Element.METAL: 0, Element.ACID: 0,
                Element.FIRE: 2, Element.ELEC: -2}

class BallisticVest(Armor):
    base_name = 'ballistic vest'
    color = Color.CYAN
    defense = 5
    aptitude = {Element.METAL: 2, Element.ACID: -2,
                Element.FIRE: 0, Element.ELEC: 0}

class DragonScaleMail(Armor):
    base_name = 'dragon scale mail'
    color = Color.GREEN
    defense = 7
    aptitude = {Element.METAL: 0, Element.ACID: 2,
                Element.FIRE: -2, Element.ELEC: 0}

class TitaniumNecklace(Necklace):
    base_name = 'titanium necklace'
    color = Color.LIGHTGRAY
    aptitude = {Element.METAL: 3, Element.ACID: -1,
                Element.FIRE: -1, Element.ELEC: -1}

class RustyNecklace(Necklace):
    base_name = 'rusty necklace'
    color = Color.BROWN
    aptitude = {Element.METAL: -1, Element.ACID: 3,
                Element.FIRE: -1, Element.ELEC: -1}

class CrimsonNecklace(Necklace):
    base_name = 'crimson necklace'
    color = Color.RED
    aptitude = {Element.METAL: -1, Element.ACID: -1,
                Element.FIRE: 3, Element.ELEC: -1}

class GlowingNecklace(Necklace):
    base_name = 'glowing necklace'
    color = Color.YELLOW
    aptitude = {Element.METAL: -1, Element.ACID: -1,
                Element.FIRE: -1, Element.ELEC: 3}

class UnholyNecklace(Necklace):
    base_name = 'unholy necklace'
    color = Color.DARKGRAY
    aptitude = {Element.METAL: -3, Element.ACID: -3,
                Element.FIRE:  -3, Element.ELEC: -3}

class WandOfDeath(Consumable):
    base_name = 'wand of death'
    color = Color.BLUE
    char = '/'

class Manual(Consumable):
    base_name = 'manual'
    color = Color.LIGHTBLUE
    char = ':'

class Guidebook(Consumable):
    base_name = 'guidebook'
    color = Color.LIGHTMAGENTA
    char = ':'

class Corruptor(Device):
    base_name = 'corruptor'
    color = Color.RED

class Offsetter(Device):
    base_name = 'offsetter'
    color = Color.YELLOW

class Copier(Device):
    base_name = 'copier'
    color = Color.LIGHTBLUE

class Palantir(Artifact):
    base_name = 'palantir'
    @property
    def color(self):
        return random.choice([Color.BLUE, Color.LIGHTBLUE,
                              Color.CYAN, Color.LIGHTCYAN])

class GoldenCandle(Artifact):
    base_name = 'golden candle'
    @property
    def color(self):
        return random.choice([Color.WHITE, Color.YELLOW, Color.LIGHTRED])
