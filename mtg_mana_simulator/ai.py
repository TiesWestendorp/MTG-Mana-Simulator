"""
Defines the AI class which is the decision agent that decides whether to mulligan
or not, and which cards should be played given a certain 'context'.
"""

from typing import Callable, Iterator, List, Optional, Tuple
from random import choice, shuffle
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.context import Context
from mtg_mana_simulator.sequence import Sequence

MayChoose   = Callable[[Context],      Optional[int]]
MustChoose  = Callable[[Context],      int]

MayChooseN  = Callable[[Context, int], Optional[List[int]]]
MustChooseN = Callable[[Context, int], List[int]]

MustSplitN  = Callable[[Context, int], Tuple[List[int], List[int]]]


class AI:
    """
    Decision agent that implements mulligan and card playing algorithms
    """

    dud : "AI"
    naive : "AI"
    less_naive : "AI"
    never_mulligan  : MayChooseN = lambda _,__: list(range(7))
    never_choose    : MayChoose  = lambda _: None
    randomly_choose : MayChoose  = lambda context: choice(context.playable_cards())


    def __init__(self, *,
            mulligan: Optional[MayChooseN] = None,
            choose: Optional[MayChoose] = None) -> None:
        self.mulligan = mulligan if mulligan is not None else AI.never_mulligan
        self.choose   = choose   if choose   is not None else AI.never_choose

    def execute_mulligan(self, deck: List[Card]) -> Context:
        """
        Keep applying chosen mulligan strategy until a valid choice is made, or the hand is empty
        """
        for keepable_cards in reversed(range(1,8)):
            hand = deck[:7]
            remaining = deck[7:]

            card_indices = self.mulligan(Context(hand=hand, deck=remaining), keepable_cards)
            if card_indices is not None and\
               len(card_indices)==keepable_cards and\
               len(card_indices)==len(set(card_indices)) and\
               all(0 <= index < 7 for index in card_indices):
                # If AI decided to keep, and the choice was valid, process the accepted cards
                accepted, rejected = [], []
                for index,card in enumerate(hand):
                    if index in card_indices:
                        accepted.append(card)
                    else:
                        rejected.append(card)
                return Context(hand=accepted, deck=remaining+rejected)

            # Otherwise, shuffle and offer to mulligan again, with one less card
            shuffle(deck)
        return Context(hand=[], deck=deck)

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
            context.draw_cards(sum(generator.__next__() for generator in draw_generators))
            context.mana  = sum(generator.__next__() for generator in mana_generators)
            context.gold += sum(generator.__next__() for generator in gold_generators)
            context.land_for_turn = False

            # Determine maximum attainable mana before cards have been played, and set
            # the value of all following turns to that value. I.e. the player could
            # have decided to not do something this turn, but to postpone it to a later
            # turn. This is relevant to decrease variance when cards like Dark Ritual
            # appear in a deck.
            max_attainable_mana = max(mana_per_turn[turn], context.max_attainable_mana())
            mana_per_turn[turn:] = [max_attainable_mana]*(turns-turn)
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
                generators = context.play_card(context.zones["hand"].pop(chosen))
                mana_generators.append(generators['mana'])
                draw_generators.append(generators['draw'])
                gold_generators.append(generators['gold'])

                # Maximum attainable mana may have changed after drawing cards
                max_attainable_mana = max(mana_per_turn[turn], context.max_attainable_mana())
                mana_per_turn[turn:] = [max_attainable_mana]*(turns-turn)
        return mana_per_turn

    @staticmethod
    def minimum_land_mulligan(min_cards: int, min_lands: int) -> MayChooseN:
        """
        Mulligan to at most some number of cards, whenever having less than some number of lands
        """
        def func(context, keepable_cards):
            if keepable_cards <= min_cards or\
               sum(card.land for card in context.zones["hand"]) >= min_lands:
                # Keep the land cards of the dealt hand if the number of cards gets too low,
                # or the desired minimum number of lands is attained.
                lands, nonlands = [], []
                for index,card in enumerate(context.zones["hand"]):
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
    hand = context.zones["hand"]
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
AI.naive      = AI(choose=AI.randomly_choose)
AI.less_naive = AI(mulligan=AI.minimum_land_mulligan(5, 3), choose=improved_land_choice)
