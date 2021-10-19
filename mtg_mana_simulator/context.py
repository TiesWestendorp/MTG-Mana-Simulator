"""
Defines the Context class which is used to manage the state. AI decisions are based
solely on a given context, and playing a card modifies a context.
"""

from typing import Dict, Iterator, List, Optional
from random import sample
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.sequence import Sequence

class Context:
    """Snapshot of the state at a particular point in time"""

    def __init__(self, *,
            turn: int = 0,
            mana: int = 0,
            gold: int = 0,
            land: int = 0,
            hand: Optional[List[Card]] = None,
            deck: Optional[List[Card]] = None,
            battlefield: Optional[List[Card]] = None,
            graveyard: Optional[List[Card]] = None,
            exile: Optional[List[Card]] = None,
            command: Optional[List[Card]] = None) -> None:
        self.turn = turn
        self.mana = mana
        self.gold = gold
        self.land = land
        self.zones: Dict[str, List[Card]] = {
            "hand":        hand        if hand is not None        else [],
            "deck":        deck        if deck is not None        else [],
            "battlefield": battlefield if battlefield is not None else [],
            "graveyard":   graveyard   if graveyard is not None   else [],
            "exile":       exile       if exile is not None       else [],
            "command":     command     if command is not None     else []
        }

        # Starting sequences
        self.mana_sequence = Sequence.zero
        self.draw_sequence = Sequence.one
        self.gold_sequence = Sequence.zero
        self.land_sequence = Sequence.one

        # Caching behaviours
        self.cached_playable_cards: Optional[List[int]] = None
        self.cached_max_attainable_mana: Optional[int] = None

    def lands_in_hand(self) -> List[Card]:
        """List of all land cards in hand"""
        return [card for card in self.zones["hand"] if card.land]

    def nonlands_in_hand(self) -> List[Card]:
        """List of all nonland cards in hand"""
        return [card for card in self.zones["hand"] if not card.land]

    def remove_lands(self, number: int) -> None:
        """Randomly removes a number of lands from the deck"""
        if number > 0:
            indices = sample([k for k,card in enumerate(self.zones["deck"]) if card.land], number)
            indices.sort(reverse=True)
            for index in indices:
                self.zones["deck"].pop(index)

    def new_turn(self) -> None:
        """Does all bookkeeping involved with starting the next turn"""
        self.turn += 1
        self.draw_cards(self.draw_sequence[0])
        self.mana  = self.mana_sequence[0]
        self.gold += self.gold_sequence[0]
        self.land  = self.land_sequence[0]
        self.draw_sequence = self.draw_sequence.take(1)
        self.mana_sequence = self.mana_sequence.take(1)
        self.gold_sequence = self.gold_sequence.take(1)
        self.land_sequence = self.land_sequence.take(1)

    def draw_cards(self, number: int) -> None:
        """Draw a number of cards"""
        number = min(number, len(self.zones["deck"]))
        if number > 0:
            self.cached_max_attainable_mana = None
            self.cached_playable_cards = None
            for _ in range(number):
                self.zones["hand"].append(self.zones["deck"].pop())

    def discard_cards(self, indices: List[int]) -> None:
        """Discard specified cards"""
        if len(indices) != len(set(indices)) or\
           any(index >= len(self.zones["hand"]) for index in indices):
            raise ValueError
        indices.sort(reverse=True)
        for index in indices:
            self.zones["hand"].pop(index)

    def play_card(self, index: int) -> None:
        """Update the context by playing a given card"""
        if index not in self.playable_cards():
            raise ValueError

        self.cached_playable_cards = None
        card = self.zones["hand"].pop(index)

        self.remove_lands(card.lands_removed)
        cost = card.cost or 0
        self.land += card.land_sequence[0] - card.land
        self.gold += card.gold_sequence[0] - min([self.gold, max([0, cost-self.mana])])
        self.mana += card.mana_sequence[0] - min([self.mana, cost])
        self.draw_cards(card.draw_sequence[0])

        self.mana_sequence += card.mana_sequence.take(1)
        self.draw_sequence += card.draw_sequence.take(1)
        self.gold_sequence += card.gold_sequence.take(1)
        self.land_sequence += card.land_sequence.take(1)

    def playable_cards(self) -> List[int]:
        """Returns a list of indices of the cards that can currently be played"""
        if self.cached_playable_cards is None:
            playables = [k for k,card in enumerate(self.zones["hand"]) if card.is_playable(self)]
            self.cached_playable_cards = playables
        return self.cached_playable_cards

    def max_attainable_mana(self) -> int:
        """Maximum attainable mana based on public information (lands and net gain)"""
        if self.cached_max_attainable_mana is None:
            max_attainable_mana = self.mana + self.gold
            if self.land > 0:
                max_attainable_mana += max([0]+[card.netgain() for card in self.lands_in_hand()])
            for card in sorted(self.nonlands_in_hand(), key=lambda card: (card.cost or 0)):
                if card.cost is not None:
                    max_attainable_mana += max(0, card.netgain())
                    # Cards are traversed in cost order, so we stop early if we can't pay the cost
                    if card.cost > max_attainable_mana:
                        break
            self.cached_max_attainable_mana = max_attainable_mana
        return self.cached_max_attainable_mana
