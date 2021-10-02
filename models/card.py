from typing import Optional
from models.sequence import Sequence

class Card:
    """Simplified model of a Magic card"""

    untapped_land = None
    tapped_land = None
    cantrip = None
    filler = None

    def __init__(self, name: str = "", land: bool = False, cost: int = 0, mana_sequence: Optional[Sequence] = None, draw_sequence: Optional[Sequence] = None, gold_sequence: Optional[Sequence] = None, lands_removed: int = 0):
        self.name = name
        self.land = land
        self.cost = cost
        self.mana_sequence = mana_sequence if mana_sequence is not None else Sequence.zero
        self.draw_sequence = draw_sequence if draw_sequence is not None else Sequence.zero
        self.gold_sequence = gold_sequence if gold_sequence is not None else Sequence.zero
        self.lands_removed = lands_removed

    def approximate_net_mana_sequence(self):
        return self.mana_sequence + self.gold_sequence + Sequence.once(-self.cost)
    def netgain(self):
        return self.mana_sequence.finite_prefix(1)[0] + self.gold_sequence.finite_prefix(1)[0] - self.cost

    def is_ramp(self):
        return self.mana_sequence != Sequence.zero or self.gold_sequence != Sequence.zero
    def is_draw(self):
        return self.draw_sequence != Sequence.zero

    @staticmethod
    def untapped_rock(cost: int, mana: int):
        return Card(cost=cost, mana_sequence=Sequence.repeat(mana))
    @staticmethod
    def tapped_rock(cost: int, mana: int):
        return Card(cost=cost, mana_sequence=Sequence.repeat(mana).prefixed_by([0]))
    @staticmethod
    def draw_spell(cost: int, cards: int):
        return Card(cost=cost, draw_sequence=Sequence.once(1))

Card.untapped_land = Card("Untapped land", land=True, mana_sequence=Sequence.one)
Card.tapped_land   = Card("Tapped land", land=True, mana_sequence=Sequence.one.prefixed_by([0]))
Card.cantrip       = Card.draw_spell(1, 1)
Card.filler        = Card(cost=float('inf'))
