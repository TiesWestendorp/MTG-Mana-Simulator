from random import shuffle
from models.sequence import Sequence

def run_single(deck, ai, turns):
    copied_deck = deck[:]

    # TODO: allow mulligan
    shuffle(copied_deck)
    hand = copied_deck[0:7]
    remaining = copied_deck[7:]
    gold = 0
    mana_generators = []
    draw_generators = [Sequence.one.generator()]
    gold_generators = []

    mana_per_turn = turns*[None]
    unplayables_per_turn = turns*[None]
    for turn in range(turns):
        # Allow playing a single land per turn
        land_for_turn = False

        # Draw as much cards as you're supposed to this turn
        for _ in range(sum([generator.__next__() for generator in draw_generators])):
            hand.append(remaining.pop())

        mana  = sum([generator.__next__() for generator in mana_generators]) # Tap everything for mana
        gold += sum([generator.__next__() for generator in gold_generators]) # Create gold

        # Consider the max mana to be gained from playing a land this turn (but don't play it)
        max_mana_from_land = max([0]+[card.mana_sequence.finite_prefix(1)[0] for card in hand if card.land])
        max_on_turn = mana + max_mana_from_land + gold

        if len(hand) > 0:
            unplayables_per_turn[turn] = sum([1 for card in hand if card.cost > max_on_turn and not card.land])/len(hand)
        else:
            unplayables_per_turn[turn] = 0.0

        # Until there's nothing left to do, or the AI stops playing
        while True:
            playable_cards = [k for k,card in enumerate(hand) if card.cost <= mana+gold and not (land_for_turn and card.land)]
            if len(playable_cards) == 0:
                break

            # Let AI choose a card
            chosen = ai.choose({'hand': hand, 'playable_cards': playable_cards, 'mana': mana, 'gold': gold, 'land_for_turn': land_for_turn})
            if chosen not in playable_cards:
                break

            # Play chosen card
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

            for _ in range(draw_generator.__next__()):
                hand.append(remaining.pop()) # Draw appropriate amount of cards

            # TODO: implement land search

            # Available mana on this turn may have increased after playing a card
            max_on_turn = max(mana + gold, max_on_turn)

        mana_per_turn[turn] = max_on_turn
    return mana_per_turn
