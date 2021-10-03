"""
Defines the Metric class which models functions that can be executed on traces.
"""

from typing import Any, Callable, List
from statistics import mean, median, mode, variance

class Metric:
    """Computations that can be executed on the amount of mana in a turn (across traces)"""

    mean = None
    median = None
    mode = None
    variance = None
    below_curve = None
    on_curve = None
    above_curve = None

    def __init__(self, name: str, func: Callable[[int, List[int]], Any]) -> None:
        self.name = name
        self.func = func

    def compute(self, traces: List[int]) -> List[Any]:
        """Compute the metric on the given traces"""
        return [self.func(turn+1, manas_by_turn) for turn,manas_by_turn in enumerate(zip(*traces))]

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
