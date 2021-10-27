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
    below_curve : "Metric"
    on_curve : "Metric"
    above_curve : "Metric"

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

    @staticmethod
    def mean(measure: str) -> "Metric":
        """Mean of the given measure"""
        return Metric("Mean", measure, lambda t,ms: mean(ms))

    @staticmethod
    def median(measure: str) -> "Metric":
        """Median of the given measure"""
        return Metric("Median", measure, lambda t,ms: int(median(ms)))

    @staticmethod
    def mode(measure: str) -> "Metric":
        """Mode of the given measure"""
        return Metric("Mode", measure, lambda t,ms: mode(ms))

    @staticmethod
    def variance(measure: str) -> "Metric":
        """Variance of the given measure"""
        return Metric("Variance", measure, lambda t,ms: variance(ms))

    @staticmethod
    def minimum(measure: str) -> "Metric":
        """Minimum of the given measure"""
        return Metric("Minimum", measure, lambda t,ms: min(ms))

    @staticmethod
    def maximum(measure: str) -> "Metric":
        """Maximum of the given measure"""
        return Metric("Maximum", measure, lambda t,ms: max(ms))

Metric.identity    = Metric("Identity",     "max_mana", lambda t,ms: (t,ms))
Metric.below_curve = Metric("<'turn' mana", "max_mana", lambda t,ms: sum(m <  t for m in ms)/len(ms))
Metric.on_curve    = Metric("≥'turn' mana", "max_mana", lambda t,ms: sum(m >= t for m in ms)/len(ms))
Metric.above_curve = Metric(">'turn' mana", "max_mana", lambda t,ms: sum(m >  t for m in ms)/len(ms))
