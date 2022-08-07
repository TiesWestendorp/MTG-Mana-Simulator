"""
Defines the Card class which models a Magic: the Gathering card's behaviour.
Currently, the following actions are supported: to gain mana instanteneously as
well as according to a pattern every turn, to create gold/create gold/draw Cards
immediately as well as according to a pattern every turn. Additionally, a card
has a mana cost and can be a land or nonland.
"""

from typing import Callable, List, Optional, TYPE_CHECKING
from mtg_mana_simulator.sequence import Sequence
if TYPE_CHECKING:
    from mtg_mana_simulator.context import Context

Transforms = List[Callable[["Context"], None]]

class Card:
    """Simplified model of a Magic card"""

    untapped_land : "Card"
    tapped_land : "Card"
    cantrip : "Card"
    filler : "Card"

    def __init__(self, name: str = "", *,
            land: bool = False,
            cost: Optional[int] = 0,
            mana_sequence: Optional[Sequence] = None,
            draw_sequence: Optional[Sequence] = None,
            gold_sequence: Optional[Sequence] = None,
            land_sequence: Optional[Sequence] = None,
            transform: Optional[Transforms] = None) -> None:
        self.name = name
        self.land = land
        self.cost = cost
        self.mana_sequence: Sequence = mana_sequence if mana_sequence is not None else Sequence.zero
        self.draw_sequence: Sequence = draw_sequence if draw_sequence is not None else Sequence.zero
        self.gold_sequence: Sequence = gold_sequence if gold_sequence is not None else Sequence.zero
        self.land_sequence: Sequence = land_sequence if land_sequence is not None else Sequence.zero
        self.transform: Transforms = transform if transform is not None else []

    def approximate_net_mana_sequence(self) -> Sequence:
        """ (assuming gold is spent immediately)"""
        return self.mana_sequence + self.gold_sequence + Sequence.once(-(self.cost or 0))

    def netgain(self) -> int:
        """The immediate return in mana upon playing this card"""
        return self.mana_sequence[0] + self.gold_sequence[0] - (self.cost or 0)

    def is_ramp(self) -> bool:
        """Whether this card produces mana at some point"""
        return self.mana_sequence != Sequence.zero or self.gold_sequence != Sequence.zero

    def is_draw(self) -> bool:
        """Whether this card draws cards at some point"""
        return self.draw_sequence != Sequence.zero

    def is_playable(self, context: "Context") -> bool:
        """Whether this card is playable given a context"""
        return (self.cost is not None and self.cost <= context.mana + context.gold) or\
               (self.land and context.land > 0)

    @staticmethod
    def untapped_rock(cost: int, mana: int) -> "Card":
        """Card with given cost and given mana gain"""
        return Card(cost=cost, mana_sequence=Sequence.repeat(mana))

    @staticmethod
    def tapped_rock(cost: int, mana: int) -> "Card":
        """Card with given cost and given mana gain starting next turn"""
        return Card(cost=cost, mana_sequence=Sequence.repeat(mana).prefixed_by([0]))

    @staticmethod
    def draw_spell(cost: int, cards: int) -> "Card":
        """Card with given cost that immediately draws given amount of cards"""
        return Card(cost=cost, draw_sequence=Sequence.once(cards))

Card.basic_land    = Card("Basic land",    cost=None, land=True, mana_sequence=Sequence.one)
Card.untapped_land = Card("Untapped land", cost=None, land=True, mana_sequence=Sequence.one)
Card.tapped_land   = Card("Tapped land",   cost=None, land=True,
                        mana_sequence=Sequence.one.prefixed_by([0]))
Card.cantrip       = Card.draw_spell(1, 1)
Card.filler        = Card("Filler", cost=20000)
