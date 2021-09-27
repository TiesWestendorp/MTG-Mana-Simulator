class AI:
    naive = None

    def __init__(self, mulligan, choose):
        self.mulligan = mulligan
        self.choose = choose

from random import choice
def naive_choice(context):
    return choice(context['playable_cards'])

def improved_land_choice(context):
    hand, mana, gold, playable_cards = [context[k] for k in ['hand', 'mana', 'gold', 'playable_cards']]

    # If there's a reason to play an untapped land, play it
    untapped_lands   = [k for k in playable_cards if hand[k].land and hand[k].mana_sequence.finite_prefix(1) != [0]]
    almost_playables = [k for k in playable_cards if hand[k].cost == mana+gold+1]
    if len(almost_playables) > 0 and len(untapped_lands) > 0:
        return choice(untapped_lands)

    # Otherwise, if there are any non-lands, play them
    nonlands = [k for k in playable_cards if not hand[k].land]
    if len(nonlands) > 0:
        return choice(nonlands)

    # Otherwise, play randomly (tapped lands)
    return naive_choice(context)


AI.naive = AI(lambda _: False, naive_choice)
AI.less_naive = AI(lambda _: False, improved_land_choice)
