"""
Defines the AI class which is the decision agent that decides whether to mulligan
or not, and which cards should be played given a certain 'context'.
"""

from typing import Callable, Iterator, List, Optional
from random import choice, shuffle
from models.card import Card
from models.context import Context
from models.sequence import Sequence

Mulligan = Callable[[Context, int], Optional[List[int]]]
Choose   = Callable[[Context],      Optional[int]]

class AI:
    """
    Decision agent that implements mulligan and card playing algorithms
    """

    dud : "AI"
    naive : "AI"
    less_naive : "AI"

    def __init__(self, *,
            mulligan: Optional[Mulligan] = None,
            choose: Optional[Choose] = None) -> None:
        self.mulligan = mulligan if mulligan is not None else (lambda _,__: list(range(7)))
        self.choose   = choose   if choose   is not None else (lambda _: None)

    def execute_mulligan(self, deck) -> Context:
        """
        Keep applying chosen mulligan strategy until a valid choice is made, or the hand is empty
        """
        for keepable_cards in reversed(range(1,8)):
            context = Context(hand=deck[:7],
                              remaining=deck[7:])
            card_indices = self.mulligan(context, keepable_cards)
            if card_indices is None or\
               len(card_indices)!=keepable_cards or\
               len(card_indices)!=len(set(card_indices)):
                # Shuffle and offer to mulligan again, if AI decided to mulligan,
                # or the choice was invalid.
                shuffle(deck)
                continue

            # Otherwise, if choice was valid, process the accepted cards
            accepted, rejected = [], []
            for index,card in enumerate(context.hand):
                if index in card_indices:
                    accepted.append(card)
                else:
                    rejected.append(card)

            return Context(hand=accepted,
                           remaining=deck[7:]+rejected)
        return Context(hand=[], remaining=deck)

    def run(self, *,
            deck: List[Card],
            turns: int) -> List[int]:
        """
        Simulate playing given deck for some number of turns and return maximum mana per turn
        """

        context = self.execute_mulligan(deck[:])
        mana_generators: List[Iterator[int]] = []
        draw_generators: List[Iterator[int]] = [Sequence.one.generator()]
        gold_generators: List[Iterator[int]] = []

        mana_per_turn = turns*[0]
        for turn in range(turns):
            # Draw as much cards as you're supposed to this turn
            context.turn  = turn+1
            context.draw_cards(sum([generator.__next__() for generator in draw_generators]))
            context.mana  = sum([generator.__next__() for generator in mana_generators])
            context.gold += sum([generator.__next__() for generator in gold_generators])
            context.land_for_turn = False
            mana_per_turn[turn] = context.max_attainable_mana()

            while True:
                playable_cards = context.playable_cards()
                if len(playable_cards) == 0:
                    # Pass the turn if there's no playable cards left
                    break

                chosen = self.choose(context)
                if chosen not in playable_cards:
                    # Pass the turn if the AI decides to stop playing
                    break

                # Play chosen card
                generators = context.play_card(context.hand.pop(chosen))
                mana_generators.append(generators['mana'])
                draw_generators.append(generators['draw'])
                gold_generators.append(generators['gold'])

                # Maximum attainable mana may have changed after drawing cards
                mana_per_turn[turn] = max(mana_per_turn[turn], context.max_attainable_mana())
        return mana_per_turn

    @staticmethod
    def minimum_land_mulligan(min_cards: int, min_lands: int) -> Mulligan:
        """
        Mulligan to at most some number of cards, whenever having less than some number of lands
        """
        def func(context, keepable_cards):
            if keepable_cards <= min_cards or\
               sum([card.land for card in context.hand]) >= min_lands:
                # Keep the land cards of the dealt hand if the number of cards gets too low,
                # or the desired minimum number of lands is attained.
                lands, nonlands = [], []
                for index,card in enumerate(context.hand):
                    if card.land:
                        lands.append(index)
                    else:
                        nonlands.append(index)
                return (lands + nonlands)[:keepable_cards]
            # Mulligan
            return None
        return func

def improved_land_choice(context: Context) -> Optional[int]:
    """
    Play untapped land if needed, then ramp, then draw, then randomly choose a playable card
    """
    hand = context.hand
    mana = context.mana
    gold = context.gold
    playable_cards = context.playable_cards()

    # If there's a reason to play an untapped land, play it
    untapped_lands   = [k for k in playable_cards if hand[k].land and hand[k].netgain() != 0]
    almost_playables = [k for k in playable_cards if hand[k].cost == mana+gold+1]
    if len(almost_playables) > 0 and len(untapped_lands) > 0:
        return choice(untapped_lands)

    # Otherwise, if there are any ramp spells, play them
    ramp = [k for k in playable_cards if hand[k].is_ramp()]
    if len(ramp) > 0:
        return choice(ramp)

    # Otherwise, if there are any draw spells, play them
    draw = [k for k in playable_cards if hand[k].is_draw()]
    if len(draw) > 0:
        return choice(draw)

    # Otherwise, play randomly (tapped lands)
    return choice(playable_cards)

AI.dud        = AI()
AI.naive      = AI(choose=lambda context: choice(context.playable_cards()))
AI.less_naive = AI(mulligan=AI.minimum_land_mulligan(5, 3), choose=improved_land_choice)
