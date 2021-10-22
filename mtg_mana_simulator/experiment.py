"""
Defines the Experiment class which is the main class of this module.
"""

from typing import Any, Dict, List, Optional
from random import shuffle
from scipy.stats import hypergeom
from mtg_mana_simulator.ai import AI
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.metric import Metric

class Experiment:
    """Wrapper class for simulating multiple runs"""

    def __init__(self,
            deck: List[Card],
            ai: AI,
            turns: int,
            repeats: int,
            *, options: Optional[Dict[str, Any]]=None) -> None:
        self.deck    = deck
        self.ai      = ai
        self.turns   = turns
        self.repeats = repeats
        self.options = options if options is not None else {}
        self.traces : List[List[int]] = self.repeats*[[0]]
        self.run()

    def run(self) -> None:
        """Run the experiment"""
        variance_reduction = self.options.get('variance_reduction')

        for iteration in range(self.repeats):
            if variance_reduction == 'antithetic-variates':
                # https://en.wikipedia.org/wiki/Antithetic_variates
                if iteration%2 == 0:
                    shuffle(self.deck)
                else:
                    self.deck.reverse()
            if variance_reduction == 'importance-sampling':
                # https://en.wikipedia.org/wiki/Importance_sampling
                cards_without_cost = len([card for card in self.deck if (card.cost or 0) <= 0])
                if cards_without_cost == 0:
                    raise ValueError
                shuffle(self.deck)
                while len([card for card in self.deck[0:6+self.turns] if (card.cost or 0) <= 0]) == 0:
                    shuffle(self.deck)
            else:
                shuffle(self.deck)

            context = self.ai.execute_mulligan(self.deck[:]) # TODO: deep-copy
            # TODO: change API, run is method of context, not of AI
            trace = self.ai.run(context=context, turns=self.turns)
            self.traces[iteration] = trace

    def evaluate(self, metrics: List[Metric]) -> Dict[str, List[Any]]:
        """Evaluate given metrics on the generated traces"""
        if self.options.get('variance_reduction') == 'importance-sampling':
            cards_without_cost = len([card for card in self.deck if (card.cost or 0) <= 0])
            probability = 1 - hypergeom.cdf(0, len(self.deck), cards_without_cost, 6+self.turns)
            return dict(map(lambda metric: (metric.name, list(map(lambda x: x*probability, metric.compute(self.traces)))), metrics))

        return dict(map(lambda metric: (metric.name, metric.compute(self.traces)), metrics))
