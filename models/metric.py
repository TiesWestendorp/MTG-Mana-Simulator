"""
Defines the Metric class which models functions that can be executed on traces.
"""

from typing import Callable, List, TypeVar
from statistics import mean, median, mode, variance
TYPE = TypeVar('TYPE')

class Metric:
    """Computations that can be executed on the amount of mana in a turn (across traces)"""

    mean : "Metric"
    median : "Metric"
    mode : "Metric"
    variance : "Metric"
    below_curve : "Metric"
    on_curve : "Metric"
    above_curve : "Metric"

    def __init__(self, name: str, func: Callable[[int, List[int]], TYPE]) -> None:
        self.name = name
        self.func = func

    def compute(self, traces: List[List[int]]) -> List[TYPE]:
        """Compute the metric on the given traces"""
        return [self.func(t+1, list(ms)) for t,ms in enumerate(zip(*traces))]

    @staticmethod
    def minimum_mana(min_mana: int) -> "Metric":
        """Probability of having at least the given amount of mana"""
        func = lambda t,ms: sum(m >= min_mana for m in ms)/len(ms)
        return Metric(f"≥{min_mana} mana", func)

    @staticmethod
    def percentile(fraction: float) -> "Metric":
        """Percentile score"""
        func = lambda t,ms: sorted(ms)[round(len(ms)*fraction)-1]
        return Metric(f"{fraction}th percentile", func)

Metric.mean        = Metric("Mean",         lambda t,ms: mean(ms))
Metric.median      = Metric("Median",       lambda t,ms: int(median(ms)))
Metric.mode        = Metric("Mode",         lambda t,ms: mode(ms))
Metric.variance    = Metric("Variance",     lambda t,ms: variance(ms))
Metric.below_curve = Metric("<'turn' mana", lambda t,ms: sum(m <  t for m in ms)/len(ms))
Metric.on_curve    = Metric("≥'turn' mana", lambda t,ms: sum(m >= t for m in ms)/len(ms))
Metric.above_curve = Metric(">'turn' mana", lambda t,ms: sum(m >  t for m in ms)/len(ms))
