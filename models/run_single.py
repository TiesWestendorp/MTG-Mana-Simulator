from models.sequence import Sequence
from models.card import Card
from models.context import Context
from random import sample

def run_single(deck, ai, turns):
    copied_deck = deck[:]

    # TODO: allow mulligan
    context = Context(turn=0, hand=copied_deck[0:7], mana=0, gold=0, land_for_turn=False, remaining=copied_deck[7:])

    mana_generators = []
    draw_generators = [Sequence.one.generator()]
    gold_generators = []

    mana_per_turn = turns*[None]
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

            chosen = ai.choose(playable_cards, context)
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
