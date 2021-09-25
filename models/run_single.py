from random import shuffle

def run_single(deck, ai, turns):
    copied_deck = deck[:]

    # TODO: allow mulligan
    shuffle(copied_deck)
    hand = copied_deck[0:7]
    remaining = copied_deck[7:]
    mana_generators = []

    mana_per_turn = turns*[None]
    for turn in range(turns):
        land_for_turn = False
        hand.append(remaining.pop()) # draw a card
        mana = sum([generator.__next__() for generator in mana_generators]) # Tap everything for mana
        max_on_turn = mana

        while True:
            playable_cards = [k for k,card in enumerate(hand) if card.cost <= mana and not (land_for_turn and card.land)]

            if len(playable_cards) == 0:
                break
            chosen = ai.choose(playable_cards) # TODO: give more context to AI
            if chosen is None or chosen not in playable_cards:
                break

            # Play chosen card
            card = hand.pop(chosen)
            land_for_turn = land_for_turn or card.land
            generator = card.mana_generator()
            mana_generators.append(generator)
            mana += generator.__next__() - card.cost
            # TODO: implement card draw

            # Available mana on this turn may have increased after playing a card
            max_on_turn = max(mana, max_on_turn)

        mana_per_turn[turn] = max_on_turn
    return mana_per_turn
