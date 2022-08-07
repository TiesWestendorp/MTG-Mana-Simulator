"""
Defines the Experiment class which is the main class of this module.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from multiprocessing import Pool, cpu_count
from random import shuffle
from mtg_mana_simulator.ai import AI
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.metric import Metric
from tqdm import tqdm
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
        """Run the experiment multiple times in parallel"""
        pool = Pool(cpu_count())
        for t in tqdm(pool.imap(self.run_single, (() for _ in range(self.repeats))), total=self.repeats):
            self.traces.append(t)
#        for _ in range(self.repeats):
#            self.traces.append(self.run_single())

    def run_single(self, i) -> None:
        """Run the experiment a single time"""
        deck = self.deck[:] # copy
        shuffle(deck)
        context = self.ai.execute_mulligan(deck)
        return self.ai.run(context=context, turns=self.turns)

    def evaluate(self, metrics: List[Metric]) -> Dict[str, List[Any]]:
        """Evaluate given metrics on the generated traces"""
        return dict(map(lambda metric: (metric.name, metric.compute(self.traces)), metrics))
