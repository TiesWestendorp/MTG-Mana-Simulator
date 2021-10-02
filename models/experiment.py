"""
Defines the Experiment class which is the main class of this module.
"""

from random import shuffle
from models.run_single import run_single

class Experiment:
    """Wrapper class for simulating multiple runs"""

    def __init__(self, deck, AI, turns, repeats, options=None):
        self.deck    = deck
        self.AI      = AI
        self.turns   = turns
        self.repeats = repeats
        self.options = options if options is not None else {}
        self.run()

    def run(self):
        """Run the experiment"""
        variance_reduction = None
        if isinstance(self.options, dict):
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
        """Evaluate given metrics on the generated traces"""
        return dict(map(lambda metric: [metric.name, metric.compute(self.traces)], metrics))
