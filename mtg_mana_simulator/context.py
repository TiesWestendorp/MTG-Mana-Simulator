"""
Defines the Context class which is used to manage the state. AI decisions are based
solely on a given context, and playing a card modifies a context.
"""

from typing import Dict, Iterator, List, Optional
from random import sample
from mtg_mana_simulator.card import Card

class Context:
    """Snapshot of the state at a particular point in time"""

    def __init__(self, *,
            turn: int = 0,
            mana: int = 0,
            gold: int = 0,
            land_for_turn: bool = False,
            hand: Optional[List[Card]] = None,
            deck: Optional[List[Card]] = None,
            battlefield: Optional[List[Card]] = None,
            graveyard: Optional[List[Card]] = None,
            exile: Optional[List[Card]] = None,
            command: Optional[List[Card]] = None) -> None:
        self.turn = turn
        self.mana = mana
        self.gold = gold
        self.land_for_turn = land_for_turn
        self.zones: Dict[str, List[Card]] = {
            "hand":        hand        if hand is not None        else [],
            "deck":        deck        if deck is not None        else [],
            "battlefield": battlefield if battlefield is not None else [],
            "graveyard":   graveyard   if graveyard is not None   else [],
            "exile":       exile       if exile is not None       else [],
            "command":     command     if command is not None     else []
        }

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

    def draw_cards(self, number: int) -> None:
        """Draw a number of cards"""
        if number > 0:
            self.cached_max_attainable_mana = None
            self.cached_playable_cards = None
            for _ in range(number):
                self.zones["hand"].append(self.zones["deck"].pop())

    def play_card(self, card: Card) -> Dict[str, Iterator[int]]:
        """Update the context by playing a given card"""
        self.cached_playable_cards = None
        generators = {
            'mana': card.mana_sequence.generator(),
            'draw': card.draw_sequence.generator(),
            'gold': card.gold_sequence.generator()
        }
        self.remove_lands(card.lands_removed)
        self.land_for_turn = self.land_for_turn or card.land
        self.gold += generators['gold'].__next__() - min([self.gold, max([0, card.cost-self.mana])])
        self.mana += generators['mana'].__next__() - min([self.mana, card.cost])
        self.draw_cards(generators['draw'].__next__())
        return generators

    def playable_cards(self) -> List[int]:
        """Returns a list of indices of the cards that can currently be played"""
        if self.cached_playable_cards is None:
            mana = self.mana+self.gold
            condition = lambda card: card.cost <= mana and not (card.land and self.land_for_turn)
            playable_cards = [k for k,card in enumerate(self.zones["hand"]) if condition(card)]
            self.cached_playable_cards = playable_cards
        return self.cached_playable_cards

    def max_attainable_mana(self) -> int:
        """Maximum attainable mana based on public information (lands and net gain)"""
        if self.cached_max_attainable_mana is None:
            max_attainable_mana = self.mana + self.gold
            if not self.land_for_turn:
                max_attainable_mana += max([0]+[card.netgain() for card in self.lands_in_hand()])
            for card in sorted(self.nonlands_in_hand(), key=lambda card: card.cost):
                max_attainable_mana += max(0, card.netgain())
                # Cards are traversed in cost order, so we can stop early if we can't pay the cost
                if card.cost > max_attainable_mana:
                    break
            self.cached_max_attainable_mana = max_attainable_mana
        return self.cached_max_attainable_mana
