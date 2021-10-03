"""
Defines the Experiment class which is the main class of this module.
"""

from typing import List
from random import shuffle

class Experiment:
    """Wrapper class for simulating multiple runs"""

    def __init__(self, deck: List["Card"], agent: "AI", turns: int, repeats: int, *, options=None):
        self.deck    = deck
        self.agent   = agent
        self.turns   = turns
        self.repeats = repeats
        self.options = options if options is not None else {}
        self.run()

    def run(self) -> None:
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

            self.traces[iteration] = self.agent.run(deck=self.deck, turns=self.turns)

    def evaluate(self, metrics: List["Metric"]):
        """Evaluate given metrics on the generated traces"""
        return dict(map(lambda metric: [metric.name, metric.compute(self.traces)], metrics))
