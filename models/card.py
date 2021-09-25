# Some examples:
# dark_ritual = Card("Dark Ritual", False, 1, [3], [])
# bounty_of_the_luxa = Card("Bounty of the Luxa", False, 4, [], [0, 3])

# TODO: implement card draw
# TODO: implement land search
class Card:
    untapped_land = None
    tapped_land = None
    filler = None

    def __init__(self, name, land, cost, mana_prefix, mana_repeat):
        self.name = name
        self.land = land
        self.cost = cost
        self.mana_prefix = mana_prefix
        self.mana_repeat = mana_repeat
        if len(mana_repeat) == 0:
            self.mana_repeat = [0]
    def mana_generator(self):
        for mana in self.mana_prefix:
            yield mana
        while True:
            for mana in self.mana_repeat:
                yield mana

    @staticmethod
    def untapped_rock(cost, mana):
        return Card("Untapped rock", False, cost, [], [mana])

    @staticmethod
    def tapped_rock(cost, mana):
        return Card("Tapped rock", False, cost, [0], [mana])

Card.untapped_land = Card("Untapped land", True, 0, [],  [1])
Card.tapped_land   = Card("Tapped land",   True, 0, [0], [1])
Card.filler = Card("Filler", False, float('inf'), [], [])
