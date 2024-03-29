"""
Defines the AI class which is the decision agent that decides whether to mulligan
or not, and which cards should be played given a certain 'context'.
"""

from typing import Callable, List, Optional, Tuple
from random import choice, shuffle
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.context import Context
from mtg_mana_simulator.trace import Trace

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

    # Default choice strategies
    default_mulligan : MayChooseN  = lambda _,number: list(range(number))
    default_choose   : MayChoose   = lambda _: None
    default_discard  : MustChooseN = lambda _,number: list(range(number))

    randomly_choose : MayChoose = lambda context: choice(context.playable_cards())

    def __init__(self, *,
            mulligan: Optional[MayChooseN] = None,
            choose:   Optional[MayChoose]  = None,
            discard:  Optional[MustChooseN] = None) -> None:
        self.mulligan = mulligan if mulligan is not None else AI.default_mulligan
        self.choose   = choose   if choose   is not None else AI.default_choose
        self.discard  = discard  if discard  is not None else AI.default_discard

    def execute_mulligan(self, deck: List[Card]) -> Context:
        """
        Keep applying chosen mulligan strategy until a valid choice is made, or the hand is empty
        """
        for keepable_cards in reversed(range(1,8)):
            hand = deck[:7]
            rest = deck[7:]

            card_indices = self.mulligan(Context(hand=hand, deck=rest, ai=self), keepable_cards)
            if card_indices is not None and\
               len(card_indices)==keepable_cards and\
               len(card_indices)==len(set(card_indices)) and\
               all(0 <= index < 7 for index in card_indices):
                # If AI decided to keep, and the choice was valid, process the accepted cards
                accepted: List[Card] = []
                rejected: List[Card] = []
                for index,card in enumerate(hand):
                    (accepted if index in card_indices else rejected).append(card)
                return Context(hand=accepted, deck=rest+rejected, ai=self)

            # Otherwise, shuffle and offer to mulligan again, with one less card
            shuffle(deck)
        return Context(hand=[], deck=deck, ai=self)

    def run(self, *,
            context: Context,
            turns: int) -> Trace:
        """
        Simulate playing given deck for some number of turns and return maximum mana per turn
        """
        trace = Trace(turns)
        for turn in range(turns):
            context.new_turn()
            trace.update(turn, context)

            while True:
                # Pass the turn if there's no playable cards left
                playable_cards = context.playable_cards()
                if len(playable_cards) == 0:
                    break

                # Pass the turn if the AI decides to stop playing or makes an invalid move
                chosen = self.choose(context)
                if chosen not in playable_cards:
                    break

                # Play the chosen card
                context.play_card("hand", chosen)
                trace.update(turn, context)

            # Discard to maximum hand size
            to_discard = max(0, len(context.zones["hand"])-7)
            cards = self.discard(context, to_discard)
            if len(cards) != to_discard:
                raise ValueError
            context.discard_cards(cards)

        return trace.finalize()

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
                lands: List[Card] = []
                nonlands: List[Card] = []
                for index,card in enumerate(context.zones["hand"]):
                    (lands if card.land else nonlands).append(index)
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
