from models.run_single import run_single
from random import shuffle

class Experiment:
    def __init__(self, deck, ai, turns, repeats, options={}):
        self.deck    = deck
        self.ai      = ai
        self.turns   = turns
        self.repeats = repeats
        self.options = options
        self.run()

    def run(self):
        variance_reduction = None
        if type(self.options) is dict:
            if 'variance_reduction' in self.options:
                variance_reduction = self.options['variance_reduction']

        self.traces = self.repeats*[None]
        for iteration in range(self.repeats):
            if variance_reduction == 'antithetic-variates':
                # https://en.wikipedia.org/wiki/Antithetic_variates
                if iteration%2 == 0:
                    shuffle(self.deck)
                else:
                    self.deck.reverse()
            else:
                shuffle(self.deck)

            self.traces[iteration] = run_single(self.deck, self.ai, self.turns)
    def evaluate(self, metrics):
        return dict(map(lambda metric: [metric.name, metric.compute(self.traces)], metrics))
