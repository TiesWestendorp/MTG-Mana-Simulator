# Some examples:
# dark_ritual = Card("Dark Ritual", False, 1, [3], [])
# bounty_of_the_luxa = Card("Bounty of the Luxa", False, 4, [0], [0, 3])

# TODO: implement card draw
# TODO: implement land search
from models.sequence import Sequence

class Card:
    untapped_land = None
    tapped_land = None
    cantrip = None
    filler = None

    def __init__(self, name, land, cost, mana_sequence=None, draw_sequence=None, gold_sequence=None):
        self.name = name
        self.land = land
        self.cost = cost
        self.mana_sequence = mana_sequence if mana_sequence is not None else Sequence.zero
        self.draw_sequence = draw_sequence if draw_sequence is not None else Sequence.zero
        self.gold_sequence = gold_sequence if gold_sequence is not None else Sequence.zero

    @staticmethod
    def untapped_rock(cost, mana):
        return Card("Untapped rock", False, cost, Sequence([], [mana]))
    @staticmethod
    def tapped_rock(cost, mana):
        return Card("Tapped rock", False, cost, Sequence([0], [mana]))

Card.untapped_land = Card("Untapped land", True,  0, mana_sequence=Sequence.one)
Card.tapped_land   = Card("Tapped land",   True,  0, mana_sequence=Sequence.one.prefixed_by([0]))
Card.cantrip       = Card("Cantrip",       False, 1, draw_sequence=Sequence.once(1))
Card.filler        = Card("Filler",        False, float('inf'))
