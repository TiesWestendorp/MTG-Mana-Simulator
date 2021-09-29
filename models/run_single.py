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
        for _ in range(sum([generator.__next__() for generator in draw_generators])):
            context.hand.append(context.remaining.pop())
        context.turn  = turn+1
        context.mana  = sum([generator.__next__() for generator in mana_generators]) # Tap everything for mana
        context.gold += sum([generator.__next__() for generator in gold_generators]) # Create gold
        context.land_for_turn = False

        mana_per_turn[turn] = context.max_attainable_mana()

        # Until there's nothing left to do, or the AI stops playing
        while True:
            playable_cards = context.playable_cards()
            if len(playable_cards) == 0:
                break

            # Let AI choose a card
            chosen = ai.choose(playable_cards, context)
            if chosen not in playable_cards:
                break

            # Play chosen card
            card = context.hand.pop(chosen)
            mana_generator = card.mana_sequence.generator()
            draw_generator = card.draw_sequence.generator()
            gold_generator = card.gold_sequence.generator()
            mana_generators.append(mana_generator)
            draw_generators.append(draw_generator)
            gold_generators.append(gold_generator)
            for land_index in sorted(sample([k for k,card in enumerate(context.remaining) if card.land], card.lands_removed), key=lambda x: -x):
                context.remaining.pop(land_index)

            context.land_for_turn = context.land_for_turn or card.land # Disable land play if it was a land
            context.gold += gold_generator.__next__() - min([context.gold, max([0, card.cost-context.mana])]) # Pay appropriate gold
            context.mana += mana_generator.__next__() - min([context.mana, card.cost])                # Pay appropriate mana
            draw = draw_generator.__next__()

            for _ in range(draw):
                context.hand.append(context.remaining.pop()) # Draw appropriate amount of cards
            if draw > 0:
                # Maximum attainable mana may have changed after drawing cards
                mana_per_turn[turn] = max(mana_per_turn[turn], context.max_attainable_mana())
    return mana_per_turn
