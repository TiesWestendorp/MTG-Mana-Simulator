from models.sequence import Sequence

def run_single(deck, ai, turns):
    copied_deck = deck[:]

    # TODO: allow mulligan
    hand = copied_deck[0:7]
    remaining = copied_deck[7:]
    gold = 0
    mana_generators = []
    draw_generators = [Sequence.one.generator()]
    gold_generators = []

    mana_per_turn = turns*[None]
    for turn in range(turns):
        # Allow playing a single land per turn
        land_for_turn = False

        # Draw as much cards as you're supposed to this turn
        for _ in range(sum([generator.__next__() for generator in draw_generators])):
            hand.append(remaining.pop())

        mana  = sum([generator.__next__() for generator in mana_generators]) # Tap everything for mana
        gold += sum([generator.__next__() for generator in gold_generators]) # Create gold

        mana_per_turn[turn] = max_attainable_mana({'hand': hand, 'mana': mana, 'gold': gold, 'land_for_turn': land_for_turn})

        # Until there's nothing left to do, or the AI stops playing
        while True:
            playable_cards = [k for k,card in enumerate(hand) if (not card.land and card.cost <= mana+gold) or (card.land and not land_for_turn)]
            if len(playable_cards) == 0:
                break

            # Let AI choose a card
            chosen = ai.choose({'turn': turn+1, 'hand': hand, 'playable_cards': playable_cards, 'mana': mana, 'gold': gold, 'land_for_turn': land_for_turn})
            if chosen not in playable_cards:
                break

            # Play chosen card
            # TODO: implement land search
            card = hand.pop(chosen)
            mana_generator = card.mana_sequence.generator()
            draw_generator = card.draw_sequence.generator()
            gold_generator = card.gold_sequence.generator()
            mana_generators.append(mana_generator)
            draw_generators.append(draw_generator)
            gold_generators.append(gold_generator)

            land_for_turn = land_for_turn or card.land # Disable land play if it was a land
            gold += gold_generator.__next__() - min([gold, max([0, card.cost-mana])]) # Pay appropriate gold
            mana += mana_generator.__next__() - min([mana, card.cost])                # Pay appropriate mana
            draw = draw_generator.__next__()

            for _ in range(draw):
                hand.append(remaining.pop()) # Draw appropriate amount of cards
            if draw > 0:
                # Maximum attainable mana may have changed after drawing cards
                mana_per_turn[turn] = max(mana_per_turn[turn], max_attainable_mana({'hand': hand, 'mana': mana, 'gold': gold, 'land_for_turn': land_for_turn}))
    return mana_per_turn

# How much mana can we attain this turn (without considering card draw), by:
#   - Tapping everything we have for mana
#   - Cracking all gold tokens for mana
#   - Playing the land that gives the most mana in the current turn
#   - And only playing cards that net mana
def max_attainable_mana(context):
    hand, mana, gold, land_for_turn = [context[k] for k in ['hand', 'mana', 'gold', 'land_for_turn']]

    max_attainable_mana = mana + gold
    max_attainable_mana += max([0]+[card.netgain() for card in hand if card.land and not land_for_turn])
    for card in sorted([card for card in hand if not card.land], key=lambda card: card.cost):
        max_attainable_mana += max([0, card.netgain()])
        if card.cost > max_attainable_mana:
            break

    return max_attainable_mana
