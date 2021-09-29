from models.sequence import Sequence

class AI:
    naive = None

    def __init__(self, mulligan, choose):
        self.mulligan = mulligan
        self.choose = choose

from random import choice
def naive_choice(playable_cards, _):
    return choice(playable_cards)

def improved_land_choice(playable_cards, context):
    hand = context.hand
    mana = context.mana
    gold = context.gold

    # If there's a reason to play an untapped land, play it
    untapped_lands   = [k for k in playable_cards if hand[k].land and hand[k].mana_sequence.finite_prefix(1) != [0]]
    almost_playables = [k for k in playable_cards if hand[k].cost == mana+gold+1]
    if len(almost_playables) > 0 and len(untapped_lands) > 0:
        return choice(untapped_lands)

    # Otherwise, if there are any ramp spells, play them
    ramp = [k for k in playable_cards if hand[k].mana_sequence != Sequence.zero or hand[k].gold_sequence != Sequence.zero]
    if len(ramp) > 0:
        return choice(ramp)

    # Otherwise, if there are any draw spells, play them
    draw = [k for k in playable_cards if hand[k].draw_sequence != Sequence.zero]
    if len(draw) > 0:
        return choice(draw)

    # Otherwise, play randomly (tapped lands)
    return naive_choice(context)


AI.naive = AI(lambda _: False, naive_choice)
AI.less_naive = AI(lambda _: False, improved_land_choice)
