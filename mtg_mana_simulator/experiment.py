"""
Defines the Experiment class which is the main class of this module.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from random import shuffle
from mtg_mana_simulator.ai import AI
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.metric import Metric
if TYPE_CHECKING:
    from mtg_mana_simulator.trace import Trace

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
        self.traces : List["Trace"] = []
        self.run()

    def run(self) -> None:
        """Run the experiment"""
        for iteration in range(self.repeats):
            shuffle(self.deck)
            context = self.ai.execute_mulligan(self.deck[:]) # deep-copy
            # change API, run is method of context, not of AI
            trace = self.ai.run(context=context, turns=self.turns)
            self.traces.append(trace)

    def evaluate(self, metrics: List[Metric]) -> Dict[str, List[Any]]:
        """Evaluate given metrics on the generated traces"""
        return dict(map(lambda metric: (metric.name, metric.compute(self.traces)), metrics))
