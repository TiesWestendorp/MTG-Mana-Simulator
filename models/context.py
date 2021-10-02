"""
Defines the Context class which is used to manage the state. AI decisions are based
solely on a given context, and playing a card modifies a context.
"""

from typing import List
from random import sample

class Context:
    """Snapshot of the state at a particular point in time"""

    def __init__(self, *, turn=None, hand=None, mana=None, gold=None, land_for_turn=None, remaining=None):
        self.turn = turn
        self.hand = hand
        self.mana = mana
        self.gold = gold
        self.land_for_turn = land_for_turn
        self.remaining = remaining
        self.cached_max_attainable_mana = None

    def lands_in_hand(self):
        """List of all land cards in hand"""
        return [card for card in self.hand if card.land]

    def nonlands_in_hand(self):
        """List of all nonland cards in hand"""
        return [card for card in self.hand if not card.land]

    def remove_lands(self, number):
        """Randomly removes a number of lands from the deck"""
        if number > 0:
            land_indices = sample([k for k,card in enumerate(self.remaining) if card.land], number)
            for land_index in land_indices.sort(reverse=True):
                self.remaining.pop(land_index)

    def draw_cards(self, number):
        """Draw a number of cards"""
        if number > 0:
            self.cached_max_attainable_mana = None
        for _ in range(number):
            self.hand.append(self.remaining.pop())

    def play_card(self, card):
        """Update the context by playing a given card"""
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
        mana = self.mana+self.gold
        condition = lambda card: card.cost <= mana and not (card.land and self.land_for_turn)
        return [k for k,card in enumerate(self.hand) if condition(card)]

    def max_attainable_mana(self) -> int:
        """Maximum attainable mana based on public information (lands and net gain)"""
        if self.cached_max_attainable_mana is not None:
            return self.cached_max_attainable_mana
        max_attainable_mana = self.mana + self.gold
        if not self.land_for_turn:
            max_attainable_mana += max([0]+[card.netgain() for card in self.lands_in_hand()])
        for card in sorted(self.nonlands_in_hand(), key=lambda card: card.cost):
            max_attainable_mana += max([0, card.netgain()])
            # Cards are traversed in cost order, so we can stop early if we can't pay the cost
            if card.cost > max_attainable_mana:
                break
        self.cached_max_attainable_mana = max_attainable_mana
        return max_attainable_mana
