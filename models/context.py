class Context:
    def __init__(self, turn=None, hand=None, mana=None, gold=None, land_for_turn=None, remaining=None):
        self.turn = turn
        self.hand = hand
        self.mana = mana
        self.gold = gold
        self.land_for_turn = land_for_turn
        self.remaining = remaining

    def play_card(self, card):
        pass

    def playable_cards(self):
        return [k for k,card in enumerate(self.hand) if (not card.land and card.cost <= self.mana+self.gold) or (card.land and not self.land_for_turn)]

    # How much mana can we attain this turn (without considering card draw), by:
    #   - Tapping everything we have for mana
    #   - Cracking all gold tokens for mana
    #   - Playing the land that gives the most mana in the current turn
    #   - And only playing cards that net mana
    def max_attainable_mana(self):
        max_attainable_mana = self.mana + self.gold
        max_attainable_mana += max([0]+[card.netgain() for card in self.hand if card.land and not self.land_for_turn])
        for card in sorted([card for card in self.hand if not card.land], key=lambda card: card.cost):
            max_attainable_mana += max([0, card.netgain()])
            if card.cost > max_attainable_mana:
                break
        return max_attainable_mana
