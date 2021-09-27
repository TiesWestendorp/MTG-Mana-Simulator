from models.sequence import Sequence

class Card:
    untapped_land = None
    tapped_land = None
    cantrip = None
    filler = None

    def __init__(self, name="", land=False, cost=0, mana_sequence=None, draw_sequence=None, gold_sequence=None):
        self.name = name
        self.land = land
        self.cost = cost
        self.mana_sequence = mana_sequence if mana_sequence is not None else Sequence.zero
        self.draw_sequence = draw_sequence if draw_sequence is not None else Sequence.zero
        self.gold_sequence = gold_sequence if gold_sequence is not None else Sequence.zero

    @staticmethod
    def untapped_rock(cost, mana):
        return Card(cost=cost, mana_sequence=Sequence.repeat(mana))
    @staticmethod
    def tapped_rock(cost, mana):
        return Card(cost=cost, mana_sequence=Sequence.repeat(mana).prefixed_by([0]))
    @staticmethod
    def draw_spell(cost, cards):
        return Card(cost=cost, draw_sequence=Sequence.once(1))

Card.untapped_land = Card(land=True, mana_sequence=Sequence.one)
Card.tapped_land   = Card(land=True, mana_sequence=Sequence.one.prefixed_by([0]))
Card.cantrip       = Card.draw_spell(1, 1)
Card.filler        = Card(cost=float('inf'))
