"""
Defines the AI class which is the decision agent that decides whether to mulligan
or not, and which cards should be played given a certain 'context'.
"""

from typing import Callable, Iterator, List, Optional
from random import choice, shuffle
from models.card import Card
from models.context import Context
from models.sequence import Sequence

class AI:
    """Decision agent that implements mulligan and card playing algorithms"""

    dud : "AI"
    naive : "AI"
    less_naive : "AI"

    def __init__(self, *,
            mulligan: Optional[Callable[[Context, int], Optional[List[int]]]] = None,
            choose: Optional[Callable[[Context], Optional[int]]] = None) -> None:
        self.mulligan = mulligan if mulligan is not None else (lambda _,__: list(range(7)))
        self.choose   = choose   if choose   is not None else (lambda _: None)

    def run(self, *,
            deck: List[Card],
            turns: int) -> List[int]:
        """Simulate playing given deck for some number of turns and return maximum mana per turn"""
        copied_deck = deck[:]

        for keepable_cards in reversed(range(8)):
            context = Context(hand=copied_deck[:keepable_cards],
                              remaining=copied_deck[keepable_cards:])
            card_indices = self.mulligan(context, keepable_cards)
            if card_indices is None or\
               len(card_indices)>keepable_cards or\
               len(card_indices)!=len(set(card_indices)):
                # Shuffle and offer to mulligan again, if AI decided to mulligan,
                # or the choice was invalid.
                shuffle(copied_deck)
                continue

            accepted_cards = [context.hand[index] for index in card_indices]
            rejected_cards = [context.hand[index] for index in range(len(context.hand))
                               if index not in card_indices]
            context = Context(hand=accepted_cards,
                              remaining=copied_deck[keepable_cards:]+rejected_cards)
            break

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
    def mulligan_too_few_lands(context: Context,
                               keepable_cards: int,
                               max_times: int,
                               min_lands: int) -> None:
        """Mulligan at most some number of times, whenever having less than some number of lands"""
        if times <= max_times and sum([card.land for card in context.hand]) >= min_lands:
            #
            return None

def improved_land_choice(context: Context) -> Optional[int]:
    """Play untapped land if needed, then ramp, then draw, then randomly choose a playable card"""
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
AI.less_naive = AI(choose=improved_land_choice)
