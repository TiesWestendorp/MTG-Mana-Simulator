"""
Defines the Metric class which models functions that can be executed on traces.
"""

from typing import Callable, List, TypeVar
from statistics import mean, median, mode, variance
from mtg_mana_simulator.trace import Trace
TYPE = TypeVar('TYPE')

class Metric:
    """Computations that can be executed on the amount of mana in a turn (across traces)"""

    identity : "Metric"
    mean : "Metric"
    median : "Metric"
    mode : "Metric"
    variance : "Metric"
    below_curve : "Metric"
    on_curve : "Metric"
    above_curve : "Metric"
    minimum : "Metric"
    maximum : "Metric"

    def __init__(self, name: str, measure: str, func: Callable[[int, Trace], TYPE]) -> None:
        self.name = name
        self.measure = measure
        self.func = func

    def compute(self, traces: List[Trace]) -> List[TYPE]:
        """Compute the metric on the given traces"""
        measures = list(map(lambda trace: getattr(trace, self.measure), traces))
        return [self.func(t+1, list(ms)) for t,ms in enumerate(zip(*measures))]

    @staticmethod
    def above_threshold(measure: str, threshold: int) -> "Metric":
        """Probability of having at least the given amount of the given measure"""
        func = lambda t,ms: sum(m >= threshold for m in ms)/len(ms)
        return Metric(f"≥{threshold}", measure, func)

    @staticmethod
    def percentile(measure: str, fraction: float) -> "Metric":
        """Percentile score"""
        func = lambda t,ms: sorted(ms)[min(len(ms), max(0, round(len(ms)*fraction)-1))]
        return Metric(f"{fraction}th percentile", measure, func)

Metric.identity    = Metric("Identity",     "max_mana", lambda t,ms: (t,ms))
Metric.mean        = Metric("Mean",         "max_mana", lambda t,ms: mean(ms))
Metric.median      = Metric("Median",       "max_mana", lambda t,ms: int(median(ms)))
Metric.mode        = Metric("Mode",         "max_mana", lambda t,ms: mode(ms))
Metric.variance    = Metric("Variance",     "max_mana", lambda t,ms: variance(ms))
Metric.below_curve = Metric("<'turn' mana", "max_mana", lambda t,ms: sum(m <  t for m in ms)/len(ms))
Metric.on_curve    = Metric("≥'turn' mana", "max_mana", lambda t,ms: sum(m >= t for m in ms)/len(ms))
Metric.above_curve = Metric(">'turn' mana", "max_mana", lambda t,ms: sum(m >  t for m in ms)/len(ms))
Metric.minimum     = Metric("Minimum",      "max_mana", lambda t,ms: min(ms))
Metric.maximum     = Metric("Maximum",      "max_mana", lambda t,ms: max(ms))
