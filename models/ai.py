class AI:
    naive = None
    
    def __init__(self, mulligan, choose):
        self.mulligan = mulligan
        self.choose = choose

from random import choice
AI.naive = AI(lambda x: False, lambda cards: choice(cards))
